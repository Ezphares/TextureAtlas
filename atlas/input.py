#!/usr/bin/env python

import png, logging

from atlas.packer import PackingRectangle

# Creates an image rectangle from a PNG file
class PngRect(PackingRectangle):
    def __init__(self, file, title):
        super(PackingRectangle, self).__init__()
        
        reader = png.Reader(file)
        info = reader.read()
        meta = info[3]
        pixels = list(info[2])
        
        self.data = [[]]
        self.title = title
        self.size = (info[0], info[1])
        if meta['greyscale']:
            logging.error('Greyscale not yet supported')
            exit(1)
        else:
            if meta['alpha']:
                self.data = [[value for value in row] for row in pixels]
            else:
                # After every (r,g,b) value in a row, insert an alpha of 255
                self.data = []
                for row in pixels:
                    self.data.append([])
                    for i in range(len(row)):
                        self.data[-1].append(row[i])
                        if i % 3 == 2:
                            self.data[-1].append(255)
        logging.info('Loaded PNG image %s with dimensions %ix%i' % (title, info[0], info[1]))
                            
    def get_data(self, x, y):
        if (self.position is None or x < self.left or x >= self.right or
                y < self.top or y >= self.bottom):
            return None
            
        row = self.data[y - self.top]
        return [row[4 * (x - self.left) + i] for i in range(4)]
        
    def get_title(self):
        return self.title