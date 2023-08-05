# True Checker for Python

Python client library for [True Checker API](https://checker.trueweb.app/redoc)

## How to install

```bash
pip install truechecker
```

## How to use

```python
# import TrueChecker
from truechecker import TrueChecker


# create an instance (poss your Telegram bot token here)
checker = TrueChecker("your_bot_token")


# prepare a file with users ids
# you should use string path, pathlib.Path object or io.BaseFile
file_path = "downloads/users.csv"


# send request to create a new job
job = await checker.check_profile(file_path)
print("Job created. ID:", job.id)


# get the status of job
job = await checker.get_job_status(job.id)
print("Job state:", job.state)
print("Job progress:", job.progress)


# if the job is done, let's get the profile
profile = await checker.get_profile("my_bot_username")
print("Bot profile:", profile)


# if you need to cancel the job
job = await checker.cancel_job(job.id)
print("Job state:", job.state)  # Cancelled


# Don't forget to close checker on your app's on_shutdown
await checker.close()

```
_CAUTION: it's not a full code example. Await statements should be used within coroutines only._

## Contributing
Before making Pull/Merge Requests, please read the [Contributing guidelines](CONTRIBUTING.md)
