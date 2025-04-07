import json
import os
from PySide6.QtWidgets import QMessageBox

##################################################
#           Extrudability Test Functions         #
##################################################

def Extrudability_Test(Manufacturer, Number, Initial_Pressure, Final_Pressure, Step_Pressure, Printing_Time, Pause_Time):

    """
    
    Generate G-code for an extrudability test based on the specified printing parameters assigned by the user.
        
    The G-code is generated for a specific well plate configuration and saved to a file.
    
    Args:
    
        Manufacturer [str]: The manufacturer of the well plate.
        Number [int]: The number of wells in the well plate.
        Initial_Pressure [float]: The initial pressure for the test.
        Final_Pressure [float]: The final pressure for the test.
        Step_Pressure [float]: The step pressure for the test.
        Printing_Time [float]: The time for printing in seconds.
        Pause_Time [float]: The pause time in milliseconds.
        
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


    Code = []
    
    Code.append(Code_Header(10))
    
    Pressures = []
    Current_Pressure = Initial_Pressure

    # Calculate the list of Pressures.
    
    if Initial_Pressure <= Final_Pressure:
        while Current_Pressure <= Final_Pressure:
            Pressures.append(Current_Pressure)
            Current_Pressure += Step_Pressure
    else:
        while Current_Pressure >= Final_Pressure:
            Pressures.append(Current_Pressure)
            Current_Pressure -= Step_Pressure
            
    Pressures.sort(reverse=True)

    # Ensure the well plate has enough wells for triplicates. In this case, we need 4 wells for each pressure value.
    
    Required_Wells = len(Pressures) * 4
    Available_Wells = Rows_Number * Columns_Number

    if Required_Wells > Available_Wells:
        MSG = (
            f"Your selected range exceeds the plate capacity.\n"
            f"Plate can handle up to {Available_Wells} wells, you need {Required_Wells} wells.\n"
            "Do you want to trim to fit, or cancel and change your values?"
        )
        Answer = QMessageBox.question(None, "Range Exceeds Capacity", MSG,
                                    QMessageBox.Yes | QMessageBox.No)
        if Answer == QMessageBox.Yes:
            Pressures = Pressures[:Available_Wells // 4]
        else:
            return None  

    # Generate G-code for each pressure value.

    for i, Pressure in enumerate(Pressures):
        if i < Columns_Number:  
            Column = i  
            if Column >= Columns_Number:
                break  
            Wells = [(row, Column) for row in range(4)]

        else:  
            Column = Columns_Number - (i - Columns_Number) - 1
            if Column < 0:
                break  
            Wells = [(row, Column) for row in range(Rows_Number - 1, Rows_Number - 5, -1)]

        for Row, Column in Wells:
            Center_X = Well_Center_Offset * Column
            Center_Y = Well_Center_Offset * Row
            Well_Position = Row * Rows_Number + Column + 1
            Code.append(f"; WELL {Well_Position}:")
            Code.append(f"T0; DEFINED TOOL TO BE USED.")
            Code.append(f"G0 X{Center_X:.3f} Y{Center_Y:.3f} F4800; MOVE TO WELL CENTER TO LAYER 0")
            Code.append(f"G0 Z0.50; ADJUST NOZZLE TIP HEIGHT")
            Code.append(f"G4 P{Pause_Time}; DWELL FOR {Pause_Time} MILLISECONDS")
            Code.append(f"M750 T0 P{Pressure} D{Printing_Time * 1000}; EXTRUDE AT {Pressure} KPA FOR {Printing_Time} SECONDS")
            Code.append(f"G0 F4800; NOZZLE TRAVEL SPEED AT 4800 mm/min")
            Code.append(f"G0 Z40; LIFT TOOLHEAD")
            
    Code.append(Code_Footer())
    
    # Export the G-code to a file.
    
    GCode = os.path.join(CURRENT_DIRECTORY, f"Extrudability_Test.gcode")
    Code_Exporter("\n".join(Code), GCode)
    print(f"G-code has been exported to {GCode}")

    return [GCode]

def Code_Header(Plaque_Temperature):
    
    """
    
    Generate G-code header for the extrudability test.
    
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
    
    Generate G-code footer for the extrudability test.
    
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
    