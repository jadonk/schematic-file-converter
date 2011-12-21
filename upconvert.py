#!/usr/bin/env python
""" A universal hardware design file format converter using 
Upverter's Open JSON Interchange Format """

# upconvert.py - A universal hardware design file format converter using
# Upverter's Open JSON Interchange Format
# (http://upverter.com/resources/open-json-format/)
#
# Authors:
#   Alex Ray ajray@ncsu.edu
#   Upverter support@upverter.com
#
# Usage example:
#   ./upconvert.py -i test.upv -o test.json 


import parser.openjson, parser.kicad, parser.eaglexml, parser.geda
import parser.fritzing
import writer.openjson, writer.kicad, writer.geda

from argparse import ArgumentParser

PARSERS = {
    'openjson': parser.openjson.JSON,
    'kicad': parser.kicad.KiCAD,
    'geda': parser.geda.GEDA,
    'eaglexml': parser.eaglexml.EagleXML,
    'fritzing': parser.fritzing.Fritzing,
}

WRITERS = {
    'openjson': writer.openjson.JSON,
    'kicad': writer.kicad.KiCAD,
    'geda': writer.geda.GEDA,
}


def parse(in_file, in_format='openjson', **parser_kwargs):
    """ Parse the given input file using the in_format """

    try:
        if in_format == 'geda':
            p = PARSERS[in_format](**parser_kwargs)
        else:
            p = PARSERS[in_format]()
    except KeyError:
        print "ERROR: Unsupported input type:", in_format
        exit(1)
    return p.parse(in_file)


def write(dsgn, out_file, out_format='openjson', **parser_kwargs):
    """ Write the converted input file to the out_format """

    try:
        if out_format == 'geda':
            w = WRITERS[out_format](**parser_kwargs)
        else:
            w = WRITERS[out_format]()
    except KeyError:
        print "ERROR: Unsupported output type:", out_format
        exit(1)
    return w.write(dsgn, out_file)


def print_help():
    """ Display program and parameter help """
    print "TODO: write help"


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-i", "--input", dest="inputfile",
            help="read INPUT file in", metavar="INPUT")
    parser.add_argument("-f", "--from", dest="inputtype",
            help="read input file as TYPE", metavar="TYPE",
            default="openjson")
    parser.add_argument("-o", "--output", dest="outputfile",
            help="write OUTPUT file out", metavar="OUTPUT")
    parser.add_argument("-s", "--sym-dirs", dest="sym_dirs",
            help="specify SYMDIRS to search for .sym files (for gEDA only)", 
            metavar="SYMDIRS", nargs="+")
    parser.add_argument("-t", "--to", dest="outputtype",
            help="write output file as TYPE", metavar="TYPE",
            default="openjson")

    args = parser.parse_args()
    inputtype = args.inputtype
    outputtype = args.outputtype
    inputfile = args.inputfile
    outputfile = args.outputfile

    parser_kwargs = {}
    if args.sym_dirs:
        parser_kwargs['symbol_dirs'] = args.sym_dirs

    if None == inputfile:
        print_help()
        exit(1)

    # parse and export the data
    design = parse(inputfile, inputtype, **parser_kwargs)
    if design is not None: # we got a good result
        write(design, outputfile, outputtype, **parser_kwargs)
    else: # parse returned None -> something went wrong
        print "Output cancelled due to previous errors."
        exit(1)
