#-----------------------------------------------------------------------------------------------
# TextureMapTiler
# A tool for slicing texture maps into tiles
#
# This software is bundled with ImageMagick. See ImageMagickLicense.txt for full details.
#
version= "Version: 1.0.0"
#
#-----------------------------------------------------------------------------------------------

import os, sys, time, threading, tkinter as tk
from tkinter import filedialog, scrolledtext, StringVar, Button, Label, Entry, Scale
from concurrent.futures import ThreadPoolExecutor
from imagemagickfunctions import convert_height, convert_layer1, convert_layer2, convert_layer3, convert_vcolor

imagemagick_path = os.path.join(os.path.dirname(__file__), 'lib', 'imagemagick')
magick_command = os.path.join(imagemagick_path, 'magick')
os.environ["PATH"] = imagemagick_path + os.pathsep + os.environ["PATH"]

# ----------------------------------------------------------------------------------------------
# ------------------------------------------ GUI -----------------------------------------------
# ----------------------------------------- Setup ----------------------------------------------

class tkGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("TextureMap Tiler")
        root.configure(bg="#1f2023")
        self.is_processing = False

        # Left frame
        self.left_frame = tk.Frame(self.root, width=300, height=600, bg="#26282d")
        self.left_frame.grid(row=0, column=2, padx=(5,20), pady=(20,10), ipadx=5, ipady=5, sticky="n")
        # Right frame
        self.right_frame = tk.Frame(self.root, width=300, height=600, bg="#1f2023")
        self.right_frame.grid(row=0, column=1, padx=(20,5), pady=(20,10), ipadx=5, ipady=5, sticky="n")

        # Variables
        self.input_dir = StringVar()
        self.output_dir = StringVar()
        self.map_name = StringVar()
        self.map_size = tk.IntVar()
        self.map_offsetx = tk.IntVar()
        self.map_offsety = tk.IntVar()

        self.height_name = StringVar()
        self.layer1_name = StringVar()
        self.layer2_name = StringVar()
        self.layer3_name = StringVar()
        self.vcolor_name = StringVar()

        self.height_exporttoggle = tk.IntVar()
        self.layer1_exporttoggle = tk.IntVar()
        self.layer2_exporttoggle = tk.IntVar()
        self.layer3_exporttoggle = tk.IntVar()
        self.vcolor_exporttoggle = tk.IntVar()

        # Tile Settings
        self.height_tileresolution = StringVar(value=256)
        self.layer1_tileresolution = StringVar(value=1024)
        self.layer2_tileresolution = StringVar(value=1024)
        self.layer3_tileresolution = StringVar(value=1024)
        self.vcolor_tileresolution = StringVar(value=1024)

        self.height_tilebitdepth = tk.IntVar(value=16)
        self.layer1_tilebitdepth = tk.IntVar(value=8)
        self.layer2_tilebitdepth = tk.IntVar(value=8)
        self.layer3_tilebitdepth = tk.IntVar(value=8)
        self.vcolor_tilebitdepth = tk.IntVar(value=8)

        self.height_tileformat = StringVar(value='.png')
        self.layer1_tileformat = StringVar(value='.png')
        self.layer2_tileformat = StringVar(value='.png')
        self.layer3_tileformat = StringVar(value='.png')
        self.vcolor_tileformat = StringVar(value='.png')

        self.height_istilegrayscale = tk.IntVar(value=1)
        self.layer1_istilegrayscale = tk.IntVar(value=1)
        self.layer2_istilegrayscale = tk.IntVar(value=1)
        self.layer3_istilegrayscale = tk.IntVar(value=1)
        self.vcolor_istilegrayscale = tk.IntVar(value=0)

        # Save on close
        root.protocol("WM_DELETE_WINDOW", self.on_close)

# ----------------------------------------------------------------------------------------------
# ----------------------------------------- GUI ------------------------------------------------
# -------------------------------------- Left Frame --------------------------------------------

