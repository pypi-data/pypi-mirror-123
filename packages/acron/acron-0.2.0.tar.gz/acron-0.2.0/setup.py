# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['acron']

package_data = \
{'': ['*']}

install_requires = \
['croniter>=1.0.15,<2.0.0']

extras_require = \
{':python_version < "3.7"': ['dataclasses>=0.8,<0.9']}

setup_kwargs = {
    'name': 'acron',
    'version': '0.2.0',
    'description': 'Lightweight scheduler',
    'long_description': 'Lightweight scheduler for python asyncio\n\nBased on croniter to support the crontab syntax.\n\n============\nInstallation\n============\n\nInstalling acron.\n\n.. code:: shell\n\n    $ pip install acron\n\n=====\nUsage\n=====\n\nTo get started you need at least one job.\nUse the top level ``acron.run`` function for simple scheduling.\n\n\n.. code:: python\n\n    import asyncio\n    import acron\n\n    async def do_the_thing():\n        print("Doing the thing")\n\n    do_thing = acron.SimpleJob(\n        name="Do the thing",\n        schedule="0/1 * * * *",\n        func=do_the_thing,\n    )\n\n    asyncio.run(acron.run({do_thing}))\n\n\nFor more advanced use cases, the ``Scheduler`` class can be used as async context manager.\nCall ``scheduler.wait()`` to keep it running forever.\nTo submit jobs call ``scheduler.update_jobs(jobs)`` with the complete set of jobs.\n\nRunning a simple example running a function every hour...\n\n\n.. code:: python\n\n    import asyncio\n    import dataclasses\n\n    from acron.scheduler import Scheduler, Job\n\n    @dataclasses.dataclass(frozen=True)\n    class ThingData:\n        foo: bool\n\n    async def do_the_thing(data: ThingData):\n        print(f"Doing the thing {data}")\n\n    async def run_jobs_forever():\n        do_thing = Job[ThingData](\n            name="Do the thing",\n            schedule="0/1 * * * *",\n            data=ThingData(True),\n            func=do_the_thing,\n        )\n\n        async with Scheduler() as scheduler:\n            await scheduler.update_jobs({do_thing})\n            await scheduler.wait()\n\n    if __name__ == "__main__":\n        try:\n            asyncio.run(run_jobs_forever())\n        except KeyboardInterrupt:\n            print("Bye.")\n\n\n\n\nSpecifying a timezone\n----------------------\n\nFor python 3.9+ you can use the standard library\'s ``zoneinfo`` module to specify a timezone.\n\n.. code:: python\n\n    import zoneinfo\n\n    async with Scheduler(tz=zoneinfo.ZoneInfo("Europe/Berlin")) as scheduler:\n        ...\n\n\n\nFor earlier python versions you can use a third party library like ``pytz``.\n\n.. code:: python\n\n    import pytz\n\n    async with Scheduler(tz=pytz.timezone("Europe/Berlin")) as scheduler:\n        ...\n\n\nJob context\n-----------\n\nIt is possible to retrieve the context for the scheduled job from the running\njob function using ``job_context()``. This returns a ``JobContext`` containing\na reference to the ``ScheduledJob``. The ``job_context()`` function is implemented\nusing contextvars to provide the correct context to the matching asyncio task.\n\n.. code:: python\n\n    async def my_job_func():\n        job_id = acron.job_context().scheduled_job.id\n        job_name = acron.job_context().scheduled_job.job.name\n        print(f"Running job {job_id!r}, scheduled with id {job_id}")\n\n\n=================\nLocal development\n=================\n\nThe project uses poetry to run the test, the linter and to build the artifacts.\n\nThe easiest way to start working on acron is to use docker with the dockerfile\nincluded in the repository (manual usage of poetry is explained here:\nhttps://python-poetry.org/docs/ ).\n\nTo use docker, first generate the docker image. Run this command from the top\nlevel directory in the repository:\n\n.. code-block:: console\n\n   docker build -t acron-builder -f docker/Dockerfile .\n\nNow you can use it to build or run the linter/tests:\n\n.. code-block:: console\n\n    $ alias acron-builder="docker run --rm -it -v $PWD/dist:/build/dist acron-builder"\n\n    $ acron-builder run pytest tests\n    =============================================================================================== test session starts ================================================================================================\n    platform linux -- Python 3.9.7, pytest-5.4.3, py-1.10.0, pluggy-0.13.1\n    rootdir: /build\n    plugins: asyncio-0.15.1\n    collected 4 items\n    tests/test_acron.py ....                                                                                                                                                                                     [100%]\n    ================================================================================================ 4 passed in 0.04s =================================================================================================\n\n    $ acron-builder build\n    Building acron (0.1.0)\n      - Building sdist\n      - Built acron-0.1.0.tar.gz\n      - Building wheel\n      - Built acron-0.1.0-py3-none-any.whl\n\n    $ ls dist\n    acron-0.1.0-py3-none-any.whl  acron-0.1.0.tar.gz\n\n\n=========\nDebugging\n=========\n\nDebug logging can be enabled by setting the ``ACRON_DEBUG`` environment variable to ``TRUE``.\n\n',
    'author': 'Aitor Iturri',
    'author_email': 'aitor.iturri@appgate.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/appgate/acron',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
