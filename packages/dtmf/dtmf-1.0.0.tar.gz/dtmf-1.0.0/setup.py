# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['dtmf']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'dtmf',
    'version': '1.0.0',
    'description': 'Package for working with DTMF - a system for signaling over the voice band of a telephony system using multi-frequency tones.',
    'long_description': '# dtmf\n\n![GitHub Workflow Status (branch)](https://img.shields.io/github/workflow/status/gdereese/dtmf/CI/main?style=for-the-badge)\n![PyPI](https://img.shields.io/pypi/v/dtmf?style=for-the-badge)\n\nPackage for working with DTMF - a system for signaling over the voice band of a telephony system using multi-frequency tones.\n\n## Features\n\n* Parses dial strings (digits, symbols, etc.) into an object representation\n* Constructs dial strings from element objects\n* Detects the presence and position of DTMF tones in an audio buffer\n* Generates DTMF audio from dial strings\n\n## Installation\n\n```shell\npip install dtmf\n```\n\n## What is DTMF?\n\nDual-tone multi-frequency signaling (DTMF) is a telecommunication signaling system used between telephone equipment and other communications devices. DTMF became known in the United States as \'Touch-Tone\' for use in push-button telephones supplied to telephone customers.\n\nDTMF tones use a mixture of two sine waves at different frequencies. Eight different audio frequencies are combined in pairs to make 16 unique tones. A tone is assigned to each of the digits from 0 to 9, the letters A to D, and the symbols # and *. The combination used for each tone are as follows:\n\n|            | **1209 Hz** | **1336 Hz** | **1477 Hz** | **1633 Hz** |\n| ---------- | :---------: | :---------: | :---------: | :---------: |\n| **697 Hz** | 1           | 2           | 3           | A           |\n| **770 Hz** | 4           | 5           | 6           | B           |\n| **852 Hz** | 7           | 8           | 9           | C           |\n| **941 Hz** | *           | 0           | #           | D           |\n\n### Dial string syntax\n\nA dial string is a textual representation of a sequence of DTMF digits and/or symbols. This format is commonly used as input to a telephone modem or another telephony device with automatic dialing as instructions for dialing the recipient of an outgoing call.\n\nDial strings use the following DTMF symbols:\n\n* `0`-`9`\n* `A`-`D`\n* `*` or `E`\n* `#` or `F`\n\nIn addition to the 16 DTMF symbols, dial strings support the following additional symbols:\n\n* `P` or `,` for a momentary pause (usually 2 seconds)\n\n## Usage\n\n### Parsing a dial string\n\n```python\nfrom dtmf import parse\n\ndial_str = "5551234,500#"\n\nobj = parse(input)\n\nprint(repr(obj))\n```\n\n**Output:**\n\n```text\nString([\n    Tone("5"),\n    Tone("5"),\n    Tone("5"),\n    Tone("1"),\n    Tone("2"),\n    Tone("3"),\n    Tone("4"),\n    Pause(),\n    Tone("5"),\n    Tone("0"),\n    Tone("0"),\n    Tone("#")\n])\n```\n\n### Constructing a dial string\n\n```python\nimport dtmf.model as model\n\nobj = model.String([\n    model.Tone("5"),\n    model.Tone("5"),\n    model.Tone("5"),\n    model.Tone("1"),\n    model.Tone("2"),\n    model.Tone("3"),\n    model.Tone("4"),\n    model.Pause(),\n    model.Tone("5"),\n    model.Tone("0"),\n    model.Tone("0"),\n    model.Tone("#")\n])\n\nprint(str(obj))\n```\n\n**Output:**\n\n```text\n5551234,500#\n```\n\n### Detecting DTMF tones in an audio buffer\n\n```python\nfrom dtmf import detect\n\n# list of audio samples as floats\ndata = [...]\nsample_rate = 8000\n\nresults = detect(data, sample_rate)\n\nfor result in results:\n    print(f"{result.start:<3d} - {result.end:>5d} : {result.tone!s}")\n```\n\n**Output:**\n\n```text\n  0 - 105 : 5\n105 - 210 : 5\n210 - 315 : 5\n315 - 420 : 5\n420 - 525 : None\n...\n```\n\n### Generating DTMF audio from a dial string\n\n```python\nfrom dtmf import generate\nimport dtmf.model as model\n\nobj = model.String([\n    model.Tone("5"),\n    model.Tone("5"),\n    model.Tone("5"),\n    model.Tone("1"),\n    model.Tone("2"),\n    model.Tone("3"),\n    model.Tone("4"),\n    model.Pause(),\n    model.Tone("5"),\n    model.Tone("0"),\n    model.Tone("0"),\n    model.Tone("#")\n])\n\naudio = generate(obj)\n```\n\n## Support\n\nPlease use the project\'s [Issues page](https://github.com/gdereese/dtmf/issues) to report any issues.\n\n## Contributing\n\n### Installing for development\n\n```shell\npoetry install\n```\n\n### Linting source files\n\n```shell\npoetry run pylint --rcfile .pylintrc src/dtmf\n```\n\n### Running tests\n\n```shell\npoetry run pytest\n```\n\n## License\n\nThis library is licensed under the terms of the [MIT](https://choosealicense.com/licenses/MIT/) license.\n',
    'author': 'Gary DeReese',
    'author_email': 'garydereese@sbcglobal.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/gdereese/dtmf',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<3.11',
}


setup(**setup_kwargs)