# ------# Group 1 - Directories
        self.group1_frame = tk.Frame(self.left_frame, bg="#26282d")
        self.group1_frame.grid(row=0, column=0, padx=15, pady=(20,30), sticky="n")
        self.group1_label = Label(self.group1_frame, fg="white", bg="#26282d", text="Directories", font=("Helvetica", 10, "bold"))
        self.group1_label.grid(row=0, column=0, columnspan=3, pady=(0,5), sticky="n")
        
        # Input
        self.input_label = Label(self.group1_frame, fg="white", bg="#26282d", text="Input:")
        self.input_label.grid(row=1, column=0, padx=2, pady=2, sticky="ne")
        self.input_entry = Entry(self.group1_frame, textvariable=self.input_dir, borderwidth=0, fg="white", bg="#1f2023", width=42)
        self.input_entry.grid(row=1, column=1, ipady=5, ipadx=4, pady=(0,5))
        self.input_browse_button = Button(self.group1_frame, highlightbackground="#26282d", activebackground="#26282d", activeforeground="white", fg="white", bg="#2d2f34", text="Browse", command=self.browse_input)
        self.input_browse_button.grid(row=1, column=2, pady=(0,3))
        
        # Output
        self.output_label = Label(self.group1_frame, fg="white", bg="#26282d", text="Output:")
        self.output_label.grid(row=2, column=0, padx=2, pady=2, sticky="ne")
        self.output_entry = Entry(self.group1_frame, textvariable=self.output_dir, borderwidth=0, fg="white", bg="#1f2023", width=42)
        self.output_entry.grid(row=2, column=1, ipady=5, ipadx=4)
        self.output_browse_button = Button(self.group1_frame, highlightbackground="#26282d", activebackground="#26282d", activeforeground="white", fg="white", bg="#2d2f34", text="Browse", command=self.browse_output)
        self.output_browse_button.grid(row=2, column=2, pady=(1,0))

        # ------# Group 2 - Filenames
        self.group2_frame = tk.Frame(self.left_frame, bg="#26282d")
        self.group2_frame.grid(row=1, padx=15, pady=(0, 30), column=0, sticky="n")
        self.group2_label = Label(self.group2_frame, fg="white", bg="#26282d", text="Input Files", font=("Helvetica", 10, "bold"))
        self.group2_label.grid(row=0, column=0, columnspan=4, pady=(0, 5), sticky="n")

        # Heightmap
        self.height_label = Label(self.group2_frame, fg="white", bg="#26282d", text="Height:")
        self.height_label.grid(row=1, column=0, padx=2, pady=2, sticky="ne")
        self.height_entry = Entry(self.group2_frame, textvariable=self.height_name, borderwidth=0, fg="white", bg="#1f2023", width=50)
        self.height_entry.grid(row=1, column=1, ipady=5, ipadx=4, pady=(0, 5))

        # Layer 1
        self.layer1_label = Label(self.group2_frame, fg="white", bg="#26282d", text="Layer 1:")
        self.layer1_label.grid(row=2, column=0, padx=2, pady=2, sticky="ne")
        self.layer1_entry = Entry(self.group2_frame, textvariable=self.layer1_name, borderwidth=0, fg="white", bg="#1f2023", width=50)
        self.layer1_entry.grid(row=2, column=1, ipady=5, ipadx=4, pady=(0, 5))

        # Layer 2
        self.layer2_label = Label(self.group2_frame, fg="white", bg="#26282d", text="Layer 2:")
        self.layer2_label.grid(row=3, column=0, padx=2, pady=2, sticky="ne")
        self.layer2_entry = Entry(self.group2_frame, textvariable=self.layer2_name, borderwidth=0, fg="white", bg="#1f2023", width=50)
        self.layer2_entry.grid(row=3, column=1, ipady=5, ipadx=4, pady=(0, 5))

        # Layer 3
        self.layer3_label = Label(self.group2_frame, fg="white", bg="#26282d", text="Layer 3:")
        self.layer3_label.grid(row=4, column=0, padx=2, pady=2, sticky="ne")
        self.layer3_entry = Entry(self.group2_frame, textvariable=self.layer3_name, borderwidth=0, fg="white", bg="#1f2023", width=50)
        self.layer3_entry.grid(row=4, column=1, ipady=5, ipadx=4, pady=(0, 5))

        # VColor
        self.vcolor_label = Label(self.group2_frame, fg="white", bg="#26282d", text="Vcolor:")
        self.vcolor_label.grid(row=5, column=0, padx=2, pady=2, sticky="ne")
        self.vcolor_entry = Entry(self.group2_frame, textvariable=self.vcolor_name, borderwidth=0, fg="white", bg="#1f2023", width=50)
        self.vcolor_entry.grid(row=5, column=1, ipady=5, ipadx=4, pady=(0, 5))
        
# ------# Group 3 - Map Settings
        self.group3_frame = tk.Frame(self.left_frame, bg="#26282d")
        self.group3_frame.grid(row=2, column=0, padx=15, pady=(0,30), sticky="n")
        self.group3_label = Label(self.group3_frame, fg="white", bg="#26282d", text="Map Settings", font=("Helvetica", 10, "bold"))
        self.group3_label.grid(row=0, column=0, columnspan=3, pady=(0,5), sticky="n")
        
        # Name
        self.map_label = Label(self.group3_frame, fg="white", bg="#26282d", text="Name:")
        self.map_label.grid(row=1, column=0, padx=(6,0), pady=(2,0), sticky="ne")
        self.map_entry = Entry(self.group3_frame, textvariable=self.map_name, borderwidth=0, fg="white", bg="#1f2023", width=50)
        self.map_entry.grid(row=1, column=1, ipady=5, ipadx=8)
        
        # Size
        self.grid_label = Label(self.group3_frame, fg="white", bg="#26282d", text="Size:")
        self.grid_label.grid(row=2, column=0, padx=2, pady=(19,0), sticky="ne")
        self.grid_slider = Scale(self.group3_frame, from_=1, fg="white", bg="#26282d", highlightthickness=0, to=64, orient="horizontal", variable=self.map_size, command=self.update_grid, width=20, length=318)
        self.grid_slider.grid(row=2, column=1, columnspan=2, padx=(0,8), sticky="n")

        # Frame for Sliders
        self.slider_frame = tk.Frame(self.group3_frame, bg="#26282d")
        self.slider_frame.grid(row=3, column=0, columnspan=3)

        # X Offset Slider
        self.offset_x_label = Label(self.slider_frame, fg="white", bg="#26282d", text="X:")
        self.offset_x_label.grid(row=0, column=0, padx=(32,2), pady=(20,0), sticky="n")
        self.offset_x_slider = Scale(self.slider_frame, from_=0, to_=64, fg="white",bg="#26282d", highlightthickness=0, orient="horizontal", variable=self.map_offsetx, command=self.update_grid, width=20, length=139)
        self.offset_x_slider.grid(row=0, column=1, padx=(2,10))

        # Y Offset Slider
        self.offset_y_label = Label(self.slider_frame, fg="white", bg="#26282d", text="Y:")
        self.offset_y_label.grid(row=0, column=2, padx=(5,2), pady=(20,0), sticky="n")
        self.offset_y_slider = Scale(self.slider_frame, from_=0, to_=64, fg="white",bg="#26282d", highlightthickness=0, orient="horizontal", variable=self.map_offsety, command=self.update_grid, width=20, length=139)
        self.offset_y_slider.grid(row=0, column=3, padx=(5,10))

