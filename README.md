# TextureAtlas

Python scripts to create a texture atlas (spritesheet) and index file from a set of images.
The packing algorithm itself is implemented based on the description at 
http://www.codeproject.com/Articles/210979/Fast-optimizing-rectangle-packing-algorithm-for-bu

## Usage
```
atlas.py { inputfiles } { options }
```

Possible options:

* `-o filename` sets the name of the output (atlas) file. Default `atlas.png`
* `-i filename` sets the name of the index file. Default `index.json`

## The Future?

No specific roadmap, but some ideas which are likely to become features:

* Support for other filetypes than PNG
* Support for other index formats than JSON (CSS backgrounds)
* Support for giving a max size to the atlas, splitting up into multiple atlases if impossible.
* Support for having conform to certain standards (e.g. always be a square, dimensions must be power of 2, etc)
