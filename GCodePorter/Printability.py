import math
import json
import os
from PySide6.QtWidgets import QMessageBox

##################################################
#           Printability Test Functions          #
##################################################

def Printability_Test(Manufacturer, Number, Patch_Size, Nozzle_Diameter, Initial_Pressure, Final_Pressure, Step_Pressure, Initial_Speed, Final_Speed, Step_Speed, Pressure=None, Speed=None):
    
    """
    
    Generate G-code for a printability test based on the specified printing parameters assigned by the user.
    
    The G-code is generated for a specific well plate configuration and saved to a file.
    
    Args:
    
        Manufacturer [str]: The manufacturer of the well plate.
        Number [int]: The number of wells in the well plate.
        Patch_Size [float]: The size of the patch in mm.
        Nozzle_Diameter [float]: The diameter of the nozzle in mm.
        Initial_Pressure [float]: The initial pressure for the test.
        Final_Pressure [float]: The final pressure for the test.
        Step_Pressure [float]: The step pressure for the test.
        Initial_Speed [float]: The initial speed for the test.
        Final_Speed [float]: The final speed for the test.
        Step_Speed [float]: The step speed for the test.
        Pressure [float, optional]: A specific pressure value to use instead of a range. Default is None.
        Speed [float, optional]: A specific speed value to use instead of a range. Default is None.
        
    Returns:
    
        GCode [str]: The path to the generated G-code file.
        
    """
    
    # Check if the parameters of the well plate are correctly defined in the JSON file.
    
    # The JSON file should be in the same directory as this script. Consider that the JSON file isn't completely defined for all the well plates.
    
    CURRENT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
    JSON_FILE = os.path.join(CURRENT_DIRECTORY, "WellPlateInfo.json")

    if not os.path.exists(JSON_FILE):
        raise FileNotFoundError(f"Error: JSON file not found at: {JSON_FILE}")

    try:
        with open(JSON_FILE, 'r', encoding="utf-8") as file:
            data = json.load(file)
    except json.JSONDecodeError:
        raise ValueError(f"Error: JSON file {JSON_FILE} is not properly formatted.")
    
    # Obtain the well plate parameters from the JSON file. 
    
    Well_Info = data[Manufacturer][str(Number)]
    Well_Diameter = Well_Info.get("Diameter")
    Well_Height = Well_Info.get("Height")
    Well_Center_Offset = Well_Info.get("Center Offset")

    if not all([Well_Diameter, Well_Height, Well_Center_Offset]):
        raise ValueError(f"Missing well parameters for {Manufacturer} with {Number} wells.")


    # According to the well plate configuration, the number of rows and columns are defined.
    
    Well_Grid = {6: (2, 3), 12: (3, 4), 24: (4, 6), 48: (6, 8), 96: (8, 12)}
    Rows_Number, Columns_Number = Well_Grid.get(Number, (0, 0))

    # Check if the well plate configuration is valid.
    
    Nozzle_Diameters_Selection = {"0.4": 0.4, "0.25": 0.25, "0.2": 0.2}
    if Nozzle_Diameter not in Nozzle_Diameters_Selection:
        raise ValueError(f"Invalid Nozzle Diameter: {Nozzle_Diameter}")
    Nozzle_Diameter_Value = Nozzle_Diameters_Selection[Nozzle_Diameter]

    Patch_Size_Selection = {"5": 5, "10": 10, "20": 20}
    if Patch_Size not in Patch_Size_Selection:
        raise ValueError(f"Invalid Patch Size: {Patch_Size}")
    Patch_Size_Value = Patch_Size_Selection[Patch_Size]

    # Generate the pressure and speed values based on the provided ranges or specific values.
    
    if Pressure is not None:
        Pressures_Values = [Pressure]
    else:
        Pressures_Values = Generate_Range(Initial_Pressure, Final_Pressure, Step_Pressure)

    if Speed is not None:
        Speeds_Values = [Speed]
    else:
        Speeds_Values = Generate_Range(Initial_Speed, Final_Speed, Step_Speed)

    # Check if the number of wells exceeds the plate capacity.
    
    Exceeds_Pressures = len(Pressures_Values) > Columns_Number
    Exceeds_Speeds = len(Speeds_Values) > Rows_Number

    if Exceeds_Pressures or Exceeds_Speeds:
        MSG = (
            "Your selected range exceeds the plate capacity.\n"
            f"Plate can handle up to {Columns_Number} columns (pressures), you have {len(Pressures_Values)}.\n"
            f"Plate can handle up to {Rows_Number} rows (speeds), you have {len(Speeds_Values)}.\n"
            "Do you want to trim to fit, or cancel and change your values?"
        )
        Answer = QMessageBox.question(None, "Range Exceeds Capacity", MSG,
                                      QMessageBox.Yes | QMessageBox.No)
        if Answer == QMessageBox.Yes:
            Pressures_Values = Pressures_Values[:Columns_Number]
            Speeds_Values = Speeds_Values[:Rows_Number]
        else:
            return None 

    # Define the points required to print the deposition patch.
    
    Points = {
        "1":  (-Patch_Size_Value/2,  Patch_Size_Value/2),
        "2":  ( Patch_Size_Value/2,  Patch_Size_Value/2),
        "3":  ( Patch_Size_Value/2,  Patch_Size_Value/3),
        "4":  (-Patch_Size_Value/2,  Patch_Size_Value/3),
        "5":  (-Patch_Size_Value/2,  Patch_Size_Value/6),
        "6":  ( Patch_Size_Value/2,  Patch_Size_Value/6),
        "7":  ( Patch_Size_Value/2,  0),
        "8":  (-Patch_Size_Value/2,  0),
        "9":  (-Patch_Size_Value/2, -Patch_Size_Value/6),
        "10": ( Patch_Size_Value/2, -Patch_Size_Value/6),
        "11": ( Patch_Size_Value/2, -Patch_Size_Value/3),
        "12": (-Patch_Size_Value/2, -Patch_Size_Value/3),
        "13": (-Patch_Size_Value/2, -Patch_Size_Value/2),
        "14": ( Patch_Size_Value/2, -Patch_Size_Value/2)
    }
    
    Code = []
    Code.append(Code_Header(10))

    Well_Parameters = []
    
    # Loop through the pressure and speed values to create well parameters.
    
    for Row_Index, Speed_Val in enumerate(Speeds_Values):
        for Column_Index, Pressure_Val in enumerate(Pressures_Values):
            Well_Position = Row_Index * Columns_Number + Column_Index + 1
            Center_X = Well_Center_Offset * Column_Index
            Center_Y = Well_Center_Offset * Row_Index
            Well_Parameters.append((Well_Position, Center_X, Center_Y, Pressure_Val, Speed_Val))
                        
    for Well_Position, Center_X, Center_Y, Pressure_Val, Speed_Val in Well_Parameters:
        for Layer in range(2):
            CurrentLayerZ = Nozzle_Diameter_Value * (Layer + 1)
            Rotation_Angle = [0,90][Layer]

            First_Point = Points["1"]
            First_Point_Rotated_X, First_Point_Rotated_Y = Rotation(First_Point[0], First_Point[1], Rotation_Angle)

            Code.append(f";")
            Code.append(f"; LAYER {Layer + 1} AT {CurrentLayerZ:.2f} MM FOR WELL {Well_Position}")
            Code.append(f";")

            Code.append(f"T0; DEFINED TOOL TO BE USED.")
            Code.append(f"M773 T0 P{Pressure_Val}; EXTRUDE AT {Pressure_Val} KPA")
            Code.append(Well_Positioning(Center_X, Center_Y, First_Point_Rotated_X + Center_X, First_Point_Rotated_Y + Center_Y, 4800, CurrentLayerZ))
            Code.append(f"G1 F{Speed_Val}; PRINTING SPEED AT {Speed_Val} MM/MIN")

            for i, (X, Y) in Points.items():
                X_Rotated, Y_Rotated = Rotation(X, Y, Rotation_Angle)
                Code.append(Printing_Move(X_Rotated + Center_X, Y_Rotated + Center_Y))  
                
            Code.append(Rise_Move(Well_Height, 4800))
    
    # Export the G-code to a file.
    
    GCode = os.path.join(CURRENT_DIRECTORY, f"Printability_Test.gcode")
    Code_Exporter("\n".join(Code), GCode)
    print(f"G-code has been exported to {GCode}")
    print(f"Pressures used: {Pressures_Values}, Speeds used: {Speeds_Values}")
    
    return [GCode]


