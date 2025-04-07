import cv2
import numpy as np
import state
import tkinter as tk
from utils import Display_ROIS_And_Filaments, Update_Image, Get_Coordinates, Unbind_Events

##################################################
#               Pore ROI Functions               #
##################################################

##################################################
#            Function: Pore_Events               #
##################################################

def Pore_Events():
    
    """

    Bind the mouse events for selecting and removing regions of interest.
                                                       
    Args:
    
        Nothing.
                                                                                                                        
    Returns:

        Nothing.
                    
    """ 
    
    # Check if an image is imported or processed.
    
    if state.Current_Image is None:
        
        print("No image imported or processed. Please import and process an image first.")
        
        return

    state.Current_Image = state.Processed_Image.copy()
    
    # Bind mouse events to select and remove ROIs based on the platform.
    # Left-click to select ROIs and right-click to remove ROIs.
    
    state.Image_Label.bind("<ButtonRelease-1>", Pore_Selection)
    
    if state.Platform == 'Darwin':  
        
        state.Image_Label.bind("<ButtonPress-2>", Remove_Pore)  
        
    else:  
        
        state.Image_Label.bind("<ButtonPress-3>", Remove_Pore)  

    state.Root.bind('<Return>', End_Pore_Selection)  

##################################################
#             Function: Pore_Selection           #
##################################################

def Pore_Selection(Event):
    
    """

    Select the region of interest (ROI) using the mouse click event.
    To do this, the function calculates the click position, performs flood fill, and displays the ROIs on the image.
                                               
    Args:
    
        Event [tk.Event]: The Tkinter event object containing the click position.
                                                                                                        
    Returns:

        Nothing.
                    
    """ 
    
    state.Pore_ROI_Image = state.Current_Image.copy()
    
    # Get the actual coordinates in the image.
    
    state.X_Coordinate, state.Y_Coordinate = Get_Coordinates(Event)
    
    # Ensure the clicked pixel is a white pore. The previous image processing should have turned the pores white.
    
    Pixel_Clicked = state.Current_Image[state.Y_Coordinate, state.X_Coordinate]
    
    if isinstance(Pixel_Clicked, np.ndarray): 
        
        Pixel_Clicked = Pixel_Clicked[0]

    if Pixel_Clicked != 255:
        
        print(f"Clicked on a white region. Pixel value: {Pixel_Clicked}. Flood fill skipped.")
        return

    # Perform flood fill operation with fixed tolerance values. Based on the pixel value of the clicked point.
      
    Lower_Difference, Upper_Difference = Dynamic_Tolerance(state.Current_Image, state.X_Coordinate, state.Y_Coordinate)
    
    # Create a mask with padding of +2 for flood fill operation. This padding is done to avoid edge cases.
     
    Mask = np.zeros((state.Current_Image.shape[0] + 2, state.Current_Image.shape[1] + 2), np.uint8)  
    
    # Set the flags for the flood fill operation.
    
    Flooding_Flags = 4 | (Lower_Difference << 8) | (Upper_Difference << 16) | cv2.FLOODFILL_FIXED_RANGE
    
    _, _, Mask, Rectangle = cv2.floodFill(state.Current_Image, Mask, (state.X_Coordinate, state.Y_Coordinate), 255, Lower_Difference, Upper_Difference, Flooding_Flags)

    # Remove the padding from the mask and get the filled indexes.
    # This is done to avoid the padding added for the flood fill operation.
    
    No_Padding_Mask = Mask[1:-1, 1:-1] 

    # Get the filled indexes for the ROI.
        
    Filled_Indexes = np.where(No_Padding_Mask != 0)

    if len(Filled_Indexes[0]) == 0:
        
        print(f"Error: No filled indexes found for ROI {len(state.ROIS_List) + 1}. Flood fill failed.")
        return

    # Create an ROI with the filled region. The ROI contains the image, mask, rectangle, filled indexes, and status.
    
    Roi = {
        
        'image': state.Pore_ROI_Image.copy(),
        'mask': No_Padding_Mask,  
        'rect': Rectangle,
        'filled_indexes': Filled_Indexes,  
        'status': 'on'  
        
    }

    # Add the ROI to the global list.
    
    state.ROIS_List.append(Roi)

    # Display the ROIs on the zoomed image.
    
    Display_ROIS_And_Filaments()
    
    state.Pore_ROI_Image = state.Current_Image.copy()



