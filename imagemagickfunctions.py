import os, sys, subprocess

# Define the path to the bundled ImageMagick binaries
if getattr(sys, 'frozen', False):
    # If running as a bundled app, use _MEIPASS to access the bundled files
    app_path = sys._MEIPASS
else:
    # If running from source, use the current directory (script location)
    app_path = os.path.dirname(__file__)

imagemagick_path = os.path.join(os.path.dirname(__file__), 'lib', 'imagemagick')
magick_command = os.path.join(imagemagick_path, 'magick')
os.environ["PATH"] = imagemagick_path + os.pathsep + os.environ["PATH"]


# ----------------------------------------------------------------------------------------------
# ------------------------------- ImageMagick Functions ----------------------------------------

def convert_height(height_dir, output_dir, map_name, map_size, offset_x, offset_y, height_tilebitdepth, height_tileformat, height_istilegrayscale, height_tileresolution):
    
    # Get the width of the image so it can be used to calculate tile coordinates
    command = ["magick", "identify", "-ping", "-format", "%w", height_dir]
    image_width = subprocess.run(command, capture_output=True, text=True)
    if image_width.returncode == 0:
        height_file_size = int(image_width.stdout.strip())
    else:
        raise Exception(f"Error: {image_width.stderr}")
    
    # Initialize ImageMagick command
    convert_command = [
        magick_command, "convert",
        "-depth", str(height_tilebitdepth),  # Use the provided bit depth
    ]

    # Add grayscale if enabled
    if height_istilegrayscale:
        convert_command.extend(["-type", "Grayscale"])
    
    # Add input image and crop options
    convert_command.extend([
        height_dir,
        "-crop", f"{map_size}x{map_size}@",
        "-set", "filename:tile", 
        f"{output_dir}/{map_name}_%[fx:round(page.x/(({height_file_size}/{map_size})*1)+{offset_x})]_%[fx:round(page.y/(({height_file_size}/{map_size})*1)+{offset_y})]_height",
        "-resize", height_tileresolution,  # Use the provided resize size
        "+repage", "+adjoin",
        f"%[filename:tile]{height_tileformat}"  # Use the dynamic format here
    ])
    
    # Run the convert command
    subprocess.run(convert_command, shell=True)

def convert_layer1(layer1_dir, output_dir, map_name, map_size, offset_x, offset_y, layer1_tilebitdepth, layer1_tileformat, layer1_istilegrayscale, layer1_tileresolution):
    
    # Get the width of the image so it can be used to calculate tile coordinates
    command = ["magick", "identify", "-ping", "-format", "%w", layer1_dir]
    image_width = subprocess.run(command, capture_output=True, text=True)
    if image_width.returncode == 0:
        layer1_file_size = int(image_width.stdout.strip())
    else:
        raise Exception(f"Error: {image_width.stderr}")
    
    # Initialize ImageMagick command
    convert_command = [
        "magick", "convert",
        "-depth", str(layer1_tilebitdepth),  # Use the provided bit depth
    ]

    # Add grayscale if enabled
    if layer1_istilegrayscale:
        convert_command.extend(["-type", "Grayscale"])
    
    # Add input image and crop options
    convert_command.extend([
        layer1_dir,
        "-crop", f"{map_size}x{map_size}@",
        "-set", "filename:tile", 
        f"{output_dir}/{map_name}_%[fx:round(page.x/(({layer1_file_size}/{map_size})*1)+{offset_x})]_%[fx:round(page.y/(({layer1_file_size}/{map_size})*1)+{offset_y})]_layer1",
        "-resize", layer1_tileresolution,  # Use the provided resize size
        "+repage", "+adjoin",
        f"%[filename:tile]{layer1_tileformat}"  # Use the dynamic format here
    ])
    
    # Run the convert command
    subprocess.run(convert_command, shell=True)

