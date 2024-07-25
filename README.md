# ComiBat

[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/comibat)](https://pypi.org/project/comibat)

<a href='https://ko-fi.com/recoskyler' target='_blank'><img height='35' style='border:0px;height:46px;' src='https://az743702.vo.msecnd.net/cdn/kofi3.png?v=0' border='0' alt='Buy Me a Coffee at ko-fi.com' /></a>

A tool to add a title page to CBZ comic book archives if it doesn't already exist. It uses the first image file in the archive as the title page, and also adds a Pages node with all the other pages to the `ComicInfo.xml` file during the process.

**This tool works only with CBZ files, as CBR and CB7 files are not supported and proprietary.**

## Requirements

- Python 3.5 or higher
- pip

## Installation

ComiBat is available on PyPI. To install it, run the following command:

```bash
pip3 install comibat
```

## Usage

To add a title page to a CBZ file, run the following command:

```bash
comibat <path/to/cbz/file>
```

This will add a title page to the CBZ file, and save it as a new CBZ file with the same name but with a `(FIXED)` suffix.

If you do not specify any files, ComiBat will look for CBZ files in the current directory (not recursive).

### Examples

#### Add a title page to a single CBZ file

```bash
comibat 'Maou-jou de Oyasumi Ch.310.cbz'
```

#### Add a title page to all CBZ files in the current directory

```bash
comibat
```

#### Add a title page to all CBZ files in the current directory recursively

```bash
comibat -r
```

#### Add a title page to all CBZ files in the current directory and output to a different directory

```bash
comibat -o 'C:\Users\User\Documents\Comic Books'
```

#### Add a title page to all CBZ files in the current directory recursively

```bash
comibat -r
```

#### Add a title page to all CBZ files in the current directory and output to a different directory

```bash
comibat -o 'C:\Users\User\Documents\Comic Books'
```

#### Add a title page to specific CBZ files using wildcards

```bash
comibat 'Maou-jou de Oyasumi Ch.*.cbz'
```

in a specific directory

```bash
comibat '/home/user/comics/*.cbz'
```

## License

ComiBat is licensed under the GNU General Public License v3.0. See the [LICENSE](LICENSE) file for more information.

## About

By [recoskyler](https://github.com/recoskyler) - 2024
