# -*- coding: utf-8 -*-
import sys
import time
import pandas as pd
import clr
import System
import re
import numpy as np
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QFileInfo
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox, QFileDialog, QMainWindow, QDialog, QCheckBox, QListWidgetItem, QLineEdit
from System import Enum
from System import Array
from PDL_Sample_Gui import Ui_PDL_Sample
from PDL_Sample_sweeping_Gui import Ui_PDL_Sweeping_Sample

# Load instrumentDll.dll
assembly_path = r".\InstrumentDLL"
sys.path.append(assembly_path)
ref = clr.AddReference(r"InstrumentDLL")

# Load STSProcessDLL.dll
assembly_path = r".\STSProcessDLL"
sys.path.append(assembly_path)
ref = clr.AddReference(r"STSProcess")

# Load FTD2XX_NET.dll 
assembly_path = r".\FTD2XX_NET"
sys.path.append(assembly_path)
ref = clr.AddReference(r"FTD2XX_NET")

# import DLL namespace
from Santec import *
from Santec.Communication import *
from Santec.Instruments import *
from Santec.STSProcess import *
from Santec.Rescaling_Process import *

# instance of DLL's class
tsl_ = TSL()             # Create TSL instance
pcu_ = PCU()             # Create PCU instance
spu_ = SPU()             # Create SPU instance
Cal_STS = PDLSTS()       # Create Calculation instance
mpms = []                # Create MPM List instance
connectTypes = []
checkedChannels = []

Flag_215 = False
Flag_213 = False
Flag_570 = False
inst_flag = False
mpmLoggData = None

errorInfo = {-2147483648:"Unknown", -40:"InUseError", -30:"ParameterError", 
             -20:"DeviceError", -14:"CommunicationFailure", 
             -13:"UnauthorizedAccess", -12:"IOException",
             -11:"NotConnected", -10:"Uninitialized",
             -2:"TimeOut", -1:"Failure", -5:"Count_mismatch",
             -6:"MonitorError", 0:"Succeed", 11:"AlreadyConnected",
             10:"Stopped"}

stsProcessErrorInfo = {-2147483648:"Unknown", -1115:"MeasureNotMatch", -1114:"MeasureNotRescaling", 
                       -1113:"MeasureNotExist", -1112:"ReferenceNotMatch", -1111:"ReferenceNotRescaling", 
                       -1110:"ReferenceNotExist", -1000:"NoCalculated", -30:"ParameterError", 
                       -1:"Failure", 0:"Succeed"}

# data struct for STS
measure_data = []  # list of measurement data
reference_data = []  # list of reference data
measure_monitor_data = []  # list of  measurement monitor data
reference_monitor_data = []  # list of reference monitor data
merge_data = []  # list of merge data
Meas_rang = []   # list of range
Data_struct = [] # structure for saving channel, range, sop
Refdata_struct = [] # reference structure
Ref_monitordata_struct=[]  # reference monitor data structure
Meas_monitordata_struct = []  # measure monitor data structure
Mergedata_struct = []  # structure for saving merged data
cal_IL_list = []
cal_IL_item_list = []

# show instrument error
def show_instrument_error(errordata):
    msg = errorInfo.get(errordata)
    QMessageBox.warning(None, 'Waring', msg, QMessageBox.Ok)
    return

# show error
def show_error_message(errordata):
    QMessageBox.warning(None, 'Waring', errordata, QMessageBox.Ok)
    return

# show pdl sts error
def show_sts_error(errordata):
    msg = stsProcessErrorInfo.get(errordata)
    QMessageBox.warning(None, 'Waring', msg, QMessageBox.Ok)
    return

# gets the USB resource connected to the PC
def get_usb_resource():
    PDL_form.cmb_tsl_usb.clear()
    usb_com = MainCommunication.Get_USB_Resouce()
    return usb_com

# gets the TSL USB resource connected to the PC
def get_tsl_usb_resource():
    usb_res = get_usb_resource()
    PDL_form.cmb_tsl_usb.addItems(usb_res)

# gets the PCU USB resource connected to the PC
def get_pcu_usb_resource():
    usb_res = get_usb_resource()
    PDL_form.cmb_pcu_usb.addItems(usb_res)

# gets the DAQ ID
def get_daq_id():
    PDL_form.cmb_dev_number.clear()
    # Get SPU connect ID 
    error_code, dev_ID = spu_.Get_Device_ID([])
    if error_code != 0:
        show_instrument_error(error_code)
        return
    
    # Set the spu id in windows combobox
    PDL_form.cmb_dev_number.addItems(dev_ID)

class PDL_Window(QMainWindow, Ui_PDL_Sample):
    def __init__(self, parent=None):
        super(PDL_Window, self).__init__(parent)
        self.setupUi(self)
        self.init_ui()

    def init_ui(self):
        self.rdo_tsl570.setChecked(True)
        self.rdo_tsl_gpib.setChecked(True)
        self.txt_tsl_ip.setDisabled(True)
        self.txt_tsl_port.setDisabled(True)
        self.cmb_tsl_usb.setDisabled(True)
        self.rdo_mpm_gpib.setChecked(True)
        self.txt_mpm_ip.setDisabled(True)
        self.txt_mpm_port.setDisabled(True)
        self.txt_mpm_gpib_board.setText("0")
        self.txt_tsl_gpib_board.setText("0")
        self.txt_tsl_port.setText("5000")
        self.txt_mpm_port.setText("5000")
        self.rdo_pcu100.setChecked(True)
        self.rdo_pcu_gpib.setChecked(True)
        self.txt_pcu_ip.setDisabled(True)
        self.txt_pcu_port.setDisabled(True)
        self.cmb_pcu_usb.setDisabled(True)
        self.txt_pcu_gpib_board.setText("0")
        self.txt_pcu_port.setText("5000")
        self.rdo_pcu_tcpip.setDisabled(True)
        self.rdo_pcu_usb.setDisabled(True)
        self.btn_add_device.clicked.connect(on_add_device)
        self.btn_delete_device.clicked.connect(on_del_device)
        self.btn_connect.clicked.connect(on_connect)
        self.btn_disconnect.clicked.connect(on_disconnect)
        
class PDL_Sweeping_Window(QDialog, Ui_PDL_Sweeping_Sample):
    def __init__(self):
        super(PDL_Sweeping_Window, self).__init__()
        self.setupUi(self)
        self.init_ui()

    def init_ui(self):
        self.btn_Set.clicked.connect(set_parameterformeasure)
        self.btn_reference.clicked.connect(reference)
        self.btn_measurement.clicked.connect(measure)
        self.btn_saverefrawdata.clicked.connect(save_reference_raw_data)
        self.btn_saverawdata.clicked.connect(save_raw_data)
        self.btn_readrefrawdata.clicked.connect(read_reference_raw_data)
        self.btn_saveCalculateIL.clicked.connect(save_calculate_IL)
        
def save_calculate_IL():

    global cal_IL_list
    global cal_IL_item_list
    
    # Get target wavelength list
    errorcode, wavelengthdata = Cal_STS.Get_Target_Wavelength_Table(None)

    if errorcode != 0:
        show_sts_error(errorcode)
        return
    
    for i in range(len(cal_IL_item_list)):
    #errorcode, cal_IL = Cal_STS.Get_Calibrated_IL(None)
    
        item = cal_IL_item_list[i]
        cal_IL = cal_IL_list[i]
    
        # Save the calculate IL data in csv file
        fpath = get_file_path_function("Save_to_Calculated_IL_" + "MPM" + str(item.MPMNumber + 1) + "Slot" + str(item.SlotNumber) + "Channel" + str(item.ChannelNumber) + ".csv")
        
        header = ["Wavelength(nm)", "IL_V(dB)", "IL_H(dB)", "IL_45(dB)", "IL_RCP(dB)"]
    
        result = []
        for loop1 in range(len(wavelengthdata)):
            data = []
            data.append(str(wavelengthdata[loop1]))
    
            for loop2 in range(4):
                data.append(str(cal_IL[loop2,loop1]))
            
            result.append(data)
        
        cal_result = pd.DataFrame(result, columns=header)
        cal_result.to_csv(fpath, index=False)

    QMessageBox.information(None, 'Information', 'Completed.', QMessageBox.Ok)
        
