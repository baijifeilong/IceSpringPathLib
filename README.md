# IceSpringPathLib

`pathlib` Wrapper with **UTF-8 first** and **LineFeed first**, based on `pathlib3x`.

## Official sites

- Home: [https://baijifeilong.github.io/2022/01/08/ice-spring-path-lib/index.html](https://baijifeilong.github.io/2022/01/08/ice-spring-path-lib/index.html)
- Github: [https://github.com/baijifeilong/IceSpringPathLib](https://github.com/baijifeilong/IceSpringPathLib)
- PyPI(IceSpringPathLib): [https://pypi.org/project/IceSpringPathLib](https://pypi.org/project/IceSpringPathLib)
- PyPI(pathlib3x): [https://pypi.org/project/pathlib3x](https://pypi.org/project/pathlib3x)

## Features

- `UTF-8` is the default encoding, even on `Windows`
- `LineFeed` is the default new-line format, even on `Windows`
- All `pathlib3x` features

## Install

- PyPI: `pip install IceSpringPathLib`

## Usage

```python
import pathlib
import tempfile

import chardet

import IceSpringPathLib

tempfile.mktemp()
filename = tempfile.mktemp()
text = "Common\n常\nSense\n识\n天地玄黄"
print("Original text:", repr(text))

pathlib.Path(filename).write_text(text)
encoding = chardet.detect(open(filename, mode="rb").read())["encoding"]
print("\nWritten text by pathlib:", repr(open(filename, newline="", encoding=encoding).read()))
print("Written encoding by pathlib:", encoding)

IceSpringPathLib.Path(filename).write_text(text)
encoding = chardet.detect(open(filename, mode="rb").read())["encoding"]
print("\nWritten text by IceSpringPathLib:", repr(open(filename, newline="", encoding=encoding).read()))
print("Written encoding by IceSpringPathLib:", encoding)
```

### Example Output

```
Original text: 'Common\n常\nSense\n识\n天地玄黄'

Written text by pathlib: 'Common\r\n常\r\nSense\r\n识\r\n天地玄黄'
Written encoding by pathlib: GB2312

Written text by IceSpringPathLib: 'Common\n常\nSense\n识\n天地玄黄'
Written encoding by IceSpringPathLib: utf-8
```

## License

MIT
