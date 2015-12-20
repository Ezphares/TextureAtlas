#!/usr/bin/env python

import sys
import os
import argparse
import logging

from atlas.packer import *
from atlas.input import *
from atlas.output import *

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
            description = '''
            Packs several image file into a single atlas image, and provides 
            an index file mapping filenames to rectangles in the atlas\n''',
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    
    parser.add_argument('files', nargs='+', metavar="IMAGE", help='filenames of the images to pack')
    parser.add_argument('-a',  '--atlas', default='atlas', help='filename of the atlas file (without extension)')
    parser.add_argument('-i',  '--index', default='index', help='filename of the index file (without extension)')
    parser.add_argument('-it', '--indextype', default='json', choices=['json', 'css'],
                        help='type of index file')
    parser.add_argument('-v',  '--verbose', action='store_const',
                        default=False, const=True, help='display verbose progress info')
    
    args = parser.parse_args()
    
    # Set parent loglevel"
    logging.basicConfig(level = logging.INFO if args.verbose else logging.WARNING)
    
    rects = []
    
    # Load images
    for name in args.files:
        try:
            # TODO: Add correct filetype
            infile = open(name, 'rb')
            rects.append(PngRect(infile, name))
            infile.close()
        except:
            logging.exception('Could not open input file [%s] for reading' % name)
            exit(1)
    
    
    
    # Packing   
    packer = Packer(rects)
    res, area = packer.pack()
    
    # Atlas
    atlasfile = '%s.%s' % (args.atlas, 'png')
    PngAtlas(res).write(atlasfile)
    
    # Index
    indexfile = '%s.%s' % (args.index, args.indextype)
    indexclass = {
        'json': JsonIndexOutput,
        'css': CssIndexOutput
    }[args.indextype]

    indexclass(res, indexfile, atlasfile).write()
        