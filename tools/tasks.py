from glob import glob

from invoke import task

PYTHON_PATH = '/opt/python/{}/bin/python'
PIP_PATH = '/opt/python/{}/bin/pip'
DIST_DIR = '/io/wheelhouse'
TMP_DIR = '/io/wheelhouse/tmp'
SUPPORTED_CPYTHON = [
    'cp27-cp27m', 'cp27-cp27mu',
    'cp34-cp34m',
    'cp35-cp35m',
    'cp36-cp36m',
]


@task
def build(ctx, version):
    """
    Build wheel

    Args:
        version: one of supported cpython
    """
    ctx.run(f'rm -rf {TMP_DIR}')
    python = PYTHON_PATH.format(version)
    pip = PIP_PATH.format(version)
    ctx.run(f'{pip} install -r requires.txt')
    # build wheel
    ctx.run(f'{pip} wheel /io/lightpipes --no-deps -w {TMP_DIR}')
    whl = find_whl(version)
    ctx.run(f'auditwheel repair {whl} -w {DIST_DIR}')
    # install and test
    ctx.run(f'{pip} install lightpipes --no-index -f {DIST_DIR}')
    ctx.run(f'{python} -c "import LightPipes;LightPipes.Init().version()"')
    ctx.run(f'rm -rf {TMP_DIR}')


def find_whl(version):
    whl = glob(f'{TMP_DIR}/*{version}*')
    if not whl:
        raise RuntimeError(f'.whl for {version} not build')
    return whl[0]


@task
def build_all(ctx):
    for version in SUPPORTED_CPYTHON:
        build(ctx, version)
