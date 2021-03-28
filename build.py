#!//usr/bin/env python
"""
fixes the arcade pyinstaller hook and builds a onefile executable in a cross platform way
"""
from os import chdir, mkdir
import pkgutil
from pathlib import Path
from subprocess import check_call as call

arcade_path = pkgutil.find_loader('arcade').path

hook_path = Path(arcade_path).parent / '__pyinstaller' / 'hook-arcade.py'
assert hook_path.exists()

# the arcade hook is incorrectly setup to include chipmunk.dll/.so which doesn't exist
with hook_path.open('a') as f:
    f.write('\nbinaries = []\n')

print('updated arcade pyinstaller hook')


call(['git', 'clone', 'https://github.com/pyinstaller/pyinstaller.git'])
chdir('pyinstaller')
chdir('bootloader')
call(['python', 'waf', 'all'])

print('rebuilt pyinstaller bootloader')

chdir('..')
chdir('..')
call(['pip', 'install', '-e', 'pyinstaller'])

print('installed pyinstaller')

call(['pyinstaller', '--onefile', 'main.pyw'])

print('created dist/main.exe')
print('done')
