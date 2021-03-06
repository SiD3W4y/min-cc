#!/usr/bin/env python
import argparse
import logging

from min.assembly.Compiler import Compiler

if __name__ == "__main__":
    log_format = "[%(levelname)s : %(module)s] %(message)s"

    parser = argparse.ArgumentParser(description="Assembler/compiler for min assembly language")

    parser.add_argument("-d","--debug",action="store_true",dest="debug_flag",help="enables debugging information")
    parser.add_argument("-i","--input",action="store",dest="input_file",help="set input file")
    parser.add_argument("-o","--output",action="store",dest="output_file",help="set output file (default -> a.mx)")


    args = parser.parse_args()

    if args.debug_flag == True:
        logging.basicConfig(format=log_format,level=logging.DEBUG)
    else:
        logging.basicConfig(format=log_format,level=logging.INFO)

    if args.output_file == None:
        args.output_file = "a.mx"
    
    if args.input_file != None:
        logging.info("Compiling {}".format(args.input_file))

        cc = Compiler()
        cc.fromFile(args.input_file,args.output_file)
    else:
        logging.error("No input file specified")
