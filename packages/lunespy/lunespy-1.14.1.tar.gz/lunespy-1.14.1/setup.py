# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lunespy',
 'lunespy.client',
 'lunespy.client.transactions',
 'lunespy.client.transactions.alias',
 'lunespy.client.transactions.burn',
 'lunespy.client.transactions.cancel',
 'lunespy.client.transactions.issue',
 'lunespy.client.transactions.lease',
 'lunespy.client.transactions.mass',
 'lunespy.client.transactions.reissue',
 'lunespy.client.transactions.transfer',
 'lunespy.client.wallet',
 'lunespy.server',
 'lunespy.server.address',
 'lunespy.utils',
 'lunespy.utils.crypto',
 'lunespy.utils.settings']

package_data = \
{'': ['*']}

install_requires = \
['base58>=2.1.0,<3.0.0',
 'python-axolotl-curve25519>=0.4.1.post2,<0.5.0',
 'requests>=2.26.0,<3.0.0']

setup_kwargs = {
    'name': 'lunespy',
    'version': '1.14.1',
    'description': 'Library for communication with nodes in mainnet or testnet of the lunes-blockchain network',
    'long_description': "# LunesPy\n\n**The [old version](https://github.com/Lunes-platform/LunesPy/tree/old) is being discontinued, but it can still be used at your own risk and risk.**\n\nLibrary for communication with nodes in mainnet or testnet of the lunes-blockchain network\nAllows the automation of **sending assets**, **issue end reissue tokens**, **lease**, **registry**, and **create new wallet**.\n<!-- \n## Prerequisites\n\nBefore you begin, ensure you have met the following requirements:\n* You have installed the latest version of `python`\n\n## Installing LunesPy\n\nTo use LunesPy, follow these steps:\n\nLinux and macOS:\n```\n<install_command>\n```\n\nWindows:\n```\n<install_command>\n``` -->\n## What's new\nLook at the changes [here](./CHANGELOG.md)\n\n\n## Using LunesPy\n\nTo use LunesPy, follow these [tutorial](./TUTORIAL.md)\n\n## Contributing to LunesPy\n\nTo contribute to LunesPy, follow these [step](./docs/CONTRIBUTING.md)\n\n## Contributors\n\nThanks to the following people who have contributed to this project:\n\n* [@olivmath](https://github.com/olivmath)\n* [@marcoslkz](https://github.com/marcoslkz)\n* [@VanJustin](https://github.com/VanJustin)\n\n<!---\nYou might want to consider using something like the [All Contributors](https://github.com/all-contributors/all-contributors) specification and its [emoji key](https://allcontributors.org/docs/en/emoji-key).\n--->\n## Contact\n\nIf you want to contact me you can reach me at <lucas.oliveira@lunes.io>.\n\n## License\n<!--- If you're not sure which open license to use see https://choosealicense.com/--->\n\nThis project uses the following license: [Apache License Version 2.0, January 2004](./LICENSE).\n",
    'author': 'Lunes Platform',
    'author_email': 'lucas.oliveira@lunes.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
