#!/usr/bin/env python
#   -*- coding: utf-8 -*-

from setuptools import setup
from setuptools.command.install import install as _install

class install(_install):
    def pre_install_script(self):
        pass

    def post_install_script(self):
        pass

    def run(self):
        self.pre_install_script()

        _install.run(self)

        self.post_install_script()

if __name__ == '__main__':
    setup(
        name = 'pybuilder',
        version = '0.13.3',
        description = 'PyBuilder — an easy-to-use build automation tool for Python.',
        long_description = '[PyBuilder &#x2014; an easy-to-use build automation tool for Python](https://pybuilder.io)\n=========\n\n[![Follow PyBuilder on Twitter](https://img.shields.io/twitter/follow/pybuilder_?label=Follow%20PyBuilder&style=social)](https://twitter.com/intent/follow?screen_name=pybuilder_)\n[![Gitter](https://img.shields.io/gitter/room/pybuilder/pybuilder?logo=gitter)](https://gitter.im/pybuilder/pybuilder)\n[![Build Status](https://img.shields.io/github/workflow/status/pybuilder/pybuilder/pybuilder/master)](https://github.com/pybuilder/pybuilder/actions/workflows/pybuilder.yml)\n[![Coverage Status](https://img.shields.io/coveralls/github/pybuilder/pybuilder/master?logo=coveralls)](https://coveralls.io/r/pybuilder/pybuilder?branch=master)\n\n[![PyBuilder Version](https://img.shields.io/pypi/v/pybuilder?logo=pypi)](https://pypi.org/project/pybuilder/)\n[![PyBuilder Python Versions](https://img.shields.io/pypi/pyversions/pybuilder?logo=pypi)](https://pypi.org/project/pybuilder/)\n[![PyBuilder Downloads Per Day](https://img.shields.io/pypi/dd/pybuilder?logo=pypi)](https://pypi.org/project/pybuilder/)\n[![PyBuilder Downloads Per Week](https://img.shields.io/pypi/dw/pybuilder?logo=pypi)](https://pypi.org/project/pybuilder/)\n[![PyBuilder Downloads Per Month](https://img.shields.io/pypi/dm/pybuilder?logo=pypi)](https://pypi.org/project/pybuilder/)\n\nPyBuilder is a software build tool written in 100% pure Python, mainly\ntargeting Python applications.\n\nPyBuilder is based on the concept of dependency based programming, but it also\ncomes with a powerful plugin mechanism, allowing the construction of build life\ncycles similar to those known from other famous (Java) build tools.\n\nPyBuilder is running on the following versions of Python 3.6, 3.7, 3.8, 3.9, 3.10, and PyPy 3.7.\n\nSee the [GitHub Actions Workflow](https://github.com/pybuilder/pybuilder/actions/workflows/pybuilder.yml) for version specific output.\n\n## Installing\n\nPyBuilder is available using pip:\n\n    $ pip install pybuilder\n\nFor development builds use:\n\n    $ pip install --pre pybuilder\n\nSee the [PyPI](https://pypi.org/project/pybuilder/) for more information.\n\n## Getting started\n\nPyBuilder emphasizes simplicity. If you want to build a pure Python project and\nuse the recommended directory layout, all you have to do is create a file\nbuild.py with the following content:\n\n```python\nfrom pybuilder.core import use_plugin\n\nuse_plugin("python.core")\nuse_plugin("python.unittest")\nuse_plugin("python.coverage")\nuse_plugin("python.distutils")\n\ndefault_task = "publish"\n```\n\nSee the [PyBuilder homepage](https://pybuilder.io) for more details and\na list of plugins.\n\n## Release Notes\n\nThe release notes can be found [here](https://pybuilder.io/release-notes/).\nThere will also be a git tag with each release. Please note that we do not currently promote tags to GitHub "releases".\n\n## Development\nSee [Developing PyBuilder](https://pybuilder.io/documentation/developing-pybuilder)\n',
        long_description_content_type = 'text/markdown',
        classifiers = [
            'Programming Language :: Python',
            'Programming Language :: Python :: Implementation :: CPython',
            'Programming Language :: Python :: Implementation :: PyPy',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
            'Programming Language :: Python :: 3.10',
            'Operating System :: MacOS :: MacOS X',
            'Operating System :: POSIX :: Linux',
            'Operating System :: Microsoft :: Windows',
            'Operating System :: OS Independent',
            'Development Status :: 5 - Production/Stable',
            'Environment :: Console',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: Apache Software License',
            'Topic :: Software Development :: Build Tools',
            'Topic :: Software Development :: Quality Assurance',
            'Topic :: Software Development :: Testing'
        ],
        keywords = 'PyBuilder PyB build tool automation Python testing QA packaging distribution',

        author = 'Arcadiy Ivanov, Alexander Metzner, Maximilien Riehl, Michael Gruber, Udo Juettner, Marcel Wolf, Valentin Haenel',
        author_email = 'arcadiy@ivanov.biz, alexander.metzner@gmail.com, max@riehl.io, aelgru@gmail.com, udo.juettner@gmail.com, marcel.wolf@me.com, valentin@haenel.co',
        maintainer = 'Arcadiy Ivanov',
        maintainer_email = 'arcadiy@ivanov.biz',

        license = 'Apache License, Version 2.0',

        url = 'https://pybuilder.io',
        project_urls = {
            'Bug Tracker': 'https://github.com/pybuilder/pybuilder/issues',
            'Documentation': 'https://pybuilder.io/documentation',
            'Source Code': 'https://github.com/pybuilder/pybuilder',
            'Twitter': 'https://twitter.com/pybuilder_'
        },

        scripts = ['scripts/pyb'],
        packages = [
            'pybuilder',
            'pybuilder._vendor',
            'pybuilder._vendor._distutils_hack',
            'pybuilder._vendor.backports',
            'pybuilder._vendor.colorama',
            'pybuilder._vendor.distlib',
            'pybuilder._vendor.distlib._backport',
            'pybuilder._vendor.filelock',
            'pybuilder._vendor.importlib_metadata',
            'pybuilder._vendor.importlib_resources',
            'pybuilder._vendor.importlib_resources.tests',
            'pybuilder._vendor.importlib_resources.tests.data01',
            'pybuilder._vendor.importlib_resources.tests.data01.subdirectory',
            'pybuilder._vendor.importlib_resources.tests.data02',
            'pybuilder._vendor.importlib_resources.tests.data02.one',
            'pybuilder._vendor.importlib_resources.tests.data02.two',
            'pybuilder._vendor.importlib_resources.tests.zipdata01',
            'pybuilder._vendor.importlib_resources.tests.zipdata02',
            'pybuilder._vendor.pkg_resources',
            'pybuilder._vendor.pkg_resources._vendor',
            'pybuilder._vendor.pkg_resources._vendor.packaging',
            'pybuilder._vendor.pkg_resources.extern',
            'pybuilder._vendor.platformdirs',
            'pybuilder._vendor.tailer',
            'pybuilder._vendor.tblib',
            'pybuilder._vendor.virtualenv',
            'pybuilder._vendor.virtualenv.activation',
            'pybuilder._vendor.virtualenv.activation.bash',
            'pybuilder._vendor.virtualenv.activation.batch',
            'pybuilder._vendor.virtualenv.activation.cshell',
            'pybuilder._vendor.virtualenv.activation.fish',
            'pybuilder._vendor.virtualenv.activation.nushell',
            'pybuilder._vendor.virtualenv.activation.powershell',
            'pybuilder._vendor.virtualenv.activation.python',
            'pybuilder._vendor.virtualenv.app_data',
            'pybuilder._vendor.virtualenv.config',
            'pybuilder._vendor.virtualenv.config.cli',
            'pybuilder._vendor.virtualenv.create',
            'pybuilder._vendor.virtualenv.create.via_global_ref',
            'pybuilder._vendor.virtualenv.create.via_global_ref.builtin',
            'pybuilder._vendor.virtualenv.create.via_global_ref.builtin.cpython',
            'pybuilder._vendor.virtualenv.create.via_global_ref.builtin.pypy',
            'pybuilder._vendor.virtualenv.create.via_global_ref.builtin.python2',
            'pybuilder._vendor.virtualenv.discovery',
            'pybuilder._vendor.virtualenv.discovery.windows',
            'pybuilder._vendor.virtualenv.run',
            'pybuilder._vendor.virtualenv.run.plugin',
            'pybuilder._vendor.virtualenv.seed',
            'pybuilder._vendor.virtualenv.seed.embed',
            'pybuilder._vendor.virtualenv.seed.embed.via_app_data',
            'pybuilder._vendor.virtualenv.seed.embed.via_app_data.pip_install',
            'pybuilder._vendor.virtualenv.seed.wheels',
            'pybuilder._vendor.virtualenv.seed.wheels.embed',
            'pybuilder._vendor.virtualenv.util',
            'pybuilder._vendor.virtualenv.util.path',
            'pybuilder._vendor.virtualenv.util.path._pathlib',
            'pybuilder._vendor.virtualenv.util.subprocess',
            'pybuilder.extern',
            'pybuilder.pluginhelper',
            'pybuilder.plugins',
            'pybuilder.plugins.python',
            'pybuilder.plugins.python.remote_tools',
            'pybuilder.remote'
        ],
        namespace_packages = [],
        py_modules = [],
        entry_points = {
            'console_scripts': ['pyb = pybuilder.cli:main']
        },
        data_files = [],
        package_data = {
            'pybuilder': ['LICENSE'],
            'pybuilder._vendor': ['distutils-precedence.pth', '__init__.py', 'six.py', 'LICENSES', 'typing_extensions.py', 'zipp.py', 'pkg_resources/__init__.py', 'pkg_resources/_vendor/pyparsing.py', 'pkg_resources/_vendor/appdirs.py', 'pkg_resources/_vendor/__init__.py', 'pkg_resources/_vendor/__pycache__/appdirs.cpython-39.pyc', 'pkg_resources/_vendor/__pycache__/pyparsing.cpython-39.pyc', 'pkg_resources/_vendor/__pycache__/__init__.cpython-39.pyc', 'pkg_resources/_vendor/packaging/_structures.py', 'pkg_resources/_vendor/packaging/_typing.py', 'pkg_resources/_vendor/packaging/version.py', 'pkg_resources/_vendor/packaging/_compat.py', 'pkg_resources/_vendor/packaging/__init__.py', 'pkg_resources/_vendor/packaging/tags.py', 'pkg_resources/_vendor/packaging/requirements.py', 'pkg_resources/_vendor/packaging/__about__.py', 'pkg_resources/_vendor/packaging/specifiers.py', 'pkg_resources/_vendor/packaging/utils.py', 'pkg_resources/_vendor/packaging/markers.py', 'pkg_resources/_vendor/packaging/__pycache__/markers.cpython-39.pyc', 'pkg_resources/_vendor/packaging/__pycache__/_compat.cpython-39.pyc', 'pkg_resources/_vendor/packaging/__pycache__/_typing.cpython-39.pyc', 'pkg_resources/_vendor/packaging/__pycache__/__about__.cpython-39.pyc', 'pkg_resources/_vendor/packaging/__pycache__/specifiers.cpython-39.pyc', 'pkg_resources/_vendor/packaging/__pycache__/__init__.cpython-39.pyc', 'pkg_resources/_vendor/packaging/__pycache__/_structures.cpython-39.pyc', 'pkg_resources/_vendor/packaging/__pycache__/requirements.cpython-39.pyc', 'pkg_resources/_vendor/packaging/__pycache__/utils.cpython-39.pyc', 'pkg_resources/_vendor/packaging/__pycache__/version.cpython-39.pyc', 'pkg_resources/extern/__init__.py', 'pkg_resources/extern/__pycache__/__init__.cpython-39.pyc', 'pkg_resources/__pycache__/__init__.cpython-39.pyc', 'pkg_resources/tests/data/my-test-package-source/setup.py', 'backports/entry_points_selectable.py', 'backports/__init__.py', 'backports/__pycache__/__init__.cpython-39.pyc', 'backports/__pycache__/entry_points_selectable.cpython-39.pyc', 'distlib/w64.exe', 'distlib/compat.py', 'distlib/t64-arm.exe', 'distlib/database.py', 'distlib/util.py', 'distlib/index.py', 'distlib/version.py', 'distlib/__init__.py', 'distlib/wheel.py', 'distlib/locators.py', 'distlib/t32.exe', 'distlib/w32.exe', 'distlib/metadata.py', 'distlib/w64-arm.exe', 'distlib/markers.py', 'distlib/t64.exe', 'distlib/resources.py', 'distlib/scripts.py', 'distlib/manifest.py', 'distlib/_backport/shutil.py', 'distlib/_backport/sysconfig.py', 'distlib/_backport/sysconfig.cfg', 'distlib/_backport/__init__.py', 'distlib/_backport/tarfile.py', 'distlib/_backport/misc.py', 'distlib/__pycache__/util.cpython-39.pyc', 'distlib/__pycache__/compat.cpython-39.pyc', 'distlib/__pycache__/resources.cpython-39.pyc', 'distlib/__pycache__/__init__.cpython-39.pyc', 'distlib/__pycache__/scripts.cpython-39.pyc', 'platformdirs/unix.py', 'platformdirs/windows.py', 'platformdirs/android.py', 'platformdirs/version.py', 'platformdirs/macos.py', 'platformdirs/__init__.py', 'platformdirs/api.py', 'platformdirs/py.typed', 'platformdirs/__main__.py', 'platformdirs/__pycache__/api.cpython-39.pyc', 'platformdirs/__pycache__/__init__.cpython-39.pyc', 'platformdirs/__pycache__/version.cpython-39.pyc', 'platformdirs/__pycache__/unix.cpython-39.pyc', 'importlib_resources/simple.py', 'importlib_resources/_adapters.py', 'importlib_resources/_compat.py', 'importlib_resources/__init__.py', 'importlib_resources/_common.py', 'importlib_resources/_legacy.py', 'importlib_resources/_itertools.py', 'importlib_resources/py.typed', 'importlib_resources/abc.py', 'importlib_resources/readers.py', 'importlib_resources/tests/test_reader.py', 'importlib_resources/tests/test_contents.py', 'importlib_resources/tests/util.py', 'importlib_resources/tests/update-zips.py', 'importlib_resources/tests/_compat.py', 'importlib_resources/tests/__init__.py', 'importlib_resources/tests/test_path.py', 'importlib_resources/tests/test_resource.py', 'importlib_resources/tests/test_open.py', 'importlib_resources/tests/test_read.py', 'importlib_resources/tests/test_files.py', 'importlib_resources/tests/test_compatibilty_files.py', 'importlib_resources/tests/zipdata01/__init__.py', 'importlib_resources/tests/zipdata01/ziptestdata.zip', 'importlib_resources/tests/zipdata02/__init__.py', 'importlib_resources/tests/zipdata02/ziptestdata.zip', 'importlib_resources/tests/namespacedata01/utf-8.file', 'importlib_resources/tests/namespacedata01/binary.file', 'importlib_resources/tests/namespacedata01/utf-16.file', 'importlib_resources/tests/data01/utf-8.file', 'importlib_resources/tests/data01/binary.file', 'importlib_resources/tests/data01/__init__.py', 'importlib_resources/tests/data01/utf-16.file', 'importlib_resources/tests/data01/subdirectory/binary.file', 'importlib_resources/tests/data01/subdirectory/__init__.py', 'importlib_resources/tests/data02/__init__.py', 'importlib_resources/tests/data02/two/__init__.py', 'importlib_resources/tests/data02/two/resource2.txt', 'importlib_resources/tests/data02/one/__init__.py', 'importlib_resources/tests/data02/one/resource1.txt', '_distutils_hack/__init__.py', '_distutils_hack/override.py', 'tblib/decorators.py', 'tblib/cpython.py', 'tblib/pickling_support.py', 'tblib/__init__.py', 'tblib/__pycache__/pickling_support.cpython-39.pyc', 'tblib/__pycache__/cpython.cpython-39.pyc', 'tblib/__pycache__/__init__.cpython-39.pyc', 'tailer/__init__.py', '__pycache__/__init__.cpython-39.pyc', '__pycache__/zipp.cpython-39.pyc', '__pycache__/six.cpython-39.pyc', 'filelock/_error.py', 'filelock/_soft.py', 'filelock/_util.py', 'filelock/version.py', 'filelock/__init__.py', 'filelock/_unix.py', 'filelock/_windows.py', 'filelock/_api.py', 'filelock/py.typed', 'filelock/__pycache__/_windows.cpython-39.pyc', 'filelock/__pycache__/_error.cpython-39.pyc', 'filelock/__pycache__/_unix.cpython-39.pyc', 'filelock/__pycache__/_soft.cpython-39.pyc', 'filelock/__pycache__/__init__.cpython-39.pyc', 'filelock/__pycache__/_util.cpython-39.pyc', 'filelock/__pycache__/_api.cpython-39.pyc', 'filelock/__pycache__/version.cpython-39.pyc', 'virtualenv/report.py', 'virtualenv/version.py', 'virtualenv/__init__.py', 'virtualenv/info.py', 'virtualenv/__main__.py', 'virtualenv/seed/seeder.py', 'virtualenv/seed/__init__.py', 'virtualenv/seed/embed/__init__.py', 'virtualenv/seed/embed/pip_invoke.py', 'virtualenv/seed/embed/base_embed.py', 'virtualenv/seed/embed/via_app_data/via_app_data.py', 'virtualenv/seed/embed/via_app_data/__init__.py', 'virtualenv/seed/embed/via_app_data/__pycache__/via_app_data.cpython-39.pyc', 'virtualenv/seed/embed/via_app_data/__pycache__/__init__.cpython-39.pyc', 'virtualenv/seed/embed/via_app_data/pip_install/symlink.py', 'virtualenv/seed/embed/via_app_data/pip_install/__init__.py', 'virtualenv/seed/embed/via_app_data/pip_install/copy.py', 'virtualenv/seed/embed/via_app_data/pip_install/base.py', 'virtualenv/seed/embed/via_app_data/pip_install/__pycache__/symlink.cpython-39.pyc', 'virtualenv/seed/embed/via_app_data/pip_install/__pycache__/base.cpython-39.pyc', 'virtualenv/seed/embed/via_app_data/pip_install/__pycache__/__init__.cpython-39.pyc', 'virtualenv/seed/embed/via_app_data/pip_install/__pycache__/copy.cpython-39.pyc', 'virtualenv/seed/embed/__pycache__/pip_invoke.cpython-39.pyc', 'virtualenv/seed/embed/__pycache__/__init__.cpython-39.pyc', 'virtualenv/seed/embed/__pycache__/base_embed.cpython-39.pyc', 'virtualenv/seed/wheels/util.py', 'virtualenv/seed/wheels/__init__.py', 'virtualenv/seed/wheels/acquire.py', 'virtualenv/seed/wheels/periodic_update.py', 'virtualenv/seed/wheels/bundle.py', 'virtualenv/seed/wheels/embed/setuptools-50.3.2-py3-none-any.whl', 'virtualenv/seed/wheels/embed/__init__.py', 'virtualenv/seed/wheels/embed/wheel-0.37.0-py2.py3-none-any.whl', 'virtualenv/seed/wheels/embed/setuptools-44.1.1-py2.py3-none-any.whl', 'virtualenv/seed/wheels/embed/pip-21.2.4-py3-none-any.whl', 'virtualenv/seed/wheels/embed/setuptools-58.1.0-py3-none-any.whl', 'virtualenv/seed/wheels/embed/pip-20.3.4-py2.py3-none-any.whl', 'virtualenv/seed/wheels/embed/__pycache__/__init__.cpython-39.pyc', 'virtualenv/seed/wheels/__pycache__/util.cpython-39.pyc', 'virtualenv/seed/wheels/__pycache__/periodic_update.cpython-39.pyc', 'virtualenv/seed/wheels/__pycache__/__init__.cpython-39.pyc', 'virtualenv/seed/wheels/__pycache__/acquire.cpython-39.pyc', 'virtualenv/seed/wheels/__pycache__/bundle.cpython-39.pyc', 'virtualenv/seed/__pycache__/__init__.cpython-39.pyc', 'virtualenv/seed/__pycache__/seeder.cpython-39.pyc', 'virtualenv/create/describe.py', 'virtualenv/create/debug.py', 'virtualenv/create/__init__.py', 'virtualenv/create/pyenv_cfg.py', 'virtualenv/create/creator.py', 'virtualenv/create/via_global_ref/_virtualenv.py', 'virtualenv/create/via_global_ref/venv.py', 'virtualenv/create/via_global_ref/__init__.py', 'virtualenv/create/via_global_ref/store.py', 'virtualenv/create/via_global_ref/api.py', 'virtualenv/create/via_global_ref/builtin/ref.py', 'virtualenv/create/via_global_ref/builtin/__init__.py', 'virtualenv/create/via_global_ref/builtin/builtin_way.py', 'virtualenv/create/via_global_ref/builtin/via_global_self_do.py', 'virtualenv/create/via_global_ref/builtin/pypy/pypy2.py', 'virtualenv/create/via_global_ref/builtin/pypy/__init__.py', 'virtualenv/create/via_global_ref/builtin/pypy/common.py', 'virtualenv/create/via_global_ref/builtin/pypy/pypy3.py', 'virtualenv/create/via_global_ref/builtin/pypy/__pycache__/common.cpython-39.pyc', 'virtualenv/create/via_global_ref/builtin/pypy/__pycache__/__init__.cpython-39.pyc', 'virtualenv/create/via_global_ref/builtin/pypy/__pycache__/pypy3.cpython-39.pyc', 'virtualenv/create/via_global_ref/builtin/pypy/__pycache__/pypy2.cpython-39.pyc', 'virtualenv/create/via_global_ref/builtin/__pycache__/builtin_way.cpython-39.pyc', 'virtualenv/create/via_global_ref/builtin/__pycache__/ref.cpython-39.pyc', 'virtualenv/create/via_global_ref/builtin/__pycache__/via_global_self_do.cpython-39.pyc', 'virtualenv/create/via_global_ref/builtin/__pycache__/__init__.cpython-39.pyc', 'virtualenv/create/via_global_ref/builtin/cpython/cpython2.py', 'virtualenv/create/via_global_ref/builtin/cpython/mac_os.py', 'virtualenv/create/via_global_ref/builtin/cpython/__init__.py', 'virtualenv/create/via_global_ref/builtin/cpython/common.py', 'virtualenv/create/via_global_ref/builtin/cpython/cpython3.py', 'virtualenv/create/via_global_ref/builtin/cpython/__pycache__/cpython3.cpython-39.pyc', 'virtualenv/create/via_global_ref/builtin/cpython/__pycache__/cpython2.cpython-39.pyc', 'virtualenv/create/via_global_ref/builtin/cpython/__pycache__/common.cpython-39.pyc', 'virtualenv/create/via_global_ref/builtin/cpython/__pycache__/__init__.cpython-39.pyc', 'virtualenv/create/via_global_ref/builtin/cpython/__pycache__/mac_os.cpython-39.pyc', 'virtualenv/create/via_global_ref/builtin/python2/site.py', 'virtualenv/create/via_global_ref/builtin/python2/__init__.py', 'virtualenv/create/via_global_ref/builtin/python2/python2.py', 'virtualenv/create/via_global_ref/builtin/python2/__pycache__/__init__.cpython-39.pyc', 'virtualenv/create/via_global_ref/builtin/python2/__pycache__/python2.cpython-39.pyc', 'virtualenv/create/via_global_ref/__pycache__/api.cpython-39.pyc', 'virtualenv/create/via_global_ref/__pycache__/venv.cpython-39.pyc', 'virtualenv/create/via_global_ref/__pycache__/__init__.cpython-39.pyc', 'virtualenv/create/via_global_ref/__pycache__/store.cpython-39.pyc', 'virtualenv/create/__pycache__/creator.cpython-39.pyc', 'virtualenv/create/__pycache__/describe.cpython-39.pyc', 'virtualenv/create/__pycache__/pyenv_cfg.cpython-39.pyc', 'virtualenv/create/__pycache__/__init__.cpython-39.pyc', 'virtualenv/config/env_var.py', 'virtualenv/config/convert.py', 'virtualenv/config/__init__.py', 'virtualenv/config/ini.py', 'virtualenv/config/cli/parser.py', 'virtualenv/config/cli/__init__.py', 'virtualenv/config/cli/__pycache__/__init__.cpython-39.pyc', 'virtualenv/config/cli/__pycache__/parser.cpython-39.pyc', 'virtualenv/config/__pycache__/env_var.cpython-39.pyc', 'virtualenv/config/__pycache__/__init__.cpython-39.pyc', 'virtualenv/config/__pycache__/convert.cpython-39.pyc', 'virtualenv/config/__pycache__/ini.cpython-39.pyc', 'virtualenv/run/__init__.py', 'virtualenv/run/session.py', 'virtualenv/run/plugin/discovery.py', 'virtualenv/run/plugin/activators.py', 'virtualenv/run/plugin/__init__.py', 'virtualenv/run/plugin/seeders.py', 'virtualenv/run/plugin/creators.py', 'virtualenv/run/plugin/base.py', 'virtualenv/run/plugin/__pycache__/base.cpython-39.pyc', 'virtualenv/run/plugin/__pycache__/__init__.cpython-39.pyc', 'virtualenv/run/plugin/__pycache__/activators.cpython-39.pyc', 'virtualenv/run/plugin/__pycache__/discovery.cpython-39.pyc', 'virtualenv/run/plugin/__pycache__/seeders.cpython-39.pyc', 'virtualenv/run/plugin/__pycache__/creators.cpython-39.pyc', 'virtualenv/run/__pycache__/__init__.cpython-39.pyc', 'virtualenv/run/__pycache__/session.cpython-39.pyc', 'virtualenv/app_data/via_tempdir.py', 'virtualenv/app_data/na.py', 'virtualenv/app_data/read_only.py', 'virtualenv/app_data/__init__.py', 'virtualenv/app_data/base.py', 'virtualenv/app_data/via_disk_folder.py', 'virtualenv/app_data/__pycache__/via_disk_folder.cpython-39.pyc', 'virtualenv/app_data/__pycache__/via_tempdir.cpython-39.pyc', 'virtualenv/app_data/__pycache__/base.cpython-39.pyc', 'virtualenv/app_data/__pycache__/__init__.cpython-39.pyc', 'virtualenv/app_data/__pycache__/read_only.cpython-39.pyc', 'virtualenv/app_data/__pycache__/na.cpython-39.pyc', 'virtualenv/discovery/py_info.py', 'virtualenv/discovery/py_spec.py', 'virtualenv/discovery/builtin.py', 'virtualenv/discovery/__init__.py', 'virtualenv/discovery/discover.py', 'virtualenv/discovery/cached_py_info.py', 'virtualenv/discovery/__pycache__/py_spec.cpython-39.pyc', 'virtualenv/discovery/__pycache__/builtin.cpython-39.pyc', 'virtualenv/discovery/__pycache__/discover.cpython-39.pyc', 'virtualenv/discovery/__pycache__/cached_py_info.cpython-39.pyc', 'virtualenv/discovery/__pycache__/__init__.cpython-39.pyc', 'virtualenv/discovery/__pycache__/py_info.cpython-39.pyc', 'virtualenv/discovery/windows/pep514.py', 'virtualenv/discovery/windows/__init__.py', 'virtualenv/__pycache__/__init__.cpython-39.pyc', 'virtualenv/__pycache__/report.cpython-39.pyc', 'virtualenv/__pycache__/info.cpython-39.pyc', 'virtualenv/__pycache__/version.cpython-39.pyc', 'virtualenv/activation/__init__.py', 'virtualenv/activation/via_template.py', 'virtualenv/activation/activator.py', 'virtualenv/activation/cshell/__init__.py', 'virtualenv/activation/cshell/activate.csh', 'virtualenv/activation/cshell/__pycache__/__init__.cpython-39.pyc', 'virtualenv/activation/fish/activate.fish', 'virtualenv/activation/fish/__init__.py', 'virtualenv/activation/fish/__pycache__/__init__.cpython-39.pyc', 'virtualenv/activation/batch/deactivate.bat', 'virtualenv/activation/batch/__init__.py', 'virtualenv/activation/batch/pydoc.bat', 'virtualenv/activation/batch/activate.bat', 'virtualenv/activation/batch/__pycache__/__init__.cpython-39.pyc', 'virtualenv/activation/nushell/deactivate.nu', 'virtualenv/activation/nushell/__init__.py', 'virtualenv/activation/nushell/activate.nu', 'virtualenv/activation/nushell/__pycache__/__init__.cpython-39.pyc', 'virtualenv/activation/python/__init__.py', 'virtualenv/activation/python/activate_this.py', 'virtualenv/activation/python/__pycache__/__init__.cpython-39.pyc', 'virtualenv/activation/__pycache__/via_template.cpython-39.pyc', 'virtualenv/activation/__pycache__/activator.cpython-39.pyc', 'virtualenv/activation/__pycache__/__init__.cpython-39.pyc', 'virtualenv/activation/bash/__init__.py', 'virtualenv/activation/bash/activate.sh', 'virtualenv/activation/bash/__pycache__/__init__.cpython-39.pyc', 'virtualenv/activation/powershell/__init__.py', 'virtualenv/activation/powershell/activate.ps1', 'virtualenv/activation/powershell/__pycache__/__init__.cpython-39.pyc', 'virtualenv/util/error.py', 'virtualenv/util/lock.py', 'virtualenv/util/__init__.py', 'virtualenv/util/zipapp.py', 'virtualenv/util/six.py', 'virtualenv/util/subprocess/__init__.py', 'virtualenv/util/subprocess/_win_subprocess.py', 'virtualenv/util/subprocess/__pycache__/__init__.cpython-39.pyc', 'virtualenv/util/path/_permission.py', 'virtualenv/util/path/_win.py', 'virtualenv/util/path/__init__.py', 'virtualenv/util/path/_sync.py', 'virtualenv/util/path/__pycache__/_permission.cpython-39.pyc', 'virtualenv/util/path/__pycache__/_sync.cpython-39.pyc', 'virtualenv/util/path/__pycache__/__init__.cpython-39.pyc', 'virtualenv/util/path/__pycache__/_win.cpython-39.pyc', 'virtualenv/util/path/_pathlib/via_os_path.py', 'virtualenv/util/path/_pathlib/__init__.py', 'virtualenv/util/path/_pathlib/__pycache__/__init__.cpython-39.pyc', 'virtualenv/util/__pycache__/zipapp.cpython-39.pyc', 'virtualenv/util/__pycache__/__init__.cpython-39.pyc', 'virtualenv/util/__pycache__/lock.cpython-39.pyc', 'virtualenv/util/__pycache__/six.cpython-39.pyc', 'virtualenv/util/__pycache__/error.cpython-39.pyc', 'colorama/win32.py', 'colorama/__init__.py', 'colorama/winterm.py', 'colorama/ansi.py', 'colorama/ansitowin32.py', 'colorama/initialise.py', 'virtualenv-20.8.1.dist-info/WHEEL', 'virtualenv-20.8.1.dist-info/top_level.txt', 'virtualenv-20.8.1.dist-info/METADATA', 'virtualenv-20.8.1.dist-info/zip-safe', 'virtualenv-20.8.1.dist-info/LICENSE', 'virtualenv-20.8.1.dist-info/RECORD', 'virtualenv-20.8.1.dist-info/INSTALLER', 'virtualenv-20.8.1.dist-info/REQUESTED', 'virtualenv-20.8.1.dist-info/entry_points.txt', 'importlib_metadata/_functools.py', 'importlib_metadata/_adapters.py', 'importlib_metadata/_collections.py', 'importlib_metadata/_meta.py', 'importlib_metadata/_compat.py', 'importlib_metadata/__init__.py', 'importlib_metadata/_itertools.py', 'importlib_metadata/_text.py', 'importlib_metadata/py.typed', 'importlib_metadata/__pycache__/_functools.cpython-39.pyc', 'importlib_metadata/__pycache__/_compat.cpython-39.pyc', 'importlib_metadata/__pycache__/_meta.cpython-39.pyc', 'importlib_metadata/__pycache__/_collections.cpython-39.pyc', 'importlib_metadata/__pycache__/__init__.cpython-39.pyc', 'importlib_metadata/__pycache__/_itertools.cpython-39.pyc', 'importlib_metadata/__pycache__/_text.cpython-39.pyc', 'importlib_metadata/__pycache__/_adapters.cpython-39.pyc']
        },
        install_requires = [],
        dependency_links = [],
        zip_safe = True,
        cmdclass = {'install': install},
        python_requires = '>=3.6',
        obsoletes = [],
    )
