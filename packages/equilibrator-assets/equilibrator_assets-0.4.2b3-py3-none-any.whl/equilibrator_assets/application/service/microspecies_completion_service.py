"""Provide a service that adds microspecies to compounds."""


import logging
from operator import attrgetter
from pathlib import Path
from typing import Dict, List

import numpy as np
from equilibrator_cache import Compound, CompoundMicrospecies
from equilibrator_cache.thermodynamic_constants import (
    default_RT,
    standard_dg_formation_mg,
)
from sqlalchemy.orm import selectinload, sessionmaker
from tqdm import tqdm


logger = logging.getLogger(__name__)


LOG10 = np.log(10.0)


Session = sessionmaker()


class MicrospeciesCompletionService:
    """
    Define a service that adds microspecies to compounds.

    Microspecies are calculated based on estimated pKa values and the structure of the
    major (most abundant) microspecies at pH 7. At least a major microspecies based on
    the compounds structure is almost always added.

    """

    @classmethod
    def batch_populate(
        cls, eq_cache: Session, log_file: Path, batch_size: int = 1000
    ) -> None:
        """Add microspecies to all compounds in the cache with a defined atom bag."""
        logger.propagate = False
        logger.addHandler(logging.FileHandler(log_file))

        query = (
            eq_cache.query(Compound)
            .options(selectinload(Compound.magnesium_dissociation_constants))
            .filter(Compound.atom_bag.is_not(None))
        )
        microspecies = []

        def update_cache():
            eq_cache.bulk_insert_mappings(CompoundMicrospecies, microspecies)
            eq_cache.commit()
            microspecies.clear()

        for compound in tqdm(
            query.yield_per(batch_size),
            total=query.count(),
            unit_scale=True,
            desc="Compound",
        ):
            eq_cache.expunge(compound)
            microspecies.extend(cls.populate_microspecies(compound))
        else:
            update_cache()

    @classmethod
    def populate_microspecies(
        cls, compound: Compound, major_ms_ph: float = 7.0
    ) -> List[Dict]:
        """Populate the microspecies of a single compound."""
        if not compound.dissociation_constants:
            num_species = 1
            major_ms_index = 0
        else:
            num_species = len(compound.dissociation_constants) + 1
            major_ms_index = sum(
                (1 for p_ka in compound.dissociation_constants if p_ka > major_ms_ph)
            )

        # Special case for proton.
        if compound.inchi_key == "GPRLSGONYQIRFK-UHFFFAOYSA-N":
            return [
                {
                    "charge": 0,
                    "number_protons": 0,
                    "number_magnesiums": 0,
                    "ddg_over_rt": 0.0,
                    "is_major": True,
                    "compound_id": compound.id,
                }
            ]

        major_ms_num_protons = compound.atom_bag.get("H", 0)
        major_ms_charge = compound.net_charge

        microspecies = {}
        for i in range(num_species):
            charge = i - major_ms_index + major_ms_charge
            num_protons = i - major_ms_index + major_ms_num_protons
            is_major = False

            if i == major_ms_index:
                ddg_over_rt = 0.0
                is_major = True
            elif i < major_ms_index:
                ddg_over_rt = (
                    sum(compound.dissociation_constants[i:major_ms_index]) * LOG10
                )
            elif i > major_ms_index:
                ddg_over_rt = (
                    -sum(compound.dissociation_constants[major_ms_index:i]) * LOG10
                )
            else:
                raise IndexError("Major microspecies index mismatch.")
            microspecies[(num_protons, 0)] = CompoundMicrospecies(
                charge=charge,
                number_protons=num_protons,
                number_magnesiums=0,
                ddg_over_rt=ddg_over_rt,
                is_major=is_major,
            )

        standard_dg_formation_mg_over_rt = standard_dg_formation_mg / default_RT.m_as(
            "kJ/mol"
        )

        # iterate through all Mg2+ dissociation constants in an order where
        # the ones with fewest Mg2+ are first, so that their reference MS will
        # already be in `microspecies_mappings`. If there is a gap in this layered
        # approach, we raise an Exception.
        for mg_diss in sorted(
            compound.magnesium_dissociation_constants,
            key=attrgetter("number_magnesiums", "number_protons"),
        ):
            dissociation_constant = mg_diss.dissociation_constant
            num_protons = mg_diss.number_protons
            num_magnesiums = mg_diss.number_magnesiums

            # find the reference MS, but looking for one with one less Mg2+ ion.
            # it should already be in the `microspecies_mappings` dictionary
            # since we sorted the pKds by increasing order of Mg2+.
            try:
                ref_ms = microspecies[(num_protons, num_magnesiums - 1)]
            except KeyError:
                logger.error(
                    f"Could not find the reference microspecies for the "
                    f"[nH={num_protons}, nMg={num_magnesiums - 1}] "
                    f"microspecies, for the compound {compound.id}, "
                    f"InChIKey={compound.inchi_key}."
                )
                continue

            charge = ref_ms.charge + 2
            ddg_over_rt = (
                ref_ms.ddg_over_rt
                + standard_dg_formation_mg_over_rt
                - dissociation_constant * LOG10
            )

            microspecies[(num_protons, num_magnesiums)] = CompoundMicrospecies(
                charge=charge,
                number_protons=num_protons,
                number_magnesiums=num_magnesiums,
                ddg_over_rt=ddg_over_rt,
                is_major=False,
            )

        return [
            cls._microspecies_to_obj(microspecies[key], compound.id)
            for key in sorted(microspecies)
        ]

    @staticmethod
    def _microspecies_to_obj(
        microspecies: CompoundMicrospecies, compound_id: int
    ) -> Dict:
        """Convert a microspecies into dictionary structure."""
        return {
            "charge": microspecies.charge,
            "number_protons": microspecies.number_protons,
            "number_magnesiums": microspecies.number_magnesiums,
            "ddg_over_rt": microspecies.ddg_over_rt,
            "is_major": microspecies.is_major,
            "compound_id": compound_id,
        }
