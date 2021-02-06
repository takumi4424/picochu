"""
MIT License

Copyright (c) 2021 Takumi Kodama

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import argparse, os, shutil
from typing import List, Callable, Dict

skelton_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'picoco_pkg_skelton'))

def replace_all(original: str, rep_table: Dict[str, str]) -> str:
    replaced = original
    for key, value in rep_table.items():
        replaced = replaced.replace('@{{{}}}'.format(key), value)
    return None if replaced == original else replaced

def exec_subcommand(namesp: argparse.Namespace, other_args: List[str], error_exit: Callable[[str, Exception, bool], None]) -> None:
    # check args (requires only package name)
    if len(other_args) == 0:
        error_exit('Requires package name.')
    elif len(other_args) > 1:
        error_exit('Only one package name should be given as an argument.')

    pkg_path = other_args[0]
    pkg_parent, pkg_name = os.path.split(pkg_path)
    # check whether the argument is valid or not
    if not pkg_name:
        error_exit('Package name must not be empty.')
    elif os.path.isdir(pkg_path):
        error_exit('"{}": The directort already exists.'.format(pkg_path))
    elif not namesp.parents and pkg_parent and not os.path.isdir(pkg_parent):
        error_exit('"{}": The parent directory does not exist. Consider to use "-p" option.'.format(pkg_parent))

    # is there a template package?
    if not os.path.isdir(skelton_path):
        error_exit('"{}": The skelton package directory not found.'.format(skelton_path), with_help_me=True)

    # string replacement table
    # replaces the directory name, file name, and contents of files
    rep_table = {
        'PACKAGE_NAME': pkg_name
    }

    copied = None
    try:
        # copy template
        shutil.copytree(skelton_path, pkg_path)
        # rename directory
        for parent, dirs, _ in os.walk(pkg_path):
            for d in dirs:
                new_d = replace_all(d, rep_table)
                if not new_d: continue
                os.rename(os.path.join(parent, d), os.path.join(parent, new_d))
        # rename file
        for parent, _, files in os.walk(pkg_path):
            for f in files:
                new_f = replace_all(f, rep_table)
                if not new_f: continue
                os.rename(os.path.join(parent, f), os.path.join(parent, new_f))
        # replace contents of files
        for parent, _, files in os.walk(pkg_path):
            for f in files:
                with open(os.path.join(parent, f), mode='r') as ff:
                    src = ff.read()
                dst = replace_all(src, rep_table)
                if not dst: continue
                with open(os.path.join(parent, f), mode='w') as ff:
                    ff.write(dst)
    except Exception as ex:
        msg = '' if not copied else ' (the directory "{}" was supposed to have been created.)'.format(copied)
        error_exit('"{}": Failed to create package.{}'.format(pkg_path, msg), ex)

    sep = '~' * shutil.get_terminal_size().columns
    print(sep)
    print('A new package has been created:')
    print('    package name: {}'.format(pkg_name))
    print('    parent path:  {}'.format(os.path.abspath(pkg_parent)))
    print('Now you can build your code by running:')
    print('    $ cd {}'.format(pkg_path))
    print('    $ picoco build')
    print(sep)

def dir_path_type(path: str) -> str:
    if os.path.isdir(path):
        return path
    else:
        raise argparse.ArgumentTypeError('"{}": no such directory.'.format(path))

def add_argument(parser: argparse.ArgumentParser) -> None:
    add = parser.add_argument
    add('-p', '--parents', action='store_true',
        help='Make parent directories as needed')
    add('--skelton', type=dir_path_type, default=skelton_path,
        help='The template directory path of the new package to be created.'
             '(Default: "{}")'.format(skelton_path))
