"""Provide a service for handling exceptions to the rule."""


import json
from pathlib import Path
from typing import Optional, Union

import pandas as pd
from equilibrator_cache import Compound, CompoundIdentifier, Registry
from equilibrator_cache.zenodo import ZenodoSettings, get_cached_filepath
from sqlalchemy.orm import sessionmaker
from tqdm import tqdm


Session = sessionmaker()


COMPOUND_EXCEPTIONS_SETTINGS = ZenodoSettings(
    doi="10.5281/zenodo.",
    filename="",
    md5="",
    url="https://zenodo.org/api/",
)


class CompoundExceptionsService:
    """Define a service for handling exceptions to the rule."""

    @classmethod
    def handle_exceptions(
        cls, eq_cache: Session, compounds: Optional[Union[Path, str]] = None
    ) -> None:
        """Add any exceptions defined in a tabular format to the compound cache."""
        if compounds is None:
            compounds = get_cached_filepath(COMPOUND_EXCEPTIONS_SETTINGS)
        exceptions = pd.read_table(compounds, sep="\t")
        registry_map = {
            registry.namespace: registry for registry in eq_cache.query(Registry)
        }
        query = (
            eq_cache.query(Compound)
            .select_from(Compound)
            .join(Compound.identifiers, isouter=True)
        )
        for row in tqdm(
            exceptions.itertuples(index=False),
            total=len(exceptions),
            unit_scale=True,
            desc="Compound Exception",
        ):
            compound: Compound = query.filter(
                CompoundIdentifier.registry_id == registry_map[row.namespace].id,
                CompoundIdentifier.accession == row.identifier,
            ).one()
            compound.atom_bag = json.loads(row.atom_bag)
            eq_cache.add(compound)
            eq_cache.commit()
