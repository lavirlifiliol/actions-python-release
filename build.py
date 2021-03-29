#!/usr/bin/env python
"""
fixes the arcade pyinstaller hook and builds a onefile executable in a cross platform way
"""
from os import chdir
from subprocess import check_call as call

call(['git', 'clone', 'https://github.com/pyinstaller/pyinstaller.git'])
chdir('pyinstaller')
call(['git', 'checkout', 'tags/v4.2'])
chdir('bootloader')
call(['python3.9', 'waf', 'all'])

print('rebuilt pyinstaller bootloader')

chdir('..')
chdir('..')
call(['python3.9', '-m', 'pip', 'install', '-e', 'pyinstaller'])

print('installed pyinstaller')

call(['python3.9', '-m', 'PyInstaller', '--onefile', 'main.pyw'])

print('created dist')
print('done')
