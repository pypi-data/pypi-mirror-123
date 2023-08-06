# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aoquality', 'aoquality.tools']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0', 'matplotlib>=3.1,<4.0', 'python-casacore>=3.0,<4.0']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=1.0,<2.0']}

entry_points = \
{'console_scripts': ['aostats = aoquality.tools.aostats:main']}

setup_kwargs = {
    'name': 'aoquality',
    'version': '0.2.3',
    'description': "Python module to access Measurement Sets' quality statistics produced by aoflagger, aoquality or DPPP.",
    'long_description': "# pyaoquality\n\nPython module to access Measurement Sets' quality statistics produced by aoflagger, aoquality or DPPP.\n\n## Installation\n\npyaoquality can be installed via pip:\n\n    $ pip install aoquality\n\nand requires Python 3.6.0 or higher.\n\n# Usage\n\nExample to retrieve baseline statistics:\n\n\n```python\naoq = aoquality.AOQualityBaselineStat(ms_file)\n\n# plot SNR as function of baseline length:\nplt.plot(aoq.blenght, aoq.SNR)\n\n# plot SNR as function of first antenna:\nplt.plot(aoq.ant1, aoq.SNR)\n\n```\n\nTo retrieve time statistics:\n\n\n```python\naot = aoquality.AOQualityTimeStat(ms_file)\n\n# plot RFI percentage as function of time:\nplt.plot(aot.time, aot.RFIPercentage)\n\n```\n\nTo retrieve frequency statistics:\n\n\n```python\naof = aoquality.AOQualityFrequencyStat(ms_file)\n\n# plot Std as function of frequencies:\nplt.plot(aof.freqs, aof.Std)\n\n```\n\n# Command line tool\n\nThere is also a command line tool, aostats, which usage is as follow:\n\n    Usage: aostats plot [OPTIONS] MS_FILES... [Mean|Std|DStd|Count|DCount|Sum|DSum\n                        |DSumP2|Variance|DVariance|SNR|RFICount|RFIPercentage]\n\n      Plot Statistics from AO Quality Tables\n\n      MS_FILES: Input MS files STAT_NAME: Statistic Name\n\n    Options:\n      -o, --out_prefix TEXT    Prefix to the output filename  [default: stat]\n      -p, --pol INTEGER RANGE  Polarization index: 0->XX, 1->XY, 2->YX, 3->YY\n                               [default: 0]\n\n      --log                    Plot in log scale\n      --vmin FLOAT             Minimum value\n      --vmax FLOAT             Maximum value\n      --name TEXT              Title of the plot\n      --help                   Show this message and exit.\n\n\n",
    'author': '"Florent Mertens"',
    'author_email': '"florent.mertens@gmail.com"',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/flomertens/aoquality/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
