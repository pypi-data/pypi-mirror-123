"""Provide an interface for molecular entity service implementations."""


from abc import ABC, abstractmethod
from typing import Dict, NamedTuple, Optional

from sqlalchemy.orm import sessionmaker


Session = sessionmaker()


class MolecularEntityServiceCommand(NamedTuple):
    """Define a command object that encapsulates molecular entity service arguments."""

    minimum_ph: float
    maximum_ph: float
    fixed_ph: float
    use_large_model: bool
    processes: int


class CompoundStructure(NamedTuple):
    """Define a minimal compound structure."""

    id: int
    inchi_key: str
    inchi: str
    smiles: Optional[str] = None


class AbstractMolecularEntityService(ABC):
    """Define an abstract interface for molecular entity service implementations."""

    @classmethod
    @abstractmethod
    def batch_populate(
        cls,
        eq_cache: Session,
        command: MolecularEntityServiceCommand,
        batch_size: int = 1000,
    ) -> None:
        """Populate every compound in the cache that has an InChI with pKa values."""

    @staticmethod
    @abstractmethod
    def setup(
        minimum_ph: float,
        maximum_ph: float,
        fixed_ph: float,
        use_large_model: bool,
    ) -> None:
        """Set up global services for multiprocessin workers."""

    @staticmethod
    @abstractmethod
    def run(row: CompoundStructure) -> Optional[Dict]:
        """Run all estimation services and return a dictionary structure."""
