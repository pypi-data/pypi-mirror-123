# filemime 

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/THAVASIGTI/filemime)
[![PyPI](https://img.shields.io/pypi/v/filemime)](https://pypi.org/project/filemime)
[![Downloads](https://pepy.tech/badge/filemime)](https://pepy.tech/project/filemime)

Python package to infer file type and MIME

## INSTALL PACKAGE

``` console
pip install filemime
```

## Features

- Provides file extension and MIME type
- File discovery by extension or MIME type
- Fast, even processing large files
- Cross-platform file recognition

## IMPORT PACKAGE

All type of `file extension` and `mimetype` support
``` python
Python 3.7.3 (default, Oct  7 2019, 12:56:13) 
[GCC 8.3.0] on windows
Type "help", "copyright", "credits" or "license" for more information.
from filemime import filemime
obj = filemime()
```

## LOAD FILE

``` python
>>> obj.load_file("D:\\photos\\IMG_4917.JPG")
"""JPEG image data, Exif standard: [TIFF image data, little-endian, direntries=12, 
    manufacturer=Canon, model=Canon EOS 1500D, orientation=lower-left, xresolution=196, 
    yresolution=204, resolutionunit=2, datetime=2021:10:16 18:03:06], baseline, precision 8, 
    6000x4000, frames 3"""
```

## MIME TYPE

``` python
>>> obj.load_file("D:\\photos\\IMG_4917.JPG",mimeType=True)
'image/jpeg'
>>> 
```
