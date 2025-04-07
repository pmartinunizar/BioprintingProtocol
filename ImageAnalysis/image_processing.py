import cv2
import state
import tkinter as tk
import numpy as np
from utils import Reset_Zoom, Update_Image, Get_Coordinates, Unbind_Events


##################################################
#            Image Processing Functions          #
##################################################

##################################################
#           Function: Processing_Image           #
##################################################

def Processing_Image():
    
    """
    
    Function to process the current image and create a binary mask.
    This function applies a bilateral filter and adaptive thresholding to the image.
    
    Args:
    
        Nothing.
        
    Returns:
        
        Nothing.
    
    """
    
    if state.Current_Image is None:
        print("No image imported. Please import an image first.")
        return
    
    Unbind_Events()
    
    # Capture the current image from the canvas and apply a bilateral filter and adaptive thresholding.
    
    state.Binary_Mask = cv2.bilateralFilter(state.Current_Image, d=9, sigmaColor=75, sigmaSpace=750)

    state.Binary_Mask = cv2.adaptiveThreshold(state.Binary_Mask, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)

    # Convert the binary image to BGR format so we can draw in color.
    
    state.Current_Image = state.Binary_Mask.copy() 
    state.Processed_Image = state.Current_Image.copy()

    Reset_Zoom()
    Update_Image(state.Current_Image)

    state.Image_Label.unbind("<ButtonPress-1>")
    state.Image_Label.unbind("<ButtonPress-2>")
    state.Image_Label.unbind("<B1-Motion>")
    state.Image_Label.unbind("<ButtonRelease-1>")
    
    print("Image processed into binary mask and converted to BGR.")
    
    state.Pore_Button.config(state=tk.NORMAL)
    state.Filament_Button.config(state=tk.NORMAL)


