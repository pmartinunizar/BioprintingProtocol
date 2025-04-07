import cv2
import numpy as np
import state
import tkinter as tk
from PIL import Image, ImageTk


##################################################
#             Zoom Feature Functions             #
##################################################

##################################################
#              Function: Reset_Zoom              #
##################################################

def Reset_Zoom():
    
    """
    
    Reset the zoom level and offsets to their default values.
    
    Args:
    
        None.
                
    Returns:

        Nothing.
    
    """   
    
    # Reset the zoom level and offsets to their default values and update the image. 
    
    state.Zoom = 1
    state.X_Offset = 0
    state.Y_Offset = 0
    
    # Update the image with the new zoom level and offsets.
    
    if state.Current_Image is not None:
        
        state.Zoomed_Image = state.Current_Image.copy()
        
        Update_Image(state.Zoomed_Image)



##################################################
#              Function: Zoom_Image              #
##################################################

def Zoom_Image(event):
    
    """
    
    Zoom in or out on the image using the mouse wheel.
    
    The zoom feature is implemented by adjusting the zoom level and offsets based on the mouse wheel movement.
    The image is then resized and displayed with the new zoom level and offsets.
        
    Args:
    
        event [tk.Event]: The mouse wheel event.
                
    Returns:

        Nothing.
    
    """   
    
    # Check if there is an image to zoom in on. 
    
    if state.Current_Image is None:
        
        return

    # Get the size of the displayed image.

    Image_Height, Image_Width = state.Current_Image.shape[:2]

    # Get the actual coordinates of the mouse event in the x and y directions.
    
    state.X_Coordinate, state.Y_Coordinate = Get_Coordinates(event)

    # Calculate the new zoom level and offsets based on the mouse wheel movement.

    if event.delta > 0:  
        
        # Zoom in on the image.
        # Increase the zoom level by 10% and ensure it does not exceed the maximum zoom level.
        
        state.Zoom *= 1.1
        state.Zoom = min(state.Zoom, state.Maximum_Zoom)
        
    else:  
        
        # Zoom out.
        # Decrease the zoom level by 10% and ensure it does not go below the minimum zoom level.
        
        state.Zoom /= 1.1
        state.Zoom = max(state.Zoom, state.Minimum_Zoom)

    # Calculate the new image width and height based on the zoom level.
    
    New_Image_Width = round(Image_Width / state.Zoom)
    New_Image_Height = round(Image_Height / state.Zoom)

    # Calculate the new offsets based on the zoom level and the actual coordinates.
    
    state.X_Offset = round(state.X_Coordinate - (state.X_Coordinate / state.Zoom))
    state.Y_Offset = round(state.Y_Coordinate - (state.Y_Coordinate / state.Zoom))

    # Ensure the offsets are within the image bounds.

    state.X_Offset = max(0, min(state.X_Offset, Image_Width - New_Image_Width))
    state.Y_Offset = max(0, min(state.Y_Offset, Image_Height - New_Image_Height))

    # Resize the image based on the new zoom level and offsets.
    
    state.Zoomed_Image = state.Current_Image[state.Y_Offset:state.Y_Offset + New_Image_Height, state.X_Offset:state.X_Offset + New_Image_Width]
    state.Zoomed_Image = cv2.resize(state.Zoomed_Image, (Image_Width, Image_Height))

    # Display the zoomed image according to the current state of the image analysis.
    
    if state.Distance_Map_Generated:
        Display_Thickness_Map()
    else:
        Display_ROIS_And_Filaments()



##################################################
#             Function: Bind_Zooming             #
##################################################

def Bind_Zooming():
   
    """
    
    Bind the zooming functionality to the mouse wheel event.
                
    Args:
    
        None.
                                
    Returns:

        Nothing.
    
    """     
    
    state.Image_Label.bind("<MouseWheel>", Zoom_Image)


        
##################################################
#             Function: Update_Image             #
##################################################

