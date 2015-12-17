# TextureAtlas

Python scripts to create a texture atlas (spritesheet) and index file from a set of images.
The packing algorithm itself is implemented based on the description at 
http://www.codeproject.com/Articles/210979/Fast-optimizing-rectangle-packing-algorithm-for-bu

## Usage

From `atlas.py --help`:

```
usage: atlas.py [-h] [-a ATLAS] [-i INDEX] IMAGE [IMAGE ...]

Packs several image file into a single atlas image, and provides an index file
mapping filenames to rectangles in the atlas

positional arguments:
  IMAGE                 filenames of the images to pack

optional arguments:
  -h, --help            show this help message and exit
  -a ATLAS, --atlas ATLAS
                        filename of the atlas file (default: atlas.png)
  -i INDEX, --index INDEX
                        filename of the index file (default: index.json)
```

## The Future?

No specific roadmap, but some ideas which are likely to become features:

* Support for other filetypes than PNG
* Support for other index formats than JSON (CSS backgrounds)
* Support for giving a max size to the atlas, splitting up into multiple atlases if impossible.
* Support for having conform to certain standards (e.g. always be a square, dimensions must be power of 2, etc)
