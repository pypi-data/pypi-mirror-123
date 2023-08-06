# pyheif-pillow-opener

[![build](https://travis-ci.org/uploadcare/heif-image-plugin.svg?branch=master)](https://travis-ci.org/uploadcare/heif-image-plugin)
[![coverage](https://img.shields.io/codecov/c/gh/uploadcare/heif-image-plugin)](https://codecov.io/gh/uploadcare/heif-image-plugin)
[![Py Versions](https://img.shields.io/pypi/pyversions/pyheif-pillow-opener)](https://pypi.python.org/pypi/pyheif-pillow-opener/)
[![license](https://img.shields.io/github/license/uploadcare/heif-image-plugin)](https://pypi.python.org/pypi/pyheif-pillow-opener/)
[![status](https://img.shields.io/pypi/status/pyheif-pillow-opener)](https://pypi.python.org/pypi/pyheif-pillow-opener/)
[![PEP8](https://img.shields.io/badge/code%20style-pep8-orange)](https://www.python.org/dev/peps/pep-0008/)

**pyheif-pillow-opener** is a *simple* HEIF/HEIC opener for *Pillow* base on *pyhief* library.

## Installation

You can install **pyheif-pillow-opener** from *PyPi*:

`pip install pyheif-pillow-opener`

## How to use

```python
from PIL import Image

import HeifImagePlugin

image = Image.open('test.heic')
image.load()
```

## How to contribute

This is not a big library but if you want to contribute is very easy!

 1. clone the repository `git clone https://github.com/uploadcare/heif-image-plugin.git`
 1. install all requirements `make init`
 1. do your fixes or add new awesome features (with tests)
 1. run the tests `make test`
 1. commit in new branch and make a pull request

---


## License

Released under [MIT License](https://github.com/uploadcare/heif-image-plugin/blob/master/LICENSE).
