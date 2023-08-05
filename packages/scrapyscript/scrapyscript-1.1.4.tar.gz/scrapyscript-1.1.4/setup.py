# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['scrapyscript']

package_data = \
{'': ['*']}

install_requires = \
['Scrapy>=2.5.1,<3.0.0', 'billiard>=3.6,<4.0']

setup_kwargs = {
    'name': 'scrapyscript',
    'version': '1.1.4',
    'description': 'Run a Scrapy spider programmatically from a script or a Celery task - no project required.',
    'long_description': '<h1 align="center">\n  <br>\n  <a href="https://github.com/jschnurr/scrapyscript"><img src="https://i.ibb.co/ww3bNZ3/scrapyscript.png" alt="Scrapyscript"></a>\n  <br>\n</h1>\n\n<h4 align="center">Embed Scrapy jobs directly in your code</h4>\n\n<p align="center">\n  <a href="https://github.com/jschnurr/scrapyscript/releases">\n    <img src="https://img.shields.io/github/release/jschnurr/scrapyscript.svg">\n  </a>\n\n  <a href="https://pypi.org/project/scrapyscript/">\n    <img src="https://img.shields.io/pypi/v/scrapyscript.svg">\n  </a>\n\n  <img src="https://github.com/jschnurr/scrapyscript/workflows/Tests/badge.svg">\n  \n  <img src="https://img.shields.io/pypi/pyversions/scrapyscript.svg">\n</p>\n\n### What is Scrapyscript?\n\nScrapyscript is a Python library you can use to run [Scrapy](https://github.com/scrapy/scrapy) spiders directly from your code. Scrapy is a great framework to use for scraping projects, but sometimes you don\'t need the whole framework, and just want to run a small spider from a script or a [Celery](https://github.com/celery/celery) job. That\'s where Scrapyscript comes in.\n\nWith Scrapyscript, you can:\n\n- wrap regular Scrapy [Spiders](https://docs.scrapy.org/en/latest/topics/spiders.html) in a `Job`\n- load the `Job(s)` in a `Processor`\n- call `processor.run()` to execute them\n\n... returning all results when the last job completes.\n\nLet\'s see an example.\n\n```python\nimport scrapy\nfrom scrapyscript import Job, Processor\n\nprocessor = Processor(settings=None)\n\nclass PythonSpider(scrapy.spiders.Spider):\n    name = "myspider"\n\n    def start_requests(self):\n        yield scrapy.Request(self.url)\n\n    def parse(self, response):\n        data = response.xpath("//title/text()").extract_first()\n        return {\'title\': data}\n\njob = Job(PythonSpider, url="http://www.python.org")\nresults = processor.run(job)\n\nprint(results)\n```\n\n```json\n[{ "title": "Welcome to Python.org" }]\n```\n\nSee the [examples](examples/) directory for more, including a complete `Celery` example.\n\n### Install\n\n```python\npip install scrapyscript\n```\n\n### Requirements\n\n- Linux or MacOS\n- Python 3.8+\n- Scrapy 2.5+\n\n### API\n\n#### Job (spider, \\*args, \\*\\*kwargs)\n\nA single request to call a spider, optionally passing in \\*args or \\*\\*kwargs, which will be passed through to the spider constructor at runtime.\n\n```python\n# url will be available as self.url inside MySpider at runtime\nmyjob = Job(MySpider, url=\'http://www.github.com\')\n```\n\n#### Processor (settings=None)\n\nCreate a multiprocessing reactor for running spiders. Optionally provide a `scrapy.settings.Settings` object to configure the Scrapy runtime.\n\n```python\nsettings = scrapy.settings.Settings(values={\'LOG_LEVEL\': \'WARNING\'})\nprocessor = Processor(settings=settings)\n```\n\n#### Processor.run(jobs)\n\nStart the Scrapy engine, and execute one or more jobs. Blocks and returns consolidated results in a single list.\n`jobs` can be a single instance of `Job`, or a list.\n\n```python\nresults = processor.run(myjob)\n```\n\nor\n\n```python\nresults = processor.run([myjob1, myjob2, ...])\n```\n\n#### A word about Spider outputs\n\nAs per the [scrapy docs](https://doc.scrapy.org/en/latest/topics/spiders.html), a `Spider`\nmust return an iterable of `Request` and/or `dict` or `Item` objects.\n\nRequests will be consumed by Scrapy inside the `Job`. `dict` or `scrapy.Item` objects will be queued\nand output together when all spiders are finished.\n\nDue to the way billiard handles communication between processes, each `dict` or `Item` must be\npickle-able using pickle protocol 0. **It\'s generally best to output `dict` objects from your Spider.**\n\n### Contributing\n\nUpdates, additional features or bug fixes are always welcome.\n\n#### Setup\n\n- Install [Poetry](https://python-poetry.org/docs/#installation)\n- `git clone git@github.com:jschnurr/scrapyscript.git`\n- `poetry install`\n\n#### Tests\n\n- `make test` or `make tox`\n\n### Version History\n\n- 1.1.4 - Oct-2021 - Remove py36,py37 support, clarify OS support, bump dependencies\n- 1.1.3 - Jul-2021 - Bump versions, add examples, readme changes\n- 1.1.2 - Jul-2021 - Fix #11 to allow billiard version to float\n- 1.1.0 - Jun-2020 - Python 3.6+ only, dependency version bumps\n- 1.0.0 - Dec-2017 - API changes to pass \\*args and \\*\\*kwargs to running spider\n- 0.1.0 - May-2017 - patches to support Celery 4+ and Billiard 3.5.+. Thanks to @mrge and @bmartel.\n\n### License\n\nThe MIT License (MIT). See LICENCE file for details.\n',
    'author': 'Jeff Schnurr',
    'author_email': 'jschnurr@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jschnurr/scrapyscript',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
