# The MIT License (MIT)
#
# Copyright (c) 2021, Moritz E. Beber.
# Copyright (c) 2018 Institute for Molecular Systems Biology, ETH Zurich.
# Copyright (c) 2018 Novo Nordisk Foundation Center for Biosustainability,
# Technical University of Denmark
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


"""Define the command line interface (CLI) for generating assets."""


import logging
import os
from pathlib import Path
from typing import Optional

import click
import click_log
from component_contribution.trainer import Trainer
from component_contribution.training_data import FullTrainingDataFactory
from equilibrator_cache import Base, CompoundCache
from equilibrator_cheminfo.application.service import CheminformaticsBackend
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from equilibrator_assets.application.service import (
    ApplicationServiceRegistry,
    CompoundExceptionsService,
    CompoundMergingService,
    GroupDecompositionService,
    MagnesiumDissociationConstantsService,
    MicrospeciesCompletionService,
    MolecularEntityServiceCommand,
    RegistryMergingService,
)


logger = logging.getLogger()
click_log.basic_config(logger)
Session = sessionmaker()


try:
    NUM_PROCESSES = len(os.sched_getaffinity(0))
except (AttributeError, OSError):
    logger.warning("Could not determine the number of cores available - assuming 1.")
    NUM_PROCESSES = 1
DEFAULT_DATABASE_URL = "sqlite:///compounds.sqlite"


@click.group()
@click.help_option("--help", "-h")
@click_log.simple_verbosity_option(
    logger,
    default="INFO",
    show_default=True,
    type=click.Choice(["CRITICAL", "ERROR", "WARN", "INFO", "DEBUG"]),
)
def cli():
    """Command line interface to populate and update the equilibrator cache."""
    if logger.isEnabledFor(logging.DEBUG):
        logging.getLogger("sqlalchemy.engine").setLevel(logging.DEBUG)


@cli.command()
@click.help_option("--help", "-h")
@click.option(
    "--db-url",
    metavar="URL",
    default=DEFAULT_DATABASE_URL,
    show_default=True,
    help="A string interpreted as an rfc1738 compatible database URL where the "
    "resulting compounds are stored.",
)
@click.argument("metanetx")
def init_registry(metanetx: str, db_url: str) -> None:
    """
    Initialize the compound cache by merging the required registries.

    \b
    METANETX: An rfc1738 compatible database URL of the cobra-component-models
        parsed from MetaNetX.

    """  # noqa: D301
    logger.info("Connect to MetaNetX cobra-component-models.")
    cobra_db = Session(bind=create_engine(metanetx))

    logger.info("Initialize eQuilibrator compound cache.")
    eq_cache = Session(bind=create_engine(db_url))
    Base.metadata.drop_all(eq_cache.bind)
    Base.metadata.create_all(eq_cache.bind)

    logger.info("Create identifier registries.")
    RegistryMergingService.batch_merge(cobra_db, eq_cache)


@cli.command()
@click.help_option("--help", "-h")
@click.option(
    "--db-url",
    metavar="URL",
    default=DEFAULT_DATABASE_URL,
    show_default=True,
    help="A string interpreted as an rfc1738 compatible database URL where the "
    "resulting compounds are stored.",
)
@click.option(
    "--batch-size",
    type=int,
    default=1000,
    show_default=True,
    help="The size of batches of compounds to transform at a time.",
)
@click.argument("metanetx")
def merge_compounds(metanetx: str, db_url: str, batch_size: int) -> None:
    """
    Merge MetaNetX chemicals with molecular entities into compound cache.

    \b
    METANETX: An rfc1738 compatible database URL of the cobra-component-models
        parsed from MetaNetX.

    """  # noqa: D301
    logger.info("Connect to MetaNetX cobra-component-models.")
    cobra_db = Session(bind=create_engine(metanetx))

    logger.info("Connect to eQuilibrator compound cache.")
    eq_cache = Session(bind=create_engine(db_url))

    logger.info("Create compounds with microspecies.")
    CompoundMergingService.batch_merge(cobra_db, eq_cache, batch_size)


@cli.command()
@click.help_option("--help", "-h")
@click.option(
    "--db-url",
    metavar="URL",
    default=DEFAULT_DATABASE_URL,
    show_default=True,
    help="A string interpreted as an rfc1738 compatible database URL where the "
    "resulting compounds are stored.",
)
@click.option(
    "--exceptions",
    metavar="EXCEPTIONS",
    default=None,
    show_default=True,
    help="The path to a table of compound exceptions that defines their atom bags. "
    "By default, uses the version stored on Zenodo.",
)
def compound_exceptions(db_url: str, exceptions: Optional[str]) -> None:
    """Handle manually defined compound exceptions."""
    logger.info("Connect to eQuilibrator compound cache.")
    eq_cache = Session(bind=create_engine(db_url))

    logger.info("Update compound exceptions.")
    CompoundExceptionsService.handle_exceptions(eq_cache, exceptions)


