# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyroscope', 'pyroscope_io']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pyroscope-io',
    'version': '0.4.3',
    'description': 'Pyroscope integration for Python',
    'long_description': '# Pyroscope Python Integration\n\n### What is Pyroscope\n[Pyroscope](https://github.com/pyroscope-io/pyroscope) is a tool that lets you continuously profile your applications to prevent and debug performance issues in your code. It consists of a low-overhead agent which sends data to the Pyroscope server which includes a custom-built storage engine. This allows for you to store and query any applications profiling data in an extremely efficient and cost effective way.\n\n\n### How to install Pyroscope for Python Applications\n```\npip install pyroscope-io\n```\n\n### Basic Usage of Pyroscope\n```\nimport pyroscope_io as pyroscope\n\npyroscope.configure(\n  app_name       = "my.python.app", # replace this with some name for your application\n  server_address = "http://my-pyroscope-server:4040", # replace this with the address of your pyroscope server\n)\n```\n\n### Adding Tags\nTags allow for users to view their data at different levels of granularity depending on what "slices" make sense for their application. This can be anything from region or microservice to more dynamic tags like controller or api route.\n\n```\nimport os\nimport pyroscope_io as pyroscope\n\npyroscope.configure(\n  app_name       = "simple.python.app",\n  server_address = "http://my-pyroscope-server:4040",\n\n  tags = {\n    "hostname": os.getenv("HOSTNAME"),\n  }\n)\n\n# You can use a wrapper:\nwith pyroscope.tag_wrapper({ "controller": "slow_controller_i_want_to_profile" }):\n  slow_code()\n```\n\n\n### Examples\nFor more examples see [examples/python](https://github.com/pyroscope-io/pyroscope/tree/main/examples/python) in the main repo.\n',
    'author': 'Pyroscope Team',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
