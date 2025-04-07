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
Date: May 10, 2024

Description:

    This script is made to modify the G-Code generated in Slic3r to adapt it to bioprinting BIO-X [CELLINK].


Usage:
    
    Run the Application and Select the desired folder to storage it.

License:

Future updates:

    Include bed temperature and printhead temperature.
    Create condition for each toolhead. Not only for T0.

"""

################################################################################################
# Main libraries import:
import sys
import os
import numpy as np
from Extrudability import Extrudability_Test
from Deposition import Filament_Deposition_Test
from Printability import Printability_Test
################################################################################################
# UI modules import:
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PySide6.QtCore import Qt
################################################################################################
# UI APP directory:
sys.path.append(r'D:\GCodePorter')
from UIoutput import Ui_Form
################################################################################################
         
class MainWindow(QMainWindow, Ui_Form):
    def __init__(self, parent=None):
        
        # Initialize the parent class and setup the UI. 
                
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        
         # Set the window title to "Bioprinting App"

        self.setWindowTitle('Bioprinting App')

        # Hide certain labels and line edits initially.

        self.Visibility(self.PrintabilityInitialPressureLabel, False)
        self.Visibility(self.PrintabilityInitialPressureValueLineEdit, False)
        self.Visibility(self.PrintabilityFinalPressureLabel, False)
        self.Visibility(self.PrintabilityFinalPressureValueLineEdit, False)
        self.Visibility(self.PrintabilityStepPressureLabel, False)
        self.Visibility(self.PrintabilityStepPressureValueLineEdit, False)

        self.Visibility(self.PrintabilityInitialSpeedLabel, False)
        self.Visibility(self.PrintabilityInitialSpeedValueLineEdit, False)
        self.Visibility(self.PrintabilityFinalSpeedLabel, False)
        self.Visibility(self.PrintabilityFinalSpeedValueLineEdit, False)
        self.Visibility(self.PrintabilityStepSpeedLabel, False)
        self.Visibility(self.PrintabilityStepSpeedValueLineEdit, False)

        self.Visibility(self.DepositionInitialPressureLabel, False)
        self.Visibility(self.DepositionInitialPressureValueLineEdit, False)
        self.Visibility(self.DepositionFinalPressureLabel, False)
        self.Visibility(self.DepositionFinalPressureValueLineEdit, False)
        self.Visibility(self.DepositionStepPressureLabel, False)
        self.Visibility(self.DepositionStepPressureValueLineEdit, False)

        self.Visibility(self.DepositionInitialSpeedLabel, False)
        self.Visibility(self.DepositionInitialSpeedValueLineEdit, False)
        self.Visibility(self.DepositionFinalSpeedLabel, False)
        self.Visibility(self.DepositionFinalSpeedValueLineEdit, False)
        self.Visibility(self.DepositionStepSpeedLabel, False)
        self.Visibility(self.DepositionStepSpeedValueLineEdit, False)

        # Populate combo boxes with specific items and center them.

        self.Populate_Combo_Box(self.ManufacturercomboBox, ["Thermo Fisher", "VWR", "Greiner Cellstar"])
        self.Center_Combo_Box(self.ManufacturercomboBox)
        self.Populate_Combo_Box(self.WellcomboBox, ["6", "12", "24", "48", "96"])
        self.Center_Combo_Box(self.WellcomboBox)
        self.Populate_Combo_Box(self.PrintabilityNozzleDiameterComboBox, ["0.2", "0.25", "0.4"])
        self.Center_Combo_Box(self.PrintabilityNozzleDiameterComboBox)
        self.Populate_Combo_Box(self.PrintabilitySizeComboBox, ["5", "10", "20"])
        self.Center_Combo_Box(self.PrintabilitySizeComboBox)
        self.Populate_Combo_Box(self.DepositionNozzleDiameterComboBox, ["0.2", "0.25", "0.4"])
        self.Center_Combo_Box(self.DepositionNozzleDiameterComboBox)
        self.Populate_Combo_Box(self.DepositionSizeComboBox, ["5", "10", "20"])
        self.Center_Combo_Box(self.DepositionSizeComboBox)
        self.Populate_Combo_Box(self.DepositionManufacturercomboBox, ["Thermo Fisher", "VWR", "Greiner Cellstar"])
        self.Center_Combo_Box(self.DepositionManufacturercomboBox)
        self.Populate_Combo_Box(self.DepositionWellcomboBox, ["6", "12", "24", "48", "96"])
        self.Center_Combo_Box(self.DepositionWellcomboBox)
        self.Populate_Combo_Box(self.PrintabilityManufacturercomboBox,["Thermo Fisher", "VWR", "Greiner Cellstar"])
        self.Center_Combo_Box(self.PrintabilityManufacturercomboBox)
        self.Populate_Combo_Box(self.PrintabilityWellcomboBox,["6", "12", "24", "48", "96"])
        self.Center_Combo_Box(self.PrintabilityWellcomboBox)
        
        # Set default radio buttons to checked.
    
        self.DepositionPressureConstantValueRadio.setChecked(True)
        self.DepositionSpeedConstantValueRadio.setChecked(True)
        
        self.PrintabilityPressureConstantValueRadio.setChecked(True)
        self.PrintabilitySpeedConstantValueRadio.setChecked(True)

        # Connect buttons to their respective functions.
                        
        self.ExtrudabilityButton.clicked.connect(self.Extrudability_GCode)
        self.PrintabilityButton.clicked.connect(self.Printability_GCode)
        self.DepositionButton.clicked.connect(self.Deposition_GCode)        
        self.Button_Connection()  
        self.labelContact.scaledContents = True

   
    def Center_Combo_Box(self, comboBox):
        
        """ 
        
        Center the text in the combo box and set it to be editable but read-only.
        This allows the user to see the selected item in the center of the combo box.
        
        Args:
        
            comboBox [QComboBox]: The combo box to be centered.
            
        Returns:
        
            Nothing.
        
        """
        
        comboBox.setEditable(True)
        comboBox.lineEdit().setReadOnly(True)
        comboBox.lineEdit().setAlignment(Qt.AlignCenter)


    def Populate_Combo_Box(self, comboBox, items):
        
        """
        
        Populate the combo box with a list of items.
        
        Args:
        
            comboBox [QComboBox]: The combo box to be populated.
            items [list]: A list of items to populate the combo box with.
        
        Returns:
        
            Nothing.
        
        """
        
        comboBox.addItems(items)  

    def Button_Connection(self):

        """ 
        
        Connect the radio buttons to the Update_Visibility function.
        
        This function will show or hide the corresponding line edits and labels based on the selected radio button.
        
        Args:
        
            Nothing.
        
        Returns:
        
            Nothing.
        
        """

        self.PrintabilityPressureConstantValueRadio.toggled.connect(self.Update_Visibility)
        self.PrintabilityPressureRangeValueRadio.toggled.connect(self.Update_Visibility)
        self.PrintabilitySpeedConstantValueRadio.toggled.connect(self.Update_Visibility)
        self.PrintabilitySpeedRangeValueRadio.toggled.connect(self.Update_Visibility)
        self.DepositionPressureConstantValueRadio.toggled.connect(self.Update_Visibility)
        self.DepositionPressureRangeValueRadio.toggled.connect(self.Update_Visibility)
        self.DepositionSpeedConstantValueRadio.toggled.connect(self.Update_Visibility)
        self.DepositionSpeedRangeValueRadio.toggled.connect(self.Update_Visibility)


    def Update_Visibility(self):  
        
        """ 
        
        Update the visibility of line edits and labels based on the selected radio button.
        
        Args:
        
            Nothing.
        
        Returns:
        
            Nothing.
        
        """

        if self.PrintabilityPressureConstantValueRadio.isChecked():
            self.Visibility(self.PrintabilityConstantPressureValueLineEdit, True)                        
            self.Visibility(self.PrintabilityConstantPressureLabel, True)
            self.Visibility(self.PrintabilityInitialPressureValueLineEdit, False)
            self.Visibility(self.PrintabilityInitialPressureLabel, False)
            self.Visibility(self.PrintabilityFinalPressureValueLineEdit, False)
            self.Visibility(self.PrintabilityFinalPressureLabel, False)
            self.Visibility(self.PrintabilityStepPressureValueLineEdit, False)
            self.Visibility(self.PrintabilityStepPressureLabel, False)
        elif self.PrintabilityPressureRangeValueRadio.isChecked():
            self.Visibility(self.PrintabilityConstantPressureValueLineEdit, False)
            self.Visibility(self.PrintabilityConstantPressureLabel, False)
            self.Visibility(self.PrintabilityInitialPressureValueLineEdit, True)
            self.Visibility(self.PrintabilityInitialPressureLabel, True)
            self.Visibility(self.PrintabilityFinalPressureValueLineEdit, True)
            self.Visibility(self.PrintabilityFinalPressureLabel, True)
            self.Visibility(self.PrintabilityStepPressureValueLineEdit, True)
            self.Visibility(self.PrintabilityStepPressureLabel, True)
        if self.PrintabilitySpeedConstantValueRadio.isChecked():
            self.Visibility(self.PrintabilityConstantSpeedValueLineEdit, True)
            self.Visibility(self.PrintabilityConstantSpeedLabel, True)
            self.Visibility(self.PrintabilityInitialSpeedValueLineEdit, False)
            self.Visibility(self.PrintabilityInitialSpeedLabel, False)
            self.Visibility(self.PrintabilityFinalSpeedValueLineEdit, False)
            self.Visibility(self.PrintabilityFinalSpeedLabel, False)
            self.Visibility(self.PrintabilityStepSpeedValueLineEdit, False)
            self.Visibility(self.PrintabilityStepSpeedLabel, False)
        elif self.PrintabilitySpeedRangeValueRadio.isChecked():
            self.Visibility(self.PrintabilityConstantSpeedValueLineEdit, False)
            self.Visibility(self.PrintabilityConstantSpeedLabel, False)
            self.Visibility(self.PrintabilityInitialSpeedValueLineEdit, True)
            self.Visibility(self.PrintabilityInitialSpeedLabel, True)
            self.Visibility(self.PrintabilityFinalSpeedValueLineEdit, True)
            self.Visibility(self.PrintabilityFinalSpeedLabel, True)
            self.Visibility(self.PrintabilityStepSpeedValueLineEdit, True)
            self.Visibility(self.PrintabilityStepSpeedLabel, True)

        if self.DepositionPressureConstantValueRadio.isChecked():
            self.Visibility(self.DepositionConstantPressureValueLineEdit, True)
            self.Visibility(self.DepositionConstantPressureLabel, True)
            self.Visibility(self.DepositionInitialPressureValueLineEdit, False)
            self.Visibility(self.DepositionInitialPressureLabel, False)
            self.Visibility(self.DepositionFinalPressureValueLineEdit, False)
            self.Visibility(self.DepositionFinalPressureLabel, False)
            self.Visibility(self.DepositionStepPressureValueLineEdit, False)
            self.Visibility(self.DepositionStepPressureLabel, False)
        elif self.DepositionPressureRangeValueRadio.isChecked():
            self.Visibility(self.DepositionConstantPressureValueLineEdit, False)
            self.Visibility(self.DepositionConstantPressureLabel, False)
            self.Visibility(self.DepositionInitialPressureValueLineEdit, True)
            self.Visibility(self.DepositionInitialPressureLabel, True)
            self.Visibility(self.DepositionFinalPressureValueLineEdit, True)
            self.Visibility(self.DepositionFinalPressureLabel, True)
            self.Visibility(self.DepositionStepPressureValueLineEdit, True)
            self.Visibility(self.DepositionStepPressureLabel, True)
        if self.DepositionSpeedConstantValueRadio.isChecked():
            self.Visibility(self.DepositionConstantSpeedValueLineEdit, True)
            self.Visibility(self.DepositionConstantSpeedLabel, True)
            self.Visibility(self.DepositionInitialSpeedValueLineEdit, False)
            self.Visibility(self.DepositionInitialSpeedLabel, False)
            self.Visibility(self.DepositionFinalSpeedValueLineEdit, False)
            self.Visibility(self.DepositionFinalSpeedLabel, False)
            self.Visibility(self.DepositionStepSpeedValueLineEdit, False)
            self.Visibility(self.DepositionStepSpeedLabel, False)
        elif self.DepositionSpeedRangeValueRadio.isChecked():
            self.Visibility(self.DepositionConstantSpeedValueLineEdit, False)
            self.Visibility(self.DepositionConstantSpeedLabel, False)
            self.Visibility(self.DepositionInitialSpeedValueLineEdit, True)
            self.Visibility(self.DepositionInitialSpeedLabel, True)
            self.Visibility(self.DepositionFinalSpeedValueLineEdit, True)
            self.Visibility(self.DepositionFinalSpeedLabel, True)
            self.Visibility(self.DepositionStepSpeedValueLineEdit, True)
            self.Visibility(self.DepositionStepSpeedLabel, True)



    def Visibility(self, widget, visible):
        
        """ 
        
        Set the visibility of a widget. If visible is True, the widget is shown and enabled.
        If visible is False, the widget is hidden and disabled.
        
        Args:
        
            widget [QWidget]: The widget to be shown or hidden.
            visible [bool]: True to show the widget, False to hide it.
        
        Returns:
        
            Nothing.
        
        """
        
        if visible:
            widget.setMaximumHeight(16777215)  
            widget.setMinimumHeight(0)  
            widget.setEnabled(True)  
        else:
            widget.setMaximumHeight(0)  
            widget.setMinimumHeight(0)  
            widget.setEnabled(False)  


    def Extrudability_GCode(self):
        
        """ 
        
        This function generates G-code for the extrudability test based on user inputs.
        
        Args:
        
            Nothing.
        
        Returns:
        
            Nothing.
        
        """
        
        try:
            
            Initial_Pressure = float(self.ExtrudabilityInitialPressureLineEdit.text()) if self.ExtrudabilityInitialPressureLineEdit.text() else None
            Final_Pressure = float(self.ExtrudabilityFinalPressureLineEdit.text()) if self.ExtrudabilityFinalPressureLineEdit.text() else None
            Step_Pressure = float(self.ExtrudabilityStepPressureLineEdit.text()) if self.ExtrudabilityStepPressureLineEdit.text() else None
            Printing_Time = float(self.PrintingTimeLineEdit.text()) if self.PrintingTimeLineEdit.text() else None
            Pause_Time = float(self.PauseTimeLineEdit.text()) if self.PauseTimeLineEdit.text() else None
            
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Please enter valid numbers for all fields.")
            return

        try:
            
            Manufacturer = self.ManufacturercomboBox.currentText()
            Number = int(self.WellcomboBox.currentText())
            self.Generated_GCode = Extrudability_Test(Manufacturer, Number, Initial_Pressure, Final_Pressure, Step_Pressure, Printing_Time, Pause_Time)

        except ValueError:
            QMessageBox.warning(self, "Input Error", "Please enter valid numbers for all required fields.")
            return

        if self.Generated_GCode:
            msg = "G-code files generated:\n" + "\n".join(self.Generated_GCode)
            QMessageBox.information(self, "Files Created", msg)



        
    def Deposition_GCode(self):
        
        """ 
        
        This function generates G-code for the deposition test based on user inputs.
        
        Args:
        
            Nothing.
        
        Returns:
        
            Nothing.
        
        """
        
        try:    
            if self.DepositionPressureConstantValueRadio.isChecked():
                Pressure = float(self.DepositionConstantPressureValueLineEdit.text())
                Initial_Pressure = Final_Pressure = Step_Pressure = None
            else:
                Pressure = None
                try:
                    Initial_Pressure = float(self.DepositionInitialPressureValueLineEdit.text()) if self.DepositionInitialPressureValueLineEdit.text() else None
                    Final_Pressure = float(self.DepositionFinalPressureValueLineEdit.text()) if self.DepositionFinalPressureValueLineEdit.text() else None
                    Step_Pressure = float(self.DepositionStepPressureValueLineEdit.text()) if self.DepositionStepPressureValueLineEdit.text() else None
                except ValueError:
                    QMessageBox.warning(self, "Input Error", "Please enter valid numbers for pressure values.")
                    return

            if self.DepositionSpeedConstantValueRadio.isChecked():
                Speed = float(self.DepositionConstantSpeedValueLineEdit.text())
                Initial_Speed = Final_Speed = Step_Speed = None
            else:
                Speed = None
                try:
                    Initial_Speed = float(self.DepositionInitialSpeedValueLineEdit.text()) if self.DepositionInitialSpeedValueLineEdit.text() else None
                    Final_Speed = float(self.DepositionFinalSpeedValueLineEdit.text()) if self.DepositionFinalSpeedValueLineEdit.text() else None
                    Step_Speed = float(self.DepositionStepSpeedValueLineEdit.text()) if self.DepositionStepSpeedValueLineEdit.text() else None
                except ValueError:
                    QMessageBox.warning(self, "Input Error", "Please enter valid numbers for speed values.")
                    return

            Manufacturer = self.DepositionManufacturercomboBox.currentText().strip()
            if not Manufacturer:
                QMessageBox.warning(self, "Input Error", "Please select a valid manufacturer.")
                return

            Number = self.DepositionWellcomboBox.currentText().strip()
            if not Number.isdigit():
                QMessageBox.warning(self, "Input Error", "Please select a valid well number.")
                return
            Number = int(Number)  

            Patch_Size = self.DepositionSizeComboBox.currentText().strip()
            Nozzle_Diameter = self.DepositionNozzleDiameterComboBox.currentText().strip()

        except ValueError:
            QMessageBox.warning(self, "Input Error", "Please enter valid numbers for all required fields.")
            return

        self.Generated_GCode = Filament_Deposition_Test(
            Manufacturer, Number, Patch_Size, Nozzle_Diameter,
            Initial_Pressure, Final_Pressure, Step_Pressure,
            Initial_Speed, Final_Speed, Step_Speed,
            Pressure, Speed
        )

        if self.Generated_GCode:
            msg = "G-code files generated:\n" + "\n".join(self.Generated_GCode)
            QMessageBox.information(self, "Files Created", msg)


    def Printability_GCode(self):
        
        """ 
        
        This function generates G-code for the printability test based on user inputs.
        
        Args:
        
            Nothing.
        
        Returns:
        
            Nothing.
        
        """
        
        try:    
            if self.PrintabilityPressureConstantValueRadio.isChecked():
                Pressure = float(self.PrintabilityConstantPressureValueLineEdit.text())
                Initial_Pressure = Final_Pressure = Step_Pressure = None
            else:
                Pressure = None
                try:
                    Initial_Pressure = float(self.PrintabilityInitialPressureValueLineEdit.text()) if self.PrintabilityInitialPressureValueLineEdit.text() else None
                    Final_Pressure = float(self.PrintabilityFinalPressureValueLineEdit.text()) if self.PrintabilityFinalPressureValueLineEdit.text() else None
                    Step_Pressure = float(self.PrintabilityStepPressureValueLineEdit.text()) if self.PrintabilityStepPressureValueLineEdit.text() else None
                except ValueError:
                    QMessageBox.warning(self, "Input Error", "Please enter valid numbers for pressure values.")
                    return

            if self.PrintabilitySpeedConstantValueRadio.isChecked():
                Speed = float(self.PrintabilityConstantSpeedValueLineEdit.text())
                Initial_Speed = Final_Speed = Step_Speed = None
            else:
                Speed = None
                try:
                    Initial_Speed = float(self.PrintabilityInitialSpeedValueLineEdit.text()) if self.PrintabilityInitialSpeedValueLineEdit.text() else None
                    Final_Speed = float(self.PrintabilityFinalSpeedValueLineEdit.text()) if self.PrintabilityFinalSpeedValueLineEdit.text() else None
                    Step_Speed = float(self.PrintabilityStepSpeedValueLineEdit.text()) if self.PrintabilityStepSpeedValueLineEdit.text() else None
                except ValueError:
                    QMessageBox.warning(self, "Input Error", "Please enter valid numbers for speed values.")
                    return

            Manufacturer = self.PrintabilityManufacturercomboBox.currentText().strip()
            if not Manufacturer:
                QMessageBox.warning(self, "Input Error", "Please select a valid manufacturer.")
                return

            Number = self.PrintabilityWellcomboBox.currentText().strip()
            if not Number.isdigit():
                QMessageBox.warning(self, "Input Error", "Please select a valid well number.")
                return
            Number = int(Number)  

            Patch_Size = self.PrintabilitySizeComboBox.currentText().strip()
            Nozzle_Diameter = self.PrintabilityNozzleDiameterComboBox.currentText().strip()

        except ValueError:
            QMessageBox.warning(self, "Input Error", "Please enter valid numbers for all required fields.")
            return

        self.Generated_GCode = Printability_Test(
            Manufacturer, Number, Patch_Size, Nozzle_Diameter,
            Initial_Pressure, Final_Pressure, Step_Pressure,
            Initial_Speed, Final_Speed, Step_Speed,
            Pressure, Speed
        )

        if self.Generated_GCode:
            msg = "G-code files generated:\n" + "\n".join(self.Generated_GCode)
            QMessageBox.information(self, "Files Created", msg)
        

    def Save_GCode(self):
        
        """ 
        
        Generate G-Code for the selected test and save it to a file.
        If no G-Code has been generated, show a warning message.
        
        Args:
        
            Nothing.
        
        Returns:
            
            Nothing.
        
        """
        
        if not self.Generated_GCode:
            QMessageBox.warning(self, "No G-Code", "Please generate the G-Code before saving.")
            return

        file_dialog = QFileDialog(self)
        file_dialog.setAcceptMode(QFileDialog.AcceptSave)
        file_dialog.setNameFilter("G-Code Files (*.gcode);;All Files (*)")
        if file_dialog.exec() == QFileDialog.Accepted:
            file_path = file_dialog.selectedFiles()[0]
            with open(file_path, "w") as file:
                file.write(self.Generated_GCode)
            QMessageBox.information(self, "File Saved", f"G-Code has been saved to {file_path}.")


if __name__ == "__main__":
    app = QApplication.instance()  
    if not app:  
        app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec())
