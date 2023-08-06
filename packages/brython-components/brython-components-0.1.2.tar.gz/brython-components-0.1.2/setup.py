# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['brython_components']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'brython-components',
    'version': '0.1.2',
    'description': "Brython-components is an easy implementation of brython's webcomonent",
    'long_description': '# Brython-components\n\nBrython-components is an easy implementation of brython\'s webcomonent.\n\n## Installation\n\nUse the package manager [pip](https://pip.pypa.io/en/stable/) to install.\n\n```bash\npip install brip\nbrip install brython-components\n```\n\n## Usage\n\n\'\'\'python\nfrom brython_components impoprt defineElement, customElement\n\n@defineElement("bold-italic")\nclass BoldItalic(customElement):\n    def connectedCallback(self):\n        super().connectedCallback()\n        print("connected callback", self)\n\n    def render(self):\n        return f"<b><i>{self.attrs[\'data-val\']}</i></b>"\n\'\'\'\n\n## License\n\n[MIT](https://choosealicense.com/licenses/mit/)\n',
    'author': 'Lorenzo A. Garcia Calzadilla',
    'author_email': 'lorenzogarciacalzadilla@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