def convert_layer2(layer2_dir, output_dir, map_name, map_size, offset_x, offset_y, layer2_tilebitdepth, layer2_tileformat, layer2_istilegrayscale, layer2_tileresolution):
    
    # Get the width of the image so it can be used to calculate tile coordinates
    command = ["magick", "identify", "-ping", "-format", "%w", layer2_dir]
    image_width = subprocess.run(command, capture_output=True, text=True)
    if image_width.returncode == 0:
        layer2_file_size = int(image_width.stdout.strip())
    else:
        raise Exception(f"Error: {image_width.stderr}")
    
    # Initialize ImageMagick command
    convert_command = [
        "magick", "convert",
        "-depth", str(layer2_tilebitdepth),  # Use the provided bit depth
    ]

    # Add grayscale if enabled
    if layer2_istilegrayscale:
        convert_command.extend(["-type", "Grayscale"])
    
    # Add input image and crop options
    convert_command.extend([
        layer2_dir,
        "-crop", f"{map_size}x{map_size}@",
        "-set", "filename:tile", 
        f"{output_dir}/{map_name}_%[fx:round(page.x/(({layer2_file_size}/{map_size})*1)+{offset_x})]_%[fx:round(page.y/(({layer2_file_size}/{map_size})*1)+{offset_y})]_layer2",
        "-resize", layer2_tileresolution,  # Use the provided resize size
        "+repage", "+adjoin",
        f"%[filename:tile]{layer2_tileformat}"  # Use the dynamic format here
    ])
    
    # Run the convert command
    subprocess.run(convert_command, shell=True)

def convert_layer3(layer3_dir, output_dir, map_name, map_size, offset_x, offset_y, layer3_tilebitdepth, layer3_tileformat, layer3_istilegrayscale, layer3_tileresolution):
    
    # Get the width of the image so it can be used to calculate tile coordinates
    command = ["magick", "identify", "-ping", "-format", "%w", layer3_dir]
    image_width = subprocess.run(command, capture_output=True, text=True)
    if image_width.returncode == 0:
        layer3_file_size = int(image_width.stdout.strip())
    else:
        raise Exception(f"Error: {image_width.stderr}")
    
    # Initialize ImageMagick command
    convert_command = [
        "magick", "convert",
        "-depth", str(layer3_tilebitdepth),  # Use the provided bit depth
    ]

    # Add grayscale if enabled
    if layer3_istilegrayscale:
        convert_command.extend(["-type", "Grayscale"])
    
    # Add input image and crop options
    convert_command.extend([
        layer3_dir,
        "-crop", f"{map_size}x{map_size}@",
        "-set", "filename:tile", 
        f"{output_dir}/{map_name}_%[fx:round(page.x/(({layer3_file_size}/{map_size})*1)+{offset_x})]_%[fx:round(page.y/(({layer3_file_size}/{map_size})*1)+{offset_y})]_layer3",
        "-resize", layer3_tileresolution,  # Use the provided resize size
        "+repage", "+adjoin",
        f"%[filename:tile]{layer3_tileformat}"  # Use the dynamic format here
    ])
    
    # Run the convert command
    subprocess.run(convert_command, shell=True)

def convert_vcolor(vcolor_dir, output_dir, map_name, map_size, offset_x, offset_y, vcolor_tilebitdepth, vcolor_tileformat, vcolor_istilegrayscale, vcolor_tileresolution):
    
    # Get the width of the image so it can be used to calculate tile coordinates
    command = ["magick", "identify", "-ping", "-format", "%w", vcolor_dir]
    image_width = subprocess.run(command, capture_output=True, text=True)
    if image_width.returncode == 0:
        vcolor_file_size = int(image_width.stdout.strip())
    else:
        raise Exception(f"Error: {image_width.stderr}")
    
    # Initialize ImageMagick command
    convert_command = [
        "magick", "convert",
        "-depth", str(vcolor_tilebitdepth),  # Use the provided bit depth
    ]

    # Add grayscale if enabled
    if vcolor_istilegrayscale:
        convert_command.extend(["-type", "Grayscale"])
    
    # Add input image and crop options
    convert_command.extend([
        vcolor_dir,
        "-crop", f"{map_size}x{map_size}@",
        "-set", "filename:tile", 
        f"{output_dir}/{map_name}_%[fx:round(page.x/(({vcolor_file_size}/{map_size})*1)+{offset_x})]_%[fx:round(page.y/(({vcolor_file_size}/{map_size})*1)+{offset_y})]_vcolor",
        "-resize", vcolor_tileresolution,  # Use the provided resize size
        "+repage", "+adjoin",
        f"%[filename:tile]{vcolor_tileformat}"  # Use the dynamic format here
    ])
    
    # Run the convert command
    subprocess.run(convert_command, shell=True)