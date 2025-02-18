from dataclasses import dataclass, field
import re

from curlviz.consts import default

CODE_PATTERN = re.compile(r"#[0-9a-fA-F]{8}")


def validate_color_code(code: str) -> bool:
    return re.match(CODE_PATTERN, code)


@dataclass
class Colors:
    """Drawing colors

    Attributes:
        background (str): background color (default: non-transparent white)
        line (str): line color (default: non-transparent black)
        inner_house_circle (str): inner-circle color of the house (default: 50%-transparent blue)
        outer_house_circle (str): outer-circle color of the house (default: 50%-transparent red)
        stones (list[str]): stone colors (default: [non-transparent red, non-transparent yellow])
    """

    background: str = default.BACKGROUND_COLOR
    line: str = default.LINE_COLOR
    inner_house_circle: str = default.INNER_HOUSE_COLOR
    outer_house_circle: str = default.OUTER_HOUSE_COLOR
    stones: list[str] = field(default_factory=lambda: default.STONE_COLORS)

    def __post_init__(self):
        from dataclasses import asdict

        for key, value in asdict(self).items():
            match key:
                case "stones":
                    for team, color in enumerate(self.stones):
                        if not validate_color_code(color):
                            raise ValueError(
                                f"Color code must start with '#' followed by 8 hex digits, but got '{color}' for team{team}'s stone color."
                            )
                case _ if not validate_color_code(value):
                    raise ValueError(
                        f"Color code must start with '#' followed by 8 hex digits, but got '{value}' for {key}."
                    )


@dataclass
class Config:
    """Configuration of a sheet

    Attributes:
        inversion (bool): draw the sheet up-side down if `True` (default: `False`)
        full (bool): [currently no-effect] draw the entire sheet if `True` (default: `False`)
        ppm (int): pixels per meter (default: `20`)
        sheet_width (float): sheet width (default: `4.75` m)
        colors (Colors): drawing colors
    """

    inversion: bool = False
    full: bool = False
    ppm: int = default.PPM
    sheet_width: float = default.SHEET_WIDTH
    colors: Colors = field(default_factory=lambda: Colors())

    def __post_init__(self):
        # if self.full:
        #     raise Warning(
        #         f"Configuration `full` currently has no-effect, set it `False` to suppress this warning."
        #     )
        if self.ppm <= 0:
            raise ValueError(f"PPM must be a positive integer, but got {self.ppm}.")
        if self.sheet_width <= 0:
            raise ValueError(
                f"Sheet width must be positive, but got {self.sheet_width}."
            )
        if isinstance(self.colors, dict):
            self.colors = Colors(**self.colors)
