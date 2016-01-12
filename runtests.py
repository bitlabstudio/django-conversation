#!/usr/bin/env python
"""
This script is a trick to setup a fake Django environment, since this reusable
app will be developed and tested outside any specific Django project.
Via ``settings.configure`` you will be able to set all necessary settings
for your app and run the tests as if you were calling ``./manage.py test``.
"""
import re

from fabric.api import abort, local
from fabric.colors import green, red


if __name__ == '__main__':
    local('flake8 --ignore=E126 --ignore=W391 --statistics'
          ' --exclude=submodules,migrations,build .')
    local('coverage run --source="conversation" manage.py test -v 2'
          ' --traceback --failfast --settings=conversation.tests.settings'
          ' --pattern="*_tests.py"')
    local('coverage html -d coverage'
          ' --omit="*__init__*,*/settings/*,*/migrations/*,*/tests/*,*admin*"')
    total_line = local('grep -n pc_cov coverage/index.html', capture=True)
    percentage = float(re.findall(r'(\d+)%', total_line)[-1])
    if percentage < 100:
        abort(red('Coverage is {0}%'.format(percentage)))
    print(green('Coverage is {0}%'.format(percentage)))
