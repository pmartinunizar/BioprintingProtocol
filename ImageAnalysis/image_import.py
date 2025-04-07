import cv2
import json
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from utils import Reset_Zoom, Update_Image, Reset_Script
import state
import os

##################################################
#            Image Importing Functions           #
##################################################

##################################################
#             Function: Import_Image             #
##################################################

def Import_Image(Root):
    
    """
    
    Import an image and resize it to fit the display frame.
    
    This function allows the user to import an image manually in a specific folder and resize it 
    to fit the display frame dimensions.
    
    Args:
    
        Root [tk.Tk]: The main Tkinter window object.
        
    Returns:

        Nothing.
    
    """   
    
    # Reset the workflow to start fresh with a new image.
    
    Reset_Script()
    
    # Open a file dialog to select an image file.
    
    Image_Path = tk.filedialog.askopenfilename()
    
    # Check if the image path is not empty.
    
    if Image_Path:
        
        # Load the image using OpenCV.
        
        state.Imported_Image = cv2.imread(Image_Path)
        
        # Check if the image was loaded successfully.
        
        if state.Imported_Image is None:
            
            print("Failed to load image.")
            return

        # Convert the image to grayscale.
        
        state.Gray_Image = cv2.cvtColor(state.Imported_Image, cv2.COLOR_BGR2GRAY)
        
        # Equalize the histogram of the grayscale image. This enhances the contrast of the image.
          
        state.Gray_Image = cv2.equalizeHist(state.Gray_Image)
        
        # Get the image label dimemensions.
        
        state.Image_Label_Width = state.Image_Label.winfo_width()
        state.Image_Label_Height = state.Image_Label.winfo_height()

        # Resize the image to fit the frame dimensions while maintaining aspect ratio
        
        state.Gray_Image_Height, state.Gray_Image_Width = state.Gray_Image.shape[:2]
        state.Gray_Image_Ratio = state.Gray_Image_Width  / state.Gray_Image_Height

        if state.Gray_Image_Width > state.Image_Label_Width or state.Gray_Image_Height > state.Image_Label_Height:
            
            if state.Gray_Image_Ratio > 1: 
                
                New_Width = state.Image_Label_Width
                New_Height = int(New_Width / state.Gray_Image_Ratio)
                
            else:  
                
                New_Height = state.Image_Label_Height
                New_Width = int(New_Height * state.Gray_Image_Ratio)
                
        else:
            
            New_Width, New_Height = state.Gray_Image_Width, state.Gray_Image_Height  

        state.Resized_Image = cv2.resize(state.Gray_Image, (New_Width, New_Height), interpolation=cv2.INTER_AREA)

        # Store the resized image for further processing.
        
        state.Base_Image = state.Resized_Image.copy()
        state.Current_Image = state.Resized_Image.copy()
    
        # Reset the zoom level and update the image.                

        Reset_Zoom()  
        Update_Image(state.Current_Image)  
        
        print("Image imported and resized to fit the display frame.")
        
        # Enable the buttons for further processing.
        
        state.Well_Info_Button.config(state=tk.NORMAL)
        state.Calibrate_Button.config(state=tk.NORMAL)
        state.Process_Button.config(state=tk.NORMAL)
        state.Import_Flag = True 
        
    else:        
        print("No image selected.")


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

##################################################
#            JSON Importing Functions            #
##################################################

##################################################
#              Function: Read_JSON               #
##################################################

def Read_JSON(Manufacturer, Well_Number):
    
    """
    
    Read the JSON file to get the diameter of the well plate.
    
    This function reads the JSON file 'WellPlateInfo.json' to get the diameter of the well plate based 
    on the Manufacturer and the number of wells.
    
    Args:
    
        Manufacturer [str]: The manufacturer brand of the well plate.
        Well_Number [int]: The number of wells in the well plate.
        
    Returns:

        Nothing.
    
    """
    
    # Read the JSON file with an specific name stored in the same file as this script.
    
    Load_JSON_File()

    # Check if the Manufacturer and Well_Number are in the JSON file.
    
    if Manufacturer not in state.JSON_File or str(Well_Number) not in state.JSON_File[Manufacturer]:
        
        raise ValueError(f"Parameters for {Manufacturer} with {Well_Number} wells not found in the JSON file.")
    
    # Get the diameter of the well plate based on the Manufacturer and Well_Number from the JSON file.
    
    state.Well_Info = state.JSON_File[Manufacturer][str(Well_Number)]
    state.Well_Diameter = state.Well_Info.get("Diameter")
    
    if state.Well_Diameter is None:
        
        raise ValueError(f"Diameter not found for {Manufacturer} with {Well_Number} wells in the JSON file.")

##################################################
#            Function: Load_JSON_File            #
##################################################

