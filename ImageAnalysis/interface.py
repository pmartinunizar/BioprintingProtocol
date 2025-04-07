from tkinter import ttk  
import state
import tkinter as tk


##################################################
#          Function: Setup_Interface             #
##################################################

def Setup_Interface(Root, Interface_Settings):
    
    """
    
    Set up the interface for the Image Processing Tool application.
    
    This function configures the main window's size, title, and background color. 
    The main style theme is set based on the current platform used.
    
    Args:
    
        Root [tk.Tk]: The main Tkinter window object.
        Interface_Settings [dict]: A dictionary containing display settings for the application.
        
    Returns:
    
        Nothing.
                
    """
    
    # Set the window size, title, and background color.
    
    Root.geometry("1280x720")
    Root.title("Image Processing Tool")
    Root.configure(bg=Interface_Settings["Label_Background_Color"])     

    # Set the style theme based on the platform.
    
    Style = ttk.Style()
    
    if state.Platform == "Windows":
        
        Style.theme_use('vista')
    
    elif state.Platform == "Darwin":
        
        Style.theme_use('clam')
    
    else:
        
        Style.theme_use('alt')  

    # Configure the appearance of buttons with the custom style.
    
    Style.configure("Custom.TButton", 
                    font=Interface_Settings["Button_Font"], 
                    padding=6, 
                    background=Interface_Settings["Button_Background_Color"],
                    foreground=Interface_Settings["Button_Font_Color"], 
                    borderwidth=2,
                    relief="raised")

    # Adjust the buttons appearance when hovered or pressed.
    
    Style.map("Custom.TButton",
              background=[('active', 'lightgray'), ('pressed', 'black')],
              foreground=[('pressed', 'black'), ('active', 'black')],
              relief=[('pressed', 'sunken'), ('!pressed', 'raised')])

    # Configure the labels appearance.
    
    Style.configure("Custom.TLabel", 
                    font=Interface_Settings["Label_Font"], 
                    background=Interface_Settings["Label_Background_Color"])

    # Configure the background color for the frames.
    
    Style.configure("TFrame", background=Interface_Settings["Label_Background_Color"])
    
##################################################
#         Function: Custom_Interface             #
##################################################

def Custom_Interface():
    
    """
    
    Define and return the configuration settings for the display elements.
    
    This function specifies the font, background color, and other settings for the display elements.
    
    Args:
    
        None.
    
    Returns:
        
            Interface_Settings [dict]: A dictionary containing the display settings for the application.
            
                - Image_Background_Color: The background color for the image frame.
                - Button_Background_Color: The background color for buttons.
                - Button_Font_Color: The font color for buttons.
                - Label_Background_Color: The background color for labels.
                - Label_Font_Color: The font color for labels.
                - Button_Font: The font settings for buttons.
                - Label_Font: The font settings for labels.
                
    """
    
    # Define the display settings for the application.
    
    Interface_Settings = {
        "Image_Background_Color": "white",
        "Button_Background_Color": "white",  
        "Button_Font_Color": "black",  
        "Label_Background_Color": "gray",
        "Label_Font_Color": "black",
        "Button_Font": ("Times", 12),
        "Label_Font": ("Times", 10, "bold")    }
    
    return Interface_Settings

##################################################
#               Function: Setup_UI               #
##################################################

