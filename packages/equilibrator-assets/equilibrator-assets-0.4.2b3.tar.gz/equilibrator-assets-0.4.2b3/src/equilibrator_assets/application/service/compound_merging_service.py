"""Provide a service class that merges COBRA information into the compound cache."""


import logging
from typing import Dict, List, Tuple

import cobra_component_models.orm as cobra_orm
import equilibrator_cache.models as eq_orm
from sqlalchemy.orm import selectinload, sessionmaker
from tqdm import tqdm

from .namespace_registry_mapping_service import NamespaceRegistryMappingService


logger = logging.getLogger(__name__)


Session = sessionmaker()


class CompoundMergingService:
    """Define a service that merges COBRA information into the compound cache."""

    @classmethod
    def batch_merge(
        cls,
        cobra_db: Session,
        eq_cache: Session,
        batch_size: int = 1000,
    ) -> None:
        """Merge all compounds defined by the SQLAlchemy database session."""
        map_service = NamespaceRegistryMappingService(eq_cache)
        query = cobra_db.query(cobra_orm.Compound).select_from(cobra_orm.Compound)
        count = query.count()
        compounds = []
        identifiers = []
        names = []

        def update_cache():
            eq_cache.bulk_insert_mappings(eq_orm.Compound, compounds)
            eq_cache.bulk_insert_mappings(eq_orm.CompoundIdentifier, identifiers)
            eq_cache.bulk_insert_mappings(eq_orm.CompoundName, names)
            eq_cache.commit()
            compounds.clear()
            identifiers.clear()
            names.clear()

        for compound in tqdm(
            query.options(
                selectinload(cobra_orm.Compound.annotation).selectinload(
                    cobra_orm.CompoundAnnotation.namespace
                )
            )
            .options(
                selectinload(cobra_orm.Compound.names).selectinload(
                    cobra_orm.CompoundName.namespace
                )
            )
            .yield_per(batch_size),
            total=count,
            unit_scale=True,
            desc="Compound",
        ):
            compound_obj, identifier_objs, name_objs = cls.merge_compound(
                compound, map_service
            )
            compounds.append(compound_obj)
            identifiers.extend(identifier_objs)
            names.extend(name_objs)
            if len(compounds) >= batch_size:
                update_cache()
        else:
            update_cache()

        assert len(compounds) == 0
        assert len(identifiers) == 0
        assert len(names) == 0

    @classmethod
    def merge_compound(
        cls,
        cobra_compound: cobra_orm.Compound,
        registry_map_service: NamespaceRegistryMappingService,
    ) -> Tuple[Dict, List[Dict], List[Dict]]:
        """Merge a single compound from COBRA model to eQuilibrator."""
        result = {
            "id": cobra_compound.id,
            "inchi_key": cobra_compound.inchi_key,
            "inchi": cobra_compound.inchi,
            "smiles": cobra_compound.smiles,
        }
        identifiers = [
            {
                "accession": identifier.identifier,
                "is_deprecated": identifier.is_deprecated,
                "registry_id": registry_map_service.map(identifier.namespace.prefix).id,
                "compound_id": cobra_compound.id,
            }
            for identifier in cobra_compound.annotation
        ]
        names = [
            {
                "name": name.name,
                "is_preferred": name.is_preferred,
                "registry_id": registry_map_service.map(name.namespace.prefix).id,
                "compound_id": cobra_compound.id,
            }
            for name in cobra_compound.names
        ]
        return result, identifiers, names
