[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# curlviz: A configurable visualization library for a curling sheet

This library helps to create a curling sheet image with the given stones.

This project is not widely tested yet.

## Install the library

### Using UV or Poetry

Configure the `pyproject.toml` as following.

```toml
[project]
...
requires-python = ">=3.12"
dependencies = [
  ...
  "curlviz",
]

[tool.uv.sources]
curlviz = { git = "https://github.com/y7amura/curlviz.git", branch = "main" }

[tool.poetry.dependencies]
curlviz = { git = "https://github.com/y7amura/curlviz.git", branch = "main" }
```

### Using pip

Download the library directly from the GitHub repository.

```sh
$ python3 -V
3.12.0
$ pip install git+https://github.com/y7amura/curlviz.git
$ python3 -m curlviz.cli --help  # shows help if the library is successfully installed
```

## How to use `curlviz` in a Python script

A basic procedure to export a sheet image is following.

1. Encode given stone positions into `curlviz.Stone` objects if required;
2. Prepare a sheet and put stones on the sheet;
3. Prepare an exporting stream;
4. Export the sheet.

The pseudo code below shows an example to export a sheet image in PDF format with default configuration.

See [examples](./examples/) for more details.

```python
import curlviz

# A stone has its position (x, y) and associated team (Team0 or Team1)
#
# The origin of the coordinate of stone positions is the position of the Hack
# in the opposite side of playing area, i.e. the Hack position to play stones.
stones = [
    curlviz.Stone(x=..., y=..., team=curlviz.Team.Team0),
    curlviz.Stone(x=..., y=..., team=curlviz.Team.Team1),
    curlviz.Stone(x=..., y=..., team=curlviz.Team.Team0),
    ...
]

# Prepare a sheet to be exported
sheet = curlviz.Sheet()
for stone in stones:
    sheet.put(stone)  # put stones on the sheet

# Export the sheet image in PDF format with the default configuration
stream = curlviz.stream.PDF("output.pdf")
stream.export(sheet)
```

## CLI command (experimental)

This library also provides a CLI command to export a sheet image with a set of stone positions given by a JSON file.

Given a JSON file `stone.json`, providing a set of stone positions. The following command will generate `output.pdf` based on the given stone positions.

```sh
python3 -m curlviz.cli export --output output.pdf stone.json
```

See the help for more details.

```sh
python3 -m curlviz.cli --help
```

Also, see the [example](examples/stones.json) about the format of JSON file for the stone positions.
Note that, `curlviz.Sheet` object accepts 16 stones at most. If you try to put 17 or more stones, the command will be terminated with error.

CLI command feature is still experimental, and not well-tested yet.

## Configuration

The exported image can be customized, e.g. you can change the sheet width, background color, stone colors, etc.
The default configuration is hard-coded as the following.

```json
{
  "inversion": false,
  "full": false,
  "ppm": 20,
  "sheet_width": 4.75,
  "colors": {
    "background": "#FFFFFFFF",
    "line": "#000000FF",
    "inner_house_circle": "#0000FF80",
    "outer_house_circle": "#FF000080",
    "stones": [
      "#FF0000FF",
      "#FFFF00FF"
    ]
  }
}
```

The following command exports the default configuration into `config.json`.

```sh
python -m curlviz.cli config --output config.json
```

### General keys

General keys control the scale, drawing direction, etc.

| Key           | Type   | Description                                                     | Default |
|---------------|--------|-----------------------------------------------------------------|--------:|
| `inversion`   | `bool` | draw the up-side down if `True`                                 | `False` |
| `full`        | `bool` | draw the entire sheet if `True` otherwise only the playing area | `False` |
| `ppm`         | `int`  | pixels-per-meter modifies the scale of the drawing              | 20      |
| `sheet_width` | `int`  | set the sheet width (unit: meter)                               | 4.75    |

### Keys for colors

Colors should be set in the form of a HEX code, starting with `#` followed by eight HEX digits.
For example, `"#FF0000FF"` stands for non-transparent red `(r = 255, g = 0, b = 0, a = 255)`.

| Key                  | Type        | Description                                 | Default                             |
|----------------------|-------------|---------------------------------------------|-------------------------------------|
| `background`         | `str`       | background color                            | `#FFFFFFFF` (non-transparent white) |
| `line`               | `str`       | color of lines                              | `#000000FF` (non-transparent black) |
| `inner_house_circle` | `str`       | color to fill the inner circle of the house | `#FF000080` (50%-transparent red)   |
| `inner_house_circle` | `str`       | color to fill the outer circle of the house | `#0000FF80` (50%-transparent blue)  |
| `stones`             | `list[str]` | list of colors to distinguish stones        | `[#FF0000FF, #FFFF00FF]` (non-transparent red and yellow) |

## Known issues

- Python >= 3.13 may cause error when resolving the dependencies. Use 3.12 in such a case.
- Lines can be disappeared in SVG format. In such a case, use PDF stream instead. Because of this issue, initializing SVG stream generates a waring.
- Some modules are not fully documented yet.
- This library is not formally tested.

## License

This project is licensed under the MIT license.
Copyrights are respective of each contributor listed at the beginning of each definition file.

See [LICENSE file](./LICENSE) for the formal statement.
