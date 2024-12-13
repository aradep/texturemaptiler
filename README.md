
### TextureMapTiler
A tool for cutting texture maps into tiles.

##### This project is bundled with **ImageMagick**. See [ImageMagickLicense.txt](./ImageMagickLicense.txt) for the full ImageMagick license.

## Download
Get the pre-built Windows executable [here](https://github.com/aradep/texturemaptiler/releases)

---------------
### How to Build

Prerequisites

    Python 3.x
    PyInstaller
    ImageMagick (Place in lib/imagemagick/ folder)

---------------

Step 1: Clone repository and nagivate to it.

	> git clone https://github.com/aradep/texturemaptiler.git
	> cd texturemaptiler

Step 2: Build using pyinstaller

	> pyinstaller --onefile --noconsole --add-data "lib/imagemagick/*;lib/imagemagick" texturemaptiler.py

After the build completes the standalone executable will be in the dist/ folder.