##################################################
#             Function: Remove_Pore              #
##################################################

def Remove_Pore(Event = None):
    
    """

    Remove the last region of interest (ROI) from the list and update the display.
                                                   
    Args:
    
        Event [tk.Event]: The Tkinter event object containing the click position.
                                                                                                                
    Returns:

        Nothing.
                    
    """ 
       
    if state.ROIS_List:

        # Remove the last ROI from the list.
        
        Roi = state.ROIS_List.pop()
        
        if Roi['status'] == 'on':
            
            Filled_Indexes = Roi['filled_indexes']
    
            state.Current_Image[Filled_Indexes] = state.Processed_Image[Filled_Indexes]

        # Update the display to remove the rectangle and red fill.
        
        Display_ROIS_And_Filaments()

##################################################
#          Function: End_Pore_Selection          #
##################################################

def End_Pore_Selection(Event = None):
    
    """

    Finalize the ROI selection process and unbind the mouse events.
                                                           
    Args:
    
        Event [tk.Event]: The Tkinter event object containing the click position.
                                                                                                                                
    Returns:

        Nothing.
                    
    """ 
        
    # Unbind the ROI selection events.
                
    print("Selected ROIs:", [Roi['rect'] for Roi in state.ROIS_List])
    
    state.Measure_Pore_Button.config(state=tk.NORMAL)

    Unbind_Events()

##################################################
#          Function: Dynamic_Tolerance           #
##################################################

def Dynamic_Tolerance(Image, X_Coordinate, Y_Coordinate, Radius=5):
    
    """

    Calculate the dynamic tolerance for the flood fill operation based on the standard deviation of the patch around the clicked point.
                                               
    Args:
    
        Image [numpy.ndarray]: The binary mask image.
        X_Coordinate [int]: The x-coordinate of the clicked point.
        Y_Coordinate [int]: The y-coordinate of the clicked point.
        Radius [int]: The radius of the patch around the clicked point.
                                                                                                                
    Returns:

        Lower_Difference [int]: The lower difference tolerance for the flood fill operation.
        Upper_Difference [int]: The upper difference tolerance for the flood fill operation.
                    
    """ 
    
    # Get a small patch around the clicked point with the given radius.
    
    Patch = Image[max(0, Y_Coordinate-Radius):min(Image.shape[0], Y_Coordinate+Radius),
                  max(0, X_Coordinate-Radius):min(Image.shape[1], X_Coordinate+Radius)]
    
    # Calculate the standard deviation of the patch as the dynamic tolerance.
    
    STD_Dev = np.std(Patch)
    
    Lower_Difference = int(STD_Dev)  
    Upper_Difference = int(STD_Dev)  
    
    # Return the lower and upper difference values for the flood fill operation.

    return Lower_Difference, Upper_Difference

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

##################################################
#            Filament ROI Functions              #
##################################################

##################################################
#         Function: Filament_Events              #
##################################################    

def Filament_Events():
    
    """
    
    Bind the mouse events for selecting and removing filaments.
                                                       
    Args:
    
        Nothing.
                                                                                                                        
    Returns:
    
        Nothing.
        
    """ 
    
    # Check if an image is imported or processed.
    
    if state.Current_Image is None:
        
        print("No image imported or processed. Please import and process an image first.")
        return
        
    state.Current_Image = state.Processed_Image.copy()
    
    # Bind mouse events to select and remove filaments.
    # Left-click to select filaments from the image.
    
    state.Image_Label.bind("<ButtonRelease-1>", Filament_Selection)
    
    # Right click to remove the last filament from the list.
    
    if state.Platform == 'Darwin':
        
        state.Image_Label.bind("<ButtonPress-2>", Remove_Filament)
        
    else:
        
        state.Image_Label.bind("<ButtonPress-3>", Remove_Filament)

    # Finalize filament selection with the Enter key.
    
    state.Root.bind('<Return>', End_Filament_Selection)

##################################################
#         Function: Filament_Selection           #
##################################################    