def Rise_Move(Well_Height, Moving_Speed):
    
    """ 
    
    Move the nozzle tip up to a specified height after printing a layer. Consider it as a retraction move.
    
    Args:
        
        Well_Height [float]: The height of the well in mm.
        Moving_Speed [float]: The speed of the move in mm/min.
    
    Returns:
            
        str: G-code for the rising move.
    
    """

    Code = [
        ";",
        "; NOZZLE TIP RISING MOVE",
        f"G1 F{Moving_Speed};",
        f"G0 Z{2*Well_Height:.4f}; ADJUSTING CURRENT LAYER HEIGHT.",
        ";"
    ]

    return "\n".join(Code)

def Well_Positioning(Center_X, Center_Y, Point_X, Point_Y, MovingSpeed, FirstLayerHeight):

    """
    
    Position the nozzle tip at the center of the well and adjust the height for printing.
    
    Args:
            
        Center_X [float]: The X coordinate of the well center.
        Center_Y [float]: The Y coordinate of the well center.
        Point_X [float]: The X coordinate of the point to move to.
        Point_Y [float]: The Y coordinate of the point to move to.
        MovingSpeed [float]: The speed of the move in mm/min.
        FirstLayerHeight [float]: The height of the first layer in mm.
        
    Returns:
        
         str: G-code for the well positioning.
         
    """
    
    Code = [
        "; WELL POSITIONING",
        f"G0 X{Point_X + Center_X:.4f} Y{Point_Y + Center_Y:.4f} F{MovingSpeed}; MOVE TO FIRST POINT.",
        f"G0 Z{FirstLayerHeight:.4f} F{MovingSpeed}; ADJUST CURRENT LAYER HEIGHT.",
        ";"
    ]

    return "\n".join(Code)

