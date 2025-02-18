"""Example to create a sheet image from the stone data given as a JSON file

This script loads stone information from JSON file (`stones.json`), and export the sheet image.
"""

import json

import curlviz


def main() -> None:
    output = "from_json.pdf"

    sheet = curlviz.Sheet()
    with open("stones.json") as fs:
        js = json.load(fs)
        for stone_dict in js["stones"]:
            stone = curlviz.Stone(**stone_dict)  # Convert dict to stone
            sheet.put(stone)  # Put stone on the sheet

    # Export the sheet image in PDF format with the default configuration
    stream = curlviz.stream.PDF(output)
    stream.export(sheet)


if __name__ == "__main__":
    main()
