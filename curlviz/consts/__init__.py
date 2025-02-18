from . import default

__all__ = ["default"]

"""Maximum number of stones on a sheet

Regulation:
    Each team plays eight stones in an end, thus the maximum number of stones in an end should be 16.
"""

MAX_NUM_OF_STONES: int = 16

"""Stone radius

Regulation:
    The stone circumference must be less then or equal to 0.914 m (= 36 in).
"""
STONE_RADIUS: float = 0.145

STONE_BORDER_RATIO: float = 0.40

# 6 ft
_SIX_FEET: float = 1.829
# distance between Hack-line and Back-line
_HACK_BACK: float = _SIX_FEET
# distance between Back-line and Tee-line
_BACK_TEE: float = _SIX_FEET
# distance between Tee-line and Hog-line
_TEE_HOG: float = 6.401
# distance between Tee-line and the center of the sheet
_TEE_CENTER: float = 17.375

"""Distance to the Hack-line

The distance from the origin to the Hack-line.
Since the y-origin is Hack-line, this value must be `0.0`.
"""
HACK: float = 0.0

"""Distance to the center of the sheet

This value is defined as the distance from the origin to the center of the sheet.
"""
CENTER: float = HACK + _HACK_BACK + _BACK_TEE + _TEE_CENTER

"""Distance to Hog-line from Hack-line

This value is defined as the distance from the origin to the Hog-line.
"""
HOG_LINE: float = CENTER + _TEE_CENTER - _TEE_HOG

"""Distance to Tee-line

This value is defined as the distance from the origin to the Tee-line
"""
TEE_LINE: float = HOG_LINE + _TEE_HOG

"""Distance to Back-line

This value is defined as the distance from the origin to the Back-line
"""
BACK_LINE: float = TEE_LINE + _BACK_TEE

"""Line width

Regulation:
    The width of lines must be less than or equal to 13 mm (= 0.5 in).
"""
LINE_WIDTH: float = 0.013

"""Radii of house circles

Regulation:
    The house is shown with four concentric circles.
    The radii must be 0.152 m (= 6 in), 0.610 m (= 2 ft), 1.219 m (= 4 ft), and 1.829 m (= 6 ft).
"""
HOUSE_RADII: list[float] = [
    0.152,  # => 6 in
    0.610,  # => 2 ft
    1.219,  # => 4 ft
    _SIX_FEET,  # => 6 ft
]
