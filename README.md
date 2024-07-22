# ComiBat

[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/comibat)](https://pypi.org/project/comibat)

<a href='https://ko-fi.com/recoskyler' target='_blank'><img height='35' style='border:0px;height:46px;' src='https://az743702.vo.msecnd.net/cdn/kofi3.png?v=0' border='0' alt='Buy Me a Coffee at ko-fi.com' /></a>

A tool to add a title page to CBZ comic book archives, and optionally convert them to EPUB.

*It won't add a title page if one already exists.*

**This tool works only with CBZ files, as CBR and CB7 files are not supported and proprietary.**

## Installation

ComiBat is available on PyPI. To install it, run the following command:

```bash
pip install comibat
```

## Usage

To add a title page to a CBZ file, run the following command:

```bash
comibat <path/to/cbz/file>
```

This will add a title page to the CBZ file, and save it as a new CBZ file with the same name but with a `(FIXED)` suffix.

To convert a CBZ file to EPUB, run the following command:

```bash
comibat <path/to/cbz/file> --to-epub
```

This will convert the CBZ file to EPUB, and save it as a new EPUB file with the same name but with a `.epub` extension.

## License

ComiBat is licensed under the GNU General Public License v3.0. See the [LICENSE](LICENSE) file for more information.

## About

By [recoskyler](https://github.com/recoskyler) - 2024
