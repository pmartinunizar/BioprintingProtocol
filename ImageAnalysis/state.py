# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# This file contains the global variables used in the application.

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Variables related to interface elements.

Root = None # Root window of the application. 
Platform = None # Platform on which the application is running.
Control_Frame = None # Frame for holding the control buttons.
Image_Frame = None # Frame for holding the image display area.
Image_Label = None # Label for displaying the image.
Image_Label_Width = None # Width of the image label.
Image_Label_Height = None # Height of the image label.
Import_Button = None # Button for importing images.
Well_Info_Button = None # Button for entering well information.
Calibrate_Button = None # Button for calibrating the system.
Process_Button = None # Button for processing the image.
Correction_Button = None # Button for enabling the brush-tool feature.
Pore_Button = None # Button for selecting pores.
Measure_Pore_Button = None # Button for measuring the pores.
Filament_Button = None # Button for selecting filaments.
Measure_Filament_Button = None # Button for measuring the filaments.

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Variables for storing well plate information.

Manufacturer = None # Manufacturer of the plate.
Well_Number = None # Number of wells in the plate.
JSON_File = None # JSON file containing well information.
Well_Info = None # Dictionary containing well information.
Well_Diameter = None  # Diameter of the well in mm.

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Variables related to the image files.

Imported_Image = None # Image imported by the user.
Gray_Image = None # Grayscale image of the imported image.
Gray_Image_Height = None # Height of the grayscale image.
Gray_Image_Width = None # Width of the grayscale image.
Gray_Image_Ratio = None # Aspect ratio of the grayscale image.
Resized_Image = None # Resized grayscale image to fit the display frame.
Base_Image = None # Base image for processing.
Current_Image = None # Current image displayed on the screen.
Calibration_Temporal_Image = None # Temporal image for calibration.
Processed_Image = None # Processed image for display.
Pore_ROI_Image = None # Image for displaying the pores.
Filament_ROI_Image = None # Image for displaying filaments.

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Variables for integrating the image zooming functionality.

Zoom = None # Zoom level of the image.
X_Offset = None # X-axis offset for panning.
Y_Offset = None # Y-axis offset for panning.
Zoomed_Image = None # Zoomed image for display.
Minimum_Zoom = 1 # Set the minimum zoom level to 1.
Maximum_Zoom = 50 # Set the maximum zoom level to 5.

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Variables for bind events.

X_Coordinate = None # X-coordinate of the mouse pointer.
Y_Coordinate = None # Y-coordinate of the mouse pointer.

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Variables for calibration process.

Circle_Starting_X = 0 # Starting X-coordinate of the circle.
Circle_Starting_Y = 0 # Starting Y-coordinate of the circle.
Circle_Ending_X = 0 # Ending X-coordinate of the circle.
Circle_Ending_Y = 0 # Ending Y-coordinate of the circle.
Drawing_Circle = False # Flag to indicate if the circle is being drawn.
Resizing_Circle = False # Flag to indicate if the circle is being resized.
Moving_Circle = False # Flag to indicate if the circle is being moved.
Circle_Center = None # Center of the circle.
Circle_Radius = None # Radius of the circle.
Difference_X = None # Difference in X-coordinates.
Difference_Y = None # Difference in Y-coordinates.
New_Center = None # New center of the circle.
Cropped_Image = None # Cropped image around the circle for calibration.
Pixel_Conversion = None # Pixel conversion factor for calibration in mm.
CirclePixelThickness = 4  # Set the default thickness to 5 pixels.

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Variables for roi selection process and pore measurement.

ROIS_List = [] # List of ROIs selected by the user.
Pore_Results = [] # List of results for pore measurements.
Filament_List = [] # List of filaments selected by the user.
Final_Filament_List = [] # List with the final filaments used.
Filament_Mean_Thickness = 0 # Mean thickness of the filaments.

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Variables for image processing.

Binary_Mask = None # Binary mask of the image.
Brush_Size = 10 # Default brush size for the brush tool.
Brush_Color = (0,0,0) # Default brush color for the brush tool.

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Variables for flagging events.

Import_Flag = False # Flag to indicate if an image has been imported.
Well_Info_Flag  = False # Flag to indicate if well information has been entered.
Calibrate_Flag = False # Flag to indicate if the system has been calibrated.
Correction_Flag  = False # Flag to indicate if the image has been corrected.
Procession_Flag = False # Flag to indicate if the image has been processed.
Pore_ROI_Flag = False # Flag to indicate if the ROIs have been selected.
Pore_Measure_Flag = False # Flag to indicate if the pores have been measured.
Filament_ROI_Flag = False # Flag to indicate if the filaments have been selected.
Filament_Measure_Flag = False # Flag to indicate if the filaments have been measured.
Distance_Map_Generated = False # Flag to indicate if the distance map has been generated.
Thickness_Map_Image = None # Image for displaying the distance map.

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
