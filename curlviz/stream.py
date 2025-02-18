from abc import ABC, abstractmethod
from os import PathLike, makedirs, path
from pathlib import PurePath

from curlviz import Sheet

from .config import Config
from .drawer import Drawer


def _canonize(filepath: str, ext: str) -> PathLike:
    if path.basename(filepath) == "":
        filepath = path.join(filepath, f"output.{ext}")
    if path.splitext(filepath)[1] != f".{ext}":
        filepath = f"{filepath}.{ext}"
    return PurePath(filepath)


def _prepare(filepath: PathLike) -> PathLike:
    filepath = path.abspath(filepath)
    makedirs(path.dirname(filepath), exist_ok=True)
    return filepath


class Stream(ABC):
    """Abstract stream to export a sheet image

    This is an abstract class for sheet exporting streams.
    """

    def __init__(self, config: Config) -> None:
        """Initialize the stream

        Arguments:
            config (Config): drawing configuration
        """
        self.config = config

    @abstractmethod
    def export(self, sheet: Sheet) -> None:
        """Exports the sheet image

        This method exports the sheet image to the output stream given by the specific implementation.

        Arguments:
            sheet (Sheet): state of the sheet to be exported
        """
        ...


class PDF(Stream):
    """PDF stream

    This stream exports the sheet image in PDF format.
    The exported file is a single page PDF file.
    """

    def __init__(self, filepath: str, config: Config = Config()) -> None:
        """Initializes PDF stream

        Arguments:
            filepath (str): path to the exported file
            config (curlviz.Config): exporting configuration
        """
        super().__init__(config)
        self.filepath = _canonize(filepath, "pdf")

    def export(self, sheet: Sheet) -> None:
        """Exports a PDF file

        Arguments:
            sheet (curlviz.Sheet): the sheet to be drawn
        """
        import skia

        filepath = _prepare(self.filepath)
        stream = skia.FILEWStream(filepath)
        with skia.PDF.MakeDocument(stream) as document:
            drawer = Drawer(self.config)
            width, height = drawer.canvas_size()
            with document.page(width, height) as canvas:
                drawer.draw(canvas, sheet)


class SVG(Stream):
    """SVG stream

    This stream exports the sheet image in SVG format.
    """

    def __init__(self, filepath: str, config: Config = Config()) -> None:
        """Initializes SVG stream

        Arguments:
            filepath (str): path to the exported file
            config (curlviz.Config): exporting configuration
        """
        import sys

        super().__init__(config)
        self.filepath = _canonize(filepath, "svg")
        print("[Warning] Lines will be disappeared in SVG format.", file=sys.stderr)

    def export(self, sheet: Sheet) -> None:
        """Exports a SVG file

        Arguments:
            sheet (curlviz.Sheet): the sheet to be drawn
        """
        import skia

        drawer = Drawer(self.config)
        filepath = _prepare(self.filepath)
        stream = skia.FILEWStream(filepath)
        canvas = skia.SVGCanvas.Make(drawer.canvas_size(), stream)
        drawer.draw(canvas, sheet)
        del canvas
        stream.flush()


class PNG(Stream):
    """PNG stream

    This stream exports the sheet image in PNG format.
    Use this stream for exporting a raster image.
    """

    def __init__(self, filepath: str, config: Config = Config()) -> None:
        """Initializes PNG stream

        Arguments:
            filepath (str): path to the exported file
            config (curlviz.Config): exporting configuration
        """
        super().__init__(config)
        self.filepath = _canonize(filepath, "png")

    def export(self, sheet: Sheet) -> None:
        """Exports a PNG file

        Arguments:
            sheet (curlviz.Sheet): the sheet to be drawn
        """
        import skia

        drawer = Drawer(self.config)
        surface = skia.Surface(*drawer.canvas_size())
        with surface as canvas:
            drawer.draw(canvas, sheet)
        image = surface.makeImageSnapshot()

        filepath = _prepare(self.filepath)
        image.save(filepath, skia.kPNG)
