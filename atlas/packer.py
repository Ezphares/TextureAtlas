#!/usr/bin/env python

def log(*args):
    return
    print(*args)

"""
This module contains functionality for tightly packing rectangles using
an optimized but not optimal algorithm. See:
http://www.codeproject.com/Articles/210979/Fast-optimizing-rectangle-packing-algorithm-for-bu
"""
class PackingMatrix(object):
    """
    PackingMatrix represents the area rectangles are being packed into.
    It consists of a two dimensional array of bools denoting whether
    a segment of the grid is occupied. As each column and row may have
    different sizes, these are kept track of as well.
    """
    def __init__(self, size):
        self.rows = [size[1]]
        self.columns = [size[0]]
        self.full = [[False]] #self.full[y][x] = is segment occupied
        
    def effective_size(self):
        """
        Returns the "effective size" of the matrix, I.E. any allocated
        space that is not "infinite buffer"
        """
        width = 0
        height = 0
        
        #TODO: Count only rows and columns with content
        for row in self.rows:
            if row != float('inf'):
                height += row
                
        for column in self.columns:
            if column != float('inf'):
                width += column
                
        return (width, height)
        
    @staticmethod
    def split_dimension(dimension, value):
        """
        Splits a column or row given the dimension and coordinate at
        which to split. This function updates the array keeping track
        of row/column sizes, but not the content array.
        Call split_column or split_row instead and let them call this.
        """
        accumulator = 0
        index = 0
        
        # Accumulate sections in the dimension until we find the one
        # containing the split coordinate
        for section in dimension:
            prev = accumulator
            accumulator += section
            
            # If we reach exactly the coordinate exactly , there is
            # already a split here, so nothing needs to be done
            if accumulator == value:
                return -1
                
            elif accumulator > value:
                # Set split to the "low" part of the section and 
                # remaining to the "high"
                split = value - prev
                remaining = section - split
                
                # Shrink the high part...
                dimension[index] = remaining
                # ... then insert the new low part before it ...
                dimension.insert(index, split)
                # ... and return the index of the split section
                return index
            index += 1
    
    def split_column(self, x):
        """
        Splits a column at the given x coordinate
        """
        index = PackingMatrix.split_dimension(self.columns, x)
        if index == -1:
            # If no split was needed, we don't need to update
            # contents
            return
        log('splitting column', x)
        for row in self.full:
            # We need to insert a copy of the value at x in
            # each row, such that each value in the new columns
            # match the one that was split
            row.insert(index, row[index])

    def split_row(self, y):
        """
        Splits a row at the given y coordinate
        """
        index = PackingMatrix.split_dimension(self.rows, y)
        if index == -1:
            # If no split was needed, we don't need to update
            # contents
            return
        log('splitting row', y)
        # Since rows are the top level of the 2d array, copy the
        # entire split row, so that the new smaller rows has the
        # same values
        self.full.insert(index, [data for data in self.full[index]])
        
    def try_place(self, rect, ix, iy):
        """
        Try to place a given ImageRect at a specific column (ix)
        and row (iy) index inside the matrix, taking into account
        space taken up by previously placed rects.
        """
        log('placing rect at', ix, iy)
        free_height = 0
        free_width = 0
        height_indices = 0
        width_indices = 0
        
        # Try to accumulate enough vertical space
        while free_height < rect.size[1]:
            # If we have surpassed the height of the matrix,
            # the rect could not be placed here
            if iy + height_indices >= len(self.rows):
                return False
            # Likewise if a necessary field is already occupied
            elif self.full[iy +  height_indices][ix]:
                return False
            # Else reserve the height in this row, and reserve
            # the index
            else:
                free_height += self.rows[iy + height_indices]
                height_indices += 1
        
        # Vertical space accumulated, do the same for horizontal
        while free_width < rect.size[0]:
            # We can't surpass the width of the matrix this time
            if ix + width_indices >= len(self.columns):
                return False
            else:
                # When reserving horizontal space we need to check
                # EACH reserved row for each necessary column
                for i in range(height_indices):
                    if self.full[iy + i][ix + width_indices]:
                        return False
            # Reserve the width and index of the column
            free_width += self.columns[ix + width_indices]
            width_indices += 1
            
        # Space reserved. Find the x and y coordinates of the
        # column and row
        x = 0
        y = 0
        for i in range(ix):
            x += self.columns[i]
        for i in range(iy):
            y += self.rows[i]
        
        # Place the rect
        log('placed at (', x, y, ')')
        rect.place((x, y))
        # Split the matrix at the bottom right corner of the
        # rect, if necessary
        self.split_column(rect.right)
        self.split_row(rect.bottom)
        
        # Fill the reserved space, leaving out anything that
        # was just split out at the corner.
        for i in range(height_indices):
            for j in range(width_indices):
                self.full[iy + i][ix + j] = True
                
        return True       

