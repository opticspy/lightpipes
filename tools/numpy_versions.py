# coding:utf-8
"""
Analyze numpy versions

Result:
    - 1.8.1 is the first version support macosx wheels, it support python 27-34
    - 1.10.4 is the first version support windows wheels , it support python 27-35
    - 1.11.3 is the first version support all platforms wheels, it support python 27-36
"""
import re
from pprint import pprint

import requests

RE_VERSION = re.compile(r'1\.\d+\.\d+.*cp(\d{2}).*(linux|macosx|win).*\.whl')
data = requests.get('https://pypi.python.org/pypi/numpy/json/').json()
releases = data['releases']

result = {}
for version in releases:
    result[version] = []
    for item in releases[version]:
        if item['packagetype'] == 'bdist_wheel':
            info = RE_VERSION.findall(item['filename'])[0]
            result[version].append(info)

pprint(result)
