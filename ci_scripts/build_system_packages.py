#!/usr/bin/env python

import os
import sys
import traceback
if sys.version_info.major < 3:
    import ci_tools as tools
else:
    import ci_tools as tools


def install_vdist():
    print("Installing vdist package from Pypi...")
    tools.run_console_command("pip install vdist")
    print("vdist installed.")


def build_packages():
    print("About to run building command from {0}".format(os.getcwd()))
    print("Building system packages...")
    tools.run_console_command("vdist batch packaging/cifra_build.cnf")
    print("System packages built.")


if __name__ == '__main__':
    try:
        print("This job is going to build cifra system packages.")
        install_vdist()
        build_packages()
    except:
        traceback.print_exc(file=sys.stdout)
        sys.exit(1)
    else:
        sys.exit(0)