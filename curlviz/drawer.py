import math

import skia

from . import consts
from .config import Config, validate_color_code
from .sheet import Sheet


def color_code_to_rgb(code: str) -> tuple[int, int, int, int]:
    if not validate_color_code(code):
        error_msg = f"Color code must start with '#' followed by 8 hex digits, but got '{code}'"
        raise ValueError(error_msg)
    r = int(code[1:3], 16)
    g = int(code[3:5], 16)
    b = int(code[5:7], 16)
    a = int(code[7:], 16)
    return (r, g, b, a)


class Drawer:
    """Drawer manages drawing the sheet on a canvas."""

    def __init__(self, config: Config) -> None:
        """Initializes the drawer

        Arguments:
            config (curlviz.Config): the configuration to draw sheets
        """
        self.config = config

    def canvas_size(self) -> tuple[int, int]:
        """Returns canvas size

        The canvas size basically depends on `sheet_width` and `ppm` given by the configuration.
        If `full` flag is `True`, the canvas covers the entire sheet between hack-line and back-line,
        otherwise it only covers the play area between hog-line to back-line.
        """
        ppm = self.config.ppm
        width = ppm * self.config.sheet_width
        if self.config.full:
            height = ppm * (consts.BACK_LINE + 4 * consts.STONE_RADIUS)
        else:
            height = ppm * (consts.BACK_LINE - consts.HOG_LINE + 4 * consts.STONE_RADIUS)
        return (math.ceil(width), math.ceil(height))

    def draw(self, canvas: skia.Canvas, sheet: Sheet) -> None:
        """Draws the sheet on the given canvas

        Arguments:
            canvas (skia.Canvas): the canvas to draw a sheet
            sheet (curlviz.Sheet): the sheet to be drawn
        """
        width = canvas.getBaseLayerSize().width()
        height = canvas.getBaseLayerSize().height()

        canvas.save()
        if not self.config.inversion:
            canvas.translate(0, height)
            canvas.scale(1, -1)

        shift = skia.Point(
            x=self.config.sheet_width / 2.0,
            y=((0 if self.config.full else -consts.HOG_LINE) + 2 * consts.STONE_RADIUS),
        )

        ppm = self.config.ppm
        line_width = consts.LINE_WIDTH * ppm

        background_color = skia.Color(*color_code_to_rgb(self.config.colors.background))
        line_color = skia.Color(*color_code_to_rgb(self.config.colors.line))
        inner_house_color = skia.Color(*color_code_to_rgb(self.config.colors.inner_house_circle))
        outer_house_color = skia.Color(*color_code_to_rgb(self.config.colors.outer_house_circle))
        stone_colors = [skia.Color(*color_code_to_rgb(c)) for c in self.config.colors.stones]

        # Clear background
        canvas.clear(0x00000000)
        canvas.drawRect(
            skia.Rect(0, 0, width, height),
            paint=skia.Paint(
                Color=background_color,
                Style=skia.Paint.kStrokeAndFill_Style,
                StrokeWidth=0,
            ),
        )

        # draw house circles
        circle_colors = [
            background_color,
            inner_house_color,
            background_color,
            outer_house_color,
        ]
        circle_center = skia.Point(0, consts.TEE_LINE) + shift
        for radius, color in zip(reversed(consts.HOUSE_RADII), reversed(circle_colors), strict=True):
            canvas.drawCircle(
                center=circle_center * ppm,
                radius=radius * ppm,
                paint=skia.Paint(Color=color, Style=skia.Paint.kFill_Style, AntiAlias=True),
            )

        # draw lines
        pen = skia.Paint(Color=line_color, StrokeWidth=line_width)
        canvas.drawLine((0 + shift.x()) * ppm, 0, (0 + shift.x()) * ppm, height, paint=pen)
        for line in [
            consts.HACK,
            consts.CENTER,
            consts.HOG_LINE,
            consts.TEE_LINE,
            consts.BACK_LINE,
        ]:
            y = line + shift.y()
            if y < 0:
                continue
            canvas.drawLine(0, y * ppm, width, y * ppm, paint=pen)

        # draw stones
        for stone in sheet.stones:
            if not stone.team.is_entity():
                continue
            center = skia.Point(stone.x, stone.y) + shift
            if center.y() < 0:
                continue
            color = stone_colors[stone.team]
            canvas.drawCircle(
                center=center * ppm,
                radius=consts.STONE_RADIUS * ppm,
                paint=skia.Paint(Color=color, Style=skia.Paint.kFill_Style, AntiAlias=True),
            )
            canvas.drawCircle(
                center=center * ppm,
                radius=(1.0 - consts.STONE_BORDER_RATIO / 2.0) * consts.STONE_RADIUS * ppm,
                paint=skia.Paint(
                    Color=line_color,
                    Style=skia.Paint.kStroke_Style,
                    StrokeWidth=consts.STONE_BORDER_RATIO * consts.STONE_RADIUS * ppm,
                    AntiAlias=True,
                ),
            )

        canvas.restore()
