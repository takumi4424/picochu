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

import argparse, os, subprocess, shutil, sys
from typing import List, Callable

def exec_subcommand(namesp: argparse.Namespace, other_args: List[str], error_exit: Callable[[str, Exception, bool], None]) -> None:
    ws_dir    = namesp.directory if namesp.directory else os.curdir
    src_dir   = namesp.source    if namesp.source    else os.path.join(ws_dir, 'src')
    build_dir = namesp.build     if namesp.build     else os.path.join(ws_dir, 'build')

    # check workspace
    # currently workspace requires:
    #   - CMakeLists.txt
    #   - src/
    if not os.path.isfile(os.path.join(ws_dir, 'CMakeLists.txt')):
        error_exit('The specified workspace "{}" has no "CMakeLists.txt" file.'.format(os.path.abspath(ws_dir)))
    elif not os.path.isdir(src_dir):
        error_exit('The specified workspace "{}" has no "src" directory.'.format(os.path.abspath(ws_dir)))

    # prepare for build
    # currently preparetions are:
    #   - create 'build' directory
    if not os.path.isdir(build_dir):
        os.mkdir(build_dir)

    # cmake/make arguments
    cmake_args = []
    cmake_args += namesp.cmake_args
    cmake_args += other_args
    cmake_args += ['-S', os.path.abspath(ws_dir)]
    make_args = []
    make_args += namesp.make_args
    # setup environment variable
    env = os.environ.copy()
    env['PICO_SDK_PATH'] = namesp.sdk_path

    sep = '~' * shutil.get_terminal_size().columns
    print(sep)
    print('Paths:')
    print('  workspace:  {}'.format(ws_dir))
    print('  build dir:  {}'.format(build_dir))
    print('  source dir: {}'.format(src_dir))
    print('  pico-sdk:   {}'.format(namesp.sdk_path))
    print('Build arguments:')
    print('  cmake: {}'.format(cmake_args))
    print('  make:  {}'.format(make_args))
    print(sep)

    # cmake
    result: subprocess.CompletedProcess = None
    try:
        result = subprocess.run(['cmake'] + cmake_args, cwd=build_dir, env=env)
    except FileNotFoundError:
        error_exit('The "cmake" command not found. Install it on your system first.')
    if result.returncode:
        sys.exit(result.returncode)

    # make
    try:
        result = subprocess.run(['make'] + make_args, cwd=build_dir, env=env)
    except FileNotFoundError:
        error_exit('The "make" command not found. Install it on your system first.')
    if result.returncode:
        sys.exit(result.returncode)

    if namesp.show_uf2:
        uf2files = []
        for parent, _, files in os.walk(build_dir):
            for f in files:
                if f.endswith('.uf2'):
                    uf2files.append(os.path.join(parent, f))
        print(sep)
        if len(uf2files) == 0:
            print('.uf2 file not found.')
        else:
            print('.uf2 files:')
            for f in uf2files:
                print('  - {}'.format(f))
        print(sep)

def dir_path_type(path: str) -> str:
    if os.path.isdir(path):
        return path
    else:
        raise argparse.ArgumentTypeError("'{}': no such directory.".format(path))

def add_argument(parser: argparse.ArgumentParser) -> None:
    add = parser.add_argument
    add('-s', '--show-uf2', action='store_true',
        help='')
    add('-C', '--directory', type=dir_path_type,
        help='The base path of the workspace (default: current directory)')
    add('--source', type=dir_path_type,
        help="The path to the source space (default: '<workspace>/src')")
    add('--build', type=dir_path_type,
        help="The path to the build space (default: '<workspace>/build')")
    add('--cmake-args', dest='cmake_args', nargs='*', type=str, default=[],
        help='Arbitrary arguments which are passed to CMake. '
             'It must be passed after other arguments since it collects all following options.')
    add('--make-args', dest='make_args', nargs='*', type=str, default=[],
        help='Arbitrary arguments which are passes to make. '
             'It must be passed after other arguments since it collects all following options. '
             'This is only necessary in combination with --cmake-args since else all unknown '
             'arguments are passed to make anyway.')
