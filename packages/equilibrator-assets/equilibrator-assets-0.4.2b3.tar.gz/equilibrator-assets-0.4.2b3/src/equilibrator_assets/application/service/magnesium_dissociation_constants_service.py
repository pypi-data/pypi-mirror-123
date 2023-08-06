"""Provide a service class that adds magnesium dissociation constants."""


import logging
from pathlib import Path
from typing import Any, Optional, Union

import pandas as pd
from equilibrator_cache import Compound, MagnesiumDissociationConstant
from equilibrator_cache.zenodo import ZenodoSettings, get_cached_filepath
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import sessionmaker
from tqdm import tqdm


logger = logging.getLogger(__name__)


MAGNESIUM_DISSOCIATION_SETTINGS = ZenodoSettings(
    doi="10.5281/zenodo.",
    filename="",
    md5="",
    url="https://zenodo.org/api/",
)


Session = sessionmaker()


class MagnesiumDissociationConstantsService:
    """Provide a service class that adds magnesium dissociation constants."""

    @classmethod
    def batch_populate(
        cls, eq_cache: Session, magnesium: Optional[Union[Path, str]] = None
    ) -> None:
        """Add all magnesium dissociation constants defined in a table."""
        magnesium_df = cls._extract_magnesium_dissociation_constants_table(magnesium)
        query = (
            eq_cache.query(Compound)
            .select_from(Compound)
            .outerjoin(Compound.magnesium_dissociation_constants)
        )
        errors = []
        for key, sub in tqdm(
            magnesium_df.groupby("inchi_key", sort=False, as_index=False),
            total=len(magnesium_df["inchi_key"].unique()),
            unit_scale=True,
            desc="Magnesium Dissociation",
        ):
            logger.debug(key)
            try:
                compound = query.filter(Compound.inchi_key == key).one()
            except NoResultFound:
                logger.error("Compound %s was not found in the cache.", key)
                errors.append(key)
                continue
            for row in sub.itertuples(index=False):
                compound.magnesium_dissociation_constants.append(
                    MagnesiumDissociationConstant(
                        number_protons=cls._ensure_none(row.n_h),
                        number_magnesiums=cls._ensure_none(row.n_mg),
                        dissociation_constant=cls._ensure_none(row.pk_d),
                    )
                )
            eq_cache.commit()
        if errors:
            logger.debug(", ".join(errors))

    @classmethod
    def _extract_magnesium_dissociation_constants_table(
        cls, magnesium: Optional[Union[Path, str]] = None
    ) -> pd.DataFrame:
        """Extract the correctly transformed magnesium information."""
        if magnesium is None:
            magnesium = get_cached_filepath(MAGNESIUM_DISSOCIATION_SETTINGS)
        raw = pd.read_csv(magnesium)
        return raw.loc[
            raw["n_h"].notnull() & raw["n_mg"].notnull() & raw["pk_d"].notnull(),
            :,
        ]

    @classmethod
    def _ensure_none(cls, value: Any) -> Optional[Any]:
        """Ensure that values are native `None` instead of `nan`."""
        return value if pd.notnull(value) else None
