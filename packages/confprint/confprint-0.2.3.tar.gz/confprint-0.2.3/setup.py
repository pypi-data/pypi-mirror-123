# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['confprint']

package_data = \
{'': ['*']}

install_requires = \
['click==7.1.2']

entry_points = \
{'console_scripts': ['vinc = vinc:cli']}

setup_kwargs = {
    'name': 'confprint',
    'version': '0.2.3',
    'description': 'Python printer configurations.',
    'long_description': '<!-- ---\njupyter:\n  jupytext:\n    formats: ipynb,md\n    text_representation:\n      extension: .md\n      format_name: markdown\n      format_version: \'1.3\'\n      jupytext_version: 1.13.0\n  kernelspec:\n    display_name: Python 3 (ipykernel)\n    language: python\n    name: python3\n--- -->\n\n<!-- #region tags=[] -->\n# ConfPrint <!-- omit in toc -->\n[![GitHub License](https://img.shields.io/github/license/lewiuberg/confprint?color=blue)](LICENSE)\n![Python](https://img.shields.io/pypi/pyversions/confprint.svg?color=blue)\n[![PyPI](https://img.shields.io/pypi/v/confprint.svg?color=blue)](https://pypi.org/project/confprint/)\n[![Downloads](https://pepy.tech/badge/confprint)](https://pepy.tech/project/confprint)\n[![Codecov code coverage](https://img.shields.io/codecov/c/github/lewiuberg/confprint?color=blue)](https://app.codecov.io/gh/lewiuberg/confprint)\n![Github Contributors](https://img.shields.io/github/contributors/lewiuberg/confprint?color=blue)\n![GitHub search hit counter](https://img.shields.io/github/search/lewiuberg/confprint/confprint?label=confprint%20searches)\n[![GitHub issues](https://img.shields.io/github/issues-raw/lewiuberg/confprint)](https://github.com/lewiuberg/confprint/issues)\n![GitHub last commit](https://img.shields.io/github/last-commit/lewiuberg/confprint)\n\n[![CICD](https://github.com/lewiuberg/confprint/actions/workflows/cicd.yml/badge.svg?branch=master)](https://github.com/lewiuberg/confprint/actions/workflows/cicd.yml)\n\nCopyright 2021 [Lewi Lie Uberg](https://uberg.me/)\\\n_Released under the MIT license_\n\n**ConfPrint** provides a simple way to make predefined printer configurations.\n\n## Contents <!-- omit in toc -->\n\n- [Citation](#citation)\n  - [APA](#apa)\n  - [BibTex](#bibtex)\n- [Prerequisites](#prerequisites)\n- [Installation](#installation)\n  - [Using pip](#using-pip)\n  - [Using Poetry](#using-poetry)\n- [Usage](#usage)\n  - [prefix_printer](#prefix_printer)\n- [Authors](#authors)\n- [License](#license)\n- [Acknowledgments](#acknowledgments)\n\n## Citation\n\nPlease see [CITATION.cff](CITATION.cff) for the full citation information.\n\n### APA\n\n```apa\nLie Uberg, L., & Hjelle, G. A. (2021). confprint (Version 0.2.3) [Computer software]. https://github.com/lewiuberg/confprint\n```\n\n### BibTex\n\n```BibTex\n@software{Lie_Uberg_confprint_2021,\nauthor = {Lie Uberg, Lewi and Hjelle, Geir Arne},\nlicense = {MIT},\nmonth = {10},\ntitle = {{confprint}},\nurl = {https://github.com/lewiuberg/confprint},\nversion = {0.2.3},\nyear = {2021}\n}\n```\n\n## Prerequisites\n\n[Click](https://pypi.org/project/click/)\n\nPlease see [pyproject.toml](pyproject.toml) for the full citation information.\n\n## Installation\n\n### Using pip\n\n```bash\npython -m pip install confprint\n```\n\n### Using Poetry\n\n```bash\npoetry add confprint\n```\n\n## Usage\n\n### prefix_printer\n<!-- #endregion -->\n\n```python\nfrom confprint import prefix_printer\n\np_test1 = prefix_printer(prefix="test1")\np_test1("Preset\\n")\n\np_test2 = prefix_printer(prefix="test2", upper=False)\np_test2("unaltered text\\n")\n\np_test3 = prefix_printer(prefix="test3", stderr=True)\np_test3("using sys.stderr.write as the print function\\n")\n\np_test4 = prefix_printer(prefix="test4", click=True)\np_test4("using click.echo as the print function\\n")\n\np_test5 = prefix_printer(prefix="test5", frame_left="( ", frame_right=" )")\np_test5("using custom frame characters\\n")\n\np_test6 = prefix_printer(prefix="test6", counter_start=1)\np_test6("By defining a \'counter_start\',")\np_test6("a counter number will be apended")\np_test6("to the prefix.\\n")\n\np_test1(\n    """With new lines in strings the text is converted\nto multiline, then all but the first are\nindented to line up with therest.\\n"""\n)\n\np_test1(\n    "The next example wil not be ending with a `:`, "\n    "since it has no input.\\nAnd as you can see, this is also a multiline text.\\n"\n)\n\np_done = prefix_printer(prefix="done")\np_done()\n```\n\n```\n[TEST1]: Preset\n\n[test2]: unaltered text\n\n[TEST3]: using sys.stderr.write as the print function\n\n[TEST4]: using click.echo as the print function\n         \n( TEST5 ): using custom frame characters\n           \n[TEST6:1]: By defining a \'counter_start\',\n[TEST6:2]: a counter number will be apended\n[TEST6:3]: to the prefix.\n           \n[TEST1]: With new lines in strings the text is converted\n         to multiline, then all but the first are\n         indented to line up with therest.\n         \n[TEST1]: The next example wil not be ending with a `:`, since it has no input.\n         And as you can see, this is also a multiline text.\n         \n[DONE]\n```\n\n\n## Authors\n\n- **[Lewi Lie Uberg](https://github.com/lewiuberg)** - [uberg.me](https://uberg.me/)\n\n## License\n\nThis project is licensed under the MIT License - see the [LICENSE](https://github.com/lewiuberg/confprint/blob/master/LICENSE) file for details\n\n## Acknowledgments\n\n- [Geir Arne Hjelle](https://github.com/gahjelle), for his presentation on \'Introduction to Decorators\' given at [PyCon 21](https://www.youtube.com/watch?v=VWZAh1QrqRE&amp;t=17m0s)\n',
    'author': 'Lewi Lie Uberg',
    'author_email': 'lewi@uberg.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/lewiuberg/confprint',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
