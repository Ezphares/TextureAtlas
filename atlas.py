#!/usr/bin/env python

import sys
import os
import argparse

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
    parser.add_argument('-a', '--atlas', default='atlas.png', help='filename of the atlas file')
    parser.add_argument('-i', '--index', default='index.json', help='filename of the index file')
   
    args = parser.parse_args()
    print(args)
    rects = []
    
    # Load images
    for name in args.files:
        try:
            # TODO: Add correct filetype
            infile = open(name, 'rb')
            rects.append(PngRect(infile, name))
            infile.close()
        except:
            print('E: Could not open input file [%s] for reading' % name)
            exit(1)
    
    # Input and output
    packer = Packer(rects)
    res, area = packer.pack()
    PngAtlas(res).write(args.atlas, args.index)
        
            