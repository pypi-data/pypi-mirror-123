# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['step_exec_lib', 'step_exec_lib.utils']

package_data = \
{'': ['*']}

install_requires = \
['configargparse>=1.4.1,<2.0.0',
 'gitpython>=3.1.17,<4.0.0',
 'semver>=2.13.0,<3.0.0']

setup_kwargs = {
    'name': 'step-exec-lib',
    'version': '0.1.3',
    'description': 'A library that helps execute pipeline of tasks using filters and simple composition',
    'long_description': "[![build](https://github.com/giantswarm/step-exec-lib/actions/workflows/main.yml/badge.svg)](https://github.com/giantswarm/step-exec-lib/actions/workflows/main.yml)\n[![codecov](https://codecov.io/gh/giantswarm/step-exec-lib/branch/master/graph/badge.svg)](https://codecov.io/gh/giantswarm/step-exec-lib)\n[![PyPI Version](https://img.shields.io/pypi/v/step-exec-lib.svg)](https://pypi.org/project/step-exec-lib/)\n[![Python Versions](https://img.shields.io/pypi/pyversions/step-exec-lib.svg)](https://pypi.org/project/step-exec-lib/)\n[![Apache License](https://img.shields.io/badge/license-apache-blue.svg)](https://pypi.org/project/step-exec-lib/)\n\n# step-exec-lib\n\nA simple library to easily orchestrate a set of Steps into a filtrable pipeline.\n\n**Disclaimer**: docs are still work-in-progress!\n\nEach step provides a defined set of actions. When a pipeline is execute first all `pre` actions\nof all Steps are executed, then `run` actions and so on. Steps can provide labels, so\nyou can easily disable/enable a subset of steps.\n\nA ready to use python app template. Based on `pipenv`.\n\n## How to use the library\n\n### BuildStep\n\nThe most important basic class is [BuildStep](step_exec_lib/steps.py). The class is abstract\nand you have to inherit from it to provide any actual functionality.  The most important methods and properties of\nthis class are:\n\n* Each `BuildStep` provides a set of step names it is associated with in the `steps_provided` property.\n  These steps are used for filtering with `--steps`/`--skip-steps` command line options.\n* `initialize_config` provides additional config options a specific class delivered from `BuildStep`\n  wants to provide.\n* `pre_run` is optional and should be used for validation and assertions. `pre_runs` of all `BuildSteps` are executed\n  before any `run` method is executed. Its purpose is to allow the `abs`\n  to quit with error even before any actual build or tests are done. The method can't be blocking and should run\n  fast. If `pre_step` of any `BuildStep` fails, `run` methods of all `BuildSteps` are skipped.\n* `run` is the method where actual long-running actions of the `BuildStep` are executed.\n* `cleanup` is an optional method used to clean up resources that might have been needed by `run` but can't be cleaned\n  up until all `runs` have executed. `cleanups` are called after any `run` failed or all of them are done.\n\n### BuildStepsFilteringPipeline\n\n`BuildStep` class provides the `steps_provided` property, but is not in control of whether it should be executed or not\nand when. `BuildSteps` have to be assembled into `pipelines`. The basic pipeline in `BuildStepsFilteringPipeline`, which\nallows you to make a sequential pipeline out of your steps and filter and skip them according to `steps_provided` they\nreturn and command line options `--steps`/`--skip-steps`. Each major part of `abs` execution is combined into a\npipeline, like `HelmBuildFilteringPipeline` used to execute build pipeline with Helm 3 or `PytestTestFilteringPipeline`\nwhich is used to execute tests using `pytest` once the build pipeline is done.\n",
    'author': 'Łukasz Piątkowski',
    'author_email': 'lukasz@giantswarm.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/giantswarm/step-exec-lib',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
