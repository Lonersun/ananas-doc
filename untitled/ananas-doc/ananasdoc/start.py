# -*- coding: utf-8 -*-
"""
ananas docs

"""
import os
from os import path
import sys
import conf
import makefile
import shutil
from utils import mkdir

package_dir = path.abspath(path.dirname(__file__))

try:
    # check if colorama is installed to support color on Windows
    import colorama
except ImportError:
    colorama = None

if False:
    # For type annotation
    from typing import Dict  # NOQA

codes = {}  # type: Dict[str, str]

def color_terminal():
    # type: () -> bool
    if sys.platform == 'win32' and colorama is not None:
        colorama.init()
        return True
    if not hasattr(sys.stdout, 'isatty'):
        return False
    if not sys.stdout.isatty():
        return False
    if 'COLORTERM' in os.environ:
        return True
    term = os.environ.get('TERM', 'dumb').lower()
    if term in ('xterm', 'linux') or 'color' in term:
        return True
    return False

def nocolor():
    # type: () -> None
    if sys.platform == 'win32' and colorama is not None:
        colorama.deinit()
    codes.clear()


def main(argv=sys.argv):
    if not color_terminal():
        nocolor()
    error = "MakeError:[%s]"

    # make project dir
    path = ""
    try:
        path = argv[1]
        if not path:
            print error % "Please enter the project name"
            exit()
    except:
        print error % "Please enter the project name"
        exit()
    is_exists = os.path.exists(path)
    if is_exists:
        print error % "The directory already exists, do not duplicate it"
        exit()
    mkdir(path)
    mkdir(path + "/docs")

    # set config
    conf_server = conf.Config(path=path)
    conf_server.config_dict['project'] = path
    conf_server.config_dict['copyright'] = '2017, ' + path
    conf_server.config_dict['author'] = path
    conf_server.mk_conf()

    # load init files
    now_dir = path + "/template"
    shutil.copytree(package_dir + '/template', str(now_dir))
    shutil.copyfile(package_dir + '/index.rst',path + '/index.rst')
    mkfile_server = makefile.MakeFile(path=path)
    mkfile_server.set_make_file()
    print "%s project created successfully!" % path



