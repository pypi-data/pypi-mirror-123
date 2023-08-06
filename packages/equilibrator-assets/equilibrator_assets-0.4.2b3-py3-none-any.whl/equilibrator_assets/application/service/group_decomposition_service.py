"""Provide a service for decomposing compounds into chemical groups."""


import logging
import multiprocessing
from pathlib import Path
from typing import Optional

from equilibrator_cache import Compound
from sqlalchemy.orm import sessionmaker
from tqdm import tqdm

from equilibrator_assets.domain import (
    GroupDecomposer,
    GroupDecompositionError,
    Molecule,
)


Session = sessionmaker()


class GroupDecompositionService:
    """Define a service for decomposing compounds into chemical groups."""

    @classmethod
    def batch_decompose(
        cls,
        eq_cache: Session,
        log_file: Path,
        processes: int,
        batch_size: int = 1000,
    ) -> None:
        """Decompose all compounds in the cache that have an InChI."""
        if processes == 1:
            cls.setup(log_file)
            cls._sequential(eq_cache, batch_size)
            return

        query = (
            eq_cache.query(
                Compound.id, Compound.inchi_key, Compound.inchi, Compound.smiles
            )
            .select_from(Compound)
            .filter(Compound.inchi.is_not(None))
        )
        compounds = []

        def update_cache():
            eq_cache.bulk_update_mappings(Compound, compounds)
            eq_cache.commit()
            compounds.clear()

        args = list(query.yield_per(batch_size))
        chunk_size = min(max(len(args) // processes, 1), batch_size)
        with multiprocessing.Pool(
            processes=processes, initializer=cls.setup, initargs=(log_file,)
        ) as pool:
            result_iter = pool.imap_unordered(
                cls.decompose_compound, args, chunksize=chunk_size
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

    @classmethod
    def _sequential(cls, eq_cache: Session, batch_size: int) -> None:
        """Perform the decomposition sequentially."""
        query = (
            eq_cache.query(Compound.id, Compound.inchi, Compound.smiles)
            .select_from(Compound)
            .filter(Compound.inchi.is_not(None))
        )
        compounds = []

        def update_cache():
            eq_cache.bulk_update_mappings(Compound, compounds)
            eq_cache.commit()
            compounds.clear()

        args = list(query.yield_per(batch_size))
        for compound in tqdm(
            args,
            total=len(args),
            desc="Compound",
            unit_scale=True,
        ):
            if (result := cls.decompose_compound(compound)) is not None:
                compounds.append(result)
            if len(compounds) >= batch_size:
                update_cache()
        else:
            update_cache()

    @staticmethod
    def setup(log_file: Path):
        """Perform global setup for multiprocessing workers."""
        global _decomposer
        global _file_logger

        _decomposer = GroupDecomposer()
        _file_logger = logging.getLogger(__name__)
        _file_logger.setLevel(logging.ERROR)
        _file_logger.propagate = False
        _file_logger.addHandler(logging.FileHandler(log_file))

    @staticmethod
    def decompose_compound(compound: Compound) -> Optional[dict]:
        """Decompose an individual compound."""
        global _decomposer
        global _file_logger

        if compound.smiles:
            mol = Molecule.FromSmiles(compound.smiles)
        else:
            mol = Molecule.FromInChI(compound.inchi)
        try:
            decomposition = _decomposer.Decompose(
                mol, ignore_protonations=False, raise_exception=True
            )
        except GroupDecompositionError:
            _file_logger.error(
                f"Failed to decompose compound {compound.id} "
                f"(InChIKey={compound.inchi_key}) into groups."
            )
            return {
                "id": compound.id,
                "group_vector": [],
            }
        else:
            return {
                "id": compound.id,
                "group_vector": list(decomposition.AsVector()),
            }