@cli.command()
@click.help_option("--help", "-h")
@click.option(
    "--db-url",
    metavar="URL",
    default=DEFAULT_DATABASE_URL,
    show_default=True,
    help="A string interpreted as an rfc1738 compatible database URL where the "
    "resulting compounds are stored.",
)
@click.option(
    "--minimum-ph",
    type=float,
    default=0.0,
    show_default=True,
    help="The minimum pH value to consider.",
)
@click.option(
    "--maximum-ph",
    type=float,
    default=14.0,
    show_default=True,
    help="The maximum pH value to consider.",
)
@click.option(
    "--ph",
    type=float,
    default=7.0,
    show_default=True,
    help="The pH value at which to determine the major microspecies.",
)
@click.option(
    "--large-model/--small-model",
    is_flag=True,
    default=False,
    show_default=True,
    help="Use a model for pKa values estimation that is suitable for large "
    "molecules. Without this flag a small model is used which is faster and works "
    "fine for most metabolites.",
)
@click.option(
    "--processes",
    type=int,
    default=NUM_PROCESSES,
    show_default=True,
    help="The number of parallel processes to start.",
)
@click.option(
    "--backend",
    type=CheminformaticsBackend,
    default=CheminformaticsBackend.ChemAxon,
    show_default=True,
    help="The cheminformatics backend to use for pKa prediction.",
)
def proton_dissociation(
    db_url: str,
    minimum_ph: float,
    maximum_ph: float,
    ph: float,
    large_model: bool,
    processes: int,
    backend: CheminformaticsBackend,
) -> None:
    """Populate compounds with proton dissociation constants and atom bags."""
    command = MolecularEntityServiceCommand(
        minimum_ph=minimum_ph,
        maximum_ph=maximum_ph,
        fixed_ph=ph,
        use_large_model=large_model,
        processes=processes,
    )

    logger.info("Connect to eQuilibrator compound cache.")
    eq_cache = Session(bind=create_engine(db_url))

    logger.info("Add proton dissociation constants and atom bags.")
    ApplicationServiceRegistry.molecular_entity_service(backend).batch_populate(
        eq_cache, command
    )


@cli.command()
@click.help_option("--help", "-h")
@click.option(
    "--db-url",
    metavar="URL",
    default=DEFAULT_DATABASE_URL,
    show_default=True,
    help="A string interpreted as an rfc1738 compatible database URL where the "
    "resulting compounds are stored.",
)
@click.option(
    "--magnesium",
    metavar="MAGNESIUM",
    default=None,
    show_default=True,
    help="The path to a table of magnesium dissociation constants. "
    "By default, uses the version stored on Zenodo.",
)
def magnesium_dissociation(db_url: str, magnesium: Optional[str]) -> None:
    """Add magnesium dissociation constants."""
    logger.info("Connect to eQuilibrator compound cache.")
    eq_cache = Session(bind=create_engine(db_url))

    logger.info("Add magnesium dissociation constants.")
    MagnesiumDissociationConstantsService.batch_populate(eq_cache, magnesium)


@cli.command()
@click.help_option("--help", "-h")
@click.option(
    "--db-url",
    metavar="URL",
    default=DEFAULT_DATABASE_URL,
    show_default=True,
    help="A string interpreted as an rfc1738 compatible database URL where the "
    "resulting compounds are stored.",
)
@click.option(
    "--log-file",
    type=Path,
    default=Path("error.log"),
    show_default=True,
    help="The file where to log errors.",
)
def populate_microspecies(db_url: str, log_file: Path) -> None:
    """Populate all compound microspecies."""
    logger.info("Connect to eQuilibrator compound cache.")
    eq_cache = Session(bind=create_engine(db_url))

    logger.info("Complete microspecies.")
    MicrospeciesCompletionService.batch_populate(eq_cache, log_file)


@cli.command()
@click.help_option("--help", "-h")
@click.option(
    "--db-url",
    metavar="URL",
    default=DEFAULT_DATABASE_URL,
    show_default=True,
    help="A string interpreted as an rfc1738 compatible database URL where the "
    "resulting compounds are stored.",
)
@click.option(
    "--processes",
    type=int,
    default=NUM_PROCESSES,
    show_default=True,
    help="The number of parallel processes to start.",
)
@click.option(
    "--log-file",
    type=Path,
    default=Path("error.log"),
    show_default=True,
    help="The file where to log errors.",
)
def decompose_compounds(db_url: str, log_file: Path, processes: int) -> None:
    """Decompose all compounds into groups."""
    logger.info("Connect to eQuilibrator compound cache.")
    eq_cache = Session(bind=create_engine(db_url))

    logger.info("Decompose compounds.")
    GroupDecompositionService.batch_decompose(eq_cache, log_file, processes=processes)


@cli.command()
@click.help_option("--help", "-h")
@click.option(
    "--db-url",
    metavar="URL",
    default=DEFAULT_DATABASE_URL,
    show_default=True,
    help="A string interpreted as an rfc1738 compatible database URL where the "
    "resulting compounds are stored.",
)
@click.option(
    "--tecrdb",
    metavar="TECRDB_PATH",
    default=None,
    show_default=True,
    help="The path to a local version of the TECR database. "
    "By default, uses the version stored on Zenodo.",
)
@click.option(
    "--redox",
    metavar="REDOX_PATH",
    default=None,
    show_default=True,
    help="The path to a local version of the reduction potential database. "
    "By default, uses the version stored on Zenodo.",
)
@click.option(
    "--formation",
    metavar="FORMATION",
    default=None,
    show_default=True,
    help="The path to a local version of the formation energy database. "
    "By default, uses the version stored on Zenodo.",
)
@click.option(
    "--parameters",
    type=Path,
    default=Path("cc_params.npz"),
    show_default=True,
    help="The path where to store the trained model parameters.",
)
def train(
    db_url: str,
    tecrdb: Optional[str],
    redox: Optional[str],
    formation: Optional[str],
    parameters: Path,
) -> None:
    """Decompose all compounds into groups."""
    logger.info("Connect to eQuilibrator compound cache.")
    ccache = CompoundCache(create_engine(db_url))

    logger.info("Load training data.")
    training_data = FullTrainingDataFactory(ccache=ccache,).make(
        tecrdb,
        redox,
        formation,
        override_p_mg=None,
        override_temperature=None,
    )
    logger.info("Train a component contribution model.")
    params = Trainer.train(training_data)
    params.to_npz(parameters)
