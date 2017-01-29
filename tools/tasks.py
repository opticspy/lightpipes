from glob import glob

from invoke import task

PYTHON_PATH = '/opt/python/{}/bin/python'
PIP_PATH = '/opt/python/{}/bin/pip'
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
    python = PYTHON_PATH.format(version)
    pip = PIP_PATH.format(version)
    ctx.run(f'{pip} install cython numpy')
    # build wheel
    ctx.run(f'{pip} wheel /io/lightpipes -w /io/wheelhouse/')
    whl = find_whl(version)
    ctx.run(f'auditwheel repair {whl} -w /io/wheelhouse/')
    # install and test
    ctx.run(f'{pip} install lightpipes --no-index -f /io/wheelhouse')
    ctx.run(f'{python} -c "import LightPipes;LightPipes.Init().version()"')


def find_whl(version):
    whl = glob(f'/io/wheelhouse/*{version}*')
    if not whl:
        raise RuntimeError(f'.whl for {version} not build')
    return whl[0]


@task
def build_all(ctx):
    for version in SUPPORTED_CPYTHON:
        build(ctx, version)
