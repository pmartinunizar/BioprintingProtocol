import state
from utils import Reset_Zoom, Update_Image, Image_Capture, Get_Coordinates
import tkinter as tk
import numpy as np
import cv2 


##################################################
#        Calibration Feature Functions           #
##################################################

##################################################
#              Function: Calibrate               #
##################################################

def Calibrate(Root):
    
    """
    
    Calibrate the image by drawing a circle and setting the pixel-to-mm conversion factor.
    The user can draw a circle on the image, and the diameter of the circle is used for calibration.
    The pixel-to-mm conversion factor is calculated based on the diameter of the circle drawn. 
    Using as a reference the well plate real diameter.
                                
    Args:
    
        Root [tk.Tk]: The main Tkinter window object.
                                                        
    Returns:

        Nothing.
                    
    """ 
    
    # Check if an image is imported.

    if state.Current_Image is None:
        print("No image imported. Please import an image first.")
        return

    # Start the calibration process by drawing a circle on the image.
        
    Circle_Events()  

    # Reset the circle variables.

    state.Drawing_Circle = False
    state.Resizing_Circle = False
    state.Moving_Circle = False
    state.Circle_Starting_X, state.Circle_Starting_Y, state.Circle_Ending_X, state.Circle_Ending_Y = 0, 0, 0, 0

    # Bind the Enter key event to complete the calibration process.
    
    Root.bind('<Return>', Ending_Calibration)

##################################################
#         Function: Ending_Calibration           #
##################################################

def Ending_Calibration(Event):
    
    """
    
    End the calibration process by setting the pixel-to-mm conversion factor.
    The pixel-to-mm conversion factor is calculated based on the diameter of the circle drawn.
    Crop the image around the circle and set the cropped image as the new base image.
                                
    Args:
    
        Event [tk.Event]: The Enter key event. 
                                                                
    Returns:

        Nothing.
                    
    """ 
        
    # Check if the circle center and radius are set.
    
    if state.Circle_Center is not None and state.Circle_Radius is not None:
        
        # Calculate the pixel-to-mm conversion factor based on the diameter of the circle. 
        # The diameter of the circle is used as a reference for calibration. The value is obtained from the user input.
        
        state.Pixel_Conversion = state.Well_Diameter / (2 * state.Circle_Radius)
        print(f"Calibration done: 1 pixel = {state.Pixel_Conversion:.6f} mm")

        # Define the bounding box for the circle to crop the image sourranding the circle.
        
        Circle_Center_X, Circle_Center_Y = state.Circle_Center
        
        Top_Left_X = max(0, Circle_Center_X - state.Circle_Radius)
        Top_Left_Y = max(0, Circle_Center_Y - state.Circle_Radius)
        Bottom_Right_X = min(state.Base_Image.shape[1], Circle_Center_X + state.Circle_Radius)
        Bottom_Right_Y = min(state.Base_Image.shape[0], Circle_Center_Y + state.Circle_Radius)

        # Crop the image around the circle.
        
        state.Cropped_Image = state.Base_Image[Top_Left_Y:Bottom_Right_Y, Top_Left_X:Bottom_Right_X]
       
        # Set the cropped image as the new base image and the current image.
        
        state.Base_Image = state.Cropped_Image.copy()
        state.Current_Image = state.Base_Image.copy()
        
        # Save the cropped image in the current folder.
        
        Image_Capture("CroppedImage.png")

        # Update the displayed image
        
        Reset_Zoom()
        Update_Image(state.Current_Image)

        # Unbind calibration events.
        
        state.Root.unbind('<Return>')
        state.Image_Label.unbind("<ButtonPress-1>")
        state.Image_Label.unbind("<B1-Motion>")
        state.Image_Label.unbind("<ButtonRelease-1>")

        if state.Platform == 'Darwin': 
            
            state.Image_Label.unbind("<ButtonPress-2>")
            
        else:  
            
            state.Image_Label.unbind("<ButtonPress-3>")

        # Enable the rest of the buttons for processing the image.

        state.Calibrate_Button.config(state=tk.DISABLED)
        state.Process_Button.config(state=tk.NORMAL)
        state.Pore_Button.config(state=tk.NORMAL)
        
    else:
        
        print("Error: Calibration failed. No circle drawn.")
        
##################################################
#            Function: Circle_Events             #
##################################################

