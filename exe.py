#!/usr/bin/env python3
import argparse
import os
from MainGenerator import *
from CatalogDocGenerator import *

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("--file", "-f", help="Path to file.")
arg_parser.add_argument("--directory", "-d", help="Path to directory.")
arg_parser.add_argument("--project", "-p", help="Path to project.")
arg_parser.add_argument("--output", "-o", help="Path to output directory.")
arg_parser.add_argument('--version', action='version', version=ProjectInfo.version)
args = arg_parser.parse_args()

Generator.init_out_path = os.path.abspath(os.path.normpath(args.output))
if not os.path.exists(Generator.init_out_path):
    os.makedirs(Generator.init_out_path)
if os.path.exists(Generator.init_out_path + '/documentation.html'):
    os.remove(Generator.init_out_path + '/documentation.html')
basename = ""

if args.file is not None:
    basename = args.file
    DocumentGenerator(args.output, args.file)
elif args.directory is not None:
    basename = args.directory
    CatalogDocGenerator(args.output, args.directory, True)
elif args.project is not None:
    basename = args.project
    CatalogDocGenerator(args.output, args.project)
if basename.endswith('/'):
    basename = basename[:-1]
basename = os.path.basename(basename)

MainGenerator(basename)
os.rename(Generator.init_out_path + '/' + basename + ".html",
          Generator.init_out_path + '/documentation.html')
AlphabetGenerator()
