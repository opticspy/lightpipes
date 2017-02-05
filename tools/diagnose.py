# coding:utf-8
"""print your platform information and package information"""
import platform


def pkginfo():
    for pkg in ['setuptools', 'pip', 'wheel', 'virtualenv',
                'distutils', 'cython', 'numpy']:
        try:
            version = getattr(__import__(pkg), '__version__', 'Unknown')
            print('{} = {}'.format(pkg, version))
        except:
            print('{} Not Found'.format(pkg))


def platforminfo():
    keys = [
        'architecture', 'dist', 'java_ver', 'libc_ver',
        'linux_distribution', 'mac_ver', 'machine', 'node',
        'platform', 'processor', 'python_branch', 'python_build',
        'python_compiler', 'python_implementation', 'python_revision',
        'python_version', 'python_version_tuple', 'release',
        'system', 'system_alias', 'version', 'win32_ver'
    ]
    for k in keys:
        try:
            v = getattr(platform, k, None)
            if callable(v):
                v = v()
        except:
            v = ''
        print('{} = {}'.format(k, v))


if __name__ == '__main__':
    print('platform information'.center(60, '-'))
    platforminfo()
    print('package information'.center(60, '-'))
    pkginfo()
