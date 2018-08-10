# TextureAtlas

Python scripts to create a texture atlas (spritesheet) and index file from a set of images.
The packing algorithm itself is implemented based on the description at 
http://www.codeproject.com/Articles/210979/Fast-optimizing-rectangle-packing-algorithm-for-bu

## Prerequisites

[pypng](https://pypi.org/project/pypng/)

## Usage
Basic usage:
```
atlas.py IMAGE [IMAGE ...]
```
This takes a number of input image files and packs them into an atlas file
called `atlas.png` and generates an index file `index.json` describing where
in the atlas each original image can be found.

Several options exists for customizing behaviour.
From `atlas.py --help`:

```
usage: atlas.py [-h] [-a ATLAS] [-i INDEX] [-it {json,css}] [-v]
                IMAGE [IMAGE ...]

Packs several image file into a single atlas image, and provides an index file
mapping filenames to rectangles in the atlas

positional arguments:
  IMAGE                 filenames of the images to pack

optional arguments:
  -h, --help            show this help message and exit
  -a ATLAS, --atlas ATLAS
                        filename of the atlas file (without extension)
                        (default: atlas)
  -i INDEX, --index INDEX
                        filename of the index file (without extension)
                        (default: index)
  -it {json,css}, --indextype {json,css}
                        type of index file (default: json)
  -v, --verbose         display verbose progress info
```

## The Future?

No specific roadmap, but some ideas which are likely to become features:

* Support for other filetypes than PNG
* Support for giving a max size to the atlas, splitting up into multiple atlases if impossible.
* Support for having conform to certain standards (e.g. always be a square, dimensions must be power of 2, etc)