def Filament_Selection(Event):
    
    """

    Select the filaments using the mouse click event.
    To do this, the function calculates the click position, performs flood fill, and displays the filaments on the image.
    
    Args:
    
        Event [tk.Event]: The Tkinter event object containing the click position.
    
    Returns:
    
        Nothing.

    """

    state.Filament_ROI_Image = state.Current_Image.copy()

    # Get the actual coordinates in the image.

    state.X_Coordinate, state.Y_Coordinate = Get_Coordinates(Event)

    # Check if the Ctrl key is pressed. If pressed, select the black filament without altering the rest of the image.
    
    Ctrl = (Event.state & 0x0004) != 0  


    # Case 1: Regular left-click (Select a filament and paint it black)
    
    if not Ctrl:
        
        print("Normal selection: Selecting filament and painting it black")

        # Ensure the clicked pixel is a white region (in a grayscale image).
        
        Pixel_Clicked = state.Filament_ROI_Image[state.Y_Coordinate, state.X_Coordinate]
        
        if isinstance(Pixel_Clicked, np.ndarray):  
            
            Pixel_Clicked = Pixel_Clicked[0]

        if Pixel_Clicked != 255:
            
            print(f"Clicked on a non-white region. Pixel value: {Pixel_Clicked}. Flood fill skipped.")
            return

        # Perform flood fill operation to turn the white region black.
        
        Lower_Difference, Upper_Difference = Dynamic_Tolerance(state.Filament_ROI_Image, state.X_Coordinate, state.Y_Coordinate)

        # Create a mask with padding of +2 for the flood fill operation.
        
        Mask = np.zeros((state.Filament_ROI_Image.shape[0] + 2, state.Filament_ROI_Image.shape[1] + 2), np.uint8)

        # Perform the flood fill operation to paint the selected region black.
        
        _, _, Mask, Rectangle = cv2.floodFill(state.Filament_ROI_Image, Mask, (state.X_Coordinate, state.Y_Coordinate), 0, Lower_Difference, Upper_Difference, cv2.FLOODFILL_FIXED_RANGE)

        # Remove the padding from the mask.
        
        No_Padding_Mask = Mask[1:-1, 1:-1]

        # Get the filled indexes for the ROI.
        
        Filled_Indexes = np.where(No_Padding_Mask != 0)
        
        if len(Filled_Indexes[0]) == 0:
            
            print(f"Error: No filled indexes found for ROI {len(state.ROIS_List) + 1}. Flood fill failed.")
            return

        # Create an ROI with the filled region and add it to the global list.
        
        Filament = {
            
            'image': state.Filament_ROI_Image.copy(),
            'mask': No_Padding_Mask,
            'rect': Rectangle,
            'filled_indexes': Filled_Indexes,
            'status': 'on',
            'operation': 'initial'
            
        }

        # Add the ROI to the global list of ROIs.
        
        state.Filament_List.append(Filament)

        # Update the image with the selected region.
        
        state.Filament_ROI_Image = state.Filament_ROI_Image.copy()

    # Case 2: Ctrl + left-click (Select a filament without altering the rest of the image).
    
    else:
        
        print("Ctrl + Selection: Selecting filament without altering the rest of the image")

        # Ensure the clicked pixel is a black filament (in a grayscale image).
        
        Pixel_Clicked = state.Filament_ROI_Image[state.Y_Coordinate, state.X_Coordinate]
        
        if isinstance(Pixel_Clicked, np.ndarray):  
            
            Pixel_Clicked = Pixel_Clicked[0]

        if Pixel_Clicked == 255:
            
            print(f"Clicked on a white region. Pixel value: {Pixel_Clicked}. Flood fill skipped.")
            return

        # Perform flood fill operation for selecting the black filament without altering the rest of the image.
        
        Lower_Difference, Upper_Difference = Dynamic_Tolerance(state.Filament_ROI_Image, state.X_Coordinate, state.Y_Coordinate)

        # Create a mask with padding of +2 for the flood fill operation.
        
        Mask = np.zeros((state.Filament_ROI_Image.shape[0] + 2, state.Filament_ROI_Image.shape[1] + 2), np.uint8)

        # Perform the flood fill without changing the color, only selecting.
        
        _, _, Mask, Rectangle = cv2.floodFill(state.Filament_ROI_Image, Mask, (state.X_Coordinate, state.Y_Coordinate), None, Lower_Difference, Upper_Difference, cv2.FLOODFILL_FIXED_RANGE)

        # Remove the padding from the mask.
        
        No_Padding_Mask = Mask[1:-1, 1:-1]

        # Get the filled indexes for the ROI.
        
        Filled_Indexes = np.where(No_Padding_Mask != 0)

        if len(Filled_Indexes[0]) == 0:
            
            print(f"Error: No filled indexes found for black filament. Flood fill failed.")
            return

        # Create an ROI with the filled region and add it to the global list.
        
        Filament = {
            
            'image': state.Filament_ROI_Image.copy(),
            'mask': No_Padding_Mask,
            'rect': Rectangle,
            'filled_indexes': Filled_Indexes,
            'status': 'on',
            'operation': 'final'
            
        }

        # Add the filament ROI to the global list.
        
        state.Final_Filament_List.append(Filament)

        # Update the image to include the new filament.
        
        state.Filament_ROI_Image = state.Filament_ROI_Image.copy()

    # Display the ROIs and filaments on the image.
    
    Display_ROIS_And_Filaments()

    state.Current_Image = state.Filament_ROI_Image.copy()
    print("Filament selection operation complete.")

