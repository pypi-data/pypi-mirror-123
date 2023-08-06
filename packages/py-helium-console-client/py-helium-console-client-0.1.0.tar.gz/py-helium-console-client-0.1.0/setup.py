# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['py_helium_console_client']

package_data = \
{'': ['*']}

install_requires = \
['certifi>=2021.10.8,<2022.0.0',
 'idna>=3.3,<4.0',
 'pydantic>=1.8.2,<2.0.0',
 'requests>=2.26.0,<3.0.0']

setup_kwargs = {
    'name': 'py-helium-console-client',
    'version': '0.1.0',
    'description': 'An unofficial Python Client library for the Helium Console API.',
    'long_description': "# py-console-http-client\nAn __unofficial__ Python Client library for the [Helium Console API](https://docs.helium.com/use-the-network/console/api/). Please see the [API Specification](https://docs.helium.com/api/console/) for full details.\n\n## Usage\nTo use the Console API, you will first need to generate an API Key from the 'My Account' tab. Use this key to initialize the `ConsoleClient` class. This interface exposes any of the methods in the specification (at the time of writing), which includes programmatic access for creating, querying, and deleting devices and labels. \n\nSome examples are shown below.\n\n```python\nfrom client import ConsoleClient\n\nAPI_KEY = 'PASTE_API_KEY_HERE'\n\nclient = ConsoleClient(API_KEY)\n\n# list devices on account\ndevices = client.get_devices()\n\n# search for a device by uuid\nuuid_device = client.get_device_by_uuid(devices[0].id)\n\n# get device events\nevents = client.get_device_events(devices[0].id)\n\n# create device\ncreated_device = client.create_device(name='python-client-test-device',\n                              app_key='850AFDC6F1CF2397D3FEAB8C1850E6E1',\n                              app_eui='B21C36EBBDC0D75F',\n                              dev_eui='ABA47D469E1021AF')\n\n# list labels\nlabels = client.get_labels()\n\n# create label\ncreated_label = client.create_label('python-client-test-label')\n\n# search for label by id\nqueried_label = client.search_for_label(created_label.id)\n\n# add label to device\nadd_label_result = client.add_device_label(created_device.id, created_label.id)\n\n# remove label from device\nremove_label_result = client.remove_device_label(created_device.id, created_label.id)\n\n# delete device\ndeleted_device_result = client.delete_device(created_device.id)\n\n# delete label\ndeleted_label_result = client.delete_label(created_label.id)\n```\n\n## Contributing\nThis is a small project that I use for developing my own applications on the Helium Network. Please feel free to submit an issue.",
    'author': 'Evan Diewald',
    'author_email': 'evandiewald@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/evandiewald/py-helium-console-client',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