def Circle_Events():
    
    """
    
    Bind mouse events for drawing, resizing, moving, and removing a circle on the image.
                
    Args:
    
        Nothing.
                                
    Returns:

        Nothing.
    
    """       
    
    # Bind the left mouse button to start drawing the circle.

    state.Image_Label.bind("<ButtonPress-1>", Start_Drawing_Circle)
    
    # When the left mouse button is moved, draw the circle.

    state.Image_Label.bind("<B1-Motion>", Drawing_Circle)
    
    # Bind the left mouse button to end drawing the circle.
        
    state.Image_Label.bind("<ButtonRelease-1>", End_Drawing_Circle)
    
    # Bind the right mouse button to remove the circle.

    if state.Platform == 'Darwin':  
        
        state.Image_Label.bind("<ButtonPress-2>", Remove_Circle) 
        
    else: 
        
        state.Image_Label.bind("<ButtonPress-3>", Remove_Circle) 

##################################################
#        Function: Start_Drawing_Circle          #
##################################################

def Start_Drawing_Circle(Event):
    
    """
    
    This function is called when the left mouse button is pressed to start drawing a circle on the image.
    Also, it is called when the circle doesn't exist or the user wants to resize/move the circle.
                
    Args:
    
        Event [tk.Event]: The mouse event.
                                
    Returns:

        Nothing.
    
    """       
    
    # Get the actual coordinates of the mouse event in the x and y directions.
    
    state.X_Coordinate, state.Y_Coordinate = Get_Coordinates(Event)

    # Check if the circle is being drawn, resized, or moved.  
    # If the circle doesn't exist, start drawing the circle.
    
    if state.Circle_Center is None:
        
        state.Drawing_Circle = True
        state.Circle_Starting_X, state.Circle_Starting_Y = state.X_Coordinate, state.Y_Coordinate
    
    # If the mouse is inside the circle, start moving the circle.
        
    elif abs(state.Circle_Center[0] - state.X_Coordinate) <= state.Circle_Radius and abs(state.Circle_Center[1] - state.Y_Coordinate) <= state.Circle_Radius:
        
        state.Moving_Circle = True
        state.Circle_Starting_X, state.Circle_Starting_Y = state.X_Coordinate, state.Y_Coordinate
    
    # If the mouse is outside the circle, start resizing the circle.
        
    else:
        
        state.Resizing_Circle = True
        state.Circle_Ending_X, state.Circle_Ending_Y = state.X_Coordinate, state.Y_Coordinate
        
##################################################
#           Function: Drawing_Circle             #
##################################################

def Drawing_Circle(Event):
    
    """
    
    This function updates the circle's position and size while the left mouse button is moved.
    As the user moves the mouse, the circle is drawn or resized accordingly.
                
    Args:
    
        Event [tk.Event]: The mouse event.
                                        
    Returns:

        Nothing.
    
    """       
        
    # Get the actual coordinates of the mouse event in the x and y directions.
        
    state.X_Coordinate, state.Y_Coordinate = Get_Coordinates(Event)

    # Check if the circle is being drawn, resized, or moved.
    # If the circle is being drawn, update the circle's position and size.
        
    if state.Drawing_Circle:
    
        state.Circle_Radius = Calculate_Radius(state.Circle_Starting_X, state.Circle_Starting_Y, state.X_Coordinate, state.Y_Coordinate)
        state.Calibration_Temporal_Image = state.Base_Image.copy()  
        cv2.circle(state.Calibration_Temporal_Image, (state.Circle_Starting_X, state.Circle_Starting_Y), state.Circle_Radius, (0, 0, 255), state.CirclePixelThickness)
        
        Update_Image(state.Calibration_Temporal_Image)
    
    # If the circle is being resized, update the circle's radius.
             
    elif state.Resizing_Circle:
        
        state.Circle_Radius = Calculate_Radius(state.Circle_Center[0], state.Circle_Center[1], state.X_Coordinate, state.Y_Coordinate)
        state.Calibration_Temporal_Image = state.Base_Image.copy()
        cv2.circle(state.Calibration_Temporal_Image, state.Circle_Center, state.Circle_Radius, (0, 0, 255), state.CirclePixelThickness)
        
        Update_Image(state.Calibration_Temporal_Image)
    
    # If the circle is being moved, update the circle's center.
     
    elif state.Moving_Circle:
        
        state.Difference_X = state.X_Coordinate - state.Circle_Starting_X
        state.Difference_Y = state.Y_Coordinate - state.Circle_Starting_Y
        state.New_Center = (state.Circle_Center[0] + state.Difference_X, state.Circle_Center[1] + state.Difference_Y)
        state.Calibration_Temporal_Image = state.Base_Image.copy()
        cv2.circle(state.Calibration_Temporal_Image, state.New_Center, state.Circle_Radius, (0, 0, 255), state.CirclePixelThickness)
        
        Update_Image(state.Calibration_Temporal_Image)