def save_reference_raw_data():

    global Refdata_struct
    global Ref_monitordata_struct
    
    lstpowdata = []
    lstmonitordata = []

    # Get target wavelength list
    process_error, wavetable = Cal_STS.Get_Target_Wavelength_Table(None)

    if process_error != 0:
        show_sts_error(process_error)
        return

    # Loop 4 ranges
    for loop1 in range(4):
        header = []
        lstpowdata = []
        lstmonitordata = []

        if loop1 == 0:
            sop_string = "Vartical_Polarization"
        elif loop1 == 1:
                sop_string = "Horizontal_Polarization"
        elif loop1 == 2:
                sop_string = "45°Linear_Polarization"
        elif loop1 == 3:
                sop_string = "Right-handed_circle_Polarization"

        fpath = get_file_path_function("Reference_Rawdata_" + sop_string)

        header.append("Wavelength(nm)")

        for item in Refdata_struct:
            if item.SOP != loop1:
                continue

            # Get reference power data
            process_error, powdata = Cal_STS.Get_Ref_Power_Rawdata(item, None)
            if process_error != 0:
                show_sts_error(process_error)
                return

            lstpowdata.append(powdata)

            header.append("MPM" + str(item.MPMNumber + 1) + "Slot" + str(item.SlotNumber) + "Ch" + str(item.ChannelNumber))

        # Monitor data is different in each channel mode,
        # add every monitor data titile in each channel
        if PDL_form.PDL_Sweeping_form.chkeach_ch.isChecked():
            for item in Refdata_struct:
                if item.SOP != loop1:
                    continue
                header.append("Monitor_MPM" + str(item.MPMNumber + 1) + "Slot" + str(item.SlotNumber) + "Ch" + str(item.ChannelNumber))
        else:
            # Add only one monitor data titile for all channels
            header.append("Monitor")

        befor_struct = STSDataStruct()

        for item in Ref_monitordata_struct:

            # Add every monitor data for each channel
            if PDL_form.PDL_Sweeping_form.chkeach_ch.isChecked():
                if item.MPMNumber == befor_struct.MPMNumber and item.SlotNumber == befor_struct.SlotNumber and item.ChannelNumber == befor_struct.ChannelNumber or item.SOP != loop1:
                    continue
            # Add only one monitor data titile for all channels
            else:
                if item.SOP != loop1:
                    continue

            # Get reference monitor data
            process_error, monitordata = Cal_STS.Get_Ref_Monitor_Rawdata(item, None)

            if process_error != 0:
                show_sts_error(process_error)
                return

            get_struct = STSDataStruct()   
            get_struct.MPMNumber = item.MPMNumber
            get_struct.SlotNumber = item.SlotNumber
            get_struct.ChannelNumber = item.ChannelNumber
            get_struct.SOP = item.SOP

            lstmonitordata.append(monitordata)
            befor_struct = get_struct

        result = []
        # Add power data and monitor data in result, and output result to csv file.
        for loop2 in range(len(wavetable)):

            data = []
            data.append(wavetable[loop2])

            for power in lstpowdata:
                data.append(power[loop2])
                
            for monitor in lstmonitordata:
                data.append(monitor[loop2])
                
            result.append(data)
        
        cal_result = pd.DataFrame(result, columns=header)
        cal_result.to_csv(fpath, index=False)

    QMessageBox.information(None, 'Information', 'Completed.', QMessageBox.Ok)

def save_raw_data():
    # Get reference power data
    errorcode, wavelength_table = Cal_STS.Get_Target_Wavelength_Table(None)

    if errorcode != 0:
        show_sts_error(errorcode)
        return

    first_rangeflag = False
    exist_flag = False

    # Get range value from input textbox in window
    rangenumber = int(PDL_form.PDL_Sweeping_form.txtsaverange.text())

    global Data_struct
    
    for item in Data_struct:
        if item.RangeNumber > rangenumber:
            first_rangeflag = True

        if item.RangeNumber == rangenumber:
            exist_flag = True

    if exist_flag == False:
        QMessageBox.information(None, 'Warning', 'Range data is not exist.', QMessageBox.Ok)
        return

    sopcount = 0
    
    # if 2SOP checked, 4 ranges used in the first sweep, 2 ranges used in other sweep
    # if 2SOP unchecked, 4 ranges used in every sweep
    if first_rangeflag == False and PDL_form.PDL_Sweeping_form.chk2sop.isChecked():
        sopcount = 1
    else:
        sopcount = 3

    for loop1 in range(sopcount + 1):
        header = []
        lstpower = []

        if loop1 == 0:
            sop_string = "Vartical"
        elif loop1 == 1:
            sop_string = "Horizontal"
        elif loop1 == 2:
            sop_string = "45°Linear"
        elif loop1 == 3:
            sop_string = "Right-handed circle"

        sweepcount = check_sweepcount(rangenumber, loop1)

        header.append("Wavelength(nm)")

        for item in Data_struct:

            if item.SOP != loop1 or item.RangeNumber != rangenumber:
                continue

            # Get Measure Power raw data.
            errorcode, powerdata = Cal_STS.Get_Meas_Power_Rawdata(item, None)

            if errorcode != 0:
                show_sts_error(errorcode)
                return

            lstpower.append(powerdata)

            header.append("MPM" + str(item.MPMNumber + 1) + "Slot" + str(item.SlotNumber) + "Ch" + str(item.ChannelNumber))

        header.append("Monitordata")

        for item in Meas_monitordata_struct:
            if item.SOP != loop1 or item.SweepCount != sweepcount:
                continue

            # Get Measure monitor raw data.
            errorcode, monitordata = Cal_STS.Get_Meas_Monitor_Rawdata(item, None)

            if errorcode != 0:
                show_sts_error(errorcode)
                return

        result = []
        # Using wavlength, power and monitor to create output result
        for loop2 in range(len(wavelength_table)):
            data = []
            data.append(str(wavelength_table[loop2]))

            for loop3 in range(len(lstpower)):
                data.append(lstpower[loop3][loop2])

            data.append(monitordata[loop2])

            result.append(data)
        
        # Save raw data to csv file.
        fpath = get_file_path_function("Save_Range" + str(rangenumber) + "_" + sop_string + "_SOP_data.csv")
        cal_result = pd.DataFrame(result, columns=header)
        cal_result.to_csv(fpath, index=False)

    QMessageBox.information(None, 'information', 'Completed.', QMessageBox.Ok)
    
def read_reference_raw_data():

    for sop_loop in range(4):
        
        if sop_loop == 0:
            sop_string = "Vartical_Polarization"
        elif sop_loop == 1:
                sop_string = "Horizontal_Polarization"
        elif sop_loop == 2:
                sop_string = "45°Linear_Polarization"
        elif sop_loop == 3:
                sop_string = "Right-handed_circle_Polarization"

        # Read reference data 
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        path= QFileDialog.getOpenFileName(None, "Read Reference data", "Reference_Rawdata_" + sop_string + ".csv", "*.csv", options=options)
        read_data = pd.read_csv(path[0])

        # Calculate count of channels
        if PDL_form.PDL_Sweeping_form.chkeach_ch.isChecked():
            ch_count = (len(read_data.columns) - 1) / 2
        else:
            ch_count = len(read_data.columns) - 2
    
        # When channels count got from csv file not equals the selected channels count  
        if ch_count != len(checkedChannels):
    
            QMessageBox.information(None, 'warning', 'Reference data mismatch.Please selecet the correct data.', QMessageBox.Ok)
            return

        match_flag = False
        if PDL_form.PDL_Sweeping_form.chkeach_ch.isChecked():

            for loop1 in range(1, int(ch_count) + 1):
                
                match_flag = False
    
                tempHeader = read_data.columns[loop1]
    
                # Get MPM index
                chk_str = tempHeader[3:4]
                mpm_number = int(chk_str) - 1
                
                # Get Module index
                chk_str = tempHeader[8:9]
                slot_number = int(chk_str)
        
                # Get Channel index
                chk_str = tempHeader[11:12]
                ch_number = int(chk_str)
        
                for item in Refdata_struct:
                    
                    if item.MPMNumber == mpm_number and item.SlotNumber == slot_number and item.ChannelNumber == ch_number and item.SOP == sop_loop:
                        match_flag = True
                        break
        
                if match_flag == False:
                    QMessageBox.information(None, 'warning', 'Reference data mismatch.Please selecet right data.', QMessageBox.Ok)
                    return
                
                # Read out wavelength data to list
                lstWave = read_data[read_data.columns[0]].to_list()
                if lstWave[len(lstWave) - 1] != float(PDL_form.PDL_Sweeping_form.txt_stopwave.text()):
                    QMessageBox.information(None, 'warning', 'Reference data mismatch.Please selecet right data.', QMessageBox.Ok)
                    return
                
                # Read out power data to list
                lstPower = read_data[tempHeader].to_list()
                
                # Read out monitor data to list
                tempMonitorHeader = read_data.columns[loop1 + int(ch_count)]
                lstMonitor = read_data[tempMonitorHeader].to_list()
                
                # Calcaulate data point
                datapoint = (float(PDL_form.PDL_Sweeping_form.txt_stopwave.text()) - float(PDL_form.PDL_Sweeping_form.txt_startwave.text())) / float(PDL_form.PDL_Sweeping_form.txt_wavestep.text()) + 1
    
                # If data count is not match, show message
                if datapoint != len(lstMonitor):
                    QMessageBox.information(None, 'warning', 'Reference data mismatch.Please selecet right data.', QMessageBox.Ok)
                    return
                
                refdata_strunct = STSDataStruct()
                refdata_strunct.MPMNumber = mpm_number
                refdata_strunct.SlotNumber = slot_number
                refdata_strunct.ChannelNumber = ch_number
                refdata_strunct.RangeNumber = 1
                refdata_strunct.SweepCount = sop_loop + 1
                refdata_strunct.SOP = sop_loop
                
                # Transfer power, monitor data in stsprocessDll 
                errorcode = Cal_STS.Add_Ref_Rawdata(lstPower, lstMonitor, item)
    
                if errorcode != 0:
                    show_instrument_error(errorcode)
                    return
                
        else:

            for loop1 in range(1, int(ch_count) + 1):
    
                tempHeader = read_data.columns[loop1]
    
                # Get MPM index
                chk_str = tempHeader[3:4]
                mpm_number = int(chk_str) - 1
                
                # Get Module index
                chk_str = tempHeader[8:9]
                slot_number = int(chk_str)
        
                # Get Channel index
                chk_str = tempHeader[11:12]
                ch_number = int(chk_str)
        
                for item in Refdata_struct:
        
                    if item.MPMNumber == mpm_number and item.SlotNumber == slot_number and item.ChannelNumber == ch_number and item.SOP == sop_loop:
                        match_flag = True
                        break
        
                if match_flag == False:
                    QMessageBox.information(None, 'warning', 'Reference data mismatch.Please selecet right data.', QMessageBox.Ok)
                    return
                
                # Read out wavelength data to list
                lstWave = read_data[read_data.columns[0]].to_list()
                if lstWave[len(lstWave) - 1] != float(PDL_form.PDL_Sweeping_form.txt_stopwave.text()):
                    QMessageBox.information(None, 'warning', 'Reference data mismatch.Please selecet right data.', QMessageBox.Ok)
                    return
        
                # Read out power data to list
                lstPower = read_data[tempHeader].to_list()
                
                # Read out monitor data to list
                tempMonitorHeader = read_data.columns[int(ch_count) + 1]
                lstMonitor = read_data[tempMonitorHeader].to_list()
                
                # Calcaulate data point
                datapoint = (float(PDL_form.PDL_Sweeping_form.txt_stopwave.text()) - float(PDL_form.PDL_Sweeping_form.txt_startwave.text())) / float(PDL_form.PDL_Sweeping_form.txt_wavestep.text()) + 1
        
                if datapoint != len(lstMonitor):
                    QMessageBox.information(None, 'warning', 'Reference data mismatch.Please selecet right data.', QMessageBox.Ok)
                    return
                
                refdata_strunct = STSDataStruct()
                refdata_strunct.MPMNumber = mpm_number
                refdata_strunct.SlotNumber = slot_number
                refdata_strunct.ChannelNumber = ch_number
                refdata_strunct.RangeNumber = 1
                refdata_strunct.SweepCount = sop_loop + 1
                refdata_strunct.SOP = sop_loop
                
                # Transfer power, monitor data in stsprocessDll 
                errorcode = Cal_STS.Add_Ref_Rawdata(lstPower, lstMonitor, item)
        
                if errorcode != 0:
                    show_instrument_error(errorcode)
                    return
        
    QMessageBox.information(None, 'information', 'Completed.', QMessageBox.Ok)

