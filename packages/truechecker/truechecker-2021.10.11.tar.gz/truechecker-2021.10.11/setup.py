# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['truechecker', 'truechecker.models', 'truechecker.utils']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.7,<4.0', 'certifi>=2021,<2022', 'pydantic>=1.8,<2.0']

setup_kwargs = {
    'name': 'truechecker',
    'version': '2021.10.11',
    'description': 'Python client for True Checker API',
    'long_description': '# True Checker for Python\n\nPython client library for [True Checker API](https://checker.trueweb.app/redoc)\n\n## How to install\n\n```bash\npip install truechecker\n```\n\n## How to use\n\n```python\n# import TrueChecker\nfrom truechecker import TrueChecker\n\n\n# create an instance (poss your Telegram bot token here)\nchecker = TrueChecker("your_bot_token")\n\n\n# prepare a file with users ids\n# you should use string path, pathlib.Path object or io.BaseFile\nfile_path = "downloads/users.csv"\n\n\n# send request to create a new job\njob = await checker.check_profile(file_path)\nprint("Job created. ID:", job.id)\n\n\n# get the status of job\njob = await checker.get_job_status(job.id)\nprint("Job state:", job.state)\nprint("Job progress:", job.progress)\n\n\n# if the job is done, let\'s get the profile\nprofile = await checker.get_profile("my_bot_username")\nprint("Bot profile:", profile)\n\n\n# if you need to cancel the job\njob = await checker.cancel_job(job.id)\nprint("Job state:", job.state)  # Cancelled\n\n\n# Don\'t forget to close checker on your app\'s on_shutdown\nawait checker.close()\n\n```\n_CAUTION: it\'s not a full code example. Await statements should be used within coroutines only._\n\n## Contributing\nBefore making Pull/Merge Requests, please read the [Contributing guidelines](CONTRIBUTING.md)\n',
    'author': 'Oleg A.',
    'author_email': 'oleg@trueweb.app',
    'maintainer': 'Oleg A.',
    'maintainer_email': 'oleg@trueweb.app',
    'url': 'https://gitlab.com/true-web-app/true-checker/true-checker-python',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