def Update_Image(image):
    
    """
    
    Update the displayed image with the new image data.
            
    Args:
    
        image [numpy.ndarray]: The image data to display.
                        
    Returns:

        Nothing.
    
    """       
    
    if image is not None:
        
        # Get the size of the displayed image.
        
        state.Image_Label_Width = state.Image_Label.winfo_width()
        state.Image_Label_Height = state.Image_Label.winfo_height()   
         
        Image_Height, Image_Width = image.shape[:2]
        
        # Calculate the scale factor based on the image and label sizes.
    
        Scale = min(state.Image_Label_Width / Image_Width, state.Image_Label_Height / Image_Height)
        Scale = max(Scale, 0.5)
        
        # Resize the image based on the scale factor.
        
        New_Image_Width = int(Image_Width * Scale)
        New_Image_Height = int(Image_Height * Scale)    
        
        Resized_Image = cv2.resize(image, (New_Image_Width, New_Image_Height))
        
        # Convert the resized image from BGR to RGB format. This is required for displaying the image correctly in Tkinter.
        
        RGB_Image = cv2.cvtColor(Resized_Image, cv2.COLOR_BGR2RGB)
        
        # Convert the RGB image to a PIL Image and then to a Tkinter Image. 
                
        try:
            
            PIL_Image = Image.fromarray(RGB_Image)  
            Tkinter_Image = ImageTk.PhotoImage(PIL_Image)
            state.Image_Label.config(image=Tkinter_Image)
            state.Image_Label.image = Tkinter_Image 
            
        except Exception as e:
            
            print("Error converting to PIL Image:", e)



##################################################
#      Function: Display_ROIS_And_Filaments      #
##################################################

