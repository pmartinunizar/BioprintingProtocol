# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'PorterUI.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QGridLayout, QGroupBox,
    QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QRadioButton, QSizePolicy, QTabWidget, QVBoxLayout,
    QWidget)

import os

class Ui_Form(object):
    def setupUi(self, Form):
        
        # Image folder location
        image_folder = os.path.join(os.path.dirname(__file__), 'Images')
        logo_image = os.path.join(image_folder, 'logo_m2be_2024.png')
        extrudability_image = os.path.join(image_folder, 'Extrudability_Image.png')
        deposition_image = os.path.join(image_folder, 'Deposition_Image.png')
        printability_image = os.path.join(image_folder, 'Printability_Image.png')
        
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(800, 376)
        self.tabWidget = QTabWidget(Form)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setGeometry(QRect(0, 10, 801, 371))
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.Extrudability = QWidget()
        self.Extrudability.setObjectName(u"Extrudability")
        self.layoutWidget = QWidget(self.Extrudability)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(360, 20, 112, 59))
        self.gridLayout_5 = QGridLayout(self.layoutWidget)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(0, 0, 0, 0)
        self.ExtrudabilityButton = QPushButton(self.layoutWidget)
        self.ExtrudabilityButton.setObjectName(u"ExtrudabilityButton")

        self.gridLayout_5.addWidget(self.ExtrudabilityButton, 2, 0, 1, 1)

        self.ExtrudabilityLabel = QLabel(self.layoutWidget)
        self.ExtrudabilityLabel.setObjectName(u"ExtrudabilityLabel")
        font = QFont()
        font.setBold(True)
        self.ExtrudabilityLabel.setFont(font)
        self.ExtrudabilityLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_5.addWidget(self.ExtrudabilityLabel, 1, 0, 1, 1)

        self.layoutWidget1 = QWidget(self.Extrudability)
        self.layoutWidget1.setObjectName(u"layoutWidget1")
        self.layoutWidget1.setGeometry(QRect(20, 100, 301, 201))
        self.gridLayout_4 = QGridLayout(self.layoutWidget1)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.ExtrudabilityInitialPressureLabel = QLabel(self.layoutWidget1)
        self.ExtrudabilityInitialPressureLabel.setObjectName(u"ExtrudabilityInitialPressureLabel")
        self.ExtrudabilityInitialPressureLabel.setFont(font)

        self.gridLayout_4.addWidget(self.ExtrudabilityInitialPressureLabel, 0, 0, 1, 1)

        self.ExtrudabilityInitialPressureLineEdit = QLineEdit(self.layoutWidget1)
        self.ExtrudabilityInitialPressureLineEdit.setObjectName(u"ExtrudabilityInitialPressureLineEdit")

        self.gridLayout_4.addWidget(self.ExtrudabilityInitialPressureLineEdit, 0, 1, 1, 1)

        self.ExtrudabilityFinalPressureLabel = QLabel(self.layoutWidget1)
        self.ExtrudabilityFinalPressureLabel.setObjectName(u"ExtrudabilityFinalPressureLabel")
        self.ExtrudabilityFinalPressureLabel.setFont(font)

        self.gridLayout_4.addWidget(self.ExtrudabilityFinalPressureLabel, 1, 0, 1, 1)

        self.ExtrudabilityFinalPressureLineEdit = QLineEdit(self.layoutWidget1)
        self.ExtrudabilityFinalPressureLineEdit.setObjectName(u"ExtrudabilityFinalPressureLineEdit")

        self.gridLayout_4.addWidget(self.ExtrudabilityFinalPressureLineEdit, 1, 1, 1, 1)

        self.ExtrudabilityStepPressureLabel = QLabel(self.layoutWidget1)
        self.ExtrudabilityStepPressureLabel.setObjectName(u"ExtrudabilityStepPressureLabel")
        self.ExtrudabilityStepPressureLabel.setFont(font)

        self.gridLayout_4.addWidget(self.ExtrudabilityStepPressureLabel, 2, 0, 1, 1)

        self.ExtrudabilityStepPressureLineEdit = QLineEdit(self.layoutWidget1)
        self.ExtrudabilityStepPressureLineEdit.setObjectName(u"ExtrudabilityStepPressureLineEdit")

        self.gridLayout_4.addWidget(self.ExtrudabilityStepPressureLineEdit, 2, 1, 1, 1)

        self.PrintingTimeLabel = QLabel(self.layoutWidget1)
        self.PrintingTimeLabel.setObjectName(u"PrintingTimeLabel")
        self.PrintingTimeLabel.setFont(font)

        self.gridLayout_4.addWidget(self.PrintingTimeLabel, 3, 0, 1, 1)

        self.PrintingTimeLineEdit = QLineEdit(self.layoutWidget1)
        self.PrintingTimeLineEdit.setObjectName(u"PrintingTimeLineEdit")

        self.gridLayout_4.addWidget(self.PrintingTimeLineEdit, 3, 1, 1, 1)

        self.PauseTimeLabel = QLabel(self.layoutWidget1)
        self.PauseTimeLabel.setObjectName(u"PauseTimeLabel")
        self.PauseTimeLabel.setFont(font)

        self.gridLayout_4.addWidget(self.PauseTimeLabel, 4, 0, 1, 1)

        self.PauseTimeLineEdit = QLineEdit(self.layoutWidget1)
        self.PauseTimeLineEdit.setObjectName(u"PauseTimeLineEdit")

        self.gridLayout_4.addWidget(self.PauseTimeLineEdit, 4, 1, 1, 1)

        self.labelLogo = QLabel(self.Extrudability)
        self.labelLogo.setObjectName(u"labelLogo")
        self.labelLogo.setGeometry(QRect(370, 220, 91, 81))
        self.labelLogo.setPixmap(QPixmap(logo_image))
        self.labelLogo.setScaledContents(True)
        self.ExtrudabilityImage = QLabel(self.Extrudability)
        self.ExtrudabilityImage.setObjectName(u"ExtrudabilityImage")
        self.ExtrudabilityImage.setGeometry(QRect(560, 60, 201, 191))
        self.ExtrudabilityImage.setPixmap(QPixmap(extrudability_image))
        self.ExtrudabilityImage.setScaledContents(True)
        self.widget = QWidget(self.Extrudability)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(20, 20, 301, 68))
        self.gridLayout = QGridLayout(self.widget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.ManufacturerLabel = QLabel(self.widget)
        self.ManufacturerLabel.setObjectName(u"ManufacturerLabel")
        sizePolicy.setHeightForWidth(self.ManufacturerLabel.sizePolicy().hasHeightForWidth())
        self.ManufacturerLabel.setSizePolicy(sizePolicy)
        self.ManufacturerLabel.setFont(font)

        self.gridLayout.addWidget(self.ManufacturerLabel, 0, 0, 1, 1)

        self.ManufacturercomboBox = QComboBox(self.widget)
        self.ManufacturercomboBox.setObjectName(u"ManufacturercomboBox")

        self.gridLayout.addWidget(self.ManufacturercomboBox, 0, 1, 1, 1)

        self.WellLabel = QLabel(self.widget)
        self.WellLabel.setObjectName(u"WellLabel")
        self.WellLabel.setFont(font)

        self.gridLayout.addWidget(self.WellLabel, 1, 0, 1, 1)

        self.WellcomboBox = QComboBox(self.widget)
        self.WellcomboBox.setObjectName(u"WellcomboBox")

        self.gridLayout.addWidget(self.WellcomboBox, 1, 1, 1, 1)

        self.widget1 = QWidget(self.Extrudability)
        self.widget1.setObjectName(u"widget1")
        self.widget1.setGeometry(QRect(350, 100, 142, 90))
        self.gridLayout_2 = QGridLayout(self.widget1)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.labelContact = QLabel(self.widget1)
        self.labelContact.setObjectName(u"labelContact")
        self.labelContact.setFont(font)
        self.labelContact.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.labelContact, 0, 0, 1, 1)

        self.labelMail1 = QLabel(self.widget1)
        self.labelMail1.setObjectName(u"labelMail1")
        self.labelMail1.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.labelMail1, 1, 0, 1, 1)

        self.labelMail1_2 = QLabel(self.widget1)
        self.labelMail1_2.setObjectName(u"labelMail1_2")
        self.labelMail1_2.setScaledContents(False)
        self.labelMail1_2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.labelMail1_2, 2, 0, 1, 1)

        self.labelMail2 = QLabel(self.widget1)
        self.labelMail2.setObjectName(u"labelMail2")
        self.labelMail2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.labelMail2, 3, 0, 1, 1)

        self.tabWidget.addTab(self.Extrudability, "")
        self.Deposition = QWidget()
        self.Deposition.setObjectName(u"Deposition")
        self.layoutWidget_10 = QWidget(self.Deposition)
        self.layoutWidget_10.setObjectName(u"layoutWidget_10")
        self.layoutWidget_10.setGeometry(QRect(270, 190, 241, 116))
        self.gridLayout_16 = QGridLayout(self.layoutWidget_10)
        self.gridLayout_16.setObjectName(u"gridLayout_16")
        self.gridLayout_16.setContentsMargins(0, 0, 0, 0)
        self.DepositionConstantSpeedLabel = QLabel(self.layoutWidget_10)
        self.DepositionConstantSpeedLabel.setObjectName(u"DepositionConstantSpeedLabel")
        self.DepositionConstantSpeedLabel.setFont(font)

        self.gridLayout_16.addWidget(self.DepositionConstantSpeedLabel, 0, 0, 1, 1)

        self.DepositionConstantSpeedValueLineEdit = QLineEdit(self.layoutWidget_10)
        self.DepositionConstantSpeedValueLineEdit.setObjectName(u"DepositionConstantSpeedValueLineEdit")

        self.gridLayout_16.addWidget(self.DepositionConstantSpeedValueLineEdit, 0, 1, 1, 1)

        self.DepositionInitialSpeedLabel = QLabel(self.layoutWidget_10)
        self.DepositionInitialSpeedLabel.setObjectName(u"DepositionInitialSpeedLabel")
        self.DepositionInitialSpeedLabel.setFont(font)

        self.gridLayout_16.addWidget(self.DepositionInitialSpeedLabel, 1, 0, 1, 1)

        self.DepositionInitialSpeedValueLineEdit = QLineEdit(self.layoutWidget_10)
        self.DepositionInitialSpeedValueLineEdit.setObjectName(u"DepositionInitialSpeedValueLineEdit")

        self.gridLayout_16.addWidget(self.DepositionInitialSpeedValueLineEdit, 1, 1, 1, 1)

        self.DepositionFinalSpeedLabel = QLabel(self.layoutWidget_10)
        self.DepositionFinalSpeedLabel.setObjectName(u"DepositionFinalSpeedLabel")
        self.DepositionFinalSpeedLabel.setFont(font)

        self.gridLayout_16.addWidget(self.DepositionFinalSpeedLabel, 2, 0, 1, 1)

        self.DepositionFinalSpeedValueLineEdit = QLineEdit(self.layoutWidget_10)
        self.DepositionFinalSpeedValueLineEdit.setObjectName(u"DepositionFinalSpeedValueLineEdit")

        self.gridLayout_16.addWidget(self.DepositionFinalSpeedValueLineEdit, 2, 1, 1, 1)

        self.DepositionStepSpeedLabel = QLabel(self.layoutWidget_10)
        self.DepositionStepSpeedLabel.setObjectName(u"DepositionStepSpeedLabel")
        self.DepositionStepSpeedLabel.setFont(font)

        self.gridLayout_16.addWidget(self.DepositionStepSpeedLabel, 3, 0, 1, 1)

        self.DepositionStepSpeedValueLineEdit = QLineEdit(self.layoutWidget_10)
        self.DepositionStepSpeedValueLineEdit.setObjectName(u"DepositionStepSpeedValueLineEdit")

        self.gridLayout_16.addWidget(self.DepositionStepSpeedValueLineEdit, 3, 1, 1, 1)

        self.layoutWidget_13 = QWidget(self.Deposition)
        self.layoutWidget_13.setObjectName(u"layoutWidget_13")
        self.layoutWidget_13.setGeometry(QRect(10, 90, 501, 91))
        self.horizontalLayout_5 = QHBoxLayout(self.layoutWidget_13)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.DepositionPressureBOX = QGroupBox(self.layoutWidget_13)
        self.DepositionPressureBOX.setObjectName(u"DepositionPressureBOX")
        font1 = QFont()
        font1.setBold(False)
        self.DepositionPressureBOX.setFont(font1)
        self.verticalLayout_9 = QVBoxLayout(self.DepositionPressureBOX)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.DepositionPressureConstantValueRadio = QRadioButton(self.DepositionPressureBOX)
        self.DepositionPressureConstantValueRadio.setObjectName(u"DepositionPressureConstantValueRadio")

        self.verticalLayout_9.addWidget(self.DepositionPressureConstantValueRadio)

        self.DepositionPressureRangeValueRadio = QRadioButton(self.DepositionPressureBOX)
        self.DepositionPressureRangeValueRadio.setObjectName(u"DepositionPressureRangeValueRadio")

        self.verticalLayout_9.addWidget(self.DepositionPressureRangeValueRadio)


        self.horizontalLayout_5.addWidget(self.DepositionPressureBOX)

        self.DepositionSpeedBOX = QGroupBox(self.layoutWidget_13)
        self.DepositionSpeedBOX.setObjectName(u"DepositionSpeedBOX")
        self.verticalLayout_10 = QVBoxLayout(self.DepositionSpeedBOX)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.DepositionSpeedConstantValueRadio = QRadioButton(self.DepositionSpeedBOX)
        self.DepositionSpeedConstantValueRadio.setObjectName(u"DepositionSpeedConstantValueRadio")

        self.verticalLayout_10.addWidget(self.DepositionSpeedConstantValueRadio)

        self.DepositionSpeedRangeValueRadio = QRadioButton(self.DepositionSpeedBOX)
        self.DepositionSpeedRangeValueRadio.setObjectName(u"DepositionSpeedRangeValueRadio")

        self.verticalLayout_10.addWidget(self.DepositionSpeedRangeValueRadio)


        self.horizontalLayout_5.addWidget(self.DepositionSpeedBOX)

        self.layoutWidget_14 = QWidget(self.Deposition)
        self.layoutWidget_14.setObjectName(u"layoutWidget_14")
        self.layoutWidget_14.setGeometry(QRect(10, 190, 241, 116))
        self.gridLayout_20 = QGridLayout(self.layoutWidget_14)
        self.gridLayout_20.setObjectName(u"gridLayout_20")
        self.gridLayout_20.setContentsMargins(0, 0, 0, 0)
        self.DepositionConstantPressureLabel = QLabel(self.layoutWidget_14)
        self.DepositionConstantPressureLabel.setObjectName(u"DepositionConstantPressureLabel")
        self.DepositionConstantPressureLabel.setFont(font)

        self.gridLayout_20.addWidget(self.DepositionConstantPressureLabel, 0, 0, 1, 1)

        self.DepositionConstantPressureValueLineEdit = QLineEdit(self.layoutWidget_14)
        self.DepositionConstantPressureValueLineEdit.setObjectName(u"DepositionConstantPressureValueLineEdit")

        self.gridLayout_20.addWidget(self.DepositionConstantPressureValueLineEdit, 0, 1, 1, 1)

        self.DepositionInitialPressureLabel = QLabel(self.layoutWidget_14)
        self.DepositionInitialPressureLabel.setObjectName(u"DepositionInitialPressureLabel")
        self.DepositionInitialPressureLabel.setFont(font)

        self.gridLayout_20.addWidget(self.DepositionInitialPressureLabel, 1, 0, 1, 1)

        self.DepositionInitialPressureValueLineEdit = QLineEdit(self.layoutWidget_14)
        self.DepositionInitialPressureValueLineEdit.setObjectName(u"DepositionInitialPressureValueLineEdit")

        self.gridLayout_20.addWidget(self.DepositionInitialPressureValueLineEdit, 1, 1, 1, 1)

        self.DepositionFinalPressureLabel = QLabel(self.layoutWidget_14)
        self.DepositionFinalPressureLabel.setObjectName(u"DepositionFinalPressureLabel")
        self.DepositionFinalPressureLabel.setFont(font)

        self.gridLayout_20.addWidget(self.DepositionFinalPressureLabel, 2, 0, 1, 1)

        self.DepositionFinalPressureValueLineEdit = QLineEdit(self.layoutWidget_14)
        self.DepositionFinalPressureValueLineEdit.setObjectName(u"DepositionFinalPressureValueLineEdit")

        self.gridLayout_20.addWidget(self.DepositionFinalPressureValueLineEdit, 2, 1, 1, 1)

        self.DepositionStepPressureLabel = QLabel(self.layoutWidget_14)
        self.DepositionStepPressureLabel.setObjectName(u"DepositionStepPressureLabel")
        self.DepositionStepPressureLabel.setFont(font)

        self.gridLayout_20.addWidget(self.DepositionStepPressureLabel, 3, 0, 1, 1)

        self.DepositionStepPressureValueLineEdit = QLineEdit(self.layoutWidget_14)
        self.DepositionStepPressureValueLineEdit.setObjectName(u"DepositionStepPressureValueLineEdit")

        self.gridLayout_20.addWidget(self.DepositionStepPressureValueLineEdit, 3, 1, 1, 1)

        self.layoutWidget_16 = QWidget(self.Deposition)
        self.layoutWidget_16.setObjectName(u"layoutWidget_16")
        self.layoutWidget_16.setGeometry(QRect(650, 20, 112, 59))
        self.gridLayout_22 = QGridLayout(self.layoutWidget_16)
        self.gridLayout_22.setObjectName(u"gridLayout_22")
        self.gridLayout_22.setContentsMargins(0, 0, 0, 0)
        self.DepositionGenerateButtonLabel = QLabel(self.layoutWidget_16)
        self.DepositionGenerateButtonLabel.setObjectName(u"DepositionGenerateButtonLabel")
        self.DepositionGenerateButtonLabel.setFont(font)
        self.DepositionGenerateButtonLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_22.addWidget(self.DepositionGenerateButtonLabel, 0, 0, 1, 1)

        self.DepositionButton = QPushButton(self.layoutWidget_16)
        self.DepositionButton.setObjectName(u"DepositionButton")

        self.gridLayout_22.addWidget(self.DepositionButton, 1, 0, 1, 1)

        self.layoutWidget2 = QWidget(self.Deposition)
        self.layoutWidget2.setObjectName(u"layoutWidget2")
        self.layoutWidget2.setGeometry(QRect(10, 20, 611, 68))
        self.gridLayout_19 = QGridLayout(self.layoutWidget2)
        self.gridLayout_19.setObjectName(u"gridLayout_19")
        self.gridLayout_19.setContentsMargins(0, 0, 0, 0)
        self.DepositionManufacturerLabel = QLabel(self.layoutWidget2)
        self.DepositionManufacturerLabel.setObjectName(u"DepositionManufacturerLabel")
        sizePolicy.setHeightForWidth(self.DepositionManufacturerLabel.sizePolicy().hasHeightForWidth())
        self.DepositionManufacturerLabel.setSizePolicy(sizePolicy)
        self.DepositionManufacturerLabel.setFont(font)

        self.gridLayout_19.addWidget(self.DepositionManufacturerLabel, 0, 0, 1, 1)

        self.DepositionManufacturercomboBox = QComboBox(self.layoutWidget2)
        self.DepositionManufacturercomboBox.setObjectName(u"DepositionManufacturercomboBox")

        self.gridLayout_19.addWidget(self.DepositionManufacturercomboBox, 0, 1, 1, 1)

        self.DepositionNozzleDiameterLabel = QLabel(self.layoutWidget2)
        self.DepositionNozzleDiameterLabel.setObjectName(u"DepositionNozzleDiameterLabel")
        self.DepositionNozzleDiameterLabel.setFont(font)

        self.gridLayout_19.addWidget(self.DepositionNozzleDiameterLabel, 0, 2, 1, 1)

        self.DepositionNozzleDiameterComboBox = QComboBox(self.layoutWidget2)
        self.DepositionNozzleDiameterComboBox.setObjectName(u"DepositionNozzleDiameterComboBox")

        self.gridLayout_19.addWidget(self.DepositionNozzleDiameterComboBox, 0, 3, 1, 1)

        self.DepositionWellLabel = QLabel(self.layoutWidget2)
        self.DepositionWellLabel.setObjectName(u"DepositionWellLabel")
        self.DepositionWellLabel.setFont(font)

        self.gridLayout_19.addWidget(self.DepositionWellLabel, 1, 0, 1, 1)

        self.DepositionWellcomboBox = QComboBox(self.layoutWidget2)
        self.DepositionWellcomboBox.setObjectName(u"DepositionWellcomboBox")

        self.gridLayout_19.addWidget(self.DepositionWellcomboBox, 1, 1, 1, 1)

        self.DepositionSizeLabel = QLabel(self.layoutWidget2)
        self.DepositionSizeLabel.setObjectName(u"DepositionSizeLabel")
        self.DepositionSizeLabel.setFont(font)

        self.gridLayout_19.addWidget(self.DepositionSizeLabel, 1, 2, 1, 1)

        self.DepositionSizeComboBox = QComboBox(self.layoutWidget2)
        self.DepositionSizeComboBox.setObjectName(u"DepositionSizeComboBox")

        self.gridLayout_19.addWidget(self.DepositionSizeComboBox, 1, 3, 1, 1)

        self.labelLogo_3 = QLabel(self.Deposition)
        self.labelLogo_3.setObjectName(u"labelLogo_3")
        self.labelLogo_3.setGeometry(QRect(540, 110, 231, 211))
        self.labelLogo_3.setPixmap(QPixmap(deposition_image))
        self.labelLogo_3.setScaledContents(True)
        self.tabWidget.addTab(self.Deposition, "")
        self.Printability = QWidget()
        self.Printability.setObjectName(u"Printability")
        self.layoutWidget_6 = QWidget(self.Printability)
        self.layoutWidget_6.setObjectName(u"layoutWidget_6")
        self.layoutWidget_6.setGeometry(QRect(270, 190, 241, 116))
        self.gridLayout_11 = QGridLayout(self.layoutWidget_6)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.gridLayout_11.setContentsMargins(0, 0, 0, 0)
        self.PrintabilityConstantSpeedValueLineEdit = QLineEdit(self.layoutWidget_6)
        self.PrintabilityConstantSpeedValueLineEdit.setObjectName(u"PrintabilityConstantSpeedValueLineEdit")

        self.gridLayout_11.addWidget(self.PrintabilityConstantSpeedValueLineEdit, 0, 1, 1, 1)

        self.PrintabilityFinalSpeedLabel = QLabel(self.layoutWidget_6)
        self.PrintabilityFinalSpeedLabel.setObjectName(u"PrintabilityFinalSpeedLabel")
        self.PrintabilityFinalSpeedLabel.setFont(font)

        self.gridLayout_11.addWidget(self.PrintabilityFinalSpeedLabel, 2, 0, 1, 1)

        self.PrintabilityInitialSpeedValueLineEdit = QLineEdit(self.layoutWidget_6)
        self.PrintabilityInitialSpeedValueLineEdit.setObjectName(u"PrintabilityInitialSpeedValueLineEdit")

        self.gridLayout_11.addWidget(self.PrintabilityInitialSpeedValueLineEdit, 1, 1, 1, 1)

        self.PrintabilityInitialSpeedLabel = QLabel(self.layoutWidget_6)
        self.PrintabilityInitialSpeedLabel.setObjectName(u"PrintabilityInitialSpeedLabel")
        self.PrintabilityInitialSpeedLabel.setFont(font)

        self.gridLayout_11.addWidget(self.PrintabilityInitialSpeedLabel, 1, 0, 1, 1)

        self.PrintabilityFinalSpeedValueLineEdit = QLineEdit(self.layoutWidget_6)
        self.PrintabilityFinalSpeedValueLineEdit.setObjectName(u"PrintabilityFinalSpeedValueLineEdit")

        self.gridLayout_11.addWidget(self.PrintabilityFinalSpeedValueLineEdit, 2, 1, 1, 1)

        self.PrintabilityStepSpeedValueLineEdit = QLineEdit(self.layoutWidget_6)
        self.PrintabilityStepSpeedValueLineEdit.setObjectName(u"PrintabilityStepSpeedValueLineEdit")

        self.gridLayout_11.addWidget(self.PrintabilityStepSpeedValueLineEdit, 3, 1, 1, 1)

        self.PrintabilityStepSpeedLabel = QLabel(self.layoutWidget_6)
        self.PrintabilityStepSpeedLabel.setObjectName(u"PrintabilityStepSpeedLabel")
        self.PrintabilityStepSpeedLabel.setFont(font)

        self.gridLayout_11.addWidget(self.PrintabilityStepSpeedLabel, 3, 0, 1, 1)

        self.PrintabilityConstantSpeedLabel = QLabel(self.layoutWidget_6)
        self.PrintabilityConstantSpeedLabel.setObjectName(u"PrintabilityConstantSpeedLabel")
        self.PrintabilityConstantSpeedLabel.setFont(font)

        self.gridLayout_11.addWidget(self.PrintabilityConstantSpeedLabel, 0, 0, 1, 1)

        self.layoutWidget_7 = QWidget(self.Printability)
        self.layoutWidget_7.setObjectName(u"layoutWidget_7")
        self.layoutWidget_7.setGeometry(QRect(10, 90, 501, 91))
        self.horizontalLayout_4 = QHBoxLayout(self.layoutWidget_7)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.PressureBOX_2 = QGroupBox(self.layoutWidget_7)
        self.PressureBOX_2.setObjectName(u"PressureBOX_2")
        self.verticalLayout_6 = QVBoxLayout(self.PressureBOX_2)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.PrintabilityPressureConstantValueRadio = QRadioButton(self.PressureBOX_2)
        self.PrintabilityPressureConstantValueRadio.setObjectName(u"PrintabilityPressureConstantValueRadio")

        self.verticalLayout_6.addWidget(self.PrintabilityPressureConstantValueRadio)

        self.PrintabilityPressureRangeValueRadio = QRadioButton(self.PressureBOX_2)
        self.PrintabilityPressureRangeValueRadio.setObjectName(u"PrintabilityPressureRangeValueRadio")

        self.verticalLayout_6.addWidget(self.PrintabilityPressureRangeValueRadio)


        self.horizontalLayout_4.addWidget(self.PressureBOX_2)

        self.SpeedBOX_2 = QGroupBox(self.layoutWidget_7)
        self.SpeedBOX_2.setObjectName(u"SpeedBOX_2")
        self.verticalLayout_7 = QVBoxLayout(self.SpeedBOX_2)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.PrintabilitySpeedConstantValueRadio = QRadioButton(self.SpeedBOX_2)
        self.PrintabilitySpeedConstantValueRadio.setObjectName(u"PrintabilitySpeedConstantValueRadio")

        self.verticalLayout_7.addWidget(self.PrintabilitySpeedConstantValueRadio)

        self.PrintabilitySpeedRangeValueRadio = QRadioButton(self.SpeedBOX_2)
        self.PrintabilitySpeedRangeValueRadio.setObjectName(u"PrintabilitySpeedRangeValueRadio")

        self.verticalLayout_7.addWidget(self.PrintabilitySpeedRangeValueRadio)


        self.horizontalLayout_4.addWidget(self.SpeedBOX_2)

        self.layoutWidget_8 = QWidget(self.Printability)
        self.layoutWidget_8.setObjectName(u"layoutWidget_8")
        self.layoutWidget_8.setGeometry(QRect(10, 190, 241, 116))
        self.gridLayout_12 = QGridLayout(self.layoutWidget_8)
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.gridLayout_12.setContentsMargins(0, 0, 0, 0)
        self.PrintabilityConstantPressureLabel = QLabel(self.layoutWidget_8)
        self.PrintabilityConstantPressureLabel.setObjectName(u"PrintabilityConstantPressureLabel")
        self.PrintabilityConstantPressureLabel.setFont(font)

        self.gridLayout_12.addWidget(self.PrintabilityConstantPressureLabel, 0, 0, 1, 1)

        self.PrintabilityConstantPressureValueLineEdit = QLineEdit(self.layoutWidget_8)
        self.PrintabilityConstantPressureValueLineEdit.setObjectName(u"PrintabilityConstantPressureValueLineEdit")

        self.gridLayout_12.addWidget(self.PrintabilityConstantPressureValueLineEdit, 0, 1, 1, 1)

        self.PrintabilityInitialPressureLabel = QLabel(self.layoutWidget_8)
        self.PrintabilityInitialPressureLabel.setObjectName(u"PrintabilityInitialPressureLabel")
        self.PrintabilityInitialPressureLabel.setFont(font)

        self.gridLayout_12.addWidget(self.PrintabilityInitialPressureLabel, 1, 0, 1, 1)

        self.PrintabilityInitialPressureValueLineEdit = QLineEdit(self.layoutWidget_8)
        self.PrintabilityInitialPressureValueLineEdit.setObjectName(u"PrintabilityInitialPressureValueLineEdit")

        self.gridLayout_12.addWidget(self.PrintabilityInitialPressureValueLineEdit, 1, 1, 1, 1)

        self.PrintabilityFinalPressureLabel = QLabel(self.layoutWidget_8)
        self.PrintabilityFinalPressureLabel.setObjectName(u"PrintabilityFinalPressureLabel")
        self.PrintabilityFinalPressureLabel.setFont(font)

        self.gridLayout_12.addWidget(self.PrintabilityFinalPressureLabel, 2, 0, 1, 1)

        self.PrintabilityFinalPressureValueLineEdit = QLineEdit(self.layoutWidget_8)
        self.PrintabilityFinalPressureValueLineEdit.setObjectName(u"PrintabilityFinalPressureValueLineEdit")

        self.gridLayout_12.addWidget(self.PrintabilityFinalPressureValueLineEdit, 2, 1, 1, 1)

        self.PrintabilityStepPressureLabel = QLabel(self.layoutWidget_8)
        self.PrintabilityStepPressureLabel.setObjectName(u"PrintabilityStepPressureLabel")
        self.PrintabilityStepPressureLabel.setFont(font)

        self.gridLayout_12.addWidget(self.PrintabilityStepPressureLabel, 3, 0, 1, 1)

        self.PrintabilityStepPressureValueLineEdit = QLineEdit(self.layoutWidget_8)
        self.PrintabilityStepPressureValueLineEdit.setObjectName(u"PrintabilityStepPressureValueLineEdit")

        self.gridLayout_12.addWidget(self.PrintabilityStepPressureValueLineEdit, 3, 1, 1, 1)

        self.layoutWidget3 = QWidget(self.Printability)
        self.layoutWidget3.setObjectName(u"layoutWidget3")
        self.layoutWidget3.setGeometry(QRect(650, 20, 112, 59))
        self.gridLayout_17 = QGridLayout(self.layoutWidget3)
        self.gridLayout_17.setObjectName(u"gridLayout_17")
        self.gridLayout_17.setContentsMargins(0, 0, 0, 0)
        self.PrintabilityGenerateButtonLabel = QLabel(self.layoutWidget3)
        self.PrintabilityGenerateButtonLabel.setObjectName(u"PrintabilityGenerateButtonLabel")
        self.PrintabilityGenerateButtonLabel.setFont(font)
        self.PrintabilityGenerateButtonLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_17.addWidget(self.PrintabilityGenerateButtonLabel, 0, 0, 1, 1)

        self.PrintabilityButton = QPushButton(self.layoutWidget3)
        self.PrintabilityButton.setObjectName(u"PrintabilityButton")

        self.gridLayout_17.addWidget(self.PrintabilityButton, 1, 0, 1, 1)

        self.layoutWidget_4 = QWidget(self.Printability)
        self.layoutWidget_4.setObjectName(u"layoutWidget_4")
        self.layoutWidget_4.setGeometry(QRect(10, 20, 611, 68))
        self.gridLayout_24 = QGridLayout(self.layoutWidget_4)
        self.gridLayout_24.setObjectName(u"gridLayout_24")
        self.gridLayout_24.setContentsMargins(0, 0, 0, 0)
        self.PrintabilityManufacturerLabel = QLabel(self.layoutWidget_4)
        self.PrintabilityManufacturerLabel.setObjectName(u"PrintabilityManufacturerLabel")
        sizePolicy.setHeightForWidth(self.PrintabilityManufacturerLabel.sizePolicy().hasHeightForWidth())
        self.PrintabilityManufacturerLabel.setSizePolicy(sizePolicy)
        self.PrintabilityManufacturerLabel.setFont(font)

        self.gridLayout_24.addWidget(self.PrintabilityManufacturerLabel, 0, 0, 1, 1)

        self.PrintabilityManufacturercomboBox = QComboBox(self.layoutWidget_4)
        self.PrintabilityManufacturercomboBox.setObjectName(u"PrintabilityManufacturercomboBox")

        self.gridLayout_24.addWidget(self.PrintabilityManufacturercomboBox, 0, 1, 1, 1)

        self.PrintabilityNozzleDiameterLabel = QLabel(self.layoutWidget_4)
        self.PrintabilityNozzleDiameterLabel.setObjectName(u"PrintabilityNozzleDiameterLabel")
        self.PrintabilityNozzleDiameterLabel.setFont(font)

        self.gridLayout_24.addWidget(self.PrintabilityNozzleDiameterLabel, 0, 2, 1, 1)

        self.PrintabilityNozzleDiameterComboBox = QComboBox(self.layoutWidget_4)
        self.PrintabilityNozzleDiameterComboBox.setObjectName(u"PrintabilityNozzleDiameterComboBox")

        self.gridLayout_24.addWidget(self.PrintabilityNozzleDiameterComboBox, 0, 3, 1, 1)

        self.PrintabilityWellLabel = QLabel(self.layoutWidget_4)
        self.PrintabilityWellLabel.setObjectName(u"PrintabilityWellLabel")
        self.PrintabilityWellLabel.setFont(font)

        self.gridLayout_24.addWidget(self.PrintabilityWellLabel, 1, 0, 1, 1)

        self.PrintabilityWellcomboBox = QComboBox(self.layoutWidget_4)
        self.PrintabilityWellcomboBox.setObjectName(u"PrintabilityWellcomboBox")

        self.gridLayout_24.addWidget(self.PrintabilityWellcomboBox, 1, 1, 1, 1)

        self.PrintabilitySizeLabel = QLabel(self.layoutWidget_4)
        self.PrintabilitySizeLabel.setObjectName(u"PrintabilitySizeLabel")
        self.PrintabilitySizeLabel.setFont(font)

        self.gridLayout_24.addWidget(self.PrintabilitySizeLabel, 1, 2, 1, 1)

        self.PrintabilitySizeComboBox = QComboBox(self.layoutWidget_4)
        self.PrintabilitySizeComboBox.setObjectName(u"PrintabilitySizeComboBox")

        self.gridLayout_24.addWidget(self.PrintabilitySizeComboBox, 1, 3, 1, 1)

        self.labelLogo_2 = QLabel(self.Printability)
        self.labelLogo_2.setObjectName(u"labelLogo_2")
        self.labelLogo_2.setGeometry(QRect(540, 110, 231, 211))
        self.labelLogo_2.setPixmap(QPixmap(printability_image))
        self.labelLogo_2.setScaledContents(True)
        self.tabWidget.addTab(self.Printability, "")

        self.retranslateUi(Form)

        self.tabWidget.setCurrentIndex(0)



        # Set all the line edit text to be align centered
        self.ExtrudabilityInitialPressureLineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ExtrudabilityFinalPressureLineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ExtrudabilityStepPressureLineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.PrintingTimeLineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.PauseTimeLineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.DepositionConstantSpeedValueLineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.DepositionInitialSpeedValueLineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.DepositionFinalSpeedValueLineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.DepositionStepSpeedValueLineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.DepositionConstantPressureValueLineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.DepositionInitialPressureValueLineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.DepositionFinalPressureValueLineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.DepositionStepPressureValueLineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.PrintabilityConstantSpeedValueLineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.PrintabilityInitialSpeedValueLineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.PrintabilityFinalSpeedValueLineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.PrintabilityStepSpeedValueLineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.PrintabilityConstantPressureValueLineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.PrintabilityInitialPressureValueLineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.PrintabilityFinalPressureValueLineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.PrintabilityStepPressureValueLineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Set all the combo box items to be align centered
        
        
        
        





        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.ExtrudabilityButton.setText(QCoreApplication.translate("Form", u"Generate", None))
        self.ExtrudabilityLabel.setText(QCoreApplication.translate("Form", u"Generate GCode:", None))
        self.ExtrudabilityInitialPressureLabel.setText(QCoreApplication.translate("Form", u"Initial Pressure Value [KPa]:", None))
        self.ExtrudabilityFinalPressureLabel.setText(QCoreApplication.translate("Form", u"Final Pressure Value [KPa]:", None))
        self.ExtrudabilityStepPressureLabel.setText(QCoreApplication.translate("Form", u"Step Pressure Value [KPa]:", None))
        self.PrintingTimeLabel.setText(QCoreApplication.translate("Form", u"Printing Time [Seconds]:", None))
        self.PrintingTimeLineEdit.setText(QCoreApplication.translate("Form", u"3", None))
        self.PauseTimeLabel.setText(QCoreApplication.translate("Form", u"Pause Time [Milliseconds]:", None))
        self.PauseTimeLineEdit.setText(QCoreApplication.translate("Form", u"100", None))
        self.labelLogo.setText("")
        self.ExtrudabilityImage.setText("")
        self.ManufacturerLabel.setText(QCoreApplication.translate("Form", u"Select Manufacturer:", None))
        self.WellLabel.setText(QCoreApplication.translate("Form", u"Select Well number:", None))
        self.labelContact.setText(QCoreApplication.translate("Form", u"Contact Information: ", None))
        self.labelMail1.setText(QCoreApplication.translate("Form", u"pablo.martin@unizar.es", None))
        self.labelMail1_2.setText(QCoreApplication.translate("Form", u"garciage@unizar.es", None))
        self.labelMail2.setText(QCoreApplication.translate("Form", u"angeles@unizar.es", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Extrudability), QCoreApplication.translate("Form", u"Extrudability", None))
        self.DepositionConstantSpeedLabel.setText(QCoreApplication.translate("Form", u"Speed Value", None))
        self.DepositionInitialSpeedLabel.setText(QCoreApplication.translate("Form", u"Initial Speed Value", None))
        self.DepositionFinalSpeedLabel.setText(QCoreApplication.translate("Form", u"Final Speed Value", None))
        self.DepositionStepSpeedLabel.setText(QCoreApplication.translate("Form", u"Step Speed Value", None))
        self.DepositionPressureBOX.setTitle(QCoreApplication.translate("Form", u"Printing Pressure [KPa]", None))
        self.DepositionPressureConstantValueRadio.setText(QCoreApplication.translate("Form", u"Constant Value", None))
        self.DepositionPressureRangeValueRadio.setText(QCoreApplication.translate("Form", u"Range Value", None))
        self.DepositionSpeedBOX.setTitle(QCoreApplication.translate("Form", u"Printing Speed [mm/s]", None))
        self.DepositionSpeedConstantValueRadio.setText(QCoreApplication.translate("Form", u"Constant Value", None))
        self.DepositionSpeedRangeValueRadio.setText(QCoreApplication.translate("Form", u"Range Value", None))
        self.DepositionConstantPressureLabel.setText(QCoreApplication.translate("Form", u"Pressure Value", None))
        self.DepositionInitialPressureLabel.setText(QCoreApplication.translate("Form", u"Initial Pressure Value", None))
        self.DepositionFinalPressureLabel.setText(QCoreApplication.translate("Form", u"Final Pressure Value", None))
        self.DepositionStepPressureLabel.setText(QCoreApplication.translate("Form", u"Step Pressure Value", None))
        self.DepositionGenerateButtonLabel.setText(QCoreApplication.translate("Form", u"Generate GCode:", None))
        self.DepositionButton.setText(QCoreApplication.translate("Form", u"Generate", None))
        self.DepositionManufacturerLabel.setText(QCoreApplication.translate("Form", u"Select Manufacturer:", None))
        self.DepositionNozzleDiameterLabel.setText(QCoreApplication.translate("Form", u"Select Nozzle Diameter [mm]:", None))
        self.DepositionWellLabel.setText(QCoreApplication.translate("Form", u"Select Well number:", None))
        self.DepositionSizeLabel.setText(QCoreApplication.translate("Form", u"Select Deposition Sample Size [mm]:", None))
        self.labelLogo_3.setText("")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Deposition), QCoreApplication.translate("Form", u"Deposition", None))
        self.PrintabilityFinalSpeedLabel.setText(QCoreApplication.translate("Form", u"Final Speed Value", None))
        self.PrintabilityInitialSpeedLabel.setText(QCoreApplication.translate("Form", u"Initial Speed Value", None))
        self.PrintabilityStepSpeedLabel.setText(QCoreApplication.translate("Form", u"Step Speed Value", None))
        self.PrintabilityConstantSpeedLabel.setText(QCoreApplication.translate("Form", u"Speed Value", None))
        self.PressureBOX_2.setTitle(QCoreApplication.translate("Form", u"Printing Pressure [KPa]", None))
        self.PrintabilityPressureConstantValueRadio.setText(QCoreApplication.translate("Form", u"Constant Value", None))
        self.PrintabilityPressureRangeValueRadio.setText(QCoreApplication.translate("Form", u"Range Value", None))
        self.SpeedBOX_2.setTitle(QCoreApplication.translate("Form", u"Printing Speed [mm/s]", None))
        self.PrintabilitySpeedConstantValueRadio.setText(QCoreApplication.translate("Form", u"Constant Value", None))
        self.PrintabilitySpeedRangeValueRadio.setText(QCoreApplication.translate("Form", u"Range Value", None))
        self.PrintabilityConstantPressureLabel.setText(QCoreApplication.translate("Form", u"Pressure Value", None))
        self.PrintabilityInitialPressureLabel.setText(QCoreApplication.translate("Form", u"Initial Pressure Value", None))
        self.PrintabilityFinalPressureLabel.setText(QCoreApplication.translate("Form", u"Final Pressure Value", None))
        self.PrintabilityStepPressureLabel.setText(QCoreApplication.translate("Form", u"Step Pressure Value", None))
        self.PrintabilityGenerateButtonLabel.setText(QCoreApplication.translate("Form", u"Generate GCode:", None))
        self.PrintabilityButton.setText(QCoreApplication.translate("Form", u"Generate", None))
        self.PrintabilityManufacturerLabel.setText(QCoreApplication.translate("Form", u"Select Manufacturer:", None))
        self.PrintabilityNozzleDiameterLabel.setText(QCoreApplication.translate("Form", u"Select Nozzle Diameter [mm]:", None))
        self.PrintabilityWellLabel.setText(QCoreApplication.translate("Form", u"Select Well number:", None))
        self.PrintabilitySizeLabel.setText(QCoreApplication.translate("Form", u"Select Printability Sample Size [mm]:", None))
        self.labelLogo_2.setText("")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Printability), QCoreApplication.translate("Form", u"Printability", None))
    # retranslateUi

