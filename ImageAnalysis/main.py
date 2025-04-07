"""


        :::   :::    ::::::::  :::::::::  ::::::::::               ::::::::  :::::::::   ::::::::  :::    ::: ::::::::: 
      :+:+: :+:+:  :+:    :+: :+:    :+: :+:                     :+:    :+: :+:    :+: :+:    :+: :+:    :+: :+:    :+: 
    +:+ +:+:+ +:+       +:+  +:+    +:+ +:+                     +:+        +:+    +:+ +:+    +:+ +:+    +:+ +:+    +:+  
   +#+  +:+  +#+     +#+    +#++:++#+  +#++:++#  +#++:++#++:++ :#:        +#++:++#:  +#+    +:+ +#+    +:+ +#++:++#+    
  +#+       +#+   +#+      +#+    +#+ +#+                     +#+   +#+# +#+    +#+ +#+    +#+ +#+    +#+ +#+           
 #+#       #+#  #+#       #+#    #+# #+#                     #+#    #+# #+#    #+# #+#    #+# #+#    #+# #+#            
###       ### ########## #########  ##########               ########  ###    ###  ########   ########  ###     



Author: Pablo Martín Compaired 
Contact: pablo.martin@unizar.es
Department: M2BE
University: Zaragoza University [UNIZAR]
Version: 1.0
Date: Aug 30, 2024

Description:

    This application is designed to process images different bioprinting test and measure these values in a simple way.

Usage:
    
    1. Import an image.
    2. Select the well plate used during the test.
    3. Calibrate the image.
    4. Process the image.
    5. Create a ROI.
    6. Measure the ROI.
    
License:
    
    This project is licensed under the MIT License. See the LICENSE file for details.

Future updates:

    - Add multiple images import mode. So after finishing of one image the next one is loaded automatically.
    - When reading the program type at the beginning of the program like in interface assign to a new parameters RightClick, LeftClick and MiddleClick the values of the buttons. So i dont have to read the program to know the values of the buttons. Like RightClick = <ButtonPress-2> and so on.
    - Develop a function to automatically detect the filament shape and make a ROI around it. Maybe a deep learning model.

"""

################################################################################################
# Main libraries import:
import tkinter as tk
import state
import platform
################################################################################################
# Main program modules import:
from image_import import Import_Image, Select_Well_Plate
from image_processing import Processing_Image, Brush_Tool
from roi_handler import Pore_Events, Filament_Events
from measure import Pore_Measure, Filament_Measure
from utils import Bind_Zooming, Closing_App
from interface import Setup_Interface, Custom_Interface, Setup_UI
from calibrating import Calibrate
################################################################################################


# Main function to initialize the application

def main():
    
    # Initialize the Tkinter root. This is the main window of the application.
    
    Root = tk.Tk()
    state.Root = Root  

    # Detect the platform used in this machine.

    state.Platform = platform.system()  
    print("Platform used in this machine:", state.Platform)

    # Create a custom interface settings object and apply it to the main window.
    
    Interface_Settings = Custom_Interface()
    Setup_Interface(state.Root, Interface_Settings)
    Setup_UI(state.Root, Interface_Settings, Import_Image, Select_Well_Plate, Calibrate, Brush_Tool, Processing_Image, Pore_Events, Pore_Measure, Filament_Events, Filament_Measure) 

    # Bind the zooming function to the main window.
    
    Bind_Zooming()  

    # Handle the window close event.
    
    state.Root.protocol("WM_DELETE_WINDOW", Closing_App(Root))  
    state.Root.mainloop()  

# Main function to run the application.

if __name__ == "__main__":
    main()
    
################################################################################################