def Display_ROIS_And_Filaments():
    
    """
    
    Display the ROIs and filaments on the zoomed image. This function is called when the distance map flag is off.
    
    Args:
    
        None.
    
    Returns:
    
        Nothing. 
    
    """
    
    if state.Zoomed_Image is None:
        return

    # Create a copy of the zoomed image to draw the ROIs and filaments on.
    
    Combined_Image = state.Zoomed_Image.copy()

    # Convert the image to a 3-channel image if it is grayscale. This is required for drawing colored ROIs and filaments.

    if Combined_Image.ndim == 2:
        
        Combined_Image = cv2.cvtColor(Combined_Image, cv2.COLOR_GRAY2BGR)

    # Draw the ROIs on the image. ROIs are drawn in red with a green bounding rectangle and labeled with their index.
    
    for Index, Roi in enumerate(state.ROIS_List):
        
        Rectangle = Roi['rect']

        if Roi['status'] == 'on':
            
            # Draw the filled indexes of the ROI. Checking if the scale is valid and within bounds.
            
            Filled_Indexes = Roi['filled_indexes']
            Scaled_Filled_Indexes_X = ((Filled_Indexes[1] - Rectangle[0]) * state.Zoom).astype(int)
            Scaled_Filled_Indexes_Y = ((Filled_Indexes[0] - Rectangle[1]) * state.Zoom).astype(int)
            Scaled_Filled_Indexes_X += int((Rectangle[0] - state.X_Offset) * state.Zoom)
            Scaled_Filled_Indexes_Y += int((Rectangle[1] - state.Y_Offset) * state.Zoom)

            # Ensure indexes are valid and within bounds
            
            Correct_Indexes = (Scaled_Filled_Indexes_Y >= 0) & (Scaled_Filled_Indexes_Y < Combined_Image.shape[0]) & \
                              (Scaled_Filled_Indexes_X >= 0) & (Scaled_Filled_Indexes_X < Combined_Image.shape[1])

            # Color the ROI red.
            
            Combined_Image[Scaled_Filled_Indexes_Y[Correct_Indexes], Scaled_Filled_Indexes_X[Correct_Indexes]] = [0, 0, 255]  

        # Scale the rectangle coordinates and draw the bounding rectangle around the ROI.
                
        Scaled_Rectangle = (
            
            int((Rectangle[0] - state.X_Offset) * state.Zoom),
            int((Rectangle[1] - state.Y_Offset) * state.Zoom),
            int(Rectangle[2] * state.Zoom),
            int(Rectangle[3] * state.Zoom)
    
        )
        
        # Draw the bounding rectangle around the ROI. The rectangle is drawn in green.
        
        cv2.rectangle(Combined_Image, (Scaled_Rectangle[0], Scaled_Rectangle[1]),
                      (Scaled_Rectangle[0] + Scaled_Rectangle[2], Scaled_Rectangle[1] + Scaled_Rectangle[3]),
                      (0, 255, 0), 2)  

        # Label the ROI with its index. The label is displayed at the center of the ROI.
        
        ROI_Center_X = Scaled_Rectangle[0] + Scaled_Rectangle[2] // 2
        ROI_Center_Y = Scaled_Rectangle[1] + Scaled_Rectangle[3] // 2
        
        cv2.putText(Combined_Image, str(Index + 1), (ROI_Center_X, ROI_Center_Y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)

    # Draw the filaments on the image. Filaments are drawn in black with an orange bounding rectangle and labeled with their index.
    
    for Index, Filament in enumerate(state.Filament_List):
        
        Rectangle = Filament['rect']

        if Filament['status'] == 'on':
            
            # Draw the filled indexes of the filament. Checking if the scale is valid and within bounds. 
            
            Filled_Indexes = Filament['filled_indexes']
            Scaled_Filled_Indexes_X = ((Filled_Indexes[1] - Rectangle[0]) * state.Zoom).astype(int)
            Scaled_Filled_Indexes_Y = ((Filled_Indexes[0] - Rectangle[1]) * state.Zoom).astype(int)
            Scaled_Filled_Indexes_X += int((Rectangle[0] - state.X_Offset) * state.Zoom)
            Scaled_Filled_Indexes_Y += int((Rectangle[1] - state.Y_Offset) * state.Zoom)

            # Ensure indexes are valid and within bounds.
            
            Correct_Indexes = (Scaled_Filled_Indexes_Y >= 0) & (Scaled_Filled_Indexes_Y < Combined_Image.shape[0]) & \
                              (Scaled_Filled_Indexes_X >= 0) & (Scaled_Filled_Indexes_X < Combined_Image.shape[1])

            # Color the filament black.
            
            Combined_Image[Scaled_Filled_Indexes_Y[Correct_Indexes], Scaled_Filled_Indexes_X[Correct_Indexes]] = [0, 0, 0] 
 
    # Update the image label with the combined image containing both ROIs and filaments.
                
    for Index, Filament in enumerate(state.Final_Filament_List):
        
        Rectangle = Filament['rect']

        if Filament['status'] == 'on':
            
            # Draw the filled indexes of the filament. Checking if the scale is valid and within bounds.
            
            Filled_Indexes = Filament['filled_indexes']
            Scaled_Filled_Indexes_X = ((Filled_Indexes[1] - Rectangle[0]) * state.Zoom).astype(int)
            Scaled_Filled_Indexes_Y = ((Filled_Indexes[0] - Rectangle[1]) * state.Zoom).astype(int)
            Scaled_Filled_Indexes_X += int((Rectangle[0] - state.X_Offset) * state.Zoom)
            Scaled_Filled_Indexes_Y += int((Rectangle[1] - state.Y_Offset) * state.Zoom)

            # Ensure indexes are valid and within bounds.
            
            Correct_Indexes = (Scaled_Filled_Indexes_Y >= 0) & (Scaled_Filled_Indexes_Y < Combined_Image.shape[0]) & \
                              (Scaled_Filled_Indexes_X >= 0) & (Scaled_Filled_Indexes_X < Combined_Image.shape[1])

            # Paint the filament black.
            
            Combined_Image[Scaled_Filled_Indexes_Y[Correct_Indexes], Scaled_Filled_Indexes_X[Correct_Indexes]] = [0, 0, 0] 
            
            
            # Scale the rectangle coordinates and draw the bounding rectangle around the filament.
            
            Scaled_Rect = (
                
                int((Rectangle[0] - state.X_Offset) * state.Zoom),
                int((Rectangle[1] - state.Y_Offset) * state.Zoom),
                int(Rectangle[2] * state.Zoom),
                int(Rectangle[3] * state.Zoom)
            
            )
            
            # Draw the bounding rectangle around the filament. The rectangle is drawn in orange.
            
            cv2.rectangle(Combined_Image, (Scaled_Rect[0], Scaled_Rect[1]),
                          (Scaled_Rect[0] + Scaled_Rect[2], Scaled_Rect[1] + Scaled_Rect[3]),
                          (0, 165, 255), 2)  

            # Label the filament with its index. The label is displayed at the center of the filament.
            
            Filament_Center_X = Scaled_Rect[0] + Scaled_Rect[2] // 2
            Filament_Center_Y = Scaled_Rect[1] + Scaled_Rect[3] // 2
            
            cv2.putText(Combined_Image, str(Index + 1), (Filament_Center_X, Filament_Center_Y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

    # Update the displayed image with the ROIs and filaments.
    
    Update_Image(Combined_Image)


##################################################
#        Function: Display_Thickness_Map         #
##################################################

def Display_Thickness_Map():
    
    """

    Display the local thickness map on the zoomed image. This function is called when the thickness map flag is on.
    
    Args:
    
        None.
        
    Returns:
    
        Nothing.
    
    """
    
    if state.Thickness_Map_Image is None:
        return
    
    # Get the size of the displayed image.
    
    Image_Height, Image_Width = state.Thickness_Map_Image.shape[:2]

    # Calculate the zoomed image width and height based on the zoom level.

    Zoomed_Image_Width = int(Image_Width / state.Zoom)
    Zoomed_Image_Height = int(Image_Height / state.Zoom)

    Zoomed_Image_Width = min(Zoomed_Image_Width, Image_Width - state.X_Offset)
    Zoomed_Image_Height = min(Zoomed_Image_Height, Image_Height - state.Y_Offset)

    # Get the zoomed region of the thickness map image based on the offsets and zoom level.

    Zoomed_Region = state.Thickness_Map_Image[
        
        state.Y_Offset: state.Y_Offset + Zoomed_Image_Height,
        state.X_Offset: state.X_Offset + Zoomed_Image_Width
        
    ]

    # Resize the zoomed region to the original image size. And update the image.
    
    Resized_Zoomed_Image = cv2.resize(Zoomed_Region, (Image_Width, Image_Height))

    Update_Image(Resized_Zoomed_Image)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

##################################################
#           Image Capture Functions              #
##################################################
        
##################################################
#            Function: Image_Capture             #
##################################################    
    
def Image_Capture(File_Name="Captured_Image.png"):
    
    """

    Capture the current image and save it as a PNG file.
                                
    Args:
    
        File_Name [str]: The name of the file to save the captured image.
                                                                        
    Returns:

        Nothing.
                    
    """ 
    
    # Check if there is a current image to capture.
    
    if state.Current_Image is not None:
        
        # Make sure the current image is in color (BGR).
        
        if len(state.Current_Image.shape) == 2:  
            
            Temporal_Image = cv2.cvtColor(state.Current_Image, cv2.COLOR_GRAY2BGR)
            
        else:

            Temporal_Image = state.Current_Image.copy()

        # Draw rectangles around ROIs and add numbers for identification.
        
        for Index, Roi in enumerate(state.ROIS_List):
            
            rect = Roi['rect']
            
            cv2.rectangle(Temporal_Image, (rect[0], rect[1]), 
                          (rect[0] + rect[2], rect[1] + rect[3]), 
                          (0, 255, 0), 2)  

            ROI_Center_X = rect[0] + rect[2] // 2
            ROI_Center_Y = rect[1] + rect[3] // 2
            
            cv2.putText(Temporal_Image, str(Index + 1), (ROI_Center_X, ROI_Center_Y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

        cv2.imwrite(File_Name, Temporal_Image)
        print(f"Image saved as {File_Name}")
        
    else:
        
        print("No image to capture.")


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

##################################################
#            Image Measurements Functions        #
##################################################

##################################################
#        Function: Font_Size_Calculation         #
##################################################

def Font_Size_Calculation():
    
    """
    
    Calculate the font size based on the Pixel_Conversion value.
    
    Args:
    
        None.
        
    Returns:
    
        Font_Size [int]: The calculated font size based on the Pixel_Conversion value.
    
    """
    
    # Set the base font size for the calculation.
    
    Base_Font_Size = 12  
    
    # Ensure that the Pixel_Conversion value is reasonable.
    
    if state.Pixel_Conversion is None or state.Pixel_Conversion <= 0:
        raise ValueError("Invalid Pixel_Conversion value. Ensure it's set and positive.")
    
    # Calculate font size scaled based on the pixel conversion factor.

    Font_Size = Base_Font_Size * (1 / state.Pixel_Conversion)    
    print("Font size calculated:", Font_Size)

    # Ensure the font size doesn't get too small or too large.
    
    Font_Size = max(4, min(Font_Size, 12)) 
    print("Font size adjusted:", Font_Size)

    return Font_Size

##################################################
#      Function: Scale_Value_Calculation         #
##################################################

def Scale_Value_Calculation(Perimeter):
    
    """

    Calculate the scale value based on the Filament_Mean_Thickness or the provided perimeter value.
        
    Args:
    
        Perimeter [float]: The perimeter value of the ROI.
    
    Returns:
    
        Scale_Value [float]: The calculated scale value in mm.
        Display_Value [float]: The scale value for display in the user interface.
        Unit [str]: The unit of the scale value (mm or µm).

    """

    # List of available scale values in mm.
    
    Possible_Values = [0.1, 0.25, 0.5, 1, 5]
    
    # Condition 1: If Filament_Mean_Thickness is set and positive.
    
    if hasattr(state, 'Filament_Mean_Thickness') and state.Filament_Mean_Thickness > 0:
        
        # Calculate the scale based on the filament mean thickness.

        Thickness = 5 * state.Filament_Mean_Thickness
        Scale_Value = min(Possible_Values, key=lambda x: abs(x - Thickness))
        print("Scale value calculated based on Filament_Mean_Thickness:", Scale_Value)
    
    # Condition 2: If a valid perimeter value is provided.
    
    elif hasattr(state, 'ROIS_List') and Perimeter is not None:
        
        # Calculate the scale based on the perimeter value.
        
        Scale_Value = min(Possible_Values, key=lambda x: abs(x - Perimeter / 3000)) 
        print("Perimeter value provided:", Perimeter)
        print("Perimeter value provided / 3000:", Perimeter/3000)
        print("Scale value calculated based on Perimeter:", Scale_Value)
    
    else:
        
        raise ValueError("Invalid conditions: Either Filament_Mean_Thickness must be set and positive, or a valid perimeter must be provided.")
    
    # Convert the scale value to µm if it's less than 1 mm. If not, keep it in mm.
    
    if Scale_Value < 1:
        
        Displayed_Value = Scale_Value * 1000  
        return Scale_Value, Displayed_Value, 'µm'
    
    else:
        
        return Scale_Value, Scale_Value, 'mm'

##################################################
#               Function: Color_Bar              #
##################################################

def Color_Bar(Image, Distance_Map):

    """

        Add a color bar to the image with the distance map. 

    
    Args:

        Image (np.ndarray): The original image (distance map with white background).
        Distance_Map (np.ndarray): The combined distance map of all filaments.

    Returns:

        Image (np.ndarray): The final image with the color bar added in the corner.
    
    """

    # Get the dimensions of the image.

    Image_Height, Image_Width = Image.shape[:2]
    
    
    # Set the size of the color bar based on the image dimensions.

    Bar_Height = int(Image_Height * 0.5) 
    Bar_Width = int(Image_Width * 0.03)  

    # Set the font Scale and thickness for the distance labels on the color bar.
    
    Font_Scale = Image_Height * 0.001  
    Font_Thickness = 1    
    
    # Calculate the maximum distance in the distance map in mm.
    
    Maximum_Map_Distance = np.max(Distance_Map) / state.Pixel_Conversion
    print("Max distance in mm: ", Maximum_Map_Distance)

    # Create a gradient from 0 to the maximum distance for the Scale bar.

    Gradient_Bar = np.linspace(0, Maximum_Map_Distance, Bar_Height).reshape(-1, 1)
    
    # Normalize the gradient to the range [0, 255] and invert it to match the colormap. 

    Gradient_Bar_Normalized = cv2.normalize(Gradient_Bar, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    Gradient_Bar_Normalized = 255 - Gradient_Bar_Normalized
    
    # Apply the inferno colormap to the normalized gradient for visualization.

    Color_Bar = cv2.applyColorMap(Gradient_Bar_Normalized, cv2.COLORMAP_INFERNO)

    # Create a  color bar label with a white background based on the color bar size.

    Color_Bar_Label = np.ones((Bar_Height, Bar_Width + 100, 3), dtype=np.uint8) * 255 
    
    # Add the color bar to the left side of the label.

    Color_Bar_Label[:, :Bar_Width] = Color_Bar

    # Add thickness labels in mm to the color bar based on the maximum distance.
    
    Label_Number = 5
    Steps = Bar_Height // (Label_Number - 1)

    # Loop through the number of labels and add the distance values to the color bar.
    
    for Label in range(Label_Number):
        
        # Calculate the corresponding distance for each label in mm
        
        Distance_Value = Maximum_Map_Distance * (1 - Label / (Label_Number - 1))
        Distance_Label = f"{Distance_Value:.4f} mm"  

        # Calculate the position for the label on the color bar.
        
        Label_Position = int(Label * Steps)

        # Get the text size to calculate appropriate positioning for the label.
        
        Text_Size = cv2.getTextSize(Distance_Label, cv2.FONT_HERSHEY_SIMPLEX, Font_Scale, Font_Thickness)[0]

        # Adjust the position of the text based on the text size and font scale.
        
        Text_X = Bar_Width + 10  

        # Add the distance label to the color bar.
        
        cv2.putText(Color_Bar_Label, Distance_Label, (Text_X, Label_Position + Text_Size[1] // 2), 
                    cv2.FONT_HERSHEY_SIMPLEX, Font_Scale, (0, 0, 0), Font_Thickness, cv2.LINE_AA)

    # The color bar is placed in the top right corner of the image with a small padding.
    # The color bar is centered vertically on the image.
    
    Color_Bar_X = Image_Width - Color_Bar_Label.shape[1] - 10
    Color_Bar_Y = (Image_Height - Bar_Height) // 2  

    # Overlay the labeled color bar on the image.

    Image[Color_Bar_Y:Color_Bar_Y + Bar_Height, Color_Bar_X:Color_Bar_X + Color_Bar_Label.shape[1]] = Color_Bar_Label

    return Image

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

##################################################
#                Other Functions                 #
##################################################

##################################################
#           Function: Get_Coordinates            #
##################################################

def Get_Coordinates(Event):

    """
    
    Get the actual coordinates of the mouse event in the x and y directions.
                    
    Args:
    
        event [tk.Event]: The mouse event.
                                        
    Returns:

        X_Coordinate [int]: The x-coordinate of the mouse event.
        Y_Coordinate [int]: The y-coordinate of the mouse event.
            
    """        
    
    # Get the size of the displayed image and calculate the scale factor.
    
    state.Image_Label_Width = state.Image_Label.winfo_width()
    state.Image_Label_Height = state.Image_Label.winfo_height()
    
    Image_Height, Image_Width = state.Current_Image.shape[:2]

    Scale = min(state.Image_Label_Width / Image_Width, state.Image_Label_Height / Image_Height)
    
    Padding_X = (state.Image_Label_Width - Image_Width * Scale) // 2
    Padding_Y = (state.Image_Label_Height - Image_Height * Scale) // 2

    # Get the actual coordinates of the mouse event in the x and y directions.
    # Calculate the actual coordinates based on the scale factor and padding.
    
    state.X_Coordinate = int((Event.x - Padding_X) / Scale / state.Zoom + state.X_Offset)
    state.Y_Coordinate = int((Event.y - Padding_Y) / Scale / state.Zoom + state.Y_Offset)
    
    state.X_Coordinate = np.clip(state.X_Coordinate, 0, Image_Width - 1)
    state.Y_Coordinate = np.clip(state.Y_Coordinate, 0, Image_Height - 1)   
    
    return state.X_Coordinate, state.Y_Coordinate

##################################################
#            Function: Closing_App               #
##################################################

def Closing_App(Root):
    
    """

    Close the application and destroy the main Tkinter window when the 'Exit' button is clicked.
                                   
    Args:
    
        Root [tk.Tk]: The main Tkinter window object.
                                                                                        
    Returns:

        Nothing.
                    
    """ 
    
    # Close the application and destroy the main Tkinter window.
    
    cv2.destroyAllWindows()
    Root.quit()

##################################################
#            Function: Reset_Script              #
##################################################

def Reset_Script():
    
    """

    Reset the script to its initial state by clearing all the variables and disabling the buttons.
                                       
    Args:
    
        None.
                                                                                                
    Returns:

        Nothing.
                    
    """ 
    
    state.Base_Image = None
    state.Current_Image = None
    state.Zoomed_Image = None
    state.Pore_ROI_Image = None
    state.Filament_ROI_Image = None
    
    state.Binary_Mask = None
    state.ROIS_List = []
    state.Filament_List = []
    state.Final_Filament_List = []
    state.Pore_Results = []
    
    
    
    state.Zoom = 1
    state.X_Offset = 0
    state.Y_Offset = 0
    state.Pixel_Conversion = None
    state.Circle_Center = None
    state.Circle_Radius = None
    state.Drawing_Circle = False
    state.Resizing_Circle = False
    state.Moving_Circle = False
    state.Circle_Starting_X, state.Circle_Starting_Y, state.Circle_Ending_X, state.Circle_Ending_Y = -1, -1, -1, -1
    state.Distance_Map_Generated = False
    
    state.Calibrate_Button.config(state=tk.DISABLED)
    state.Process_Button.config(state=tk.DISABLED)
    state.Pore_Button.config(state=tk.DISABLED)
    state.Measure_Pore_Button.config(state=tk.DISABLED)
    state.Import_Button.config(state=tk.NORMAL)

##################################################
#            Function: Unbind_Events             #
##################################################

def Unbind_Events():
    
    """

    Unbind all the events from the image label and the main Tkinter window.
                                               
    Args:
    
        None.   
                                                                                                
    Returns:

        Nothing.
                    
    """ 

    # Unbind all the events from the image label and the main Tkinter window.
    
    state.Image_Label.unbind("<ButtonPress-1>")
    state.Image_Label.unbind("<ButtonPress-2>")
    state.Image_Label.unbind("<ButtonPress-3>")
    state.Image_Label.unbind("<B1-Motion>")
    state.Image_Label.unbind("<Motion>")
    state.Image_Label.unbind("<ButtonRelease-1>")
    state.Image_Label.unbind("<ButtonRelease-2>")
    state.Image_Label.unbind("<ButtonPress-3>")
    state.Root.unbind('<KeyPress>')  
    state.Root.unbind('<Return>')  
    state.Root.unbind('0x0004')
    