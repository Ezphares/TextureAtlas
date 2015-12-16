#!/usr/bin/env python

import sys
import os
from atlas.packer import *
from atlas.input import *
from atlas.output import *

if __name__ == '__main__':
    output = 'atlas.png'
    index = 'index.json'
    write = None
    filenames = []
    for arg in sys.argv[1:]:
        if arg == '-o':
            write = 'o'
        if arg == '-i':
            write = 'i'
        else:
            if write == 'o':
                output = arg
            elif write == 'i':
                index = arg
            else:
                filenames.append(arg)
            write = None
                
    if len(filenames) == 0:
        print('E: No input file(s) given')
        exit(1)

    rects = []
        
    for name in filenames:
        try:
            # TODO: Add correct filetype
            infile = open(name, 'rb')
            rects.append(PngRect(infile, name))
            infile.close()
        except:
            print('E: Could not open input file [%s] for reading' % name)
            exit(1)
            
    packer = Packer(rects)
    res, area = packer.pack()
    PngAtlas(res).write(output, index)
        
            