def Brush_Tool():
    
    """

    This function is implemented in case the image used presents illumination aberrations.
    It allows the user to paint over the image to correct these aberrations.
    
    If the image is good, the user can skip this step and go directly to the processing of the image.
    
    Arguments:
        
        Nothing.
    
    Returns:
            
        NOthing.

    """

    # Set the initial brush color and size. In this case, we use a black brush to paint over the image.
    # The brush size is set to 10 pixels.
    
    Brush_Color = (0, 0, 0)  
    Brush_Size = [10] 

    # Stack to keep track of image states for undo functionality.
    
    Image_Updated = [state.Current_Image.copy()]

    # Variables to track the last position of the mouse.
    
    Previous_X, Previous_Y = None, None

    def Start_Painting(event):
        
        """ 
        
        Start the painting operation when the mouse button is pressed.

        Args:
        
            event: The Tkinter event containing the mouse coordinates.
        
        Returns:
        
            Nothing.
            
        """
        
        nonlocal Previous_X, Previous_Y
        Previous_X, Previous_Y = Get_Coordinates(event)
        Apply_Paint(Previous_X, Previous_Y)

    def Continue_Painting(event):
        
        """
        
        Continue the painting operation as the mouse moves while the button is held down.

        Args:
        
            event: The Tkinter event containing the new mouse coordinates.
        
        Returns:
        
            Nothing.
            
        """
        
        nonlocal Previous_X, Previous_Y
        X, Y = Get_Coordinates(event)

        # Draw a line between the last position and the current position.
        
        if Previous_X is not None and Previous_Y is not None:
            # Apply the stroke with constant brush size relative to the screen.
            cv2.line(state.Current_Image, (Previous_X, Previous_Y), (X, Y), Brush_Color, Brush_Size[0])
            Apply_Paint(X, Y)
        Previous_X, Previous_Y = X, Y

    def Stop_Painting(event):
        
        """
        
        Stop the painting operation when the mouse button is released.
        Saves the current image to the undo stack.
        
        Args:
        
            event: The Tkinter event.

        Returns:
        
            Nothing.
            
        """
        
        nonlocal Previous_X, Previous_Y
        Previous_X, Previous_Y = None, None
        # Save the current state of the image to history for undo .
        Image_Updated.append(state.Current_Image.copy())

    def Apply_Paint(X, Y):
        
        """
        
        Apply a paint stroke (circle) at the specified coordinates.

        Args:
        
            x [in+t: X-coordinate of the point.
            y [int]: Y-coordinate of the point.

        Returns:
        
            Nothing.
            
        """

        # Paint a circle at the given coordinates with the current brush size
        cv2.circle(state.Current_Image, (X, Y), Brush_Size[0], Brush_Color, -1)
        # Update the zoomed-in region of the image
        Update_Zoomed_Image()

    def Brush_Preview(event=None):
        
        """
        
        Preview the brush at the mouse position by displaying a circle outline.
        If the mouse event is not available, it uses the last known position.

        Args:
        
            event (tk.Event, optional): The event object with current mouse position.
        
        Returns:
        
            Nothing.
            
        """
        
        # Get the current mouse position.
        
        nonlocal Previous_X, Previous_Y
        
        if event:
            Previous_X, Previous_Y = Get_Coordinates(event)
        
        # If no valid position is available, skip previewing.
        
        if Previous_X is None or Previous_Y is None:
            return

        # Create a copy of the current image to show the preview circle.
        
        Preview_Image = state.Current_Image.copy()

        # Draw the brush preview circle at the mouse position.
        
        cv2.circle(Preview_Image, (Previous_X, Previous_Y), Brush_Size[0], (0, 0, 0), 1)  

        # Update the zoomed-in region of the image with the preview circle.
        
        Update_Zoomed_Image(Preview_Image)

    def Brush_Size_Adjust(event):
        
        """
        
        Adjust the brush size using the '+' and '-' keys.

        Args:
        
            event (tk.Event): The event that carries the pressed key.
        
        Returns:
        
            Nothing.
            
        """
        
        # Increase or decrease brush size by 1 pxl according to the key pressed.
        
        if event.char == '+': 
            Brush_Size[0] += 1
        elif event.char == '-':  # Decrease brush size
            Brush_Size[0] = max(1, Brush_Size[0] - 1)  

        # Print the updated brush size for debugging.
        
        print(f"Brush size: {Brush_Size[0]}")

        # Immediately update the brush preview after changing the size.
        Brush_Preview()  

    def Brush_Color_Change(event):
        
        """
        
        Change the brush color with keyboard shortcuts.
        'W' or 'w' sets it to white, 'B' or 'b' sets it to black.

        Args:
        
            event (tk.Event): The key event with the character.
        
        Returns:
        
            Nothing.
            
        """
        
        # Set the color of the brush according to the key pressed.
        
        nonlocal Brush_Color
        if event.char.lower() == 'w':
            Brush_Color = (255, 255, 255)  
        elif event.char.lower() == 'b':
            Brush_Color = (0, 0, 0)  
        print(f"Brush color changed to: {'White' if Brush_Color == (255, 255, 255) else 'Black'}")

    def Undo(event):
        
        """
        
        Undo the last painting action when right-click is pressed.

        Args:
        
            event (tk.Event): The mouse click event.
        
        Returns:
        
            Nothing.
            
        """
        
        if len(Image_Updated) > 1:
            Image_Updated.pop()
            state.Current_Image = Image_Updated[-1].copy()
            Update_Zoomed_Image()
            print("Last painting action undone.")
        else:
            print("No more actions to undo.")

    def Brush_Finishing(event=None):
        
        """
        
        Finalize the brush tool operation.
        Converts the image to grayscale and updates the display.

        Args:
        
            event (tk.Event, optional): Triggered by pressing the Enter key.
        
        Returns:
        
            Nothing.
            
        """
        
        # Check if the image has 3 channels (BGR). Only convert to grayscale if it's a color image.
        
        if len(state.Current_Image.shape) == 3 and state.Current_Image.shape[2] == 3:
            Gray_Image = cv2.cvtColor(state.Current_Image, cv2.COLOR_BGR2GRAY)
            state.Current_Image = Gray_Image
        else:
            print("Image is already grayscale.")

        # Display the binary image to check the result
        Update_Image(state.Current_Image)
        print("Brush operation finalized. Binary mask created.")
        
        # Unbind events after finalization
        Unbind_Events()

    # Bind the events to the Image_Label widget.
    
    state.Image_Label.bind("<ButtonPress-1>", Start_Painting)
    state.Image_Label.bind("<B1-Motion>", Continue_Painting)
    state.Image_Label.bind("<Motion>", Brush_Preview)  
    state.Image_Label.bind("<ButtonRelease-1>", Stop_Painting)

    if state.Platform == 'Darwin':  
        
        state.Image_Label.bind("<ButtonPress-2>", Undo) 
        
    else: 
        
        state.Image_Label.bind("<ButtonPress-3>", Undo) 

    # Bind the + and - keys for brush size adjustment.
    # Bind the 'W' key to change brush color to white.
    # Bind the 'B' key to change brush color to black.
    
    state.Root.bind('<KeyPress>', Brush_Size_Adjust)  
    state.Root.bind('<KeyPress-w>', Brush_Color_Change)  
    state.Root.bind('<KeyPress-b>', Brush_Color_Change)  

    # Bind the Enter key to finalize the brush operation and create the binary mask.
    
    state.Root.bind('<Return>', Brush_Finishing)

def Update_Zoomed_Image(Preview_Image=None):
    
    """
    
    Update the displayed image based on the current zoom level, applying zoom and panning offsets.
    If a preview image is provided, it will be shown instead of the original image.
    
    Arguments:
    
        Preview_Image [numpy.ndarray]: The image data to display.
        
    Returns: 
    
        Nothing.
    
    """
    
    # Get the original image dimensions.
    
    Image_Height, Image_Width = state.Current_Image.shape[:2]

    # Calculate the region of the image that is currently being displayed based on zoom and offsets.
    
    Zoomed_Height = int(Image_Height / state.Zoom)
    Zoomed_Width = int(Image_Width / state.Zoom)

    # Extract the zoomed region from the image.
    
    Displayable_Image = Preview_Image if Preview_Image is not None else state.Current_Image
    
    Zoomed_Region = Displayable_Image[ state.Y_Offset: state.Y_Offset + Zoomed_Height, state.X_Offset: state.X_Offset + Zoomed_Width]

    # Resize the zoomed region to the size of the display.
    
    Resized_Zoomed_Image = cv2.resize(Zoomed_Region, (Image_Width, Image_Height))

    # Update the displayed image in the GUI.
    
    Update_Image(Resized_Zoomed_Image)


















