# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rich_tools']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.3.3,<2.0.0', 'rich>=10.12.0,<11.0.0']

setup_kwargs = {
    'name': 'rich-tools',
    'version': '0.5.0',
    'description': 'A python package with helpful tools when working with the rich python library.',
    'long_description': '<h1 align="center" style="font-size:50px;">🔧 Rich Tools</h1>\n<p align="center">\n    <em>A python package with helpful functions for use alongside with the <a href="https://github.com/willmcgugan/rich">rich</a> python library.</em>\n</p>\n<p align="center">\n<a href="https://pypi.org/project/rich-tools/" target="_blank">\n    <img src="https://badge.fury.io/py/rich-tools.svg" alt="PyPI version">\n</a>\n<a href="https://badge.fury.io/py/rich_tools"code>\n    <img src="https://img.shields.io/pypi/pyversions/rich_tools" alt="Supported Python Versions">\n</a>\n<a href="https://github.com/avi-perl/rich_tools/actions/workflows/test.yml" target="_blank">\n    <img src="https://github.com/avi-perl/rich_tools/actions/workflows/test.yml/badge.svg" alt="Test">\n</a>\n<a href="https://codecov.io/gh/avi-perl/rich_tools" target="_blank">\n  <img src="https://codecov.io/gh/avi-perl/rich_tools/branch/master/graph/badge.svg?token=7A5RYLZ37B"/>\n</a>\n\U000e0020\U000e0020\n<a href="https://twitter.com/__aviperl__" target="_blank">\n    <img src="https://badgen.net/badge/icon/twitter?icon=twitter&label=Chat%20with%20me" alt="Twitter">\n</a>\n</p>\n\n---\n\n#### The current features are:\n\n- **Convert a [Pandas](https://pandas.pydata.org/) DataFrame into a [rich](https://github.com/willmcgugan/rich) Table ➜ `df_to_table()`**\n\n  By making this conversion, we can now pretty print a DataFrame in the terminal with rich. Bridging the gap between \n  pandas and rich also provides a path for loading external data into a rich Table using Pandas functions such as `.from_csv()`!\n- **Convert a [rich](https://github.com/willmcgugan/rich) Table into a [Pandas](https://pandas.pydata.org/) DataFrame ➜ `table_to_df()`**\n\n  By bridging the gap between a rich Table and a DataFrame, we can now take additional actions on our data such as   \n  saving the data to a csv using the Pandas function `.to_csv()`!\n- **Convert a [rich](https://github.com/willmcgugan/rich) Table into a list of dictionaries. ➜ `table_to_dicts()`**\n\n  Get your tables rows as a list of dictionaries with column names as key, and row contents as values.\n- **Strip [rich](https://github.com/willmcgugan/rich) markup tags from a string. ➜ `strip_markup_tags()`**\n\n  Helper function to remove tags from text formatted with rich. `"[bold]Bold[/bold]"` becomes `"Bold"`\n\n### Installation\n```bash\n$ pip install rich-tools\n```\n\n### Example\nAdditional examples can be found in the [examples](examples) dir.\n```python\n# Print csv data to the terminal as a pretty printed rich formatted table\n\nimport pandas as pd\nfrom rich import print\nfrom rich_tools import df_to_table\n\nif __name__ == \'__main__\':\n    df = pd.read_csv("sample_input.csv")\n    table = df_to_table(df)\n    print(table)\n\n```\n\n### Credits\n- Like the [rich](https://github.com/willmcgugan/rich) package itself, its creator [Will McGugan](https://twitter.com/willmcgugan)\nis awesome! Check out [Textual](https://github.com/willmcgugan/textual) "a TUI (Text User Interface) framework for \nPython inspired by modern web development". Thank you for the advice you\'ve given on this project! 🙏\n- I am grateful for folks who give some of their time to this project in any form. Check out the list of \n[contributors](https://github.com/avi-perl/rich_tools/graphs/contributors) and learn more about contributing [here](CONTRIBUTING.md).',
    'author': 'Avi Perl',
    'author_email': 'avi@aviperl.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/avi-perl/rich_tools',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
