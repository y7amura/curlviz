from typing import List


"""Default ppm

This is the default value of pixels-per-meter that determines the size of the exported sheet image.
"""
PPM: int = 20

"""Default sheet width

Regulation:
    The sheet width must be less than or equal to 4.750 m (= 15 ft 7 in).
"""
SHEET_WIDTH: float = 4.750

"""Default background color

This is the default color to fill the background of the sheet.
The default is non-transparent white.
"""
BACKGROUND_COLOR: str = "#FFFFFFFF"

"""Default line color

This is the default color to draw lines on the sheet.
The default is non-transparent black.
"""
LINE_COLOR: str = "#000000FF"

"""Default color of the inner circle of the house

This is the default color to fill the inner circle of the house.
The default is 50%-transparent red.
"""
INNER_HOUSE_COLOR: str = "#FF000080"

"""Default color of the outer circle of the house

This is the default color to fill the outer circle of the house.
The default is 50%-transparent blue.
"""
OUTER_HOUSE_COLOR: str = "#0000FF80"

"""Default stone colors

The is a set of default colors to fill the stones.
The default is non-transparent red for Team0, and non-transparent yellow for Team1.
"""
STONE_COLORS: List[str] = [
    "#FF0000FF",  # => team0
    "#FFFF00FF",  # => team1
]
