"""Provide a service for estimating proton dissociation constants."""


import logging
import multiprocessing
from typing import Dict, Optional

from equilibrator_cache import Compound
from equilibrator_cheminfo.domain.model import Structure, StructureIdentifier
from equilibrator_cheminfo.infrastructure.service.chemaxon import (
    ChemAxonMajorMicrospeciesService,
    ChemAxonMolecularEntityFactory,
    ChemAxonProtonDissociationConstantsService,
)
from sqlalchemy.orm import sessionmaker
from tqdm import tqdm

from .abstract_molecular_entity_service import (
    AbstractMolecularEntityService,
    CompoundStructure,
    MolecularEntityServiceCommand,
)


logger = logging.getLogger(__name__)


Session = sessionmaker()


class ChemAxonMolecularEntityService(AbstractMolecularEntityService):
    """Define a service for estimating proton dissociation constants."""

    @classmethod
    def batch_populate(
        cls,
        eq_cache: Session,
        command: MolecularEntityServiceCommand,
        batch_size: int = 1000,
    ) -> None:
        """Estimate pKa for any compound in the cache that has an InChI."""
        query = (
            eq_cache.query(
                Compound.id, Compound.inchi_key, Compound.inchi, Compound.smiles
            )
            .select_from(Compound)
            .filter(
                Compound.inchi.is_not(None),
                Compound.dissociation_constants.is_(None),
            )
        )
        compounds = []

        def update_cache():
            eq_cache.bulk_update_mappings(Compound, compounds)
            eq_cache.commit()
            compounds.clear()

        args = list(query.yield_per(batch_size))
        chunk_size = min(max(len(args) // command.processes, 1), batch_size)
        with multiprocessing.get_context("spawn").Pool(
            processes=command.processes,
            initializer=cls.setup,
            initargs=(
                command.minimum_ph,
                command.maximum_ph,
                command.fixed_ph,
                command.use_large_model,
            ),
        ) as pool:
            result_iter = pool.imap_unordered(
                cls.run,
                args,
                chunksize=chunk_size,
            )
            for obj in (
                result
                for result in tqdm(
                    result_iter,
                    total=len(args),
                    desc="Compound",
                    unit_scale=True,
                )
                if result is not None
            ):
                compounds.append(obj)
                if len(compounds) >= batch_size:
                    update_cache()
            else:
                update_cache()

    @staticmethod
    def setup(
        minimum_ph: float,
        maximum_ph: float,
        fixed_ph: float,
        use_large_model: bool,
    ) -> None:
        """Set up globally configured ChemAxon adapters."""
        global _pka
        global _majorms

        _pka = ChemAxonProtonDissociationConstantsService(
            minimum_ph=minimum_ph,
            minimum_basic_pka=minimum_ph,
            maximum_ph=maximum_ph,
            maximum_acidic_pka=maximum_ph,
            use_large_model=use_large_model,
        )
        _majorms = ChemAxonMajorMicrospeciesService(ph=fixed_ph)

    @staticmethod
    def run(row: CompoundStructure) -> Optional[Dict]:
        """Run all ChemAxon Marvin predictions returning a molecular entity."""
        global _pka
        global _majorms

        logger.debug(row.inchi_key)

        molecular_entity = ChemAxonMolecularEntityFactory.make(
            structure=Structure(
                identifier=StructureIdentifier(inchikey=row.inchi_key, inchi=row.inchi),
                # We disable SMILES in order to be in line with previous eQuilibrator
                # versions.
                smiles=None,
            ),
            majorms_service=_majorms,
            pka_service=_pka,
        )
        if molecular_entity is None:
            return {
                "id": row.id,
                "dissociation_constants": [],
            }

        result = {
            "id": row.id,
            "dissociation_constants": molecular_entity.pka_values,
        }
        if not molecular_entity.microspecies:
            return result
        major_ms = molecular_entity.microspecies[0]
        result["atom_bag"] = major_ms.atom_bag
        return result
