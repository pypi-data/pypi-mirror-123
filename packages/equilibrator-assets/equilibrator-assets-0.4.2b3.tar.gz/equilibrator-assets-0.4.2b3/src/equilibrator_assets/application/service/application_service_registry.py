"""Provide an application service registry that returns configured service instances."""


from typing import Type

from equilibrator_cheminfo.application.service import CheminformaticsBackend

from .abstract_molecular_entity_service import AbstractMolecularEntityService


class ApplicationServiceRegistry:
    """Define an application service registry to access configured service instances."""

    @classmethod
    def molecular_entity_service(
        cls, backend: CheminformaticsBackend
    ) -> Type[AbstractMolecularEntityService]:
        """Return a molecular entity service based on the cheminformatics backend."""
        if backend == CheminformaticsBackend.ChemAxon:
            from .chemaxon_molecular_entity_service import (
                ChemAxonMolecularEntityService,
            )

            return ChemAxonMolecularEntityService
        else:
            raise ValueError(
                f"The chosen cheminformatics backend {backend.value} does not support "
                f"pKa prediciton."
            )
