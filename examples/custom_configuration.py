"""Example to create a sheet image with a customized configuration

This script provides a sample code how to modify the configuration
and to apply the modified configuration for exporting.
"""

import json

import curlviz

stones = [
    curlviz.Stone(x=0.08, y=35.3, team=curlviz.Team.Team0),
    curlviz.Stone(x=1.57, y=37.2, team=curlviz.Team.Team1),
    curlviz.Stone(x=0.12, y=37.9, team=curlviz.Team.Team0),
]


def main() -> None:
    output = "custom_configuration.pdf"

    config = curlviz.Config()
    config.inversion = True  # Make up-side down
    config.ppm = 50  # Make the image larger
    config.colors.line = "#555555FF"  # change line color
    config.colors.outer_house_circle = "#00880080"  # change outer house color
    config.colors.stones = reversed(config.colors.stones)  # swap stone colors

    sheet = curlviz.Sheet()
    for stone in stones:
        sheet.put(stone)

    # Export the sheet image in PDF format with the modified configuration
    stream = curlviz.stream.PDF(output, config)
    stream.export(sheet)


if __name__ == "__main__":
    main()
