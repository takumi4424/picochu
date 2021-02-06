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

import sys, os, argparse, importlib, re, types, traceback
from typing import Tuple, List, Dict, Callable

# the directory path where this script is located
here: str = os.path.dirname(__file__)
# subcommands are <here>/picoco_commands/picoco_<subcommand>.py
subcommands_dirname: str = 'picoco_commands'
subcommands_prefix: str = 'picoco_'
# $PICO_SDK_PATH
pico_sdk_path_env_name: str = 'PICO_SDK_PATH'
pico_sdk_path_env: str = os.getenv(pico_sdk_path_env_name)
# as a global variable in order to use the paraser.error function.
parser: argparse.ArgumentParser = None
def error_exit(parser: argparse.ArgumentParser, message: str, ex: Exception=None, with_help_me: bool=False):
    if with_help_me:
        message += ' Would you kindly report this issue? (https://github.com/takumi4424/picoco/issues)'
    if not parser:
        print('{}: error: {}'.format(os.path.basename(__file__), message))
        if ex:
            for line in traceback.TracebackException.from_exception(ex).format():
                print('{}{}'.format(' ' * 4, line), end='')
        exit(1)
    else:
        if ex:
            message += '\n'
            for line in traceback.TracebackException.from_exception(ex).format():
                message += '{}{}'.format(' ' * 4, line)
        parser.error(message)

def main() -> None:
    # parse argument and load subcommand
    subcommands = get_subcommands()
    subcmd_name, subparser, namesp, other_args = parse_args(subcommands=subcommands)

    # check sdk path
    if namesp.sdk_path:
        pass
    if pico_sdk_path_env:
        try:
            namesp.sdk_path = dir_path_type(pico_sdk_path_env)
        except:
            error_exit(parser, '${}: "{}": No such directory.'.format(pico_sdk_path_env_name, pico_sdk_path_env))
    else:
        error_exit(parser, 'Failed to load pico-sdk path. Use "--sdk-path" option or set "{}" environment variable.'.format(pico_sdk_path_env_name))

    # exec subcommand
    try:
        error_exit_callable = lambda message, ex=None, with_help_me=False: error_exit(subparser, message, ex, with_help_me)
        subcommands[subcmd_name].exec_subcommand(namesp, other_args, error_exit_callable)
    except Exception as ex:
        error_exit(subparser, 'subcommand error "{}".'.format(subcmd_name), ex, with_help_me=True)

def get_subcommands() -> Dict[str, types.ModuleType]:
    subcommands = {}
    subcmd_path = os.path.join(here, subcommands_dirname)
    for f in os.listdir(subcmd_path):
        # file?
        if not os.path.isfile(os.path.join(subcmd_path, f)): continue
        # picoco_*.py?
        mat = re.match('^{}(.+)\\.py$'.format(subcommands_prefix), f)
        if not mat: continue
        subcmd_name = mat.group(1)

        # import as module
        mod_name = '{}.{}'.format(subcommands_dirname, subcommands_prefix + subcmd_name)
        try:
            mod = importlib.import_module(mod_name)
        except Exception as ex:
            error_exit(None, 'Failed to load subcommand "{}".'.format(subcmd_name), ex, with_help_me=True)

        # has required functions?
        for func in ['exec_subcommand', 'add_argument']:
            if func in dir(mod) and callable(getattr(mod, func)): continue
            error_exit(None, 'Failed to load subcommand "{}": "{}" not found or not callable.'.format(subcmd_name, func), with_help_me=True)

        subcommands[subcmd_name] = mod
    return subcommands

def dir_path_type(path: str) -> str:
    if os.path.isdir(path):
        return path
    else:
        raise argparse.ArgumentTypeError('"{}": no such directory.'.format(path))

def parse_args(subcommands: Dict[str, types.ModuleType], args: List[str] = sys.argv[1:]) -> Tuple[types.ModuleType, argparse.Namespace, List[str]]:
    global parser
    parser = argparse.ArgumentParser(description=(
        'Build tool for Raspberry Pi Pico.\n'
        'This tool wraps cmake, make, ...'
    ))

    # add general options
    add = parser.add_argument
    add('--sdk-path', type=dir_path_type,
        help='The path to pico-sdk (default "$PICO_SDK_PATH")')

    # add options for each command
    subparsers = parser.add_subparsers(dest='subcmd')
    subparsers_dict = {}
    for subcmd_name, mod in subcommands.items():
        subparser = subparsers.add_parser(subcmd_name, help='see `{} --help`'.format(subcmd_name))
        try:
            mod.add_argument(subparser)
        except Exception as ex:
            error_exit(parser, 'Failed to prepare to parse argument for subcommand "{}".'.format(subcmd_name), ex, with_help_me=True)
        subparsers_dict[subcmd_name] = subparser

    # parse args
    namesp, other_args = parser.parse_known_args(args)
    # check given subcommand
    if 'subcmd' not in namesp:
        # maybe unreachable
        error_exit(parser, 'Empty subcommand.')
    if namesp.subcmd not in subcommands:
        # maybe unreachable
        error_exit(parser, '{}: Unknown subcommand.'.format(namesp.subcmd))

    # print(subparsers["build"])
    return (namesp.subcmd, subparsers_dict[namesp.subcmd], namesp, other_args)

if __name__ == '__main__':
    main()