# initial TSL
def initial_tsl():
    tsl_information = {"Product: ": tsl_.Information.ProductName, "SN: ": tsl_.Information.SerialNumber,
                       "FW Ver: ": tsl_.Information.FWversion, "Wavelength range: ":
                           str(tsl_.Information.MinimunWavelength) + ' ~ ' + str(tsl_.Information.MaximumWavelength),
                       "Power range: ": str(tsl_.Information.MinimumAPCPower_dBm) + ' ~ ' + str(tsl_.Information.
                                                                                                MaximumAPCPower_dBm)}
    if tsl_.Information.ProductName == "TSL-570":
        # Get the firmed speed list from TSL-570
        error_code, sweep_table = tsl_.Get_Sweep_Speed_table([])
        if error_code != 0:
            show_instrument_error(error_code)
            return
    return tsl_information

# disconnect instrument
def on_disconnect():
    # Disconnect TSL
    tsl_.DisConnect()
    # Disconnect PCU
    pcu_.DisConnect()
    
    # Disconnect All MPMs
    for mpm in mpms:
        mpm.DisConnect()
        
    # Disconnect SPU
    spu_.DisConnect()
    PDL_form.btn_connect.setDisabled(False)
    PDL_form.btn_add_device.setDisabled(False)
    PDL_form.btn_delete_device.setDisabled(False)
    
    if PDL_form.PDL_Sweeping_form != None:
        # Close sweeping window
        PDL_form.PDL_Sweeping_form.close()
    
# add mpm into listview
def on_add_device():
    # MPM GPIB communication
    if PDL_form.rdo_mpm_gpib.isChecked():
        # Add GPIB communicator in listview
        PDL_form.list_widget_1.addItem(str(PDL_form.txt_mpm_gpib_board.text()) + "::" + str(PDL_form.txt_mpm_gpib_address.text()))
    else:
        # Add LAN communicator in listview
        PDL_form.list_widget_1.addItem(str(PDL_form.txt_mpm_ip.text()) + ":" + str(PDL_form.txt_mpm_port.text()))
        
# delete mpm from listview
def on_del_device():
    PDL_form.list_widget_1.takeItem(PDL_form.list_widget_1.row(PDL_form.list_widget_1.currentItem()))
    
# connect instrument and initial
def on_connect():
    
    global Flag_570
    
    # TSL GPIB communication
    if PDL_form.rdo_tsl_gpib.isChecked():
        tsl_connect_type = CommunicationMethod.GPIB
        tsl_.GPIBConnectType = GPIBConnectType.NI4882
        tsl_.GPIBBoard = PDL_form.txt_tsl_gpib_board.text()
        tsl_.GPIBAddress = str(PDL_form.txt_tsl_gpib_address.text())
        tsl_.Terminator = CommunicationTerminator.CrLf
        # TSL LAN communication
    if PDL_form.rdo_tsl_tcpip.isChecked():
        tsl_connect_type = CommunicationMethod.TCPIP
        tsl_.IPAddress = str(PDL_form.txt_tsl_ip.text())
        tsl_.Port = str(PDL_form.txt_tsl_port.text())
        tsl_.Terminator = CommunicationTerminator.Cr
        # TSL USB communication
    if PDL_form.rdo_tsl_usb.isChecked():
        tsl_connect_type = CommunicationMethod.USB
        tsl_.Terminator = CommunicationTerminator.Cr
        tsl_.DeviceID = PDL_form.cmb_tsl_usb.currentIndex()

    # Connect TSL
    error_code = tsl_.Connect(tsl_connect_type)
    if error_code != 0:
        show_instrument_error(error_code)
        return
    
    for i in range(PDL_form.list_widget_1.count()):
        connectString = PDL_form.list_widget_1.item(i).text()
        # GPIB communication
        if connectString.find('::') > -1:
            connectStrs = connectString.split('::', 1)
            mpm = MPM()
            mpm.GPIBConnectType = GPIBConnectType.NI4882
            mpm.GPIBBoard = connectStrs[0]
            mpm.GPIBAddress = connectStrs[1]
            
            # Connect MPM
            error_code = mpm.Connect(CommunicationMethod.GPIB)

            if error_code != 0:
                show_instrument_error(error_code)
                return
            mpms.append(mpm)
            
        # LAN communication
        elif connectString.find(':') > -1:
            connectStrs = connectString.split(':', 1)

            mpm = MPM()
            mpm.IPAddress = str(connectStrs[0])
            mpm.Port = connectStrs[1]
            # Connect MPM
            error_code = mpm.Connect(CommunicationMethod.TCPIP)
            if error_code != 0:
                show_instrument_error(error_code)
                return
            mpms.append(mpm)
    
    # GPIB communication
    if PDL_form.rdo_pcu_gpib.isChecked():

        pcu_connect_type = CommunicationMethod.GPIB
        pcu_.GPIBBoard = int(PDL_form.txt_pcu_gpib_board.text())
        pcu_.GPIBAddress = int(PDL_form.txt_pcu_gpib_address.text())
        pcu_.Terminator = CommunicationTerminator.CrLf
    # LAN communication
    if PDL_form.rdo_pcu_tcpip.isChecked():
        pcu_connect_type = CommunicationMethod.TCPIP
        pcu_.IPAddress = str(PDL_form.txt_pcu_ip.text())
        pcu_.Port = str(PDL_form.txt_pcu_port.text())
    # USB communication
    if PDL_form.rdo_pcu_usb.isChecked():
        pcu_connect_type = CommunicationMethod.USB
        pcu_.Terminator = CommunicationTerminator.Cr
        pcu_.DeviceID = PDL_form.cmb_pcu_usb.currentIndex()
        
    if PDL_form.rdo_pcu100.isChecked():
        pcu_.DeviceName = PDL_form.cmb_dev_number.currentText()

    # Connect PCU
    error_code = pcu_.Connect(pcu_connect_type)

    if error_code != 0:
        show_instrument_error(error_code)
        return

    # DAQ(SPU) communication
    spu_ID = PDL_form.cmb_dev_number.currentText()
    spu_.DeviceName = spu_ID
    error_code, ans_ = spu_.Connect(' ')
    if error_code != 0:
        show_instrument_error(error_code)
        return
    
    if PDL_form.rdo_tsl570.isChecked() == True:
        Flag_570 = True
    else:
        Flag_570 = False

    # TSL initialized
    initial_tsl()
    
    # Check MPM module type
    error_code = Check_Module_Information()
    if error_code != 0:
        show_instrument_error(error_code)
        return
    
    # Add all channels of all MPM in sweeping window
    Referect_EnableCh_for_form()
    # Add all ranges in sweeping window
    Referect_EnableRange_for_form()
    # Add TSL-570 speed list in sweeping window
    error_code = Add_TSL_Sweep_Speed()
    if error_code != 0:
        QMessageBox.warning(None, 'Waring', "TSL Device is not TSL-570.", QMessageBox.Ok)
        on_disconnect()
        return
    
    # 全てのインスツルメント通信出来た場合、メッセージ出す
    QMessageBox.information(None, 'Information', 'All instrument was connected.', QMessageBox.Ok)
    PDL_form.btn_connect.setDisabled(True)
    PDL_form.btn_add_device.setDisabled(True)
    PDL_form.btn_delete_device.setDisabled(True)
    
    PDL_form.PDL_Sweeping_form.setWindowTitle('PDL STS Sample')
    PDL_form.PDL_Sweeping_form.setWindowIcon(QIcon(root + "./SANTEC.ico"))
    PDL_form.PDL_Sweeping_form.show()
    
    PDL_form.PDL_Sweeping_form.txt_wavestep.setText("0.01")
    PDL_form.PDL_Sweeping_form.txt_power.setText("10")
    if Flag_570 == False:
        PDL_form.PDL_Sweeping_form.txt_sweepspeed.setText("50")
    PDL_form.PDL_Sweeping_form.txt_startwave.setText(str(tsl_.Information.MinimunWavelength))
    PDL_form.PDL_Sweeping_form.txt_stopwave.setText(str(tsl_.Information.MaximumWavelength))
 
