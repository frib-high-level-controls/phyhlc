# encoding: UTF-8

"""
Implement phytool command 'frib-channels'. 

Prepare FRIB channel names from accelerator layout.

:author: Dylan Maxwell <maxwelld@frib.msu.edu>
:date: 2015-06-15
"""

from __future__ import print_function

import sys, os.path, logging, traceback

from argparse import ArgumentParser

from ..phylib.layout import build_layout

from ..phylib.common.csv_utils import write_csv

from ..phylib.chanfinder import importCfLocalData

from phyutil.machine.frib.channels import build_channels



parser = ArgumentParser(prog=os.path.basename(sys.argv[0])+" frib-channels",
                        description="Generate FRIB channel names from accelerator layout.")
parser.add_argument("-v", dest="verbosity", nargs='?', type=int, const=1, default=0, help="set the amount of output")
#parser.add_argument("--start", help="name of accelerator element to start processing")
#parser.add_argument("--end", help="name of accelerator element to end processing")
parser.add_argument("--tag", action="append", help="additional tag (can be used multiple times)")
parser.add_argument("--machine", help="name of machine (used to indicate VA)")
parser.add_argument("layoutPath", help="path to accelerator layout file")
parser.add_argument("channelsPath", help="path to output data file (csv or sqlite)")

print_help = parser.print_help


def main():
    """
    Entry point for command 'frib-channels'.
    """
    args = parser.parse_args(sys.argv[2:])

    if args.verbosity == 1:
        logging.getLogger().setLevel(logging.INFO)
    elif args.verbosity > 1:
        logging.getLogger().setLevel(logging.DEBUG)


    if not os.path.isfile(args.layoutPath):
        print("Accelerator layout file not found: {}".format(args.layoutPath), file=sys.stderr)
        return 1


    if (args.channelsPath is not None) and os.path.exists(args.channelsPath):
        print("Channels output file already exists: {}".format(args.channelsPath), file=sys.stderr)
        return 1

    try:
        layout = build_layout(layoutPath=args.layoutPath)
    except Exception as e:
        if args.verbosity > 0: traceback.print_exc()
        print("Error reading accelerator layout:", e, file=sys.stderr)
        return 1

    try:
        channels = build_channels(layout, machine=args.machine)
    except Exception as e:
        if args.verbosity > 0: traceback.print_exc()
        print("Error building channels:", e, file=sys.stderr)
        return 1

    # Append tags specified on the command-line.
    if args.tag is not None:
        for _, _, tags in channels:
            tags.extend(args.tag)

    _, ext = os.path.splitext(args.channelsPath)
    if ext == ".csv":
        try:
            write_csv(channels, args.channelsPath)
        except Exception as e:
            if args.verbosity > 0: traceback.print_exc()
            print("Error writing channels csv file:", e, file=sys.stderr)
            return 1

    elif ext == ".sqlite":
        try:
            importCfLocalData(channels, args.channelsPath, overwrite=True)
        except Exception as e:
            if args.verbosity > 0: traceback.print_exc()
            print("Error writing channels sqlite file:", e, file=sys.stderr)
            return 1

    else:
        print("Error writing channels file: unsupported format '{}'".format(ext), file=sys.stderr)
        return 1

    return 0

