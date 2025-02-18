import argparse
import dataclasses
import io
import json
from os import path
import sys

import curlviz


def show_config(args: argparse.Namespace) -> None:

    def print_config(fs: io.TextIOBase):
        json.dump(dataclasses.asdict(curlviz.Config()), fs, indent=2)

    match args.output:
        case None:
            print_config(sys.stdout)
        case "stderr" | "STDERR":
            print_config(sys.stderr)
        case filepath:
            with open(filepath, "w") as fs:
                print_config(fs)


def export_image(args: argparse.Namespace) -> None:
    def parse_config(filename: str | None):
        if filename is None:
            return curlviz.Config()
        with open(filename, "r") as fs:
            dict = json.load(fs)
            return curlviz.Config(**dict)

    def parse_sheet(filename: str) -> curlviz.Sheet:
        sheet = curlviz.Sheet()
        with open(filename, "r") as fs:
            dict = json.load(fs)
            for stone in dict["stones"]:
                sheet.put(curlviz.Stone(**stone))
        return sheet

    output = args.filename if args.output is None else args.output
    target = args.format if args.output is None else path.splitext(args.output)[1][1:]

    config = parse_config(args.config)
    sheet = parse_sheet(args.filename)
    stream: curlviz.stream.Stream = None
    match target:
        case "pdf":
            stream = curlviz.stream.PDF(output, config)
        case "svg":
            stream = curlviz.stream.SVG(output, config)
        case "png":
            stream = curlviz.stream.PNG(output, config)
        case _:
            msg = f"Unknown target: {target}"
            raise RuntimeError(msg)
    stream.export(sheet)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate a sheet image from a set of stone positions."
    )
    command_group = parser.add_subparsers()

    config_command = command_group.add_parser(
        "config",
        help="Print default config",
    )
    config_command.add_argument(
        "-o",
        "--output",
        default=None,
    )
    config_command.set_defaults(handler=show_config)

    export_command = command_group.add_parser(
        "export",
        help="Export sheet image with given stones",
    )
    export_command.add_argument(
        "filename",
        help="JSON file of stone positions",
    )
    export_command.add_argument(
        "-o",
        "--output",
        default=None,
        help="Set output filename",
    )
    export_command.add_argument(
        "-c",
        "--config",
        default=None,
        help="Set configuration file",
    )
    export_command.add_argument(
        "--format",
        choices=["pdf", "svg", "png"],
        default="pdf",
        help="Set output format",
    )
    export_command.set_defaults(handler=export_image)

    args = parser.parse_args()
    if hasattr(args, "handler"):
        args.handler(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
