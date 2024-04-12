#!/usr/bin/env python
import pandas as pd # type: ignore
from datetime import timedelta
from args import parse_arguments
from data import get_filtered_images


def lens_by_year_month(images, property):
    # Create a new DataFrame with columns for Year-Month and LensName
    new_data = pd.DataFrame({
        "Year-Month": images["captureTime"].dt.strftime("%Y-%m"),
        property: images[property]
    })

    # Calculate the count of images for each combination of Year-Month and LensName
    count_data = new_data.groupby(["Year-Month", property]).size().reset_index(name="Count")

    # Save the new data to a CSV file
    count_data.to_csv("output.csv", index=False)


def main():
    filtered_data = get_filtered_images()

    lens_by_year_month(filtered_data, parse_arguments().property)


if __name__ == "__main__":
    main()
