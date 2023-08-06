import sys
import logging

entry_points = ["mastprov", "imasprov"]

if not any(entry_point in sys.argv[0] for entry_point in entry_points): # To suppress irrelevant warning if using CLI entry points
    logging.basicConfig(level=logging.INFO, format="%(message)s")

try:
    from .imasprov import ImasProv
except ModuleNotFoundError as error:
    logging.info(
        f"{error}. An IMAS installation is required to write provenance for IMAS formatted data."
    )
try:
    from .mastprov import write_provenance
except ModuleNotFoundError as error:
    logging.info(f"{error}. A UDA installation is required write provenance for MAST signals.")
except ImportError as error:
    logging.info(f"{error}. A UDA installation is required write provenance for MAST signals.")

__version__ = "1.1.1"