def Check_Module_Information():
    
    global Flag_215
    global Flag_213

    counter_215 = 0

    for mpm in mpms:
        for module in range(5):
            if mpm.Information.ModuleEnable[module] == True:

                if mpm.Information.ModuleType[module] == "MPM-215":
                    Flag_215 = True
                    counter_215 = counter_215 + 1

                if mpm.Information.ModuleType[module] == "MPM-213":
                    Flag_213 = True


    enable_module_count = 0
    
    for mpm in mpms:
        enable_module_count = mpm.Information.NumberofModule + enable_module_count 

    if Flag_215 == True:
        if enable_module_count != counter_215:
            return -1
    return 0

def Referect_EnableCh_for_form():

    mpm_index = 0
    for mpm in mpms:
        enable_slot = mpm.Information.ModuleEnable;
        mpm_index = mpm_index + 1

        for moduleIndex in range(5):
            if enable_slot[moduleIndex] == True:
                slot_type = mpm.Information.ModuleType[moduleIndex]
                if slot_type != "MPM-212":
                    box = QCheckBox(str(mpm_index) + "-" + str(moduleIndex) + "-1")
                    item = QListWidgetItem()
                    PDL_form.PDL_Sweeping_form.list_widget_channel.addItem(item)
                    PDL_form.PDL_Sweeping_form.list_widget_channel.setItemWidget(item, box)
                    
                    box1 = QCheckBox(str(mpm_index) + "-" + str(moduleIndex) + "-2")
                    item1 = QListWidgetItem()
                    PDL_form.PDL_Sweeping_form.list_widget_channel.addItem(item1)
                    PDL_form.PDL_Sweeping_form.list_widget_channel.setItemWidget(item1, box1)
                    
                    box2 = QCheckBox(str(mpm_index) + "-" + str(moduleIndex) + "-3")
                    item2 = QListWidgetItem()
                    PDL_form.PDL_Sweeping_form.list_widget_channel.addItem(item2)
                    PDL_form.PDL_Sweeping_form.list_widget_channel.setItemWidget(item2, box2)

                    box3 = QCheckBox(str(mpm_index) + "-" + str(moduleIndex) + "-4")
                    item3 = QListWidgetItem()
                    PDL_form.PDL_Sweeping_form.list_widget_channel.addItem(item3)
                    PDL_form.PDL_Sweeping_form.list_widget_channel.setItemWidget(item3, box3)
                else:
                    box = QCheckBox(str(mpm_index) + "-" + str(moduleIndex) + "-1")
                    item = QListWidgetItem()
                    PDL_form.PDL_Sweeping_form.list_widget_channel.addItem(item)
                    PDL_form.PDL_Sweeping_form.list_widget_channel.setItemWidget(item, box)
                    
                    box1 = QCheckBox(str(mpm_index) + "-" + str(moduleIndex) + "-2")
                    item1 = QListWidgetItem()
                    PDL_form.PDL_Sweeping_form.list_widget_channel.addItem(item1)
                    PDL_form.PDL_Sweeping_form.list_widget_channel.setItemWidget(item1, box1)
                    
def Referect_EnableRange_for_form():
    
    global Flag_213
    # Range 1-4 are enabled for MPM-213 
    if Flag_213 == True:
        
        box = QCheckBox("Range1")
        item = QListWidgetItem()
        PDL_form.PDL_Sweeping_form.list_widget_range.addItem(item)
        PDL_form.PDL_Sweeping_form.list_widget_range.setItemWidget(item, box)

        box1 = QCheckBox("Range2")
        item1 = QListWidgetItem()
        PDL_form.PDL_Sweeping_form.list_widget_range.addItem(item1)
        PDL_form.PDL_Sweeping_form.list_widget_range.setItemWidget(item1, box1)
        
        box2 = QCheckBox("Range3")
        item2 = QListWidgetItem()
        PDL_form.PDL_Sweeping_form.list_widget_range.addItem(item2)
        PDL_form.PDL_Sweeping_form.list_widget_range.setItemWidget(item2, box2)
        
        box3 = QCheckBox("Range4")
        item3 = QListWidgetItem()
        PDL_form.PDL_Sweeping_form.list_widget_range.addItem(item3)
        PDL_form.PDL_Sweeping_form.list_widget_range.setItemWidget(item3, box3)

    # Range 1-5 are enabled for other module 
    else:

        box = QCheckBox("Range1")
        item = QListWidgetItem()
        PDL_form.PDL_Sweeping_form.list_widget_range.addItem(item)
        PDL_form.PDL_Sweeping_form.list_widget_range.setItemWidget(item, box)

        box1 = QCheckBox("Range2")
        item1 = QListWidgetItem()
        PDL_form.PDL_Sweeping_form.list_widget_range.addItem(item1)
        PDL_form.PDL_Sweeping_form.list_widget_range.setItemWidget(item1, box1)
        
        box2 = QCheckBox("Range3")
        item2 = QListWidgetItem()
        PDL_form.PDL_Sweeping_form.list_widget_range.addItem(item2)
        PDL_form.PDL_Sweeping_form.list_widget_range.setItemWidget(item2, box2)
        
        box3 = QCheckBox("Range4")
        item3 = QListWidgetItem()
        PDL_form.PDL_Sweeping_form.list_widget_range.addItem(item3)
        PDL_form.PDL_Sweeping_form.list_widget_range.setItemWidget(item3, box3)
        
        box4 = QCheckBox("Range5")
        item4 = QListWidgetItem()
        PDL_form.PDL_Sweeping_form.list_widget_range.addItem(item4)
        PDL_form.PDL_Sweeping_form.list_widget_range.setItemWidget(item4, box4)

    # No range enabled for MPM-215 
    if Flag_215 == True:
        PDL_form.PDL_Sweeping_form.list_widget_range.setDisabled(True)

def Add_TSL_Sweep_Speed():
    
    global Flag_570

    if Flag_570 == True:
        sweep_table = []
        inst_error, sweep_table = tsl_.Get_Sweep_Speed_table(None)
    
        if inst_error != 0 & inst_error != ExceptionCode.DeviceError:
            return inst_error

    #if inst_error != ExceptionCode.DeviceError:
    #    for speed in sweep_table:
    #        this.cmbspeed.Items.Add(speed)
    
    if Flag_570 == True:
        PDL_form.PDL_Sweeping_form.txt_sweepspeed = QtWidgets.QComboBox(PDL_form.PDL_Sweeping_form.grb_sweep_setting)
        PDL_form.PDL_Sweeping_form.txt_sweepspeed.setGeometry(QtCore.QRect(400, 40, 113, 26))
        PDL_form.PDL_Sweeping_form.txt_sweepspeed.setTabletTracking(True)
        PDL_form.PDL_Sweeping_form.txt_sweepspeed.setObjectName("txt_sweepspeed")
        
        for speed in sweep_table:
            PDL_form.PDL_Sweeping_form.txt_sweepspeed.addItem(str(speed))
        
    else:
        PDL_form.PDL_Sweeping_form.txt_sweepspeed = QtWidgets.QLineEdit(PDL_form.PDL_Sweeping_form.grb_sweep_setting)
        PDL_form.PDL_Sweeping_form.txt_sweepspeed.setGeometry(QtCore.QRect(400, 40, 113, 26))
        PDL_form.PDL_Sweeping_form.txt_sweepspeed.setTabletTracking(True)
        PDL_form.PDL_Sweeping_form.txt_sweepspeed.setObjectName("txt_sweepspeed")
            
    return 0