class Packer(object):
    """
    The packer class contains the algorithm to actually pack
    the ImageRects.
    """
    def __init__(self, rects):
        """
        When constructing the packer, give it a list of the
        rectangles it should pack
        """
        self.rects = rects
        self.size = None
        self.best_pack = (float('inf'), None)
        self.max_width = 0
        
    def pack(self):
        """
        The main packing loop. Calling this will try to create
        the best possible packing of the rectangles given to the
        Packer
        """
        
        # We want to try to sort the rectangles by largest height
        # every time, so sort them
        self.rects.sort(key = lambda rect: rect.size[1], reverse = True)
        # The find the largest width among the rectangles. This is
        # used as the exit condition, when shrinking the packing area,
        # if the width becomes too small, we emit the best packing up
        # to that point
        for rect in self.rects:
            self.max_width = max(self.max_width, rect.size[1])
            
        # Set the initial size of the packing area to (Infinite x Largest Height)
        self.size = (float('inf'), self.rects[0].size[1])
        
        # The actual loop. While we still want to try...
        while self.size[0] > self.max_width:
            # ... see if we can pack the rectangles into the current size.
            # (First time this should always succeed, given the infinite
            # width)
            success, param1, param2 = self.attempt()
            if success:
                # On success, (param1, param2) is the effective (width, height)
                # of the packing matrix (see Packer.attempt())
                w = param1
                h = param2
                
                # Shrink the width of the packing area to the effective width
                # of the matrix
                self.size = (w, self.size[1])
                
                # Calculate the total area of the matrix and if it is smaller than
                # the current best pack...
                area = w * h
                if area < self.best_pack[0]:
                    # Save the area size and the positions of each rectangle
                    self.best_pack = (area, [(r.left, r.top) for r in self.rects])
                
                # Now, shrink the width of the area
                self.shrink_width()
                
                # Then grow the height. To find the necessary growth,
                # take the size of the largest rectangle touching the right edge
                # of the matrix
                grow = 1
                for rect in self.rects:
                    if rect.right == w:
                        grow = max(grow, rect.size[1])
                self.grow_height(grow)
            else:
                # If unsuccessful, param1 contains the total amount of rectangles
                # placed, and param2 contains the amount placed in the first column
                placed = param1
                col1 = param2
                # When calculating the size to grow height, to ensure that rectangles
                # actually rearrange, take the minimum of:
                # (A) the height of the first rectangle that could not be placed
                val1 = self.rects[placed].size[1]
                val2 = -self.size[1]
                # (B) the necessary increase to place an extra rectangle in the
                # first column
                for i in range(col1 + 1):
                    val2 += self.rects[i].size[1]
                
                self.grow_height(val1, val2)
            # Then go back and try again, unless the width is too small, in which case...
        
        # ... we place the rectangle at their best packing, then return them
        for i in range(len(self.rects)):
            self.rects[i].place(self.best_pack[1][i])
        return self.rects, self.best_pack[0]
        
    def attempt(self):
        """
        A single attempt at placing all rectangles within the given size
        On success returns:
            True, effective_width, effective_height
        On failure:
            False, number_placed, number_placed_in_col_1
        This inconsistency is purely due to laziness and will be refactored
        soon(tm)
        """
        log ('attempt at', self.size)
        placed = 0
        col1 = 0
        # Create a packing matrix
        matrix = PackingMatrix(self.size)
        # For each rect ...
        for rect in self.rects:
            rect.unplace()
            # ... go through each combination of rows ...
            for i in range(len(matrix.rows)):
                # ... and columns ...
                for j in range(len(matrix.columns)):
                    # ... until it is successfully placed
                    matrix.try_place(rect, j, i)
                    if rect.position is not None:
                        # If placed, update counters
                        placed += 1
                        if j == 0:
                            col1 += 1
                        break
                if rect.position is not None:
                    break
            # If any rect is not successfully placed, we were unsuccessful
            if rect.position is None:
                return False, placed, col1
        return True, matrix.effective_size()[0], matrix.effective_size()[1]
    
    def shrink_width(self):
        self.size = (self.size[0] - 1, self.size[1])
    
    def grow_height(self, val1, val2 = 0):
        self.size = (self.size[0], self.size[1] + min(val1, val2))

class PackingRectangle(object):
    """
    This class represents a rectangle that should be packed. It contains
    a size and position, as well as properties to retrieve coordinates 
    of the left, top, bottom and right edges.
    """
    def __init__(self):
        self.size = (0,0)
        self.position = None

    def get_data(self, x, y):
        """
        Returns image data as [r, g, b, a] at the absolute pixel position
        (x, y). If this is not placed, or the coordinate is outside the
        location, return None
        """
        return None
        
        
    @property
    def left(self):
        if self.position is None:
            return 0
        else:
            return self.position[0]
    
    @property
    def top(self):
        if self.position is None:
            return 0
        else:
            return self.position[1]
    
    @property
    def right(self):
        if self.position is None:
            return self.size[0]
        else:
            return self.position[0] + self.size[0]
    
    @property
    def bottom(self):
        if self.position is None:
            return self.size[1]
        else:
            return self.position[1] + self.size[1]
            
    @property
    def rect(self):
        return(self.left, self.top, self.right, self.bottom)
            
    def place(self, pos=(0,0)):
        """
        Places the rectangle at the given (x, y) coordinates
        """
        self.position = pos
        
    def unplace(self):
        """
        "Unplaces" the rectangle, that is, removing its position.
        """
        self.position = None
