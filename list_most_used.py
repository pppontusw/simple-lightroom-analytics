#!/usr/bin/env python
from args import parse_arguments
from data import get_filtered_images



def main():
    filtered_data = get_filtered_images()

    # Group by property, count the total pictures taken with each lens, and sort in descending order
    lens_usage = (
        filtered_data.groupby(parse_arguments().property)
        .size()
        .sort_values(ascending=False)
        .reset_index(name="Total Pictures")
    )

    # Display the sorted list of lenses and the total pictures taken with each
    print(lens_usage)


if __name__ == "__main__":
    main()