# set parameter for measure
def set_parameterformeasure():
    
    inst_error = tsl_.Sweep_Stop()
    
    global mpms
    for mpm in mpms:
        mpm.Logging_Stop()

    startwave = float(PDL_form.PDL_Sweeping_form.txt_startwave.text())
    stopwave = float(PDL_form.PDL_Sweeping_form.txt_stopwave.text())
    wavestep = float(PDL_form.PDL_Sweeping_form.txt_wavestep.text())
    if Flag_570 == True:
        speed = float(PDL_form.PDL_Sweeping_form.txt_sweepspeed.currentText())
    else:
        speed = float(PDL_form.PDL_Sweeping_form.txt_sweepspeed.text())
    set_pow = float(PDL_form.PDL_Sweeping_form.txt_power.text())
    
    # ----TSL Setting 
    # set TSL power 
    inst_error = tsl_.Set_APC_Power_dBm(set_pow)
    if inst_error != 0:
        show_instrument_error(inst_error)
        return

    # Set wavelength, step, speed in TSL and get acctual step
    inst_error, tsl_acctualstep = tsl_.Set_Sweep_Parameter_for_STS(startwave, stopwave, speed, wavestep, -9999);

    if inst_error != 0:
        show_instrument_error(inst_error)
        return
    
    # Get start wavelength from TSL
    inst_error, setstartwave = tsl_.Get_Sweep_Start_Wavelength(0)
    if inst_error != 0:
        show_instrument_error(inst_error)
        return
    
    if startwave != setstartwave:
        show_error_message("The input start wavelength cannot be set in TSL.\r Please check with TSL")
        return
    
    # Get stop wavelength from TSL
    inst_error, setstopwave = tsl_.Get_Sweep_Stop_Wavelength(0)
    if inst_error != 0:
        show_instrument_error(inst_error)
        return
    
    if stopwave != setstopwave:
        show_error_message("The input stop wavelength cannot be set in TSL.\rPlease check with TSL")
        return
    # Set firmed wavelength
    inst_error = tsl_.Set_Wavelength(startwave)
    if inst_error != 0:
        show_instrument_error(inst_error)
        return

    # Set busy status timeout value 3 sec
    inst_error = tsl_.TSL_Busy_Check(3000)
    if inst_error != 0:
        show_instrument_error(inst_error)
        return
    
    for mpm in mpms:

        # Set sweep condition into all mpm
        inst_error = mpm.Set_Logging_Paremeter_for_STS(startwave, stopwave, wavestep, speed, MPM.Measurement_Mode.Freerun)

        if inst_error != 0:
            show_instrument_error(inst_error)
            return

    # Get average time from mpm
    inst_error, averaging_time = mpms[0].Get_Averaging_Time(-999);

    if inst_error != 0:
        show_instrument_error(inst_error)
        return
    
    # Set sweeping condition for spu
    inst_error = spu_.Set_Sampling_Parameter(startwave, stopwave, speed, tsl_acctualstep);

    if inst_error != 0:
        show_instrument_error(inst_error)
        return

    # Set average time into spu
    spu_.AveragingTime = averaging_time
    
    # Adjust PCU range
    inst_error = pcu_.Range_Adjust()

    if inst_error != 0 :
        show_instrument_error(inst_error)
        return
    
    # Clear all measure data structure
    sts_error = Cal_STS.Clear_Measdata();

    if sts_error != 0:
        show_sts_error(sts_error)
        return

    # Clear all reference data structure
    sts_error = Cal_STS.Clear_Refdata()
    if sts_error != 0:
        show_sts_error(sts_error)
        return
    
    # Setting for Rescaling mode
    sts_error = Cal_STS.Set_Rescaling_Setting(RescalingMode.Freerun_SPU, averaging_time, True)
    if sts_error != 0:
        show_sts_error(sts_error)
        return

    # Get sweepinf wavelength table
    sts_error = Cal_STS.Make_Sweep_Wavelength_Table(startwave, stopwave, tsl_acctualstep)
    if sts_error != 0:
        show_sts_error(sts_error)
        return
    
    # Get target wavelength table
    sts_error = Cal_STS.Make_Target_Wavelength_Table(startwave, stopwave, wavestep)
    if sts_error != 0:
        show_sts_error(sts_error)
        return
    
    if PDL_form.PDL_Sweeping_form.chkeach_ch.isChecked():
        Prepare_dataST_Each()
    else:
        Prepare_dataST()

    if float(tsl_acctualstep) != wavestep:
        QMessageBox.warning(None, 'Waring', "Parameter set Success.\nThe acctual step set with " + str(tsl_acctualstep), QMessageBox.Ok)
    else:
        QMessageBox.warning(None, 'Waring', "Parameter set Success.", QMessageBox.Ok)

# STS reference
def reference():

    for mpm in mpms:
        # Set range 1 in every mpm
        inst_error = mpm.Set_Range(Meas_rang[0])
        if inst_error != 0:
            show_instrument_error(inst_error)
            return

    # Set tsl with status "wait for soft trigger"
    inst_error = tsl_.Sweep_Start()
    if inst_error != 0:
        show_instrument_error(inst_error)

    global inst_flag
    
    if PDL_form.PDL_Sweeping_form.chkeach_ch.isChecked():
        inst_error = Each_channel_reference()
    else:
        inst_error = All_channel_reference()

    if inst_error != 0:
        if inst_error == -9999:
            QMessageBox.warning(None, 'Warning', 'MPM Trigger receive error! Please check trigger cable connection.', QMessageBox.Ok)
        elif inst_flag == True:
            show_instrument_error(inst_error)
        else:
            show_sts_error(inst_error)
        return

    # Stop TSL sweeping
    inst_error = tsl_.Sweep_Stop()
    if inst_error != 0:
        show_instrument_error(inst_error)

    QMessageBox.warning(None, 'Information', 'Completed.', QMessageBox.Ok)
    
def Sweep_Process():

    for mpm in mpms:
        # Set mpm in sweeping status
        inst_error = mpm.Logging_Start()
        if inst_error != 0:
            return inst_error

    # Set tsl in status "waiting for soft trigger"
    inst_error = tsl_.Waiting_For_Sweep_Status(4000, TSL.Sweep_Status.WaitingforTrigger)

    if inst_error != 0:
        for mpm in mpms:
            mpm.Logging_Stop()

        return inst_error

    # Set spu starting sweep
    inst_error = spu_.Sampling_Start()

    if inst_error != 0:
        for mpm in mpms:
            mpm.Logging_Stop()

        return inst_error

    # Sent soft trigger to tsl
    inst_error = tsl_.Set_Software_Trigger()

    if inst_error != 0:
        for mpm in mpms:
            mpm.Logging_Stop()
            
        return inst_error

    # Waiting for SPU sampling
    inst_error = spu_.Waiting_for_sampling()

    if inst_error != 0:
        for mpm in mpms:
            mpm.Logging_Stop()
            
        return inst_error

    mpm_stauts = 0
    mpm_count = 0       
    mpm_complet_flag = True                 
    isSweeping = True

    first_time = time.time() * 1000
    while isSweeping:
        for mpm in mpms:

            # Using logg command to get power data
            inst_error, mpm_stauts, mpm_count = mpm.Get_Logging_Status(0, 0)
            if inst_error != 0:
                return inst_error
            if mpm_stauts == 1:
                isSweeping = False
                break
            
            second_time = time.time() * 1000
            
            # 2 minutes timeout
            if (second_time - first_time) >= 2000:

                mpm_complet_flag = False
                isSweeping = False
                break

    for mpm in mpms:
        # stop mpm's sweeping
        inst_error = mpm.Logging_Stop()
        if inst_error != 0:
            return inst_error

    # Wait tsl in standby status
    inst_error = tsl_.Waiting_For_Sweep_Status(5000, TSL.Sweep_Status.Standby)

    if inst_error != 0:
        return inst_error

    if mpm_complet_flag == False:
        return -9999

    return 0

def Get_reference_samplingdata(currentSOP):
    global Ref_monitordata_struct

    for item in Refdata_struct:

        if item.SOP != currentSOP:
            continue

        inst_error = Get_MPM_Loggdata(item.MPMNumber, item.SlotNumber, item.ChannelNumber)

        if inst_error != 0:
            inst_flag = True
            return inst_error
        
        logg_data = mpmLoggData  

        # Transfer Reference data to stsprocessDLL
        cal_error = Cal_STS.Add_Ref_MPMData_CH(logg_data, item)

        if cal_error != 0:
            inst_flag = False
            return cal_error

    # Get rawdata (trigger, monitor) from SPU 
    inst_error, triggerdata, monitordata = spu_.Get_Sampling_Rawdata(None, None)

    if inst_error != 0:
        inst_flag = True
        return inst_error
    
    for monitor_item in Ref_monitordata_struct:
        if monitor_item.SOP == currentSOP:
            # Transfer trigger, monitor data to stsprocessDll to create data structure
            cal_error = Cal_STS.Add_Ref_MonitorData(triggerdata, monitordata, monitor_item)

            if cal_error != 0:
                inst_flag = False
                return cal_error

            break
    return 0

