# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tidypolars']

package_data = \
{'': ['*']}

install_requires = \
['polars>=0.10.2']

setup_kwargs = {
    'name': 'tidypolars',
    'version': '0.1.5',
    'description': 'Tidy interface to polars',
    'long_description': '# tidypolars\n\ntidypolars is a data frame library built on top of the blazingly fast [polars](https://github.com/pola-rs/polars) library that gives access to methods and functions familiar to R tidyverse users.\n\n*Please be aware that tidypolars is still early in development and may be subject to fast API changes*\n\n## Installation\n```bash\n$ pip3 install tidypolars\n```\n\n## Usage\n\n```python\nimport tidypolars as tp\nfrom tidypolars import col\n\ntest_df = tp.Tibble({\'x\': range(3), \'y\': range(4, 7), \'z\': [\'a\', \'a\', \'b\']})\n\n(\n    test_df\n    .select(\'x\', \'y\', \'z\')\n    .filter(col(\'x\') < 4, col(\'y\') > 1)\n    .arrange(\'x\', \'y\')\n    .mutate(double_x = col(\'x\') * 2,\n            x_plus_y = col(\'x\') + col(\'y\'))\n)\n┌─────┬─────┬─────┬──────────┬──────────┐\n│ x   ┆ y   ┆ z   ┆ double_x ┆ x_plus_y │\n│ --- ┆ --- ┆ --- ┆ ---      ┆ ---      │\n│ i64 ┆ i64 ┆ str ┆ i64      ┆ i64      │\n╞═════╪═════╪═════╪══════════╪══════════╡\n│ 0   ┆ 4   ┆ "a" ┆ 0        ┆ 4        │\n├╌╌╌╌╌┼╌╌╌╌╌┼╌╌╌╌╌┼╌╌╌╌╌╌╌╌╌╌┼╌╌╌╌╌╌╌╌╌╌┤\n│ 1   ┆ 5   ┆ "a" ┆ 2        ┆ 6        │\n├╌╌╌╌╌┼╌╌╌╌╌┼╌╌╌╌╌┼╌╌╌╌╌╌╌╌╌╌┼╌╌╌╌╌╌╌╌╌╌┤\n│ 2   ┆ 6   ┆ "b" ┆ 4        ┆ 8        │\n└─────┴─────┴─────┴──────────┴──────────┘\n```\n\n\n### Using `groupby`\n\nMethods operate by group by calling the `groupby` arg.\n\n* A single column can be passed with `groupby = \'z\'`\n* Multiple columns can be passed with `groupby = [\'y\', \'z\']`\n\n```python\n(\n    test_df\n    .summarize(avg_x = col(\'x\').mean(),\n               groupby = \'z\')\n)\n┌─────┬───────┐\n│ z   ┆ avg_x │\n│ --- ┆ ---   │\n│ str ┆ f64   │\n╞═════╪═══════╡\n│ "b" ┆ 2     │\n├╌╌╌╌╌┼╌╌╌╌╌╌╌┤\n│ "a" ┆ 0.5   │\n└─────┴───────┘\n```\n\n## Contributing\n\nInterested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.\n\n## License\n\n`tidypolars` was created by Mark Fairbanks. It is licensed under the terms of the MIT license.\n\n## Credits\n\n`tidypolars` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).\n',
    'author': 'Mark Fairbanks',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.11',
}


setup(**setup_kwargs)