##################################################
#          Function: Remove_Filament             #
##################################################   

def Remove_Filament(Event = None):
    
    """
    
    Remove the last filament from the list and update the display.
                                                   
    Args:
    
        Event [tk.Event]: The Tkinter event object containing the click position.
                                                                                                                
    Returns:
    
        Nothing.
        
    """ 
    
    if state.Filament_List:
        
        Filament = state.Filament_List.pop()

        # Remove the last filament from the list.
        
        if Filament['status'] == 'on':
            
            Filled_Indexes = Filament['filled_indexes']
            state.Current_Image[Filled_Indexes] = state.Processed_Image[Filled_Indexes]

        # Update the display to remove the rectangle.
        
        Display_ROIS_And_Filaments()
        
        
def End_Filament_Selection(Event = None):
    
    """
    
    Finalize the filament selection process and unbind the mouse events.
    
    Args:
    
        Event [tk.Event]: The Tkinter event object containing the click position.
            
    Returns:
    
        Nothing.
    
    """ 

    # Unbind the filament selection events.
    
    print("Selected Filaments:", [filament['rect'] for filament in state.Filament_List])

    state.Measure_Filament_Button.config(state=tk.NORMAL)

    # Reset the operation status for all filaments. This is done to avoid any confusion in the next selection.
    
    for Filament in state.Filament_List:
        
        if Filament['operation'] == 'initial' or Filament['operation'] == 'final':
            Filament['operation'] = 'none'  

    # Fill holes in all filaments before finalizing the selection.
    
    Fill_Holes_In_Filaments()

    # After pressing Enter to finalize the selection of filaments, the user can paint the selected filaments black.
    
    Combined_Image = np.full_like(state.Current_Image, 255)  

    # Loop through the filaments in the Final_Filament_List and paint them black.
    
    for Index, Filament in enumerate(state.Final_Filament_List):
        
        if Filament['status'] == 'on':
            
            Filled_Indexes = Filament['filled_indexes']
            Combined_Image[Filled_Indexes] = 0  

    # Update the display with the new image containing only the masks on a white background.
    
    Update_Image(Combined_Image)
    
    state.Current_Image = Combined_Image.copy()

    # Unbind the events after finalizing selection.
    
    Unbind_Events()
    print("Ending operation in filament")



def Fill_Holes_In_Filaments(Event = None):
    
    """
    
    Fill holes inside the masks of all filaments in the Final_Filament_List and update the mask in each filament.
    
    Args:
    
        Event: The Tkinter event object containing the click position (optional).
    
    Returns:
    
        Nothing.
    
    """
    
    # Loop through the filaments in the Final_Filament_List and fill the holes in each mask.
    
    for Index, Filament in enumerate(state.Final_Filament_List):
        
        print(f"Processing Filament {Index + 1}")

        # Ensure the mask is in the correct format for the morphological operations.
        
        Mask = (Filament['mask'].astype(np.uint8) == 1).astype(np.uint8) * 255

        # Fill the holes in the mask using morphological closing.
        
        Kernel = np.ones((3, 3), np.uint8)  
        Closed_Mask = cv2.morphologyEx(Mask, cv2.MORPH_CLOSE, Kernel)
        Closed_Mask = cv2.bitwise_not(Closed_Mask)

        # Update the mask in the filament with the filled mask.
        
        Filament['mask'] = Closed_Mask
        Filled_Indexes = np.where(Closed_Mask == 0)
        Filament['filled_indexes'] = Filled_Indexes
    
    # Display the updated filaments with the filled holes.
        
    Display_ROIS_And_Filaments()
    print("Holes in all filaments have been filled.")