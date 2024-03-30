#!/usr/bin/env python
import pandas as pd
from datetime import datetime, timedelta
import argparse

from config import LR_CATALOG_FILE
from lightroom import LightroomDB

FIELD_NAMES_LIST = [
    "captureTime",
    "lensName",
    "cameraName",
    "focalLength",
    "aperture",
    "shutterSpeed",
]


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
    

    # Parse the command line arguments
    args = parser.parse_args()
    return args


def main():
    args = parse_arguments()
    
    lightroom_db = LightroomDB(args.catalog_path)
    results = lightroom_db.get_all_picks(args.picks_only)
    
    selected_data = [{key: item[key] for key in FIELD_NAMES_LIST} for item in results]
    data = pd.DataFrame(selected_data)

    # Convert the "captureTime" column to datetime type
    data["captureTime"] = pd.to_datetime(data["captureTime"], format="mixed")

    # Calculate the date one year ago based on the lookback argument
    one_year_ago = data["captureTime"].max() - timedelta(days=args.lookback)

    # Filter out images taken in the last year and exclude iPhone camera usage
    filtered_data = data[
        (data["captureTime"] > one_year_ago)
        & (~data["cameraName"].str.contains("iPhone", case=False, na=False))
    ]

    # Group by property, count the total pictures taken with each lens, and sort in descending order
    lens_usage = (
        filtered_data.groupby(args.property)
        .size()
        .sort_values(ascending=False)
        .reset_index(name="Total Pictures")
    )

    # Display the sorted list of lenses and the total pictures taken with each
    print(lens_usage)


if __name__ == "__main__":
    main()
