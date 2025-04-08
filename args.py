
import argparse

from config import LR_CATALOG_FILE
from lightroom import FIELD_NAMES_LIST

def parse_arguments():
    # Create an argument parser
    parser = argparse.ArgumentParser(description="List most used lenses")

    # Add an argument for the amount of time to look back
    parser.add_argument(
        "--lookback",
        type=int,
        default=365,
        help="Number of days to look back (default: 365)",
    )

    parser.add_argument(
        "--property",
        type=str,
        default="lensName",
        choices=[f for f in FIELD_NAMES_LIST if f != "captureTime"],
        help="The property to group by (default: lensName)",
    )
    
    parser.add_argument(
        "--catalog-path",
        type=str,
        default=LR_CATALOG_FILE,
        help=f"The path to the Lightroom catalog file (default: {LR_CATALOG_FILE})",
    )

    parser.add_argument(
        "--picks-only",
        action="store_true",
        default=False,
        help="Count only picks (flagged)",
    )
    
    parser.add_argument(
        "--rating",
        type=int,
        default=0,
        help="Count only picks (flagged)",
    )

    # Parse the command line arguments
    args = parser.parse_args()
    return args
