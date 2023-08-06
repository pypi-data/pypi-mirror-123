"""Provide a registry merging service."""


import cobra_component_models.orm as cobra_orm
import equilibrator_cache.models as eq_orm
from sqlalchemy.orm import sessionmaker
from tqdm import tqdm


Session = sessionmaker()


class RegistryMergingService:
    """Define a service that merges COBRA namespaces into eQuilibrator registries."""

    @classmethod
    def batch_merge(
        cls,
        cobra_db: Session,
        eq_cache: Session,
    ) -> None:
        """
        Merge registries from cobra-component-models into the compound cache.

        The compound cache is assumed to be empty so no registries should previously
        exist.

        """
        query = cobra_db.query(cobra_orm.Namespace)
        count = query.count()
        for namespace in tqdm(query, total=count, unit_scale=True, desc="Registry"):
            eq_cache.add(cls.merge_registry(namespace))
        eq_cache.commit()

    @classmethod
    def merge_registry(cls, namespace: cobra_orm.Namespace) -> eq_orm.Registry:
        """Create a single eQuilibrator registry using a namespace object."""
        return eq_orm.Registry(
            namespace=namespace.prefix,
            name=namespace.name,
            is_prefixed=namespace.embedded_prefix,
            pattern=namespace.pattern,
        )