def Get_Each_channel_reference_samplingdata(currentMPMNumber, currentSlotNumber, currentChannelNumber, currentSOP, currentSweepCount):
    global inst_flag
    global Refdata_struct

    for item in Refdata_struct:

        if item.MPMNumber != currentMPMNumber or item.SlotNumber != currentSlotNumber or item.ChannelNumber != currentChannelNumber or item.SOP != currentSOP:
            continue

        inst_error = Get_MPM_Loggdata(item.MPMNumber, item.SlotNumber, item.ChannelNumber)

        if inst_error != 0:
            inst_flag = True
            return inst_error
        
        logg_data = mpmLoggData  

        # Transfer Reference data to stsprocessDLL
        cal_error = Cal_STS.Add_Ref_MPMData_CH(logg_data, item)

        if cal_error != 0:
            inst_flag = False
            return cal_error

    # Get rawdata (trigger, monitor) from SPU 
    inst_error, triggerdata, monitordata = spu_.Get_Sampling_Rawdata(None, None)

    if inst_error != 0:
        inst_flag = True
        return inst_error

    for monitor_item in Ref_monitordata_struct:
        if monitor_item.SlotNumber == currentSlotNumber and monitor_item.ChannelNumber == currentChannelNumber and monitor_item.SOP == currentSOP and monitor_item.SweepCount == currentSweepCount:
            # Transfer trigger, monitor data to stsprocessDll to create data structure
            cal_error = Cal_STS.Add_Ref_MonitorData(triggerdata, monitordata, monitor_item)

            if cal_error != 0:
                inst_flag = False
                return cal_error

            break
    return 0

def Get_MPM_Loggdata(deveice, slot, ch):

    global mpmLoggData
    # Get power data from channel
    inst_error, mpmLoggData = mpms[deveice].Get_Each_Channel_Logdata(slot, ch, None)
    return inst_error

# Measure process
def measure():
    sweepcounter = 0

    # Clear measure data
    Cal_STS.Clear_Measdata()

    # Make tsl into status "wait for soft trigger"
    inst_error = tsl_.Sweep_Start()

    if inst_error != 0:
        show_instrument_error(inst_error)
        
    global inst_flag

    for loop1 in range(len(Meas_rang)):

        for mpm in mpms:

            # Set the sweeping range to mpm
            inst_error = mpm.Set_Range(Meas_rang[loop1])

            if inst_error != 0:
                show_instrument_error(inst_error)
                return

        if PDL_form.PDL_Sweeping_form.chk2sop.isChecked() and loop1 != 0:
            soploop = 2
        else:
            soploop = 4

        for loop2 in range(soploop):

            # Set range to pcu
            if loop2 == 0:
                pcu_.Set_SOP_Stauts(pcu_.SOP_Stauts.LVP)
            if loop2 == 1:
                pcu_.Set_SOP_Stauts(pcu_.SOP_Stauts.LHP)
            if loop2 == 2:
                pcu_.Set_SOP_Stauts(pcu_.SOP_Stauts.LP45)
            if loop2 == 3:
                pcu_.Set_SOP_Stauts(pcu_.SOP_Stauts.RCP)

            if inst_error != 0:
                show_instrument_error(inst_error)
                return

            inst_error = Sweep_Process()
            if inst_error != 0 and inst_error != -9999:
                show_instrument_error(inst_error)
                return

            if inst_error == -9999:
                QMessageBox.warning(None, 'Warning', 'MPM Trigger receive error! Please check trigger cable connection.', QMessageBox.Ok)
                return

            # Make tsl into status "wait for soft trigger"
            inst_error = tsl_.Sweep_Start()

            if inst_error != 0:
                show_instrument_error(inst_error)
                return

            if loop2 == 0:
                inst_error = Get_measurement_samplingdata(sweepcounter + 1, pcu_.SOP_Stauts.LVP)
            if loop2 == 1:
                inst_error = Get_measurement_samplingdata(sweepcounter + 1, pcu_.SOP_Stauts.LHP)
            if loop2 == 2:
                inst_error = Get_measurement_samplingdata(sweepcounter + 1, pcu_.SOP_Stauts.LP45)
            if loop2 == 3:
                inst_error = Get_measurement_samplingdata(sweepcounter + 1, pcu_.SOP_Stauts.RCP)

            if inst_error != 0:
                if inst_flag == True:
                    show_instrument_error(inst_error)
                else:
                    show_sts_error(inst_error)

                return
            sweepcounter = sweepcounter + 1

    # Rescaling Measurement data
    process_error = Cal_STS.Cal_MeasData_Rescaling()

    if process_error != 0:
        show_sts_error(process_error)
        return

    # Merge IL data
    if Flag_215 == True:
        process_error = Cal_STS.Cal_IL_Merge(Module_Type.MPM_215)
    elif Flag_213 == True:
        process_error = Cal_STS.Cal_IL_Merge(Module_Type.MPM_213)
    else:
        process_error = Cal_STS.Cal_IL_Merge(Module_Type.MPM_211)

    # Stop sweeping
    inst_error = tsl_.Sweep_Stop()

    process_error = PDL_Process_AndSave()

    QMessageBox.warning(None, 'Information', 'Completed.', QMessageBox.Ok)

def Get_measurement_samplingdata(sweepcount, currentSOP):
 
    global Data_struct
    global Meas_monitor_struct
    global inst_flag

    for item in Data_struct:

        if item.SweepCount != sweepcount or item.SOP != currentSOP:
            continue

        inst_error = Get_MPM_Loggdata(item.MPMNumber, item.SlotNumber, item.ChannelNumber)

        if inst_error != 0:
            inst_flag = True
            return inst_error
        
        logg_data = mpmLoggData

        # Transfer logging data in stsprocessDLL for calculation
        cal_error = Cal_STS.Add_Meas_MPMData_CH(logg_data, item)

        if cal_error != 0:
            inst_flag = False
            return cal_error

    # Get sampling data from SPU
    inst_error, triggerdata, monitordata = spu_.Get_Sampling_Rawdata(None, None)

    if inst_error != 0:
        inst_flag = True
        return inst_error

    for monitor_item in Meas_monitordata_struct:

        if monitor_item.SweepCount == sweepcount and monitor_item.SOP == currentSOP:
            # Transfer trigger, monitor data in stsprocessDll for calculating 
            cal_error = Cal_STS.Add_Meas_MonitorData(triggerdata, monitordata, monitor_item)

            if cal_error != 0:
                inst_flag = False
                return cal_error

            break
        
    return 0

# Save data function
def save_function():
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    file_path, filetype = QFileDialog.getSaveFileName(None, "Save data", "", "*.csv", options=options)
    if file_path.find('.csv') < 0:
        file_path = file_path + ".csv"
        
    return file_path

def get_file_path_function(filePath):
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    file_path, filetype = QFileDialog.getSaveFileName(None, "Save data", filePath, "*.csv", options=options)
    if file_path.find('.csv') < 0:
        file_path = file_path + ".csv"
        
    return file_path

def Prepare_dataST():
    
    global Ref_monitor_struct
    global Meas_rang
    global Data_struct
    global Refdata_struct
    global Meas_monitordata_struct
    global Mergedata_struct
    global Ref_monitordata_struct

    Meas_rang.clear()
    Data_struct.clear()
    Refdata_struct.clear()
    Ref_monitordata_struct.clear()
    Meas_monitordata_struct.clear()
    Mergedata_struct.clear()
    
    allRangeCount = PDL_form.PDL_Sweeping_form.list_widget_range.count()
    allRangeList = [PDL_form.PDL_Sweeping_form.list_widget_range.itemWidget(PDL_form.PDL_Sweeping_form.list_widget_range.item(i))
                for i in range(allRangeCount)]
    
    checkedRanges = []
    for range1 in allRangeList:
        if range1.isChecked():
            checkedRanges.append(range1.text())
            
    rangecout = checkedRanges.count
    
    allChannelCount = PDL_form.PDL_Sweeping_form.list_widget_channel.count()
    allChannelList = [PDL_form.PDL_Sweeping_form.list_widget_channel.itemWidget(PDL_form.PDL_Sweeping_form.list_widget_channel.item(i))
                    for i in range(allChannelCount)]
    
    global checkedChannels
    checkedChannels = []
    for channel in allChannelList:
        if channel.isChecked():
            checkedChannels.append(channel.text())
            
    chcount = checkedChannels.count
    
    if Flag_215 == True:
        Meas_rang.append(1)
    else:
        if rangecout == 0 or chcount == 0:
            QMessageBox.warning(None, 'Waring', 'Please check measurement parameters.', QMessageBox.Ok)
            return

        for range1 in checkedRanges:
            Meas_rang.append(int(range1.replace("Range","")))

    sweep_count = 1
    
    # Make Data_struct for saving channel, range, SOP
    for channel in checkedChannels:

        text_st = channel
        split_st = text_st.split("-")
        device_number = int(split_st[0]) - 1
        slot_number = int(split_st[1])
        ch_number = int(split_st[2])

        for rangeloop in range(len(Meas_rang)):

            if PDL_form.PDL_Sweeping_form.chk2sop.isChecked() and rangeloop != 0:
                sopcount = 2
            else:
                sopcount = 4

            for soploop in range(sopcount):
                set_struct = STSDataStruct()
                set_struct.MPMNumber = device_number
                set_struct.SlotNumber = slot_number
                set_struct.ChannelNumber = ch_number
                set_struct.RangeNumber = Meas_rang[rangeloop]
                set_struct.SOP = soploop
                set_struct.SweepCount = sweep_count
                sweep_count = sweep_count + 1

                Data_struct.append(set_struct)

        sweep_count = 1

    sweep_count = 1
    # Make Refdata_struct for saving channel, range, SOP
    # Make Mergedata_struct for saving channel, SOP
    for channel in checkedChannels:
        text_st = channel
        split_st = text_st.split("-")
        device_number = int(split_st[0]) - 1
        slot_number = int(split_st[1])
        ch_number = int(split_st[2])

        sopcount = 4

        for soploop in range(sopcount):
            set_struct = STSDataStruct()
            set_struct.MPMNumber = device_number
            set_struct.SlotNumber = slot_number
            set_struct.ChannelNumber = ch_number
            set_struct.RangeNumber = 1
            set_struct.SOP = soploop
            set_struct.SweepCount = sweep_count

            set_merge_struct = STSDataStructForMerge()
            set_merge_struct.MPMNumber = device_number
            set_merge_struct.SlotNumber = slot_number
            set_merge_struct.ChannelNumber = ch_number
            set_merge_struct.SOP = soploop

            sweep_count = sweep_count + 1
            Refdata_struct.append(set_struct)
            Mergedata_struct.append(set_merge_struct)
            
        sweep_count = 1

    sweep_count = 1

    # Make Meas_monitordata_struct for saving channel, SOP
    for channel in checkedChannels:
        
        text_st = channel
        split_st = text_st.split("-")
        device_number = int(split_st[0]) - 1

        for rangeloop in range(len(Meas_rang)):

            if PDL_form.PDL_Sweeping_form.chk2sop.isChecked() and rangeloop != 0:
                sopcount = 2
            else:
                sopcount = 4

            for soploop in range(sopcount):
                set_monitor_struct = STSMonitorStruct()
                set_monitor_struct.MPMNumber = device_number
                set_monitor_struct.SOP = soploop
                set_monitor_struct.SweepCount = sweep_count
                Meas_monitordata_struct.append(set_monitor_struct)
                sweep_count = sweep_count + 1
        break

    sweep_count = 1
    # Make set_ref_monitor_struct for saving channel, range, SOP
    for channel in checkedChannels:

        text_st = channel
        split_st = text_st.split("-")
        device_number = int(split_st[0]) - 1
        slot_number = int(split_st[1])
        ch_number = int(split_st[2])

        for soploop in range(4):
            set_ref_monitor_struct = STSDataStruct()
            set_ref_monitor_struct.MPMNumber = device_number
            set_ref_monitor_struct.SlotNumber = slot_number
            set_ref_monitor_struct.ChannelNumber = ch_number
            set_ref_monitor_struct.RangeNumber = 1
            set_ref_monitor_struct.SOP = soploop
            set_ref_monitor_struct.SweepCount = soploop + 1
            Ref_monitordata_struct.append(set_ref_monitor_struct)

        break

