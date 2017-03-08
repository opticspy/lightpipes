# coding:utf-8
import os
import sys
import traceback
from getpass import getuser
from os.path import abspath, dirname, exists, join

from invoke import task
from invoke.platform import WINDOWS

CONDA_32 = r'C:\Users\{}\Miniconda32\Scripts\conda.exe'.format(getuser())
CONDA_64 = r'C:\Users\{}\Miniconda64\Scripts\conda.exe'.format(getuser())

SHELL = r'C:\Windows\system32\cmd.exe'
if WINDOWS:
    os.environ['INVOKE_RUN_SHELL'] = SHELL

PROJECT = abspath(join(dirname(__file__), '..', '..'))


def project_path(*path):
    return join(PROJECT, *path)


def conda_path(bit):
    if bit == '32':
        return CONDA_32
    elif bit == '64':
        return CONDA_64
    else:
        raise ValueError(
            "unknown bit '{}', please choose one of {}"
            .format(bit, SUPPORTED_BIT)
        )


DIST = project_path('wheelhouse')
SOURCE = project_path('.')
REQUIRES = project_path('tools', 'requires.txt')
CACHE = project_path('.cache', 'pip')
DIAGNOSE = project_path('tools', 'diagnose.py')

SUPPORTED_BIT = ['32','64']
SUPPORTED_CPYTHON = [
    '27',
#    '34',
    '35',
    '36',
]


class Builder:

    def __init__(self, ctx, bit, version, index_url=None):
        if version not in SUPPORTED_CPYTHON:
            raise ValueError(
                "unknown version '{}', please choose one of {}"
                .format(version, SUPPORTED_CPYTHON)
            )
        self.run = ctx.run
        self.bit = bit
        self.version = version
        self.index_url = index_url
        self.conda = conda_path(bit)
        self.dot_version = version[0] + '.' + version[1]
        self.name = 'py{} {}bit'.format(version, bit)
        self.python_dir = project_path(
            'tools', 'windows', 'envs', bit+'bit', 'py'+version)
        self.python = join(self.python_dir, 'python.exe')
        self.pip = join(self.python_dir, 'Scripts', 'pip.exe')

    def conda_create(self):
        CREATE = '{conda} create -y -p {python_dir} python={dot_version}'
        self.run(CREATE.format(
            conda=self.conda,
            python_dir=self.python_dir,
            dot_version=self.dot_version
        ))

    def pip_install(self):
        INSTALL = r'{pip} install -r {requires} --cache-dir={cache}'
        if self.index_url:
            INSTALL = INSTALL + " -i " + self.index_url
        self.run(INSTALL.format(
            pip=self.pip,
            requires=REQUIRES,
            cache=CACHE
        ))

    def pip_wheel(self):
        self.run(r'{pip} wheel --no-deps -w {dist} {source}'.format(
            pip=self.pip,
            dist=DIST,
            source=SOURCE
        ))

    def diagnose(self):
        self.run(r'{python} {diagnose}'.format(
            python=self.python,
            diagnose=DIAGNOSE
        ))

    def test(self):
        INSTALL = '{pip} install lightpipes --upgrade --force-reinstall --no-index -f {dist}'
        if self.index_url:
            INSTALL = INSTALL + " -i " + self.index_url
        self.run(INSTALL.format(pip=self.pip, dist=DIST))
        TEST = '{python} -c "from LightPipes import *;LPtest()"'
        self.run(TEST.format(python=self.python))

    def build(self):
        print('build for {}'.format(self.name).center(60, '-'))
        if exists(self.python_dir):
            print('{} already exists, skip creating'.format(self.python_dir))
        else:
            self.conda_create()
        self.pip_install()
        self.diagnose()
        self.pip_wheel()
        self.test()


@task
def build(ctx,  bit, version, index_url=None):
    Builder(ctx, bit, version, index_url=index_url).build()


@task
def build_all(ctx, index_url=None):
    result = []
    for bit in SUPPORTED_BIT:
        for version in SUPPORTED_CPYTHON:
            builder = Builder(ctx, bit, version, index_url=index_url)
            try:
                builder.build()
                result.append((builder.name, True))
            except:
                result.append((builder.name, False))
                traceback.print_exc()
    print('-'*60)
    for name, ok in result:
        status = 'OK' if ok else 'Failed'
        print('{}  {}'.format(name, status))
    all_ok = all(x[1] for x in result)
    if not all_ok:
        sys.exit(1)
