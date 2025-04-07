import cv2
import pandas as pd
import numpy as np
import state

from utils import Image_Capture, Update_Image, Font_Size_Calculation, Scale_Value_Calculation

from scipy.ndimage import  grey_dilation
import scipy.ndimage as ndimage

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors



##################################################
#           Pore Measuring Functions             #
##################################################

##################################################
#            Function: Pore_Measure              #
##################################################

def Pore_Measure():
    
    """

    Measure the surface area, perimeter, and printability of the selected ROIs.
                                           
    Args:
    
        Nothing.
                                                                                                
    Returns:

        Nothing.
                    
    """ 

    # Check if ROIs are selected and if calibration is done.

    if not state.ROIS_List:
        
        print("No ROIs selected. Please select ROIs first.")
        return
    
    if state.Pixel_Conversion is None:

        print("Calibration not done. Please calibrate first.")
        return
    
    state.Pore_Results = []
    
    for Index, Roi in enumerate(state.ROIS_List):
        
        # Get the mask from the ROI.
        
        Mask = Roi['mask']
        
        # Ensure the mask is binary.
    
        Binary_Mask = np.where(Mask > 0, 255, 0).astype(np.uint8)

        # Calculate surface pixels where the mask is filled.
        
        Pixels_Surface = np.sum(Binary_Mask == 255)

        # Find contours in the binary mask. 
        
        Contours, _ = cv2.findContours(Binary_Mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                    
        if Contours and Pixels_Surface > 0:
            
            # Calculate the perimeter, the surface area, and the printability of the pore.
            
            Contour = Contours[0].reshape(-1, 2) 
            Pixels_Perimeter = np.sum(np.sqrt(np.sum(np.diff(Contour, axis=0) ** 2, axis=1)))
            Pixels_Perimeter += np.linalg.norm(Contour[-1] - Contour[0])  
            
            Pore_Perimeter = Pixels_Perimeter * state.Pixel_Conversion
            Pore_Surface = Pixels_Surface * (state.Pixel_Conversion ** 2)
            Pore_Printability = (Pore_Perimeter ** 2) / (16 * Pore_Surface) if Pore_Surface > 0 else float('inf')
            
            print(f"Pore {Index + 1}: Surface {Pore_Surface:.2f} mm² Perimeter {Pore_Perimeter:.2f} mm Printability {Pore_Printability:.2f}")

            
            state.Pore_Results.append({
                
                'Pore': Index + 1,
                'Surface': Pore_Surface,
                'Perimeter': Pore_Perimeter,
                'Printability': Pore_Printability
                
            })
            
        else:
            
            print(f"Pore {Index + 1}: No contours found or zero surface area.")
            
            state.Pore_Results.append({
                
                'Pore': Index + 1,
                'Surface': 0,
                'Perimeter': 0,
                'Printability': float('inf')
                
            })

    # Save the pore results to an Excel file.
    
    Data = pd.DataFrame(state.Pore_Results)
    Data.to_excel("PoreValues.xlsx", index=False)
    print("state.Pore_Results saved to PoreValues.xlsx")

    # Capture the image with the ROIs and update the image.
    
    Image_Capture("ROIImage.png")
    Pore_Map()

##################################################
#              Function: Pore_Map                #
##################################################

def Pore_Map():
    
    """
    
    Create a pore map with the selected ROIs and save it as an image.
    The pore map is created by centering the selected ROIs in a single image.
    
    Args:
    
        Nothing.
    
    Returns:

        Nothing.
        
    """
    
    for Index, Roi in enumerate(state.ROIS_List):

        # Get the mask and rectangle for the ROI.
        
        Mask = Roi['mask']
        Mask = np.where(Mask > 0, 0, 255).astype(np.uint8)

        # Get the bounding box of the pore region.
        
        Pore_Region = np.column_stack(np.where(Mask == 0))  
        
        Y_min, X_min = Pore_Region.min(axis=0)
        Y_max, X_max = Pore_Region.max(axis=0)
        
        # Crop the pore region from the mask.
        
        Cropped_Pore = Mask[Y_min:Y_max+1, X_min:X_max+1]
        
        # Get the maximum dimension of the cropped pore.
        
        Max_Dimension = max(Cropped_Pore.shape)

        # Add a white border around the image. 
        # The border size is 25% of the maximum dimension.
        
        Border_Size = int(Max_Dimension * 0.25)  
        Updated_Size = Max_Dimension + 2 * Border_Size
        Updated_Border = np.ones((Updated_Size, Updated_Size), dtype=np.uint8) * 255  

        # Calculate the offsets to center the cropped pore in the new canvas.
        
        Y_Offset = Border_Size + (Updated_Size - Cropped_Pore.shape[0]) // 2 - Border_Size
        X_Offset = Border_Size + (Updated_Size - Cropped_Pore.shape[1]) // 2 - Border_Size

        # Place the cropped pore in the center of the new canvas.
        
        Updated_Border[Y_Offset:Y_Offset + Cropped_Pore.shape[0], 
                        X_Offset:X_Offset + Cropped_Pore.shape[1]] = Cropped_Pore

        # Get the perimeter of the pore for scale bar calculation.
        
        Pore_Results = state.Pore_Results[Index]
        Perimeter = Pore_Results['Perimeter']

        # Calculate the scale value based on the perimeter.
        
        Bar_Length_mm, Value, Unit = Scale_Value_Calculation(Perimeter)
        Bar_Length_pxl = Bar_Length_mm / state.Pixel_Conversion
        print("Scale bar length in pixels:", Bar_Length_pxl)

        # Create a high-quality figure and axes.
        
        Figure, Axes = plt.subplots(figsize=(8, 8))

        # Display the updated pore map with the white border.
        
        Axes.imshow(Updated_Border, cmap='gray', vmin=0, vmax=255)

        # Remove axis labels and set the title.
        
        Axes.axis('off')
        Axes.set_title(f"Pore Map {Index + 1}", fontsize=16)

        # Calculate the scale bar position based on the new canvas dimensions.
        # The scale bar will be placed at the bottom left corner. 
        
        Image_Height, Image_Width = Updated_Border.shape
        Bar_X_Start = int(Image_Width * 0.05)  
        Bar_X_End = Bar_X_Start + Bar_Length_pxl
        Bar_Y = int(Image_Height * 0.90)  

        # Add the scale bar to the image.
        
        Axes.plot([Bar_X_Start, Bar_X_End], 
                [Bar_Y, Bar_Y], 
                color='black', linewidth=3)

        # Add a text label for the scale bar below it.

        Label_Y = Bar_Y + int(Image_Height * 0.05)
        Axes.text((Bar_X_Start + Bar_X_End) / 2, Label_Y, 
                f'{Value} {Unit}', color='black', fontsize=Font_Size_Calculation(), ha='center')

        # Save the figure with high quality.
        
        Pore_File = f"Pore_Map_{Index + 1}_with_Scale_Bar.png"
        plt.savefig(Pore_File, dpi=300, bbox_inches='tight')
        print(f"Pore map with scale bar saved as {Pore_File}")
        plt.close(Figure)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

##################################################
#         Filament Measuring Functions           #
##################################################

##################################################
#            Function: Create_Circle             #
##################################################

def Create_Circle(Radius):
    
    """
    
    Create a circular structuring element for local thickness computation.
    
    Args:  

        Radius [int]: The radius of the circular structuring element.
        
    Returns:

        Circular_Element [np.ndarray]: The circular structuring element.
        
    """

    # Create a grid of coordinates for the structuring element.
    # To enclose the circle, the structuring element must have enough space to include the entire diameter plus 1 extra row/column for the center itself.
    
    Length = 2 * Radius + 1 
    X, Y = np.ogrid[:Length, :Length]
    
    # Calculate the distance from the center of the circle.
    
    Center_Distance = np.sqrt((X - Radius) ** 2 + (Y - Radius) ** 2)
    
    # Create a binary mask for the circular structuring element.
    
    Circular_Element = Center_Distance <= Radius
    
    return Circular_Element.astype(np.uint8)

##################################################
#           Function: Local_Thickness            #
##################################################

def Local_Thickness(Mask):
    
    """
    
    Compute the local thickness of a binary mask using a custom implementation.
    The local thickness is calculated by calculating the distance transform and then dilating the super-level sets.
    
    Args:
    
        Mask [np.ndarray]: The binary mask of the object.
        
    Returns:
    
        Thickness_Map [np.ndarray]: The local thickness map of the object.
        
    """
    
    # Compute the distance transform of the mask.
    
    Distance_Field = cv2.distanceTransform(Mask, cv2.DIST_L2, 3)
    
    # Initialize the thickness map with zeros.
    
    Thickness_Map = np.zeros_like(Distance_Field)
    
    # The maximum radius is the maximum distance value in the distance field.
    
    Maximum_Radius = int(np.floor(np.max(Distance_Field)))
    
    # Iterate over each radius and dilate the super-level sets.
    
    for Radius in range(1, Maximum_Radius + 1):
        
        # Create a circular structuring element for the current radius.
        Circle = Create_Circle(Radius)
        
        # Dilate the super-level sets using the circular structuring element.
        
        Super_Level_Set = np.where(Distance_Field >= Radius, Distance_Field, 0)
        
        # Apply the dilation operation to the super-level sets.
        
        Dilation = ndimage.grey_dilation(Super_Level_Set, footprint=Circle)
        
        # Update the thickness map by taking the maximum value.
        
        Thickness_Map = np.maximum(Thickness_Map, Dilation)

    # Calculate the value from radius to diameter.
    
    Thickness_Map = Thickness_Map * 2
    
    return Thickness_Map

##################################################
#          Function: Filament_Meaasure           #
##################################################

def Filament_Measure():
    
    """

    Measure the mean thickness and surface area of the selected filaments.
    
    Args:

        Nothing.

    Returns:
        
        Nothing.
            
    """

    # Check if filaments are selected and if calibration is done.
    
    if not state.Final_Filament_List:
        
        print("No filaments selected. Please select filaments first.")
        return

    if state.Pixel_Conversion is None:
        
        print("Calibration not done. Please calibrate first.")
        return

    # Initialize the thickness map and the list of filament areas.
    
    Thickness_Map = None
    Filament_Areas = [] 

    # Iterate over each filament and calculate the local thickness.

    for Index, Filament in enumerate(state.Final_Filament_List):
        
        # Get the mask of the filament and convert it to a binary mask.
        
        Mask = cv2.bitwise_not(Filament['mask'].astype(np.uint8))

        # Compute local thickness for the filament.
        
        Local_Thickness_Map = Local_Thickness(Mask)

        # Convert thickness map to mm using the pixel conversion factor.
        
        Local_Thickness_mm = Local_Thickness_Map * state.Pixel_Conversion

        # Update the thickness map by taking the maximum thickness for overlapping regions.

        if Thickness_Map is None:
            
            Thickness_Map = np.zeros_like(Local_Thickness_mm)

        # Update the thickness map by taking the maximum thickness for overlapping regions.

        Thickness_Map = np.maximum(Thickness_Map, Local_Thickness_mm)

        # Calculate the surface area of the current filament in mm^2.
        
        Pixel_Filament_Surface = np.count_nonzero(Mask)  
        Filament_Surface = Pixel_Filament_Surface * (state.Pixel_Conversion ** 2) 
        Filament_Areas.append(Filament_Surface)  

        print(f"Surface area of filament {Index + 1}: {Filament_Surface:.2f} mm²")

    # Calculate the mean thickness of all filaments. 
    
    Non_Zero_Thickness = Thickness_Map[Thickness_Map > 0]
    Mean_Thickness = np.mean(Non_Zero_Thickness)
    print(f"Mean thickness: {Mean_Thickness:.2f} mm")
    state.Filament_Mean_Thickness = Mean_Thickness

    # Calculate the mean surface area of all filaments.
    
    Total_Filament_Surface = np.sum(Filament_Areas)
    print(f"Total surface area of all filaments: {Total_Filament_Surface:.2f} mm²")

    # Normalize the thickness map for display.
    
    Normalized_Thickness_Map = cv2.normalize(Thickness_Map, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

    # Apply a color map to the thickness map.
    
    Color_Gradient_Image = cv2.applyColorMap(Normalized_Thickness_Map, cv2.COLORMAP_INFERNO)

    # Save the final image with the color map.
    
    File_Name = "Local_Thickness_Map.png"
    cv2.imwrite(File_Name, Color_Gradient_Image)
    print(f"Thickness map saved as {File_Name}")

    # Create a high-quality figure and axes.
    
    Figure, Axes = plt.subplots(figsize=(8, 6))

    # Display the thickness map with the color gradient.
    
    Color_Map = plt.cm.inferno
    Normalized_Color_Map = mcolors.Normalize(vmin=np.min(Thickness_Map), vmax=np.max(Thickness_Map))
    Color_Axes = Axes.imshow(Thickness_Map, cmap = Color_Map, norm = Normalized_Color_Map)

    # Add a title with the mean thickness.
    
    Axes.set_title(f"Local Thickness Map\nMean Thickness: {Mean_Thickness:.2f} mm", fontsize=16)

    # Add the color bar with proper scaling.
    
    Color_Bar = Figure.colorbar(Color_Axes, ax=Axes)
    Color_Bar.set_label('Thickness (mm)', fontsize=12)

    # Remove axis labels.
    
    Axes.axis('off')

    # Calculate the scale value using the mean thickness.
    
    Bar_Length_mm, Value, Unit = Scale_Value_Calculation(Mean_Thickness)
    Bar_Length_pxl = Bar_Length_mm / state.Pixel_Conversion
    print("Scale bar length in pixels:", Bar_Length_pxl)

    # Add a scale bar to the image with the calculated length.
 
    Bar_X_Start = 50  
    Bar_X_End = Bar_X_Start + Bar_Length_pxl
    Bar_Y = Thickness_Map.shape[0] - 70  

    # Add the scale bar to the image.
    
    Axes.plot([Bar_X_Start, Bar_X_End],
            [Bar_Y, Bar_Y],
            color='white', linewidth=3)

    # Add a text label for the scale bar below it.
    
    Label_Y = Bar_Y + 20  
    Axes.text((Bar_X_Start + Bar_X_End) / 2, Label_Y,
            f'{Value} {Unit}', color='white', fontsize=Font_Size_Calculation(), ha='center')

    # Save the figure with high quality.
    
    Filament_File = "Local_Thickness_with_Scale_Bar.png"
    plt.savefig(Filament_File, dpi=300, bbox_inches='tight')
    print(f"High-quality thickness map with scale bar saved as {Filament_File}")

    # Update the state with the combined image.
    
    state.Thickness_Map_Image = Color_Gradient_Image.copy()
    Update_Image(state.Thickness_Map_Image)
    state.Distance_Map_Generated = True
    plt.close(Figure)
