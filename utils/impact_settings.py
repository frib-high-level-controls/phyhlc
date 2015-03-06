# encoding: UTF-8

"""
Implement phylib command 'impact-settings'.
"""

from __future__ import print_function

import sys, json

from argparse import ArgumentParser

from phylib import cfg

from machine.frib import layout, lattice


parser = ArgumentParser(description="Generate settings file from IMPACT input file.")
parser.add_argument("--xlf", dest="xlfpath", required=True)
parser.add_argument("--cfg", dest="cfgpath", required=True)
parser.add_argument("--start")
parser.add_argument("--end")
parser.add_argument("--mach")
parser.add_argument("latpath")
parser.add_argument("setpath")


help = parser.print_help


def main():
    """
    Entry point for command 'impact-settings'.
    """
    args = parser.parse_args(sys.argv[2:])


    try:
        with open(args.cfgpath, "r") as fp:
            config = cfg.Configuration()
            config.readfp(fp)
    except Exception as e:
        print(e, file=sys.stderr)
        return 1

    if args.mach != None:
        prefix = args.mach+":"
    else:
        prefix = ""

    try:
        accel = layout.fribxlf.build_accel(args.xlfpath, config, prefix=prefix)
    except Exception as e:
        print(e, file=sys.stderr)
        return 1


    settings = lattice.impact.build_settings(accel, args.latpath, start=args.start, end=args.end)

    with open(args.setpath, "w") as fp:
        json.dump(settings, fp, indent=2)
    
    return 0
