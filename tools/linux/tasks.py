import os
import shutil
import sys
import traceback
from glob import glob

from invoke import task

TARGET = os.getenv('TARGET', 'tmp')
PYTHON_PATH = '/opt/python/{}/bin/python'
PIP_CACHE = '/io/.cache/pip'
PIP_PATH = '/opt/python/{}/bin/pip --cache-dir=' + PIP_CACHE
DIST_DIR = '/io/wheelhouse'
TMP_DIR = '/io/wheelhouse/' + TARGET
SUPPORTED_CPYTHON = [
    'cp27-cp27m', 'cp27-cp27mu',
    'cp34-cp34m',
    'cp35-cp35m',
    'cp36-cp36m',
]


@task
def setup(ctx):
    try:
        os.makedirs(PIP_CACHE)
    except OSError as e:
        print(f'Create {PIP_CACHE}: {e}')
    # fix: The directory '/io/.cache/pip/http' or its parent directory
    # is not owned by the current user and the cache has been disabled.
    ctx.run(f'chown -R root {PIP_CACHE}')


def clean_tmpdir():
    shutil.rmtree(TMP_DIR, ignore_errors=True)


@task(pre=[setup])
def build(ctx, version):
    """
    Build wheel

    Args:
        version: one of supported cpython
    """
    print('build for {}'.format(version).center(60, '-'))
    clean_tmpdir()
    python = PYTHON_PATH.format(version)
    pip = PIP_PATH.format(version)
    ctx.run(f'{pip} install -r ../requires.txt')
    # build wheel
    ctx.run(f'{pip} wheel /io --no-deps -w {TMP_DIR}')
    whl = find_whl(version)
    ctx.run(f'auditwheel repair {whl} -w {DIST_DIR}')
    # install and test
    ctx.run(f'{pip} install lightpipes --no-index -f {DIST_DIR}')
    ctx.run(f'{python} -c "import LightPipes;LightPipes.Init().version()"')
    clean_tmpdir()


def find_whl(version):
    whl = glob(f'{TMP_DIR}/*{version}*linux*')
    if not whl:
        raise RuntimeError(f'.whl for {version} not build')
    return whl[0]


@task(pre=[setup])
def build_all(ctx):
    result = []
    for version in SUPPORTED_CPYTHON:
        try:
            build(ctx, version)
            result.append((version, True))
        except:
            result.append((version, False))
            traceback.print_exc()
    print('-'*60)
    for name, ok in result:
        status = 'OK' if ok else 'Failed'
        print('{}  {}'.format(name, status))
    all_ok = all(x[1] for x in result)
    if not all_ok:
        sys.exit(1)