def Setup_UI(Root, Interface_Settings, Import_Image, Select_Well_Plate, Calibrate, Brush_Tool, Processing_Image, Pore_Selection, Pore_Measure, Filament_Selection, Filament_Measure):
   
    """
    
    Set up the main UI elements like control frames, image display area, and buttons.
    
    Args:
    
        Root [tk.Tk]: The main Tkinter window object.
        Interface_Settings [dict]: A dictionary containing display settings for the application.
        Import_Image [function]: Function to import and process images.
        Select_Well_Plate [function]: Function to ask well information.
        Calibrate [function]: Function to calibrate the system.
        Brush_Tool [function]: Function to manually correct the image by painting pixels.
        Processing_Image [function]: Function to process images.
        Pore_Selection [function]: Function to select pores.
        Pore_Measure [function]: Function to perform printability measurements on pores.
        Filament_Selection [function]: Function to select filaments.
        Filament_Measure [function]: Function to measure the thickness of filaments.
        
    Returns:
    
        Nothing.
        
    """

    # Create the control frame
    
    state.Control_Frame = ttk.Frame(Root, padding="10")
    state.Control_Frame.grid(row=0, column=0, sticky=(tk.N, tk.W, tk.S))
    
    # Configure the grid layout for the Control_Frame to evenly distribute buttons
    
    for i in range(9):  
        state.Control_Frame.grid_rowconfigure(i, weight=1)

    state.Control_Frame.grid_columnconfigure(0, weight=1)

    
    state.Image_Frame = ttk.Frame(Root, padding=(0, 0))
    state.Image_Frame.grid(row=0, column=1, sticky=(tk.N, tk.W, tk.E, tk.S))

    # Create a label for displaying the image and add it to the image frame centered.
    
    state.Image_Label = ttk.Label(state.Image_Frame)
    state.Image_Label.grid(row=0, column=0, sticky=(tk.N, tk.W, tk.E, tk.S))
    state.Image_Label.config(anchor="center")
    
    # Configure the grid layout for the main window and frames.

    Root.grid_rowconfigure(0, weight=1)
    Root.grid_columnconfigure(1, weight=1)

    state.Image_Frame.grid_rowconfigure(0, weight=1)
    state.Image_Frame.grid_columnconfigure(0, weight=1)

    # Create buttons for importing, processing, and measuring images.

    state.Import_Button = ttk.Button(state.Control_Frame, text="Import Image", command=lambda: Import_Image(state.Root), style="Custom.TButton")
    state.Import_Button.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

    state.Well_Info_Button = ttk.Button(state.Control_Frame, text="Well Info", command=Select_Well_Plate, state=tk.DISABLED, style="Custom.TButton")
    state.Well_Info_Button.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

    state.Calibrate_Button = ttk.Button(state.Control_Frame, text="Calibrate", command=lambda: Calibrate(state.Root), state=tk.DISABLED, style="Custom.TButton")
    state.Calibrate_Button.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")

    state.Correction_Button = ttk.Button(state.Control_Frame, text="Correct", command=Brush_Tool , state=tk.NORMAL, style="Custom.TButton")
    state.Correction_Button.grid(row=3, column=0, padx=5, pady=5, sticky="nsew")

    state.Process_Button = ttk.Button(state.Control_Frame, text="Process Image", command=Processing_Image, state=tk.DISABLED, style="Custom.TButton")
    state.Process_Button.grid(row=4, column=0, padx=5, pady=5, sticky="nsew")

    state.Pore_Button = ttk.Button(state.Control_Frame, text="Select Pores", command=Pore_Selection, state=tk.DISABLED, style="Custom.TButton")
    state.Pore_Button.grid(row=5, column=0, padx=5, pady=5, sticky="nsew")

    state.Measure_Pore_Button = ttk.Button(state.Control_Frame, text="Printability", command=Pore_Measure, state=tk.DISABLED, style="Custom.TButton")
    state.Measure_Pore_Button.grid(row=6, column=0, padx=5, pady=5, sticky="nsew")

    state.Filament_Button = ttk.Button(state.Control_Frame, text="Select Filament", command=Filament_Selection, state=tk.DISABLED, style="Custom.TButton")
    state.Filament_Button.grid(row=7, column=0, padx=5, pady=5, sticky="nsew")

    state.Measure_Filament_Button = ttk.Button(state.Control_Frame, text="Local Thickness", command=Filament_Measure, state=tk.DISABLED, style="Custom.TButton")
    state.Measure_Filament_Button.grid(row=8, column=0, padx=5, pady=5, sticky="nsew")