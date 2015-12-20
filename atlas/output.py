#!/usr/bin/env python

import png, json, logging, io

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
        
    def write(self, atlasname):
        outfile = None
        indexfile = None
        
        try:
            outfile = open(atlasname, 'wb')
        except:
            logging.exception('Could not open output file for writing')
            exit(1)
            
        outdata = []
        size = self.get_size()
        for y in range(size[1]):
            outdata.append([])
            for x in range(size[0]):
                outdata[y].extend(self.get_data(x, y))
                
        logging.info('Writing PNG atlas file with dimensions %ix%i' % size)
        writer = png.Writer(*size, alpha = True)
        writer.write(outfile, outdata);
        outfile.close()
        
class IndexOutput(object):
    '''
    Abstract superclass for index writers
    '''
    def __init__(self, rectangles, indexname, atlasname):
        self.rectangles = rectangles
        self.indexname = indexname
        self.atlasname = atlasname
        self.indexfile = None
        
    def open(self):
        try:
            self.indexfile = open(self.indexname, 'wb')
        except:
            logging.exception('Could not open index file for writing')
            exit(1)

    def write(self):
        logging.error('Attempted to write index with abstract class')
        
class JsonIndexOutput(IndexOutput):
    def write(self):
        self.open()
            
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
                            'a': self.atlasname}
                            
        logging.info('Writing JSON index file')                  
        self.indexfile.write(bytes(json.dumps(index), 'UTF-8'))
        self.indexfile.close()
        
class CssIndexOutput(IndexOutput):
    def write(self):
        self.open()
            
        index = io.StringIO()
        for rectangle in self.rectangles:
            title = rectangle.get_title().replace('\\', '-').replace('/', '-').replace('.', '_')
            if title in index:
                logging.warning('Attempted to index two rectangles with the same title: "%s" (one will be missing from index)' % title)
                continue
            
            index.write('.%s {\n' % title)
            index.write('    background-image: url(\'%s\');\n' % self.atlasname)
            index.write('    background-position: %ipx %ipx;\n' % rectangle.position)
            index.write('    width: %ipx;\n    height: %ipx;\n' % rectangle.size)
            index.write('    background-repeat: no-repeat;\n')
            index.write('}\n')
                            
        logging.info('Writing CSS index file')                  
        self.indexfile.write(bytes(index.getvalue(), 'UTF-8'))
        self.indexfile.close()
        