def Prepare_dataST_Each():

    global Ref_monitor_struct
    global Meas_rang
    global Data_struct
    global Refdata_struct
    global Meas_monitordata_struct
    global Mergedata_struct
    global Ref_monitordata_struct

    Meas_rang.clear()
    Data_struct.clear()
    Refdata_struct.clear()
    Ref_monitordata_struct.clear()
    Meas_monitordata_struct.clear()
    Mergedata_struct.clear()

    allRangeCount = PDL_form.PDL_Sweeping_form.list_widget_range.count()
    allRangeList = [PDL_form.PDL_Sweeping_form.list_widget_range.itemWidget(PDL_form.PDL_Sweeping_form.list_widget_range.item(i))
                for i in range(allRangeCount)]
    
    checkedRanges = []
    for range1 in allRangeList:
        if range1.isChecked():
            checkedRanges.append(range1.text())
            
    rangecout = checkedRanges.count
    
    allChannelCount = PDL_form.PDL_Sweeping_form.list_widget_channel.count()
    allChannelList = [PDL_form.PDL_Sweeping_form.list_widget_channel.itemWidget(PDL_form.PDL_Sweeping_form.list_widget_channel.item(i))
                    for i in range(allChannelCount)]
    
    global checkedChannels
    checkedChannels = []
    for channel in allChannelList:
        if channel.isChecked():
            checkedChannels.append(channel.text())
            
    chcount = checkedChannels.count
    
    if Flag_215 == True:
        Meas_rang.append(1)
    else:
        if rangecout == 0 or chcount == 0:
            QMessageBox.warning(None, 'Waring', 'Please check measurement parameters.', QMessageBox.Ok)
            return

        for range1 in checkedRanges:
            Meas_rang.append(int(range1.replace("Range","")))

    sweep_count = 1

    # Make Data_struct for saving channel, range, SOP
    for channel in checkedChannels:

        text_st = channel
        split_st = text_st.split("-")
        device_number = int(split_st[0]) - 1
        slot_number = int(split_st[1])
        ch_number = int(split_st[2])

        for rangeloop in range(len(Meas_rang)):
            
            if PDL_form.PDL_Sweeping_form.chk2sop.isChecked() and rangeloop != 0:
                sopcount = 2
            else:
                sopcount = 4

            for soploop in range(sopcount):
                set_struct = STSDataStruct()
                set_struct.MPMNumber = device_number
                set_struct.SlotNumber = slot_number
                set_struct.ChannelNumber = ch_number
                set_struct.RangeNumber = Meas_rang[rangeloop]
                set_struct.SOP = soploop
                set_struct.SweepCount = sweep_count
                sweep_count = sweep_count + 1
                Data_struct.append(set_struct)

        sweep_count = 1

    sweep_count = 1
    # Make Refdata_struct for saving channel, range, SOP
    # Make Ref_monitordata_struct for saving channel, range, SOP
    for channel in checkedChannels:

        text_st = channel
        split_st = text_st.split("-")
        device_number = int(split_st[0]) - 1
        slot_number = int(split_st[1])
        ch_number = int(split_st[2])

        sopcount = 4

        for soploop in range(sopcount):
            set_struct = STSDataStruct()
            set_struct.MPMNumber = device_number
            set_struct.SlotNumber = slot_number
            set_struct.ChannelNumber = ch_number
            set_struct.RangeNumber = 1
            set_struct.SOP = soploop
            set_struct.SweepCount = sweep_count

            set_ref_monitor_struct = STSDataStruct()
            set_ref_monitor_struct.MPMNumber = device_number
            set_ref_monitor_struct.SlotNumber = slot_number
            set_ref_monitor_struct.ChannelNumber = ch_number
            set_ref_monitor_struct.RangeNumber = 1
            set_ref_monitor_struct.SOP = soploop
            set_ref_monitor_struct.SweepCount = sweep_count

            sweep_count = sweep_count + 1
            Refdata_struct.append(set_struct)
            Ref_monitordata_struct.append(set_ref_monitor_struct)

    sweep_count = 1
    # Make set_merge_struct for saving channel, SOP
    for channel in checkedChannels:

        text_st = channel
        split_st = text_st.split("-")
        device_number = int(split_st[0]) - 1
        slot_number = int(split_st[1])
        ch_number = int(split_st[2])

        sopcount = 4

        for soploop in range(sopcount):

            set_merge_struct = STSDataStructForMerge()
            set_merge_struct.MPMNumber = device_number
            set_merge_struct.SlotNumber = slot_number
            set_merge_struct.ChannelNumber = ch_number
            set_merge_struct.SOP = soploop

            sweep_count = sweep_count + 1
            Mergedata_struct.append(set_merge_struct)

        sweep_count = 1

    sweep_count = 1
    # Make Meas_monitordata_struct for saving channel, SOP
    for channel in checkedChannels:

        text_st = channel
        split_st = text_st.split("-")
        device_number = int(split_st[0]) - 1

        for rangeloop in range(len(Meas_rang)):

            if PDL_form.PDL_Sweeping_form.chk2sop.isChecked() and rangeloop != 0:
                sopcount = 2
            else:
                sopcount = 4

            for soploop in range(sopcount):
                set_monitor_struct = STSMonitorStruct()
                set_monitor_struct.MPMNumber = device_number
                set_monitor_struct.SOP = soploop
                set_monitor_struct.SweepCount = sweep_count
                Meas_monitordata_struct.append(set_monitor_struct)
                sweep_count = sweep_count + 1
        break