def Load_JSON_File():
    
    """
    
    Load the JSON file containing well plate information if it hasn't been loaded already.

    Args:
        
        Nothing.

    Returns:
    
        Nothing.
    
    """
    # Get the directory of the script and the JSON file path.
    
    Direction = os.path.dirname(os.path.abspath(__file__))
    File_Path = os.path.join(Direction, 'WellPlateInfo.json')

    # Check if the JSON file has been loaded already and load it if not.
    
    if state.JSON_File is None:
        
        try:
            
            with open(File_Path, 'r') as file:
                
                state.JSON_File = json.load(file)
                
        except FileNotFoundError:
            
            raise ValueError("WellPlateInfo.json file not found.")
        
        except json.JSONDecodeError:
            
            raise ValueError("Error decoding JSON file.")  


##################################################
#         Function: Select_Well_Plate            #
##################################################

def Select_Well_Plate():
    
    """
    
    Ask the user for the manufacturer and the well number of the plate being used by comboboxes,
    and read the corresponding diameter from the JSON file.
    
    This function creates a new window with comboboxes to select the Manufacturer and the number of wells.
    
    Args:
    
        Nothing.
            
    Returns:
    
        Nothing.
    
    """
    
    # Get the list of manufacturers from the JSON file.
    
    Load_JSON_File()
        
    Manufacturers_List = list(state.JSON_File.keys())
    
    # Create a new window to select the Manufacturer and the number of wells.

    Top = tk.Toplevel()
    Top.title("Select well plate information")
    
    tk.Label(Top, text="Manufacturer:").grid(row=0, column=0, padx=10, pady=5)
    Manufacturers_Variable = tk.StringVar()
    Manufacturers_ComboBox = ttk.Combobox(Top, textvariable=Manufacturers_Variable, values=Manufacturers_List, state="readonly")
    Manufacturers_ComboBox.grid(row=0, column=1, padx=10, pady=5)
    
    tk.Label(Top, text="Number of Wells:").grid(row=1, column=0, padx=10, pady=5)
    Number_Variable = tk.StringVar()
    Number_ComboBox = ttk.Combobox(Top, textvariable=Number_Variable, state="readonly")
    Number_ComboBox.grid(row=1, column=1, padx=10, pady=5)

    Manufacturers_ComboBox.bind("<<ComboboxSelected>>", lambda e: Update_Well_Number(Manufacturers_Variable, Number_ComboBox, state.JSON_File))

    Submit_Button = tk.Button(Top, text="Submit", command=lambda: Well_Info_Submit(Manufacturers_Variable, Number_Variable, Top))
    Submit_Button.grid(row=2, columnspan=2, pady=10)

    Top.mainloop()


##################################################
#         Function: Update_Well_Number           #
##################################################

def Update_Well_Number(Manufacturers_Variable, Number_ComboBox, Data):
    
    """
    
    Update the well numbers combobox based on the selected manufacturer according to the JSON file.
    
    Args:
        
            Manufacturers_Variable [tk.StringVar]: The selected Manufacturer.
            Number_ComboBox [ttk.Combobox]: The combobox for selecting the number of wells.
            Data [dict]: The dictionary containing the well plate information.
            
    Returns:
        
                Nothing.
    
    """
    # Get the selected Manufacturer from the combobox.
    
    Selected_Manufacturer = Manufacturers_Variable.get()
    
    # Check if the selected Manufacturer is in the JSON file and update the numbers in the combobox.
    
    if Selected_Manufacturer in Data:
        
        Imported_Numbers = list(Data[Selected_Manufacturer].keys())
        Number_ComboBox.config(values=Imported_Numbers)

##################################################
#         Function: Well_Info_Submit             #
##################################################

def Well_Info_Submit(Manufacturers_Variable, Number_Variable, Top):
    
    """
    
    Handle the submission of the Manufacturer and Well_Number of wells.
    
    Args:
        
            Manufacturers_Variable [tk.StringVar]: The selected Manufacturer.
            Number_Variable [tk.StringVar]: The selected number of wells.
            Top [tk.Toplevel]: The top level window.
            
    Returns:
    
            Nothing.
    
    """
    
    Manufacturer = Manufacturers_Variable.get()
    Well_Number = Number_Variable.get()
    
    if Manufacturer and Well_Number:
        
        try:
            
            Read_JSON(Manufacturer, Well_Number)
            print(f"Diameter from JSON: {state.Well_Diameter}")
            Top.destroy()
            state.Calibrate_Button.config(state=tk.NORMAL)  
            
        except ValueError as e:
            
            messagebox.showerror("Error", str(e))
            
    else:
        
        messagebox.showerror("Error", "Manufacturer and Well Number of wells are required.")