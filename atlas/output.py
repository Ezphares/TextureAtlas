#!/usr/bin/env python

import png, json, logging

class PngAtlas(object):
    def __init__(self, rectangles):
        self.rectangles = rectangles
        
    def get_size(self):
        width = 0
        height = 0
        for rectangle in self.rectangles:
            width = max(width, rectangle.right)
            height = max(height, rectangle.bottom)
            
        return (width, height)
        
    def get_data(self, x, y):
        for rectangle in self.rectangles:
            data = rectangle.get_data(x, y)
            if data is not None:
                return data
                
        return [0, 0, 0, 0]
        
    def write(self, atlasname, indexname):
        outfile = None
        indexfile = None
        
        try:
            outfile = open(atlasname, 'wb')
        except:
            logging.exception('Could not open output file for writing')
            exit(1)
            
        try:
            indexfile = open(indexname, 'wb')
        except:
            logging.exception('Could not open index file for writing')
            exit(1)
            
        outdata = []
        size = self.get_size()
        for y in range(size[1]):
            outdata.append([])
            for x in range(size[0]):
                outdata[y].extend(self.get_data(x, y))
                
        writer = png.Writer(*size, alpha = True)
        writer.write(outfile, outdata);
        outfile.close()
        
        index = {}
        for rectangle in self.rectangles:
            title = rectangle.get_title().replace('\\', '/')
            if title in index:
                logging.warning('Attempted to index two rectangles with the same title: "%s" (one will be missing from index)' % title)
                continue
                
            index[title] = {'x': rectangle.left,
                            'y': rectangle.top,
                            'w': rectangle.size[0],
                            'h': rectangle.size[1],
                            'a': atlasname}
        
        logging.info('Writing atlas file with dimensions %ix%i' % size)
        indexfile.write(bytes(json.dumps(index), 'UTF-8'))
        indexfile.close()
        
        