# ------# Group 4 - Exporting
        self.group4 = tk.Frame(self.left_frame, bg="#26282d")
        self.group4.grid(row=3, column=0, columnspan=6, padx=15, pady=3)
        self.checkbox_label = Label(self.group4, text="Exporting", fg="white", bg="#26282d", font=("Helvetica", 10, "bold"))
        self.checkbox_label.grid(row=0, column=0, columnspan=5, pady=(0, 10), sticky="n")

        # Selectors
        self.height_check = tk.Checkbutton(self.group4, text="Height", bg="#2d2f34", fg="white", selectcolor="#393a3d", variable=self.height_exporttoggle, highlightthickness=0, highlightbackground="#26282d", activebackground="#26282d", activeforeground="white", indicatoron=False)
        self.height_check.grid(row=1, column=0, ipadx=10, padx=5, ipady=2, pady=(5, 0))
        self.layer1_check = tk.Checkbutton(self.group4, text="Layer 1", bg="#2d2f34", fg="white", selectcolor="#393a3d", variable=self.layer1_exporttoggle, highlightthickness=0, highlightbackground="#26282d", activebackground="#26282d", activeforeground="white", indicatoron=False)
        self.layer1_check.grid(row=1, column=1, ipadx=10, padx=5, ipady=2, pady=(5, 0))
        self.layer2_check = tk.Checkbutton(self.group4, text="Layer 2", bg="#2d2f34", fg="white", selectcolor="#393a3d", variable=self.layer2_exporttoggle, highlightthickness=0, highlightbackground="#26282d", activebackground="#26282d", activeforeground="white", indicatoron=False)
        self.layer2_check.grid(row=1, column=2, ipadx=10, padx=5, ipady=2, pady=(5, 0))
        self.layer3_check = tk.Checkbutton(self.group4, text="Layer 3", bg="#2d2f34", fg="white", selectcolor="#393a3d", variable=self.layer3_exporttoggle, highlightthickness=0, highlightbackground="#26282d", activebackground="#26282d", activeforeground="white", indicatoron=False)
        self.layer3_check.grid(row=1, column=3, ipadx=10, padx=5, ipady=2, pady=(5, 0))
        self.vcolor_check = tk.Checkbutton(self.group4, text="Vcolor", bg="#2d2f34", fg="white", selectcolor="#393a3d", variable=self.vcolor_exporttoggle, highlightthickness=0, highlightbackground="#26282d", activebackground="#26282d", activeforeground="white", indicatoron=False)
        self.vcolor_check.grid(row=1, column=4, ipadx=10, padx=5, ipady=2, pady=(5, 0))
        
        # Frame for Buttons
        self.button_frame = tk.Frame(self.group4, bg="#26282d")
        self.button_frame.grid(row=2, column=0, columnspan=6)

        # Settings Button
        self.height_config_button = Button(self.button_frame,text="Config",height=3, highlightbackground="#26282d", activebackground="#26282d", activeforeground="white", command=self.open_config_window, width=12, fg="white", bg="#2d2f34", font=("Helvetica", 10, "bold"))
        self.height_config_button.grid(row=0, column=0, columnspan=1, padx=(5,5))

        # Run Button
        self.run_button = Button(self.button_frame, text="Run", height=3, highlightbackground="#26282d", activebackground="#26282d", activeforeground="white", command=self.start_processing, width=30, fg="white", bg="#2d2f34", font=("Helvetica", 10, "bold"))
        self.run_button.grid(row=0, column=1, columnspan=1, pady=10, padx=(0,5), sticky="ew")

# ----------------------------------------------------------------------------------------------
# ----------------------------------------- GUI ------------------------------------------------
# ------------------------------------- Right Frame --------------------------------------------

        # Canvas for grid
        self.canvas = tk.Canvas(self.right_frame, width=513, height=513, borderwidth=0, highlightthickness=0, bg="#393a3d")
        self.canvas.grid(row=0, column=0)

        # Grid
        self.draw_grid()

        # Log window
        self.output_text = scrolledtext.ScrolledText(self.right_frame, wrap=tk.WORD, width=61, height=9, borderwidth=0, highlightthickness=0, bg="#26282d", fg="white")
        self.output_text.grid(row=1, column=0, columnspan=2, ipadx=2, ipady=2, padx=(0,5), pady=(21,0))
        self.output_text.config(state=tk.DISABLED)

# ----------------------------------------------------------------------------------------------
# ----------------------------------------- GUI ------------------------------------------------
# -------------------------------------- Functions ---------------------------------------------
# --------------------------------------- Logging ----------------------------------------------
    # Redirect stdout and error
        self.old_stdout = sys.stdout
        self.old_stderr = sys.stderr
        sys.stdout = self
        sys.stderr = self
# ----------------------------------------------------------------------------------------------
# ----------------------------------------- GUI ------------------------------------------------
# --------------------------------------- Startup ----------------------------------------------

        print("TextureMap Tiler")
        print(version)
        print("----------------------------")
        self.load_settings()
        self.update_grid()
        print("Ready")
        
    def gui_logger(self, message):
        self.write(message)

    def write(self, message):
        self.output_text.config(state=tk.NORMAL)  # Enable editing
        self.output_text.insert(tk.END, message) # Add text
        self.output_text.config(state=tk.DISABLED)  # Disable editing
        self.output_text.yview(tk.END)  # Scroll to end

    def flush(self):
        pass

