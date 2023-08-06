# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['future_map']

package_data = \
{'': ['*']}

install_requires = \
['tox>=3.24.4,<4.0.0']

setup_kwargs = {
    'name': 'future-map',
    'version': '0.1.1',
    'description': "Simple package to enhance Python's concurrent.futures for memory efficiency",
    'long_description': "# future-map\n\nfuture-map is a Python library to use together with the official `concurrent.futures` module.\n\n## Why future-map?\n\nBecause it's difficult to deal with an infinite or huge input with `concurrent.future.ThreadPoolExecutor` and `concurrent.future.ProcessPoolExecutor`. See the following example.\n\n```python\nfrom concurrent.futures import ThreadPoolExecutor\n\ndef make_input(length):\n    return range(length)\n\ndef make_infinite_input():\n    count = 0\n    while True:\n        yield count\n        count += 1\n\ndef process(value):\n    return value * 2\n\nif __name__ == '__main__':\n    with ThreadPoolExecutor(max_workers=3) as executor:\n        # Works well\n        for value in executor.map(process, make_input(10)):\n            print('Doubled value:', value)\n\n        # This freezes the process and memory usage keeps growing\n        for value in executor.map(process, make_infinite_input()):\n            print('Doubled value:', value)\n```\n\n## Installation\n\nUse the package manager [pip](https://pip.pypa.io/en/stable/) to install `future-map`.\n\n    $ pip install future-map\n\n## Usage\n\nThis library provides `FutureMap`. See the following example.\n\n```python\nfrom future_map import FutureMap\nfrom concurrent.futures import ThreadPoolExecutor\n\ndef make_infinite_input():\n    count = 0\n    while True:\n        yield count\n        count += 1\n\ndef process(value):\n    return value * 2\n\nif __name__ == '__main__':\n    with ThreadPoolExecutor(max_workers=3) as executor:\n        fm = FutureMap(\n            lambda value: executor.submit(process, value),\n            make_infinite_input(), buffersize=5\n        )\n        for value in fm:\n            print('Doubled value:', value)\n```\n\n### API\n\n#### `FutureMap(fn, iterable, buffersize)`\n\nConstructor of `FutureMap`.\n\n`FutureMap` is an iterable object that maps an iterable object (`iterable` argument) to a function (`fn` argument), waits until each future object is done, and yields each result.\n\nPlease note that this object will yield unordered results.\n\n- Arguments\n  - `fn`: Callable object that takes an argument from iterable, and return a `concurrent.futures.Future`.\n  - `iterable`: Iterable object.\n  - `buffersize`: Maximum size of internal buffer. Each `concurrent.futures.Future` object is stored in the buffer until it's done. If the buffer is fulfilled, `FutureMap` stops reading values from `iterable`.\n- Return\n  - `FutureMap` instance\n\n#### `future_map(fn, iterable, buffersize)`\n\nAlias of `FutureMap`. You can use this function if you prefer a similar syntax with the `map` function.\n\nFor more details, please refer to `FutureMap(fn, iterable, buffersize)`.\n\n## Contributing\nPull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.\n\nPlease make sure to update tests as appropriate.\n\n## License\n[MIT](https://choosealicense.com/licenses/mit/)\n",
    'author': 'Arai Hiroki',
    'author_email': 'hiroara62@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/hiroara/future-map',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
