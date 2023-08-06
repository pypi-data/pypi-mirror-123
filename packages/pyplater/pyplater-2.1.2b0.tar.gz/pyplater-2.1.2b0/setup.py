# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyplater']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pyplater',
    'version': '2.1.2b0',
    'description': 'Build html component with python',
    'long_description': 'pyplater\n=========\n\nBuild ``html`` component with python.\n\n.. code-block:: python\n\n    from pyplater import *  # import all tag\n\n    documents = html(\n        head(\n            meta(charset="utf-8"),\n            link(rel="stylesheet", href="./style.css"),\n            title("Documents"),\n        ),\n        body(\n            h1("The title"),\n            p("lorem ipsum"),\n        ),\n    )\n\n    print(documents.render())\n\n\nContributing\n------------\n\nWhether reporting bugs, discussing improvements and new ideas or writing\nextensions: Contributions to pyplater are welcome! Here\'s how to get started:\n\n1. Check for open issues or open a fresh issue to start a discussion around\n   a feature idea or a bug\n2. Fork `the repository <https://github.com/Unviray/pyplater/>`_ on Github,\n   create a new branch off the `master` branch and start making your changes\n   (known as `GitHub Flow <https://guides.github.com/introduction/flow/index.html>`_)\n3. Write a test which shows that the bug was fixed or that the feature works\n   as expected to cover your change\n4. Send a pull request and bug the maintainer until it gets merged and\n   published ☺\n',
    'author': 'Unviray',
    'author_email': 'unviray@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Unviray/pyplater',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
