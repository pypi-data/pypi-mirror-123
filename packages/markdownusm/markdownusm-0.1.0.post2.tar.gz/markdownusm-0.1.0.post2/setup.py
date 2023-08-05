# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['markdownusm', 'markdownusm.tests']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=3.0.1,<4.0.0', 'pydantic>=1.8.2,<2.0.0']

entry_points = \
{'console_scripts': ['musm = markdownusm.cli:main']}

setup_kwargs = {
    'name': 'markdownusm',
    'version': '0.1.0.post2',
    'description': 'MarkdownUSM is the best way to draw a beautiful user story mapping diagram from simple markdown file.',
    'long_description': '# MarkdownUSM\n[![MIT License](http://img.shields.io/badge/license-MIT-blue.svg?style=flat)](LICENSE)\n[![CircleCI](https://circleci.com/gh/kbyky/markdownusm/tree/main.svg?style=shield&circle-token=33d038de0f7a2600f831702d67d7887b71f77eea)](https://circleci.com/gh/kbyky/markdownusm/tree/main)\n[![codecov](https://codecov.io/gh/kbyky/markdownusm/branch/main/graph/badge.svg?token=ZD51BWEICH)](https://codecov.io/gh/kbyky/markdownusm)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)\n\nMarkdownUSM is the best way to draw a beautiful user story mapping diagram from simple markdown file.\\\nMarkdown file will be converted to XML format then you can easily use the diagram on [draw.io](https://app.diagrams.net) and export in another format.\n\n![](https://github.com/kbyky/public/blob/main/img/markdownusm.svg?raw=true)\n\n## Installation\n```\n$ pip install markdownusm\n```\n\n## Examples\n\n### Create it\n\nCreate a file sample.md with:\n\n```\n<!-- Comment -->\n\n<!-- Release titles -->\n- Release 1\n- Release 2\n- Release 3\n- Release 4\n- Release 5\n\n# Activity 1\n## Task 1\nStory 1\n--- <!-- Release separator -->\nStory 2\n---\nStory 3\n\n## Task 2\n---\nStory 4\n\n<!-- Suffix `!` changes story postit color for warning -->\nStory 5!\n\n# Activity 2\n## Task 3\n---\n---\nStory 6 &lt;br&gt; Next line\n<!-- Story can change their colors by setting hex code following story title -->\nStory 7 #a6dfb5\n```\n\n### Run it\n\nThe simplest way with:\n\n```\n$ musm sample.md\n\n<mxfile>\n    <diagram>\n        <mxGraphModel dx="661" dy="316" grid="0" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="827" pageHeight="1169" math="0" shadow="0" background="#FFFFFF">\n        ...\n```\n\nOutput XML file with:\n```\n$ musm -o sample.dio sample.md\n```\n\n## License\nThis project is licensed under the terms of the MIT license.\n',
    'author': 'kbyky',
    'author_email': 'kbyky36@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
