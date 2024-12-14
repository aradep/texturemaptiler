#-----------------------------------------------------------------------------------------------
# ImageMagickFunctions.py
# Predefined ImageMagick functions for use in TextureMapTiler.py
#
# This software is bundled with ImageMagick. See ImageMagickLicense.txt for full details.
#-----------------------------------------------------------------------------------------------

import os, sys, subprocess

# Define path to bundled ImageMagick
if getattr(sys, 'frozen', False): app_path = sys._MEIPASS # If running as a bundled app
else: app_path = os.path.dirname(__file__) # If running from source
imagemagick_path = os.path.join(app_path, 'lib', 'imagemagick')
magick_command = os.path.join(imagemagick_path, 'magick')
# Set environment variables
os.environ['MAGICK_HOME'] = imagemagick_path
os.environ['PATH'] = imagemagick_path + os.pathsep + os.environ.get('PATH', '')

# ----------------------------------------------------------------------------------------------
# ------------------------------- ImageMagick Functions ----------------------------------------

def convert_height(height_dir, output_dir, map_name, map_size, offset_x, offset_y, height_tilelabel, height_tilebitdepth, height_tileformat, height_istilegrayscale, height_tileresolution):

    # Get the width of the input file so it can be used to calculate tile coordinates
    command = [magick_command, "identify", "-ping", "-format", "%w", height_dir]
    image_width = subprocess.run(command, capture_output=True, text=True)
    if image_width.returncode == 0: height_file_size = int(image_width.stdout.strip())
    else: raise Exception(f"Error: {image_width.stderr}")
    
    # Initialize convert command
    convert_command = [magick_command]

    # Input file
    convert_command.extend([height_dir])

    # Input file tiling amount
    convert_command.extend(["-crop", f"{map_size}x{map_size}@"])
    
    # Output tile naming
    convert_command.extend(["-set", "filename:tile", f"{output_dir}/{map_name}_%[fx:round(page.x/(({height_file_size}/{map_size})*1)+{offset_x})]_%[fx:round(page.y/(({height_file_size}/{map_size})*1)+{offset_y})]_{height_tilelabel}"])
    
    # Output tile bitdepth
    convert_command.extend(["-depth", str(height_tilebitdepth)])

    # Output tile grayscale
    if height_istilegrayscale: convert_command.extend(["-type", "Grayscale"])
    
    # Output tile resolution
    convert_command.extend(["-resize", f"{height_tileresolution}x{height_tileresolution}!"])

    # Output tile save individually
    convert_command.extend(["+repage", "+adjoin"])
    
    # Output tile format
    convert_command.extend([f"%[filename:tile]{height_tileformat}"])
    
    # Run convert command
    try:
        result = subprocess.run(convert_command, capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
        if result.returncode != 0: raise Exception(f"Error: {result.stderr}")
    except Exception as e: print(f"Error: {e}")

def convert_layer1(layer1_dir, output_dir, map_name, map_size, offset_x, offset_y, layer1_tilelabel, layer1_tilebitdepth, layer1_tileformat, layer1_istilegrayscale, layer1_tileresolution):
    
    # Get the width of the input file so it can be used to calculate tile coordinates
    command = [magick_command, "identify", "-ping", "-format", "%w", layer1_dir]
    image_width = subprocess.run(command, capture_output=True, text=True)
    if image_width.returncode == 0: layer1_file_size = int(image_width.stdout.strip())
    else: raise Exception(f"Error: {image_width.stderr}")
    
    # Initialize convert command
    convert_command = [magick_command]

    # Input file
    convert_command.extend([layer1_dir])

    # Input file tiling amount
    convert_command.extend(["-crop", f"{map_size}x{map_size}@"])
    
    # Output tile naming
    convert_command.extend(["-set", "filename:tile", f"{output_dir}/{map_name}_%[fx:round(page.x/(({layer1_file_size}/{map_size})*1)+{offset_x})]_%[fx:round(page.y/(({layer1_file_size}/{map_size})*1)+{offset_y})]_{layer1_tilelabel}"])
    
    # Output tile bitdepth
    convert_command.extend(["-depth", str(layer1_tilebitdepth)])

    # Output tile grayscale
    if layer1_istilegrayscale: convert_command.extend(["-type", "Grayscale"])
    
    # Output tile resolution
    convert_command.extend(["-resize", f"{layer1_tileresolution}x{layer1_tileresolution}!"])

    # Output tile save individually
    convert_command.extend(["+repage", "+adjoin"])
    
    # Output tile format
    convert_command.extend([f"%[filename:tile]{layer1_tileformat}"])
    
    # Run convert command
    try:
        result = subprocess.run(convert_command, capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
        if result.returncode != 0: raise Exception(f"Error: {result.stderr}")
    except Exception as e: print(f"Error: {e}")

def convert_layer2(layer2_dir, output_dir, map_name, map_size, offset_x, offset_y, layer2_tilelabel, layer2_tilebitdepth, layer2_tileformat, layer2_istilegrayscale, layer2_tileresolution):
    
    # Get the width of the input file so it can be used to calculate tile coordinates
    command = [magick_command, "identify", "-ping", "-format", "%w", layer2_dir]
    image_width = subprocess.run(command, capture_output=True, text=True)
    if image_width.returncode == 0: layer2_file_size = int(image_width.stdout.strip())
    else: raise Exception(f"Error: {image_width.stderr}")
    
    # Initialize convert command
    convert_command = [magick_command]

    # Input file
    convert_command.extend([layer2_dir])

    # Input file tiling amount
    convert_command.extend(["-crop", f"{map_size}x{map_size}@"])
    
    # Output tile naming
    convert_command.extend(["-set", "filename:tile", f"{output_dir}/{map_name}_%[fx:round(page.x/(({layer2_file_size}/{map_size})*1)+{offset_x})]_%[fx:round(page.y/(({layer2_file_size}/{map_size})*1)+{offset_y})]_{layer2_tilelabel}"])
    
    # Output tile bitdepth
    convert_command.extend(["-depth", str(layer2_tilebitdepth)])

    # Output tile grayscale
    if layer2_istilegrayscale: convert_command.extend(["-type", "Grayscale"])
    
    # Output tile resolution
    convert_command.extend(["-resize", f"{layer2_tileresolution}x{layer2_tileresolution}!"])

    # Output tile save individually
    convert_command.extend(["+repage", "+adjoin"])
    
    # Output tile format
    convert_command.extend([f"%[filename:tile]{layer2_tileformat}"])
    
    # Run convert command
    try:
        result = subprocess.run(convert_command, capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
        if result.returncode != 0: raise Exception(f"Error: {result.stderr}")
    except Exception as e: print(f"Error: {e}")

def convert_layer3(layer3_dir, output_dir, map_name, map_size, offset_x, offset_y, layer3_tilelabel, layer3_tilebitdepth, layer3_tileformat, layer3_istilegrayscale, layer3_tileresolution):
    
    # Get the width of the input file so it can be used to calculate tile coordinates
    command = [magick_command, "identify", "-ping", "-format", "%w", layer3_dir]
    image_width = subprocess.run(command, capture_output=True, text=True)
    if image_width.returncode == 0: layer3_file_size = int(image_width.stdout.strip())
    else: raise Exception(f"Error: {image_width.stderr}")
    
    # Initialize convert command
    convert_command = [magick_command]

    # Input file
    convert_command.extend([layer3_dir])

    # Input file tiling amount
    convert_command.extend(["-crop", f"{map_size}x{map_size}@"])
    
    # Output tile naming
    convert_command.extend(["-set", "filename:tile", f"{output_dir}/{map_name}_%[fx:round(page.x/(({layer3_file_size}/{map_size})*1)+{offset_x})]_%[fx:round(page.y/(({layer3_file_size}/{map_size})*1)+{offset_y})]_{layer3_tilelabel}"])
    
    # Output tile bitdepth
    convert_command.extend(["-depth", str(layer3_tilebitdepth)])

    # Output tile grayscale
    if layer3_istilegrayscale: convert_command.extend(["-type", "Grayscale"])
    
    # Output tile resolution
    convert_command.extend(["-resize", f"{layer3_tileresolution}x{layer3_tileresolution}!"])

    # Output tile save individually
    convert_command.extend(["+repage", "+adjoin"])
    
    # Output tile format
    convert_command.extend([f"%[filename:tile]{layer3_tileformat}"])
    
    # Run convert command
    try:
        result = subprocess.run(convert_command, capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
        if result.returncode != 0: raise Exception(f"Error: {result.stderr}")
    except Exception as e: print(f"Error: {e}")

def convert_vcolor(vcolor_dir, output_dir, map_name, map_size, offset_x, offset_y, vcolor_tilelabel, vcolor_tilebitdepth, vcolor_tileformat, vcolor_istilegrayscale, vcolor_tileresolution):
    
    # Get the width of the input file so it can be used to calculate tile coordinates
    command = [magick_command, "identify", "-ping", "-format", "%w", vcolor_dir]
    image_width = subprocess.run(command, capture_output=True, text=True)
    if image_width.returncode == 0: vcolor_file_size = int(image_width.stdout.strip())
    else: raise Exception(f"Error: {image_width.stderr}")

    # Initialize convert command
    convert_command = [magick_command]

    # Input file
    convert_command.extend([vcolor_dir])

    # Input file tiling amount
    convert_command.extend(["-crop", f"{map_size}x{map_size}@"])
    
    # Output tile naming
    convert_command.extend(["-set", "filename:tile", f"{output_dir}/{map_name}_%[fx:round(page.x/(({vcolor_file_size}/{map_size})*1)+{offset_x})]_%[fx:round(page.y/(({vcolor_file_size}/{map_size})*1)+{offset_y})]_{vcolor_tilelabel}"])
    
    # Output tile bitdepth
    convert_command.extend(["-depth", str(vcolor_tilebitdepth)])

    # Output tile grayscale
    if vcolor_istilegrayscale: convert_command.extend(["-type", "Grayscale"])
    
    # Output tile resolution
    convert_command.extend(["-resize", f"{vcolor_tileresolution}x{vcolor_tileresolution}!"])

    # Output tile save individually
    convert_command.extend(["+repage", "+adjoin"])
    
    # Output tile format
    convert_command.extend([f"%[filename:tile]{vcolor_tileformat}"])
    
    # Run convert command
    try:
        result = subprocess.run(convert_command, capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
        if result.returncode != 0: raise Exception(f"Error: {result.stderr}")
    except Exception as e: print(f"Error: {e}")