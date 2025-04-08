import pandas as pd # type: ignore
from datetime import timedelta
from args import parse_arguments
from lightroom import FIELD_NAMES_LIST, LightroomDB


def get_filtered_images():
    args = parse_arguments()
    
    lightroom_db = LightroomDB(args.catalog_path)
    results = lightroom_db.get_all_images(args.picks_only, args.rating)
    
    selected_data = [{key: item[key] for key in FIELD_NAMES_LIST} for item in results]
    data = pd.DataFrame(selected_data)

    # Convert the "captureTime" column to datetime type
    data["captureTime"] = pd.to_datetime(data["captureTime"], format="mixed")

    # Calculate the date one year ago based on the lookback argument
    start_date = data["captureTime"].max() - timedelta(days=args.lookback)

    # Filter out images taken in the last year and exclude iPhone camera usage
    filtered_data = data[
        (data["captureTime"] > start_date)
        & (~data["cameraName"].str.contains("iPhone", case=False, na=False))
    ]

    return filtered_data 
    