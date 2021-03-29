#!/usr/bin/env python
"""
fixes the arcade pyinstaller hook and builds a onefile executable in a cross platform way
"""
from os import chdir
from subprocess import check_call as call


call(['git', 'clone', 'https://github.com/pyinstaller/pyinstaller.git'])
call(['git', 'checkout', 'tags/v4.2'])
chdir('pyinstaller')
chdir('bootloader')
call(['python', 'waf', 'all'])

print('rebuilt pyinstaller bootloader')

chdir('..')
chdir('..')
call(['pip', 'install', '-e', 'pyinstaller'])

print('installed pyinstaller')

call(['pyinstaller', '--onefile', '--hidden-import', 'arcade', 'main.pyw'])

print('created dist')
print('done')
