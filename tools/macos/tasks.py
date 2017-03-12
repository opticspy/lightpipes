# coding:utf-8
import os
import sys
import traceback
from getpass import getuser
from glob import glob
from os.path import abspath, dirname, exists, join

from invoke import task
from invoke.exceptions import UnexpectedExit

os.environ['INVOKE_RUN_ECHO'] = '1'
CONDA = '/Users/{user}/miniconda3/bin/conda'.format(user=getuser())
PROJECT = abspath(join(dirname(__file__), '..', '..'))

def project_path(*path):
    return join(PROJECT, *path)


DIST = project_path('wheelhouse')
SOURCE = project_path()
REQUIRES = project_path('tools', 'requires.txt')
CACHE = project_path('.cache', 'pip')
DIAGNOSE = project_path('tools', 'diagnose.py')

SUPPORTED_CPYTHON = [
    '27',
    '34',
    '35',
    '36',
]


def find_whl(version):
    whl = glob('{dist}/*{version}*macosx*'.format(dist=DIST, version=version))
    if not whl:
        raise RuntimeError(f'.whl for {version} not build')
    return whl[0]


@task
def check_before_build(ctx):
    if not exists(CONDA):
        raise RuntimeError(
            "'Miniconda3' is required for build wheels, "
            "but it not exists in '{conda}', "
            "see https://conda.io/miniconda.html for installation.".format(conda=CONDA)
        )
    try:
        ctx.run('which delocate-wheel')
    except UnexpectedExit:
        raise RuntimeError(
            "'delocate' is required for build wheels, "
            "try install it via `pip install delocate`, "
            "see also https://github.com/matthew-brett/delocate."
        ) from None


class Builder:

    def __init__(self, ctx, version, index_url=None):
        if version not in SUPPORTED_CPYTHON:
            raise ValueError(
                "unknown version '{}', please choose one of {}"
                .format(version, SUPPORTED_CPYTHON)
            )
        self.run = ctx.run
        self.version = version
        self.index_url = index_url
        self.dot_version = version[0] + '.' + version[1]
        self.name = 'py'+version
        self.python_dir = project_path('tools', 'macosx', 'envs', 'py'+version)
        self.python = join(self.python_dir, 'bin', 'python')
        self.pip = join(self.python_dir, 'bin', 'pip')

    def conda_create(self):
        CREATE = '{conda} create -y -p {python_dir} python={dot_version}'
        self.run(CREATE.format(
            conda=CONDA,
            python_dir=self.python_dir,
            dot_version=self.dot_version
        ))

    def pip_install(self):
        INSTALL = '{pip} install -r {requires} --cache-dir={cache}'
        if self.index_url:
            INSTALL = INSTALL + " -i " + self.index_url
        self.run(INSTALL.format(
            pip=self.pip,
            requires=REQUIRES,
            cache=CACHE
        ))

    def pip_wheel(self):
        self.run('{pip} wheel --no-deps -w {dist} {source}'.format(
            pip=self.pip,
            dist=DIST,
            source=SOURCE
        ))

    def diagnose(self):
        self.run('{python} {diagnose}'.format(
            python=self.python,
            diagnose=DIAGNOSE
        ))

    def fix_wheel(self):
        self.run('delocate-wheel -v -w {dist} {whl}'.format(
            dist=DIST,
            whl=find_whl(self.version)
        ))

    def test(self):
        INSTALL = '{pip} install lightpipes --no-index -f {dist}'
        if self.index_url:
            INSTALL = INSTALL + " -i " + self.index_url
        self.run(INSTALL.format(pip=self.pip, dist=DIST))
        #TEST = '{python} -c "import LightPipes;LightPipes.Init().version()"'
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
        self.fix_wheel()
        self.test()


@task(pre=[check_before_build])
def build(ctx, version, index_url=None):
    Builder(ctx, version, index_url=index_url).build()


@task(pre=[check_before_build])
def build_all(ctx, index_url=None):
    result = []
    for version in SUPPORTED_CPYTHON:
        builder = Builder(ctx, version, index_url=index_url)
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