# ----------------------------------------------------------------------------------------------
# ----------------------------------------- GUI ------------------------------------------------
# -------------------------------------- Functions ---------------------------------------------
# ---------------------------------------- Input -----------------------------------------------

    def browse_input(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.input_dir.set(folder_selected)

    def browse_output(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.output_dir.set(folder_selected)

# ----------------------------------------------------------------------------------------------
# ----------------------------------------- GUI ------------------------------------------------
# -------------------------------------- Functions ---------------------------------------------
# ------------------------------------ Settings Window -----------------------------------------

    def open_config_window(self):
        """ Opens a configuration window for all layers at once. """
        # Create new window
        config_window = tk.Toplevel(self.root)
        config_window.title("Tile Settings")
        config_window.configure(bg="#26282d")
        config_window.geometry("400x310")
        config_window.resizable(False, False)

        # Window Title
        window_label = Label(config_window, text="Exported Tile Settings", bg="#26282d", fg="white", font=("Helvetica", 12, "bold"))
        window_label.grid(row=0, column=0, columnspan=7, pady=(10, 10), sticky="n")

        # Configure rows/columns to not stretch
        for col in range(4):
            config_window.grid_columnconfigure(col, weight=1)
        for row in range(7):
            config_window.grid_rowconfigure(row, weight=0)

        # Top labels for Resolution and Bit Depth
        resolution_label = Label(config_window, text="Resolution", bg="#26282d", fg="white")
        resolution_label.grid(row=1, column=1, padx=2, pady=3, sticky="n")
        resolution_label = Label(config_window, text="Format", bg="#26282d", fg="white")
        resolution_label.grid(row=1, column=2, padx=2, pady=3, sticky="n")
        bit_depth_label = Label(config_window, text="Bit Depth", bg="#26282d", fg="white")
        bit_depth_label.grid(row=1, column=3, columnspan=3, padx=(6,0), pady=3, sticky="n")
        bit_depth_label = Label(config_window, text="Color", bg="#26282d", fg="white")
        bit_depth_label.grid(row=1, column=6, columnspan=3, padx=(7,15), pady=3, sticky="n")

#-------# Height
        height_label = Label(config_window, text="Height:", bg="#26282d", fg="white")
        height_label.grid(row=2, column=0, padx=(10, 0), sticky="e")
        # Resolution
        height_tileresolution_entry = Entry(config_window, textvariable=self.height_tileresolution, borderwidth=0, fg="white", bg="#1f2023", width=10)
        height_tileresolution_entry.grid(row=2, column=1, padx=0, pady=3, ipadx=3, ipady=4)
        # Format
        height_tileformat_entry = Entry(config_window, textvariable=self.height_tileformat, borderwidth=0, fg="white", bg="#1f2023", width=8)
        height_tileformat_entry.grid(row=2, column=2, padx=2, pady=3, ipadx=3, ipady=4)
        # 8bit
        bit_depth_8_button = tk.Radiobutton(config_window, text="8", variable=self.height_tilebitdepth, value=8, bg="#26282d", fg="white", selectcolor="#393a3d", indicatoron=False, activebackground="#26282d", activeforeground="white")
        bit_depth_8_button.grid(row=2, column=3, padx=(2,0), pady=3, ipadx=6, ipady=1)
        # 16bit
        bit_depth_16_button = tk.Radiobutton(config_window, text="16", variable=self.height_tilebitdepth, value=16, bg="#26282d", fg="white", selectcolor="#393a3d", indicatoron=False, activebackground="#26282d", activeforeground="white")
        bit_depth_16_button.grid(row=2, column=4, padx=2, pady=3, ipadx=3, ipady=1)
        # 32bit
        bit_depth_32_button = tk.Radiobutton(config_window, text="32", variable=self.height_tilebitdepth, value=32, bg="#26282d", fg="white", selectcolor="#393a3d", indicatoron=False, activebackground="#26282d", activeforeground="white")
        bit_depth_32_button.grid(row=2, column=5, padx=2, pady=3, ipadx=3, ipady=1)
        # Grayscale
        height_istilegrayscale_toggle = tk.Checkbutton(config_window, text="Grayscale", bg="#2d2f34", fg="white", selectcolor="#393a3d", variable=self.height_istilegrayscale, highlightthickness=0, highlightbackground="#26282d", activebackground="#26282d", activeforeground="white", indicatoron=False)
        height_istilegrayscale_toggle.grid(row=2, column=6, pady=3, padx=(10, 15), ipadx=2, ipady=2)

#-------# Layer 1
        layer1_label = Label(config_window, text="Layer 1:", bg="#26282d", fg="white")
        layer1_label.grid(row=3, column=0, padx=(10, 0), sticky="e")
        # Resolution
        layer1_tileresolution_entry = Entry(config_window, textvariable=self.layer1_tileresolution, borderwidth=0, fg="white", bg="#1f2023", width=10)
        layer1_tileresolution_entry.grid(row=3, column=1, padx=2, pady=3, ipadx=3, ipady=4)
        # Format
        layer1_tileformat_entry = Entry(config_window, textvariable=self.layer1_tileformat, borderwidth=0, fg="white", bg="#1f2023", width=8)
        layer1_tileformat_entry.grid(row=3, column=2, padx=2, pady=3, ipadx=3, ipady=4)
        # 8bit
        bit_depth_8_button_layer1 = tk.Radiobutton(config_window, text="8", variable=self.layer1_tilebitdepth, value=8, bg="#26282d", fg="white", selectcolor="#393a3d", indicatoron=False, activebackground="#26282d", activeforeground="white")
        bit_depth_8_button_layer1.grid(row=3, column=3, padx=(2,0), pady=3, ipadx=6, ipady=1)
        # 16bit
        bit_depth_16_button_layer1 = tk.Radiobutton(config_window, text="16", variable=self.layer1_tilebitdepth, value=16, bg="#26282d", fg="white", selectcolor="#393a3d", indicatoron=False, activebackground="#26282d", activeforeground="white")
        bit_depth_16_button_layer1.grid(row=3, column=4, padx=(0,2), pady=3, ipadx=3, ipady=1)
        # 32bit
        bit_depth_32_button_layer1 = tk.Radiobutton(config_window, text="32", variable=self.layer1_tilebitdepth, value=32, bg="#26282d", fg="white", selectcolor="#393a3d", indicatoron=False, activebackground="#26282d", activeforeground="white")
        bit_depth_32_button_layer1.grid(row=3, column=5, padx=2, pady=3, ipadx=3, ipady=1)
        # Grayscale
        layer1_istilegrayscale_toggle = tk.Checkbutton(config_window, text="Grayscale", bg="#2d2f34", fg="white", selectcolor="#393a3d", variable=self.layer1_istilegrayscale, highlightthickness=0, highlightbackground="#26282d", activebackground="#26282d", activeforeground="white", indicatoron=False)
        layer1_istilegrayscale_toggle.grid(row=3, column=6, pady=3, padx=(10, 15), ipadx=2, ipady=2)

#-------# Layer 2
        layer2_label = Label(config_window, text="Layer 2:", bg="#26282d", fg="white")
        layer2_label.grid(row=4, column=0, padx=(10, 0), sticky="e")
        # Resolution
        layer2_tileresolution_entry = Entry(config_window, textvariable=self.layer2_tileresolution, borderwidth=0, fg="white", bg="#1f2023", width=10)
        layer2_tileresolution_entry.grid(row=4, column=1, padx=2, pady=3, ipadx=3, ipady=4)
        # Format
        layer2_tileformat_entry = Entry(config_window, textvariable=self.layer2_tileformat, borderwidth=0, fg="white", bg="#1f2023", width=8)
        layer2_tileformat_entry.grid(row=4, column=2, padx=2, pady=3, ipadx=3, ipady=4)
        # 8bit
        bit_depth_8_button_layer2 = tk.Radiobutton(config_window, text="8", variable=self.layer2_tilebitdepth, value=8, bg="#26282d", fg="white", selectcolor="#393a3d", indicatoron=False, activebackground="#26282d", activeforeground="white")
        bit_depth_8_button_layer2.grid(row=4, column=3, padx=(2,0), pady=3, ipadx=6, ipady=1)
        # 16bit
        bit_depth_16_button_layer2 = tk.Radiobutton(config_window, text="16", variable=self.layer2_tilebitdepth, value=16, bg="#26282d", fg="white", selectcolor="#393a3d", indicatoron=False, activebackground="#26282d", activeforeground="white")
        bit_depth_16_button_layer2.grid(row=4, column=4, padx=(0,2), pady=3, ipadx=3, ipady=1)
        # 32bit
        bit_depth_32_button_layer2 = tk.Radiobutton(config_window, text="32", variable=self.layer2_tilebitdepth, value=32, bg="#26282d", fg="white", selectcolor="#393a3d", indicatoron=False, activebackground="#26282d", activeforeground="white")
        bit_depth_32_button_layer2.grid(row=4, column=5, padx=2, pady=3, ipadx=3, ipady=1)
        # Grayscale
        layer2_istilegrayscale_toggle = tk.Checkbutton(config_window, text="Grayscale", bg="#2d2f34", fg="white", selectcolor="#393a3d", variable=self.layer2_istilegrayscale, highlightthickness=0, highlightbackground="#26282d", activebackground="#26282d", activeforeground="white", indicatoron=False)
        layer2_istilegrayscale_toggle.grid(row=4, column=6, pady=3, padx=(10, 15), ipadx=2, ipady=2)

#-------# Layer 3
        layer3_label = Label(config_window, text="Layer 3:", bg="#26282d", fg="white")
        layer3_label.grid(row=5, column=0, padx=(10, 0), sticky="e")
        # Resolution
        layer3_tileresolution_entry = Entry(config_window, textvariable=self.layer3_tileresolution, borderwidth=0, fg="white", bg="#1f2023", width=10)
        layer3_tileresolution_entry.grid(row=5, column=1, padx=2, pady=3, ipadx=3, ipady=4)
        # Format
        layer3_tileformat_entry = Entry(config_window, textvariable=self.layer3_tileformat, borderwidth=0, fg="white", bg="#1f2023", width=8)
        layer3_tileformat_entry.grid(row=5, column=2, padx=2, pady=3, ipadx=3, ipady=4)
        # 8bit
        bit_depth_8_button_layer3 = tk.Radiobutton(config_window, text="8", variable=self.layer3_tilebitdepth, value=8, bg="#26282d", fg="white", selectcolor="#393a3d", indicatoron=False, activebackground="#26282d", activeforeground="white")
        bit_depth_8_button_layer3.grid(row=5, column=3, padx=(2,0), pady=3, ipadx=6, ipady=1)
        # 16bit
        bit_depth_16_button_layer3 = tk.Radiobutton(config_window, text="16", variable=self.layer3_tilebitdepth, value=16, bg="#26282d", fg="white", selectcolor="#393a3d", indicatoron=False, activebackground="#26282d", activeforeground="white")
        bit_depth_16_button_layer3.grid(row=5, column=4, padx=(0,2), pady=3, ipadx=3, ipady=1)
        # 32bit
        bit_depth_32_button_layer3 = tk.Radiobutton(config_window, text="32", variable=self.layer3_tilebitdepth, value=32, bg="#26282d", fg="white", selectcolor="#393a3d", indicatoron=False, activebackground="#26282d", activeforeground="white")
        bit_depth_32_button_layer3.grid(row=5, column=5, padx=2, pady=3, ipadx=3, ipady=1)
        # Grayscale
        layer3_istilegrayscale_toggle = tk.Checkbutton(config_window, text="Grayscale", bg="#2d2f34", fg="white", selectcolor="#393a3d", variable=self.layer3_istilegrayscale, highlightthickness=0, highlightbackground="#26282d", activebackground="#26282d", activeforeground="white", indicatoron=False)
        layer3_istilegrayscale_toggle.grid(row=5, column=6, pady=3, padx=(10, 15), ipadx=2, ipady=2)

#-------# VColor
        vcolor_label = Label(config_window, text="Vcolor:", bg="#26282d", fg="white")
        vcolor_label.grid(row=6, column=0, padx=(10, 0), sticky="e")
        # Resolution
        vcolor_tileresolution_entry = Entry(config_window, textvariable=self.vcolor_tileresolution, borderwidth=0, fg="white", bg="#1f2023", width=10)
        vcolor_tileresolution_entry.grid(row=6, column=1, padx=2, pady=3, ipadx=3, ipady=4)
        # Format
        vcolor_tileformat_entry = Entry(config_window, textvariable=self.vcolor_tileformat, borderwidth=0, fg="white", bg="#1f2023", width=8)
        vcolor_tileformat_entry.grid(row=6, column=2, padx=2, pady=3, ipadx=3, ipady=4)
        # 8bit
        bit_depth_8_button_vcolor = tk.Radiobutton(config_window, text="8", variable=self.vcolor_tilebitdepth, value=8, bg="#26282d", fg="white", selectcolor="#393a3d", indicatoron=False, activebackground="#26282d", activeforeground="white")
        bit_depth_8_button_vcolor.grid(row=6, column=3, padx=(2,0), pady=3, ipadx=6, ipady=1)
        # 16bit
        bit_depth_16_button_vcolor = tk.Radiobutton(config_window, text="16", variable=self.vcolor_tilebitdepth, value=16, bg="#26282d", fg="white", selectcolor="#393a3d", indicatoron=False, activebackground="#26282d", activeforeground="white")
        bit_depth_16_button_vcolor.grid(row=6, column=4, padx=(0,2), pady=3, ipadx=3, ipady=1)
        # 32bit
        bit_depth_32_button_vcolor = tk.Radiobutton(config_window, text="32", variable=self.vcolor_tilebitdepth, value=32, bg="#26282d", fg="white", selectcolor="#393a3d", indicatoron=False, activebackground="#26282d", activeforeground="white")
        bit_depth_32_button_vcolor.grid(row=6, column=5, padx=2, pady=3, ipadx=3, ipady=1)
        # Grayscale
        vcolor_istilegrayscale_toggle = tk.Checkbutton(config_window, text="Grayscale", bg="#2d2f34", fg="white", selectcolor="#393a3d", variable=self.vcolor_istilegrayscale, highlightthickness=0, highlightbackground="#26282d", activebackground="#26282d", activeforeground="white", indicatoron=False)
        vcolor_istilegrayscale_toggle.grid(row=6, column=6, pady=3, padx=(10, 15), ipadx=2, ipady=2)
 
        # Close Button
        close_button = Button(config_window, text="Save and close", bg="#2d2f34", fg="white", activebackground="#393a3d", width=15, command=config_window.destroy)
        close_button.grid(row=7, column=0, columnspan=7, pady=(20,0), ipadx=3, ipady=3)

# ----------------------------------------------------------------------------------------------
# ----------------------------------------- GUI ------------------------------------------------
# -------------------------------------- Functions ---------------------------------------------
# ------------------------------------- Grid Drawing -------------------------------------------

    # 65x65 lines to create a grid of 64 squares
    def draw_grid(self):
        square_size = 8
        for i in range(0, 65):
            self.canvas.create_line(i * square_size, 0, i * square_size, 513, fill="black")
            self.canvas.create_line(0, i * square_size, 513, i * square_size, fill="black")

    # Update grid when sliders are moved
    def update_grid(self, event=None):
        square_size = 8
        map_size = self.map_size.get()
        offset_x = self.offset_x_slider.get()
        offset_y = self.offset_y_slider.get()

        # Get highlight region
        highlight_width = map_size * square_size
        highlight_height = map_size * square_size
        x0 = offset_x * square_size
        y0 = offset_y * square_size

        # Make green square cover highlight region
        highlight_rect = self.canvas.find_withtag("highlight")
        if highlight_rect:  # If it exists, change the position and size
            self.canvas.coords( highlight_rect, x0, y0, x0 + highlight_width, y0 + highlight_height)
        else:               # If it doesn't exist, create it
            self.canvas.create_rectangle(x0, y0, x0 + highlight_width, y0 + highlight_height, fill="lightgreen", outline="green", tags="highlight")

        self.canvas.tag_lower("highlight") # Make sure rectangle is behind the grid lines
            
# ----------------------------------------------------------------------------------------------
# ----------------------------------------- GUI ------------------------------------------------
# -------------------------------------- Functions ---------------------------------------------
# ------------------------------------ Process Tiles -------------------------------------------

    def start_processing(self):
        
        # Stop function if tasks are already running
        if self.is_processing:
            print("Error: Already running")
            return

        # Get variables
        input_dir = self.input_dir.get()
        output_dir = self.output_dir.get()
        map_name = self.map_name.get()
        map_size = self.map_size.get()
        offset_x = self.offset_x_slider.get()
        offset_y = self.offset_y_slider.get()
        outputnum = 0

        height_tileresolution = self.height_tileresolution.get()
        layer1_tileresolution = self.layer1_tileresolution.get()
        layer2_tileresolution = self.layer2_tileresolution.get()
        layer3_tileresolution = self.layer3_tileresolution.get()
        vcolor_tileresolution = self.vcolor_tileresolution.get()

        height_tilebitdepth = self.height_tilebitdepth.get()
        layer1_tilebitdepth = self.layer1_tilebitdepth.get()
        layer2_tilebitdepth = self.layer2_tilebitdepth.get()
        layer3_tilebitdepth = self.layer3_tilebitdepth.get()
        vcolor_tilebitdepth = self.vcolor_tilebitdepth.get()

        height_tileformat = self.height_tileformat.get()
        layer1_tileformat = self.layer1_tileformat.get()
        layer2_tileformat = self.layer2_tileformat.get()
        layer3_tileformat = self.layer3_tileformat.get()
        vcolor_tileformat = self.vcolor_tileformat.get()

        height_istilegrayscale = self.height_istilegrayscale.get()
        layer1_istilegrayscale = self.layer1_istilegrayscale.get()
        layer2_istilegrayscale = self.layer2_istilegrayscale.get()
        layer3_istilegrayscale = self.layer3_istilegrayscale.get()
        vcolor_istilegrayscale = self.vcolor_istilegrayscale.get()

        # Construct filepaths
        height_dir = os.path.join(input_dir, self.height_name.get()).replace("\\", "/")
        layer1_dir = os.path.join(input_dir, self.layer1_name.get()).replace("\\", "/")
        layer2_dir = os.path.join(input_dir, self.layer2_name.get()).replace("\\", "/")
        layer3_dir = os.path.join(input_dir, self.layer3_name.get()).replace("\\", "/")
        vcolor_dir = os.path.join(input_dir, self.vcolor_name.get()).replace("\\", "/")

        # Check if directories are set
        if os.path.exists(input_dir) and os.path.exists(output_dir):
            # Check if map name is set
            if map_name:
                try:
                    futures = []

                    # If files exist and are selected for export, create a task for each one
                    if self.height_exporttoggle.get() and self.height_name.get() and os.path.exists(height_dir):
                        futures.append((convert_height, height_dir, output_dir, map_name, map_size, offset_x, offset_y, height_tilebitdepth, height_tileformat, height_istilegrayscale, height_tileresolution))
                    if self.layer1_exporttoggle.get() and self.layer1_name.get() and os.path.exists(layer1_dir):
                        futures.append((convert_layer1, layer1_dir, output_dir, map_name, map_size, offset_x, offset_y, layer1_tilebitdepth, layer1_tileformat, layer1_istilegrayscale, layer1_tileresolution))
                    if self.layer2_exporttoggle.get() and self.layer2_name.get() and os.path.exists(layer2_dir):
                        futures.append((convert_layer2, layer2_dir, output_dir, map_name, map_size, offset_x, offset_y, layer2_tilebitdepth, layer2_tileformat, layer2_istilegrayscale, layer2_tileresolution))
                    if self.layer3_exporttoggle.get() and self.layer3_name.get() and os.path.exists(layer3_dir):
                        futures.append((convert_layer3, layer3_dir, output_dir, map_name, map_size, offset_x, offset_y, layer3_tilebitdepth, layer3_tileformat, layer3_istilegrayscale, layer3_tileresolution))
                    if self.vcolor_exporttoggle.get() and self.vcolor_name.get() and os.path.exists(vcolor_dir):
                        futures.append((convert_vcolor, vcolor_dir, output_dir, map_name, map_size, offset_x, offset_y, vcolor_tilebitdepth, vcolor_tileformat, vcolor_istilegrayscale, vcolor_tileresolution))
                    
                    # If there are tasks, add them to the processing pool
                    if futures:
                        def process_tasks():

                            # Create generic labels for printing to log
                            file_info = [
                                ("Height", self.height_exporttoggle.get(), self.height_name.get()),
                                ("Layer1", self.layer1_exporttoggle.get(), self.layer1_name.get()),
                                ("Layer2", self.layer2_exporttoggle.get(), self.layer2_name.get()),
                                ("Layer3", self.layer3_exporttoggle.get(), self.layer3_name.get()),
                                ("Vcolor", self.vcolor_exporttoggle.get(), self.vcolor_name.get())
                            ]
                            
                            # Check if given filename has an extension
                            def has_file_extension(name):
                                return name.endswith(('.txt', '.csv', '.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif'))
                            
                            # If an extension is used that means the file will get processed so add the generic label to the starting message array
                            process_files = [
                                label for label, export_flag, file_name in file_info
                                if export_flag and file_name and has_file_extension(file_name)
                            ]

                            # Print starting message
                            print("----------------------------" + "\n" + "Processing:", ", ".join(process_files))
                            self.is_processing = True
                            start_time = time.time()

#---------------------------# Start processing
                            with ThreadPoolExecutor() as executor:
                                nonlocal outputnum
                                for func, *args in futures:
                                    executor.submit(func, *args)
                                    outputnum += 1  # Count number of processed files
#---------------------------# End processing

                            # Print ending messages
                            self.is_processing = False
                            end_time = time.time() - start_time
                            print(f"Complete! (Time - {end_time:.2f}s)")
                            print((map_size * map_size) * outputnum, "tiles sent to:", output_dir)

                        # Do all this in a separate thread to avoid freezing the GUI
                        task_thread = threading.Thread(target=process_tasks)
                        task_thread.start()
                    else:
                        print("Error: No files selected or missing file extension")
                except Exception as e:
                    print(f"Error: {e}")
            else:
                print("Error: No map name")
        else:
            print("Error: Input/output directory not set")

# ----------------------------------------------------------------------------------------------
# ----------------------------------------- GUI ------------------------------------------------
# -------------------------------------- Functions ---------------------------------------------
# ------------------------------------ Loading/Saving  -----------------------------------------

    def on_close(self):
        # Save settings on close
        self.save_settings()
        self.root.destroy()

    def save_settings(self):
        # Save settings in plain text file
        with open("savedsettings.txt", "w") as f:
            # Saving existing settings
            f.write(self.input_dir.get() + "\n")
            f.write(self.output_dir.get() + "\n")
            f.write(self.map_name.get() + "\n")
            f.write(str(self.map_size.get()) + "\n")  # Convert int to str
            f.write(str(self.map_offsetx.get()) + "\n")  # Convert int to str
            f.write(str(self.map_offsety.get()) + "\n")  # Convert int to str
            f.write(self.height_name.get() + "\n")
            f.write(self.layer1_name.get() + "\n")
            f.write(self.layer2_name.get() + "\n")
            f.write(self.layer3_name.get() + "\n")
            f.write(self.vcolor_name.get() + "\n")
            f.write(str(self.height_exporttoggle.get()) + "\n")
            f.write(str(self.layer1_exporttoggle.get()) + "\n")
            f.write(str(self.layer2_exporttoggle.get()) + "\n")
            f.write(str(self.layer3_exporttoggle.get()) + "\n")
            f.write(str(self.vcolor_exporttoggle.get()) + "\n")
            f.write(self.height_tileresolution.get() + "\n")
            f.write(self.layer1_tileresolution.get() + "\n")
            f.write(self.layer2_tileresolution.get() + "\n")
            f.write(self.layer3_tileresolution.get() + "\n")
            f.write(self.vcolor_tileresolution.get() + "\n")
            f.write(self.height_tileformat.get() + "\n")
            f.write(self.layer1_tileformat.get() + "\n")
            f.write(self.layer2_tileformat.get() + "\n")
            f.write(self.layer3_tileformat.get() + "\n")
            f.write(self.vcolor_tileformat.get() + "\n")
            f.write(str(self.height_tilebitdepth.get()) + "\n")
            f.write(str(self.layer1_tilebitdepth.get()) + "\n")
            f.write(str(self.layer2_tilebitdepth.get()) + "\n")
            f.write(str(self.layer3_tilebitdepth.get()) + "\n")
            f.write(str(self.vcolor_tilebitdepth.get()) + "\n")
            f.write(str(self.height_istilegrayscale.get()) + "\n")
            f.write(str(self.layer1_istilegrayscale.get()) + "\n")
            f.write(str(self.layer2_istilegrayscale.get()) + "\n")
            f.write(str(self.layer3_istilegrayscale.get()) + "\n")
            f.write(str(self.vcolor_istilegrayscale.get()) + "\n")

    def load_settings(self):
        # If settings file exists, load from it
        if os.path.exists("savedsettings.txt"):
            with open("savedsettings.txt", "r") as f:
                self.input_dir.set(f.readline().strip())
                self.output_dir.set(f.readline().strip())
                self.map_name.set(f.readline().strip())
                self.map_size.set(f.readline().strip())
                self.map_offsetx.set(f.readline().strip())
                self.map_offsety.set(f.readline().strip())
                self.height_name.set(f.readline().strip())
                self.layer1_name.set(f.readline().strip())
                self.layer2_name.set(f.readline().strip())
                self.layer3_name.set(f.readline().strip())
                self.vcolor_name.set(f.readline().strip())
                height_exporttoggle_line = f.readline().strip()
                self.height_exporttoggle.set(int(height_exporttoggle_line) if height_exporttoggle_line else 0)
                layer1_exporttoggle_line = f.readline().strip()
                self.layer1_exporttoggle.set(int(layer1_exporttoggle_line) if layer1_exporttoggle_line else 0)
                layer2_exporttoggle_line = f.readline().strip()
                self.layer2_exporttoggle.set(int(layer2_exporttoggle_line) if layer2_exporttoggle_line else 0)
                layer3_exporttoggle_line = f.readline().strip()
                self.layer3_exporttoggle.set(int(layer3_exporttoggle_line) if layer3_exporttoggle_line else 0)
                vcolor_exporttoggle_line = f.readline().strip()
                self.vcolor_exporttoggle.set(int(vcolor_exporttoggle_line) if vcolor_exporttoggle_line else 0)
                self.height_tileresolution.set(f.readline().strip())
                self.layer1_tileresolution.set(f.readline().strip())
                self.layer2_tileresolution.set(f.readline().strip())
                self.layer3_tileresolution.set(f.readline().strip())
                self.vcolor_tileresolution.set(f.readline().strip())
                self.height_tileformat.set(f.readline().strip())
                self.layer1_tileformat.set(f.readline().strip())
                self.layer2_tileformat.set(f.readline().strip())
                self.layer3_tileformat.set(f.readline().strip())
                self.vcolor_tileformat.set(f.readline().strip())
                height_tilebitdepth_line = f.readline().strip()
                self.height_tilebitdepth.set(int(height_tilebitdepth_line) if height_tilebitdepth_line else 16)
                layer1_tilebitdepth_line = f.readline().strip()
                self.layer1_tilebitdepth.set(int(layer1_tilebitdepth_line) if layer1_tilebitdepth_line else 8)
                layer2_tilebitdepth_line = f.readline().strip()
                self.layer2_tilebitdepth.set(int(layer2_tilebitdepth_line) if layer2_tilebitdepth_line else 8)
                layer3_tilebitdepth_line = f.readline().strip()
                self.layer3_tilebitdepth.set(int(layer3_tilebitdepth_line) if layer3_tilebitdepth_line else 8)
                vcolor_tilebitdepth_line = f.readline().strip()
                self.vcolor_tilebitdepth.set(int(vcolor_tilebitdepth_line) if vcolor_tilebitdepth_line else 8)
                height_istilegrayscale_line = f.readline().strip()
                self.height_istilegrayscale.set(int(height_istilegrayscale_line) if height_istilegrayscale_line else 1)
                layer1_istilegrayscale_line = f.readline().strip()
                self.layer1_istilegrayscale.set(int(layer1_istilegrayscale_line) if layer1_istilegrayscale_line else 1)
                layer2_istilegrayscale_line = f.readline().strip()
                self.layer2_istilegrayscale.set(int(layer2_istilegrayscale_line) if layer2_istilegrayscale_line else 1)
                layer3_istilegrayscale_line = f.readline().strip()
                self.layer3_istilegrayscale.set(int(layer3_istilegrayscale_line) if layer3_istilegrayscale_line else 1)
                vcolor_istilegrayscale_line = f.readline().strip()
                self.vcolor_istilegrayscale.set(int(vcolor_istilegrayscale_line) if vcolor_istilegrayscale_line else 0)
            print("Loaded settings:", self.map_name.get()) if self.map_name.get() else None
        else:

            # If file doesn't exist, create it
            with open("savedsettings.txt", "w") as f:
                f.write("\n" * 16)  # Fill new config with placeholder lines
            print("savedsettings.txt not found, creating a new one...")
        
        # Set Slider Positions
        self.map_size.set(self.map_size.get())
        self.offset_x_slider.set(self.map_offsetx.get())
        self.offset_y_slider.set(self.map_offsety.get())
                
if __name__ == "__main__":
    root = tk.Tk()
    root.resizable(False, False)
    app = tkGUI(root)
    root.mainloop()

# ----------------------------------------- GUI ------------------------------------------------
# ----------------------------------------------------------------------------------------------
