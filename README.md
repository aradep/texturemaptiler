### TextureMapTiler
A tool for cutting texture maps into tiles.

##### This project is bundled with **ImageMagick**. See [ImageMagickLicense.txt](./ImageMagickLicense.txt) for the full ImageMagick license.

## Download
Get the pre-built Windows executable [here](https://github.com/aradep/texturemaptiler/releases)

### How to Use
Directories
- Set input to the folder the texturemaps are located in.
- Set output to the folder the generated tiles will be sent to.

Input Files
- Fill in the filenames (including extension) for the images you want to process.
- Input files must be located in the input directory.

Map Settings
- Set the map name, this is the prefix for each tile filename. (ex: mapname_0_0_height.png)
- Set the size. This is the tiling amount of the input images.
- Set the offset. This affects the coordinates of the filename. (ex: mapname_42_42_height.png)

Exporting
- Use the first row of buttons to select which input files should be processed.
- Use the Config button to modify the output tile settings if required.
- Use the Run button when you are ready to process the texturemaps.
- TexturemapTiler generates an image for each tile in the grid without altering the original input files.

---------------
### How to Build

Prerequisites

    Python 3.x
    PyInstaller
    ImageMagick portable binary (Place magick.exe and other files included in portable install in lib/imagemagick/)

Step 1: Clone repository and nagivate to it.

	> git clone https://github.com/aradep/texturemaptiler.git
	> cd texturemaptiler

Step 2: Build using pyinstaller

	> pyinstaller --onefile --noconsole --add-data "lib/imagemagick/*;lib/imagemagick" texturemaptiler.py

After the build completes the standalone executable will be in the dist/ folder.
