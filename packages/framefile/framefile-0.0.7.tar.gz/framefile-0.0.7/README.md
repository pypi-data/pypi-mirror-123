[![PyPI version shields.io](https://img.shields.io/pypi/v/framefile.svg)](https://pypi.python.org/pypi/framefile/)
[![Generic badge](https://img.shields.io/badge/Python-3.7+-blue.svg)](#)
[![Generic badge](https://img.shields.io/badge/Tested_on-Windows%20|%20Linux-blue.svg)](#)
[![Downloads](https://pepy.tech/badge/framefile/month)](https://pepy.tech/project/framefile)

# [framefile](https://github.com/rtmigo/framefile_py#readme)

Python library for parsing and matching file name patterns like `IMG_####.JPG` or 
`IMG_%04d.JPG`.

---

Such files are often created by cameras and video production software.
As a rule, this is a set of images with consecutive numbers, 
like `IMG_0001.JPG`, `IMG_0002.JPG`, `IMG_0003.JPG` and so on.

To handle files such as video sequences, [Blender](https://www.blender.org/)
and [AE](https://www.adobe.com/products/aftereffects.html) use patterns like
`IMG_####.JPG`. [ffmpeg](https://www.ffmpeg.org/) uses patterns like
`IMG_%04d.JPG`.

This package can create and parse patterns in both formats.

# Install

```
pip3 install framefile
```

<details>
<summary>other options</summary>

#### Install pre-release from GitHub:
```
pip3 install git+https://github.com/rtmigo/framefile_py@staging#egg=framefile
```

</details>

# Use

## Guess pattern from file name

```python
import framefile

print(framefile.filename_to_hash_pattern("IMG_4567.JPG"))  # IMG_####.JPG
print(framefile.filename_to_pct_pattern("IMG_4567.JPG"))  # IMG_%04d.JPG
```

Any names with numbers in them are supported. The path can also be part of 
the file name.

```python
import framefile

print(framefile.filename_to_hash_pattern("/video/frame-01234.png"))

# /video/frame-#####.png
```

If there are several number sequences in the file name, only the last of them 
will be considered a pattern. And only if its length is more than one digit.

```python
import framefile

print(framefile.filename_to_hash_pattern("/video/take505_frame01234.cr2"))

# /video/take505_frame#####.cr2
```


## Find files by pattern

```python
import glob
import framefile

# print all files matching /path/to/img####.jpg
file_mask = framefile.hash_pattern_to_glob('/path/to/img####.jpg')
print(glob.glob(file_mask))

# print all files matching /path/to/img%04d.jpg
file_mask = framefile.pct_pattern_to_glob('/path/to/img%04d.jpg')
print(glob.glob(file_mask))
```

## Match file names as strings

```python
import re
import framefile

regex = framefile.hash_pattern_to_regex('img####.jpg')
# or framefile.pct_pattern_to_regex('img%04d.jpg')

a = re.match(regex, 'img0023.jpg')
print(a.group(0))  # img0023.jpg
print(a.group(1))  # 0023

b = re.match(regex, 'anything.txt')
print(b)  # None
```

## Extract number from file name

```python
import framefile

x: int = framefile.hash_extract_number("img####.jpg", "img0023.jpg")
print(x)  # 23

y: int = framefile.pct_extract_number("img%04d.jpg", "img0023.jpg")
print(y)  # 23
```

If the name does not match the pattern, both functions throw the same `PatternMismatchError`.

```python
import framefile

try:
    z = framefile.hash_extract_number("img####.jpg", "thumbs.db")
except framefile.PatternMismatchError:
    print("Oops!")
```