def Each_channel_reference():

    global inst_flag
    global Refdata_struct
    
    for item in Refdata_struct:

        # Set SOP for PCU
        if item.SOP == 0:
            QMessageBox.warning(None, 'Information', "Connect fiber to MPM" + str(item.MPMNumber + 1) + "_Slot" + str(item.SlotNumber) + "_Ch" + str(item.ChannelNumber) + ".", QMessageBox.Ok)
            inst_error = pcu_.Set_SOP_Stauts(pcu_.SOP_Stauts.LVP)
        elif item.SOP == 1:
            inst_error = pcu_.Set_SOP_Stauts(pcu_.SOP_Stauts.LHP)
        elif item.SOP == 2:
            inst_error = pcu_.Set_SOP_Stauts(pcu_.SOP_Stauts.LP45)
        elif item.SOP == 3:
            inst_error = pcu_.Set_SOP_Stauts(pcu_.SOP_Stauts.RCP)

        if inst_error != 0:
            inst_flag = True
            return inst_error

        # Sweeping process 
        inst_error = Sweep_Process()

        if inst_error != 0:
            inst_flag = True
            return inst_error

        # Make tsl in status "wait for trigger"
        inst_error = tsl_.Sweep_Start()
        if inst_error != 0:
            inst_flag = True
            return inst_error
        
        # Get sampling data in every channel
        if item.SOP == 0:
            inst_error = Get_Each_channel_reference_samplingdata(item.MPMNumber, item.SlotNumber, item.ChannelNumber, pcu_.SOP_Stauts.LVP, item.SweepCount)
        elif item.SOP == 1:
            inst_error = Get_Each_channel_reference_samplingdata(item.MPMNumber, item.SlotNumber, item.ChannelNumber, pcu_.SOP_Stauts.LHP, item.SweepCount)
        elif item.SOP == 2:
            inst_error = Get_Each_channel_reference_samplingdata(item.MPMNumber, item.SlotNumber, item.ChannelNumber, pcu_.SOP_Stauts.LP45, item.SweepCount)
        elif item.SOP == 3:
            inst_error = Get_Each_channel_reference_samplingdata(item.MPMNumber, item.SlotNumber, item.ChannelNumber, pcu_.SOP_Stauts.RCP, item.SweepCount)

        if inst_error != 0:
            return inst_error

        # Rescaling for Refernece data
        process_error = Cal_STS.Cal_RefData_Rescaling()

        if process_error != 0:
            inst_flag = False
            return process_error

    return 0

def All_channel_reference():

    global inst_flag

    for loop1 in range(4):

        # Set SOP for PCU
        if loop1 == 0:
            inst_error = pcu_.Set_SOP_Stauts(pcu_.SOP_Stauts.LVP)
        elif loop1 == 1:
            inst_error = pcu_.Set_SOP_Stauts(pcu_.SOP_Stauts.LHP)
        elif loop1 == 2:
            inst_error = pcu_.Set_SOP_Stauts(pcu_.SOP_Stauts.LP45)
        elif loop1== 3:
            inst_error = pcu_.Set_SOP_Stauts(pcu_.SOP_Stauts.RCP)

        if inst_error != 0:
            inst_flag = True
            return inst_error

        # Sweeping process 
        inst_error = Sweep_Process()

        if inst_error != 0:
            inst_flag = True
            return inst_error

        # Make tsl in status "wait for trigger"
        inst_error = tsl_.Sweep_Start()
        if inst_error != 0:
            inst_flag = True
            return inst_error
        
        # Get sampling data in every channel
        if loop1 == 0:
            inst_error = Get_reference_samplingdata(pcu_.SOP_Stauts.LVP)
        elif loop1 == 1:
            inst_error = Get_reference_samplingdata(pcu_.SOP_Stauts.LHP)
        elif loop1 == 2:
            inst_error = Get_reference_samplingdata(pcu_.SOP_Stauts.LP45)
        elif loop1== 3:
            inst_error = Get_reference_samplingdata(pcu_.SOP_Stauts.RCP)

        if inst_error != 0:
            return inst_error

    # Rescaling for Refernece data
    process_error = Cal_STS.Cal_RefData_Rescaling()

    if process_error != 0:
        inst_flag = False
        return process_error

    return 0

def PDL_Process_AndSave():
    # Get target wavelength list
    cal_error, wavetable = Cal_STS.Get_Target_Wavelength_Table(None)
    if cal_error != 0:
        show_sts_error(cal_error)
        return cal_error

    # get correctting data
    inst_error, correctionSOP = pcu_.Cal_All_SOP_Parametar(wavetable, None)

    if inst_error != 0:
        show_instrument_error(inst_error)
        return cal_error

    # Add Calculated Each SOP Array
    cal_error = Cal_STS.Add_PCU_CalData(correctionSOP)
    if cal_error != 0:
        show_sts_error(cal_error)
        return cal_error

    befor_struct = STSDataStructForMerge()
    SOPIL = Array.CreateInstance(System.Single, 4, len(wavetable))
    
    global cal_IL_list
    global cal_IL_item_list
    cal_IL_list = []
    cal_IL_item_list = []
    
    # Loop Merged structure
    for item in Mergedata_struct:
        if item.MPMNumber == befor_struct.MPMNumber and item.SlotNumber == befor_struct.SlotNumber and item.ChannelNumber == befor_struct.ChannelNumber:
            continue

        # Loop 4 ranges
        for loop1 in range(4):
            get_struct = STSDataStructForMerge()
            get_struct.MPMNumber = item.MPMNumber
            get_struct.SlotNumber = item.SlotNumber
            get_struct.ChannelNumber = item.ChannelNumber
            get_struct.SOP = loop1

            # Get Merged IL data
            cal_error, ildata = Cal_STS.Get_IL_Merge_Data(None, get_struct)

            if cal_error != 0:
                show_sts_error(cal_error)
                return cal_error

            for loop2 in range(len(ildata)):
                SOPIL[loop1, loop2] = ildata[loop2]

        befor_struct = get_struct
        
        calPDL = []
        calIL = []
        calILmax = []
        calILmin = []
        
        # Calculate PDL
        cal_error, calPDL, calIL, calILmax, calILmin = Cal_STS.Cal_PDL(SOPIL, [], [], [], [])

        if cal_error != 0:
            show_sts_error(cal_error)
            return cal_error
        
        # Get IL data of cancel to SOP Wavelength dependence
        cal_error, cal_IL = Cal_STS.Get_Calibrated_IL(None)
        if cal_error != 0:
            show_sts_error(cal_error)
            return cal_error
        
        # Add Calculate IL
        cal_IL_list.append(cal_IL)
        # Add the item got from merged structure to cal_IL_item 
        cal_IL_item_list.append(item)

        # Save Calculate date into csv file
        fpath = get_file_path_function("Device" + str(get_struct.MPMNumber + 1) + "Slot" + str(get_struct.SlotNumber) + "Ch" + str(get_struct.ChannelNumber) + "_PDL_data.csv")

        header = ["Wavelength(nm)", "IL(dB)", "PDL(dB)", "ILMax(dB)", "ILMin(dB)"]
        
        result = []
        for loop3 in range(len(wavetable)):
            
            writestr = []
            writestr.append(str(wavetable[loop3]))
            writestr.append(str(calIL[loop3]))
            writestr.append(str(calPDL[loop3]))
            writestr.append(str(calILmax[loop3]))
            writestr.append(str(calILmin[loop3]))
            
            result.append(writestr)
        
        cal_result = pd.DataFrame(result, columns=header)
        cal_result.to_csv(fpath, index=False)

        # if Save of muller parameter is checked
        if PDL_form.PDL_Sweeping_form.chkmuller.isChecked():

            # get muller raw data
            cal_error, m11, m12, m13, m14 = Cal_STS.Get_Mueller_Raw_Data(None, None, None, None)

            if cal_error != 0:
                show_sts_error(cal_error)
                return cal_error

            # Save muller data into csv file.
            fpath = get_file_path_function("Device" + str(get_struct.MPMNumber + 1) + "Slot" + str(get_struct.SlotNumber) + "Ch" + str(get_struct.ChannelNumber) + "_Mueller_data.csv")

            header = ["Wavelength(nm)", "m11(mW)", "m12(mW)", "m13(mW)", "m14(mW)"]

            result = []
            for loop3 in range(len(wavetable)):
                
                writestr = []
                writestr.append(str(wavetable[loop3]))
                writestr.append(str(m11[loop3]))
                writestr.append(str(m12[loop3]))
                writestr.append(str(m13[loop3]))
                writestr.append(str(m14[loop3]))
                
                result.append(writestr)

        cal_result = pd.DataFrame(result, columns=header)
        cal_result.to_csv(fpath, index=False)

    return 0

def check_sweepcount(rangenumber, sopcount):

    sweepcount = 0
    
    for loop1 in range(len(Meas_rang)):

        if Meas_rang[loop1] == rangenumber:

            if loop1 == 0:
                sweepcount = sopcount + 1
                return sweepcount
            elif loop1 == 1:

                sweepcount = 4 + sopcount + 1
                return sweepcount
            elif loop1 == 2:

                if PDL_form.PDL_Sweeping_form.chk2sop.isChecked():
                    sweepcount = 6 + sopcount + 1
                else:
                    sweepcount = 8 + sopcount + 1

                return sweepcount

            elif loop1 == 3:

                if PDL_form.PDL_Sweeping_form.chk2sop.isChecked():
                    sweepcount = 8 + sopcount + 1
                else:
                    sweepcount = 12 + sopcount + 1

                return sweepcount

            elif loop1 == 4:

                if PDL_form.PDL_Sweeping_form.chk2sop.isChecked():
                    sweepcount = 10 + sopcount + 1
                else:
                    sweepcount = 16 + sopcount + 1

                return sopcount

    return 0

if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    PDL_form = PDL_Window()
    PDL_form.setWindowTitle('PDL STS Sample')
    root = QFileInfo(__file__).absolutePath()
    PDL_form.setWindowIcon(QIcon(root + "./SANTEC.ico"))
    app.setStyle('Fusion')
    PDL_form.PDL_Sweeping_form = PDL_Sweeping_Window()
    PDL_form.show()
    get_daq_id()
    get_pcu_usb_resource()
    get_tsl_usb_resource()
    sys.exit(app.exec_())

