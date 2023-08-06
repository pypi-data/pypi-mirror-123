<!-- #region -->
# ConfPrint <!-- omit in toc -->
![GitHub License](https://img.shields.io/github/license/lewiuberg/confprint?color=blue)
![Python](https://img.shields.io/pypi/pyversions/confprint.svg?color=blue)
![PyPI](https://img.shields.io/pypi/v/confprint.svg?color=blue)
![Downloads](https://pepy.tech/badge/confprint)
![Codecov code coverage](https://img.shields.io/codecov/c/github/lewiuberg/confprint?color=blue)
![Github Contributors](https://img.shields.io/github/contributors/lewiuberg/confprint?color=blue)
![GitHub search hit counter](https://img.shields.io/github/search/lewiuberg/confprint/confprint?label=confprint%20searches)
![GitHub issues](https://img.shields.io/github/issues-raw/lewiuberg/confprint)
![GitHub last commit](https://img.shields.io/github/last-commit/lewiuberg/confprint)


![GitHub workflow CI](https://github.com/lewiuberg/confprint/actions/workflows/ci.yml/badge.svg)
![GitHub workflow CD](https://github.com/lewiuberg/confprint/actions/workflows/cd.yml/badge.svg)

Copyright 2021 [Lewi Lie Uberg](https://uberg.me/)\
_Released under the MIT license_

**ConfPrint** provides a simple way to make predefined printer configurations.

## Contents <!-- omit in toc -->

- [Citation](#citation)
  - [APA](#apa)
  - [BibTex](#bibtex)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
  - [Using pip:](#using-pip)
  - [Using Poetry:](#using-poetry)
- [Usage](#usage)
  - [prefix_printer](#prefix_printer)
- [Authors](#authors)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Citation

Please see [CITATION.cff](CITATION.cff) for the full citation information.

### APA

```apa
Lie Uberg, L., & Hjelle, G. A. (2021). confprint (Version 0.1.1) [Computer software]. https://github.com/lewiuberg/confprint
```

### BibTex

```BibTex
@software{Lie_Uberg_confprint_2021,
author = {Lie Uberg, Lewi and Hjelle, Geir Arne},
license = {MIT},
month = {10},
title = {{confprint}},
url = {https://github.com/lewiuberg/confprint},
version = {0.1.1},
year = {2021}
}
```

## Prerequisites

[Click](https://pypi.org/project/click/)

Please see [pyproject.toml](pyproject.toml) for the full citation information.

## Installation

### Using pip:

```bash
python -m pip install confprint
```

### Using Poetry:

```bash
poetry add confprint
```

## Usage

### prefix_printer
<!-- #endregion -->

```python
from confprint import prefix_printer

p_test1 = prefix_printer(prefix="test1")
p_test1("Preset")

p_test2 = prefix_printer(prefix="test2", upper=False)
p_test2("unaltered text")

p_test3 = prefix_printer(prefix="test3", stderr=True)
p_test3("using sys.stderr.write as the print function")

p_test4 = prefix_printer(prefix="test4", click=True)
p_test4("using click.echo as the print function")

p_test5 = prefix_printer(prefix="test5", frame_left="( ", frame_right=" )")
p_test5("using custom frame characters")

p_test1(
    """With new lines in strings the text is converted
to multiline, then all but the first are
indented to line up with therest."""
)

p_test1(
    "The next example wil not be ending with a `:`, "
    "since it has no input.\nAnd as you can see, this is also a multiline text."
)

p_done = prefix_printer(prefix="done")
p_done()
```

```
[TEST1]: Preset
[test2]: unaltered text
[TEST3]: using sys.stderr.write as the print function
[TEST4]: using click.echo as the print function
( TEST5 ): using custom frame characters
[TEST1]: With new lines in strings the text is converted
         to multiline, then all but the first are
         indented to line up with therest.
[TEST1]: The next example wil not be ending with a `:`, since it has no input.
         And as you can see, this is also a multiline text.
[DONE]
```


## Authors

- **[Lewi Lie Uberg](https://github.com/lewiuberg)** - [uberg.me](https://uberg.me/)

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/lewiuberg/confprint/blob/master/LICENSE) file for details

## Acknowledgments

- [Geir Arne Hjelle](https://github.com/gahjelle), for his presentation on 'Introduction to Decorators' given at [PyCon 21](https://www.youtube.com/watch?v=VWZAh1QrqRE&amp;t=17m0s)