def Code_Header(Plaque_Temperature):
    
    """
    
    Generate G-code header for the printability test.
    
    The header includes settings for the printer, such as units, positioning, and temperature.
    
    Args:
    
        Plaque_Temperature [float]: The temperature of the print bed in degrees Celsius.
            
    Returns:   
        
        str: G-code header.
    
    """  
    
    return "\n".join([
        "; PRINTING",
        "G21; SET UNITS TO MILLIMETERS. UNITS FROM NOW ARE IN MILLIMETERS",
        "G90; ABSOLUTE POSITIONING. COORDINATES ARE ABSOLUTE TO ORIGIN",
        "M82; DISABLE EXTRUDER RELATIVE MODE. DISABLE RELIVE MODE FOR EXTRUDE VALUES",
        f"M801 S{Plaque_Temperature}; SET PLAQUE TEMPERATURE AT {Plaque_Temperature}ºC",
        "G0 Z40.000; CONTROLLED MOVE UP THE PLAQUE",
        ";",
        ";"
    ])

def Code_Footer():
    
    """
    
    Generate G-code footer for the printability test.
    
    The footer includes commands to lift the toolhead and stop idle hold.
    
    Args:
    
        Nothing.
                    
    Returns:   
    
        str: G-code footer.    
    
    """  
    
    return "\n".join([
        ";",
        ";",
        ";",
        "G0 Z40; LIFT TOOLHEAD",
        "M84; STOP IDLE HOLD",
        "; END"
    ])
    
def Printing_Move(X_Position, Y_Position):
    
    """ 
    
    Create a printing move command in G-code format.
    
    Args:
        
        X_Position [float]: The X coordinate for the move.
        Y_Position [float]: The Y coordinate for the move.
    
    Returns:
            
        str: G-code for the printing move.
    
    """
    
    return f"G1 X{X_Position:.4f} Y{Y_Position:.4f}  E1; PRINTING LINE"

def Code_Exporter(Gcode, Filename):
    
    """
    
    Export GCode to a file.
    
    Args:
        
        Gcode [str]: The G-code to be exported.
        Filename [str]: The name of the file to save the G-code.
         
    Returns:   
        
        Nothing.
    
    """  
    
    with open(Filename, 'w') as file:
        file.write(Gcode)
    print(f"G-code has been exported to {Filename}")
    
def Rotation(PreviousX, PreviousY, RotationAngle):
    
    """ 

    The patch is rotated around the center of the well. In this case, the center of the well is defined as (0,0).
    
    Args:
        
        PreviousX [float]: The X coordinate before rotation.
        PreviousY [float]: The Y coordinate before rotation.
        RotationAngle [float]: The angle of rotation in degrees.
    
    Returns:
        
        NewX [float]: The new X coordinate after rotation.
        NewY [float]: The new Y coordinate after rotation.
        
    """
    
    Angle = math.radians(RotationAngle)
    Cosinus = math.cos(Angle)
    Sinus = math.sin(Angle)
    NewX = PreviousX * Cosinus - PreviousY * Sinus
    NewY = PreviousX * Sinus + PreviousY * Cosinus

    return NewX, NewY

def Generate_Range(Initial, Final, Step):

    """
    Generate float range from Initial to Final in increments of Step (inclusive).
    
    This function creates a list of float values starting from Initial and ending at Final, with increments of Step. The range is generated to properly handle both ascending and descending values for mapping all the values of the test.
    
    Args:
        
        Initial [float]: The starting value of the range.
        Final [float]: The ending value of the range.
        Step [float]: The increment value for the range.
            
    Returns:
    
        Values [list]: A list of float values in the specified range.
            
    """

    if Initial is None or Final is None or Step is None:
        return []

    Values = []
    Current_Value = Initial
    
    # Ascending range.
    
    if Step > 0 and Initial <= Final:
        while Current_Value <= Final:
            Values.append(round(Current_Value, 4))
            Current_Value += Step
            
    # Descending range. 
    
    elif Step < 0 and Initial >= Final:
        while Current_Value >= Final:
            Values.append(round(Current_Value, 4))
            Current_Value += Step
            
    return Values
    