##################################################
#         Function: End_Drawing_Circle           #
##################################################

def End_Drawing_Circle(Event):
    
    """
    
    This function is called when the left mouse button is released to end drawing, resizing, or moving the circle.                
    
    Args:
    
        Event [tk.Event]: The mouse event.
                                        
    Returns:

        Nothing.
    
    """       
    
    # Get the actual coordinates of the mouse event in the x and y directions.
    
    state.X_Coordinate, state.Y_Coordinate = Get_Coordinates(Event)

    # Check if the circle is being drawn, resized, or moved.
    # If the circle is being drawn, end drawing the circle.
        
    if state.Drawing_Circle:
        
        state.Drawing_Circle = False
        state.Circle_Ending_X, state.Circle_Ending_Y = state.X_Coordinate, state.Y_Coordinate
        state.Circle_Radius = Calculate_Radius(state.Circle_Starting_X, state.Circle_Starting_Y, state.Circle_Ending_X, state.Circle_Ending_Y)
        state.Circle_Center = (state.Circle_Starting_X, state.Circle_Starting_Y)

    # If the circle is being resized, end resizing the circle.

    elif state.Resizing_Circle:
        
        state.Resizing_Circle = False
        state.Circle_Radius = Calculate_Radius(state.Circle_Center[0], state.Circle_Center[1], state.X_Coordinate, state.Y_Coordinate)
            
    # If the circle is being moved, end moving the circle.
    
    elif state.Moving_Circle:
        
        state.Moving_Circle = False
        state.Difference_X = state.X_Coordinate - state.Circle_Starting_X
        state.Difference_Y = state.Y_Coordinate - state.Circle_Starting_Y
        state.Circle_Center = (state.Circle_Center[0] + state.Difference_X, state.Circle_Center[1] + state.Difference_Y)

    # Draw the circle on the image and update the display.
    
    state.Current_Image = state.Base_Image.copy()
    cv2.circle(state.Current_Image, state.Circle_Center, state.Circle_Radius, (0, 0, 255), state.CirclePixelThickness)
    Update_Image(state.Current_Image)
    print(f"Circle drawn at {state.Circle_Center} with radius {state.Circle_Radius} pixels")

##################################################
#            Function: Remove_Circle             #
##################################################

def Remove_Circle(Event):
    
    """
    
    Bind mouse events for drawing, resizing, moving, and removing a circle on the image.
                
    Args:
    
        Event [tk.Event]: The mouse event.
                                
    Returns:

        Nothing.
    
    """       
    
    # Remove the circle from the image and update the display.
    
    state.Circle_Center = None
    state.Circle_Radius = None
    state.Current_Image = state.Base_Image.copy()
    
    Update_Image(state.Current_Image)
    print("Circle removed")  

##################################################
#          Function: Calculate_Radius            #
##################################################

def Calculate_Radius(Circle_Starting_X, Circle_Starting_Y, Circle_Ending_X, Circle_Ending_Y):
    
    """
    
    Calculate the radius of the circle based on the starting and ending coordinates.
                        
    Args:
    
        Circle_Starting_X [int]: The starting x-coordinate of the circle.
        Circle_Starting_Y [int]: The starting y-coordinate of the circle.
        Circle_Ending_X [int]: The ending x-coordinate of the circle.
        Circle_Ending_Y [int]: The ending y-coordinate of the circle.
                                                
    Returns:

        Radius [int]: The radius of the circle.
            
    """    
    
    # Calculate the distance between the starting and ending coordinates to get the radius.
    
    X_Distance = abs(Circle_Ending_X - Circle_Starting_X)
    Y_Distance = abs(Circle_Ending_Y - Circle_Starting_Y)
    Radius = int(np.sqrt((X_Distance ** 2) + (Y_Distance ** 2)))
    
    return Radius
        