"""Provide a namespace to registry mapping service."""


import equilibrator_cache.models as eq_orm
from sqlalchemy.orm import sessionmaker


Session = sessionmaker()


class NamespaceRegistryMappingService:
    """Define a namespace to registry mapping service."""

    def __init__(self, eq_cache: Session) -> None:
        """Initialize a namespace mapping service using an active ORM session."""
        self._registry_map = {
            registry.namespace: registry for registry in eq_cache.query(eq_orm.Registry)
        }

    def map(self, namespace: str) -> eq_orm.Registry:
        """Return the registry with the given namespace string."""
        return self._registry_map[namespace]
