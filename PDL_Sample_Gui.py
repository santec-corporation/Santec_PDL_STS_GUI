# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PDL_Sample_Gui.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_PDL_Sample(object):
    def setupUi(self, PDL_Sample):
        PDL_Sample.setObjectName("PDL_Sample")
        PDL_Sample.resize(729, 580)
        PDL_Sample.setMinimumSize(QtCore.QSize(729, 580))
        PDL_Sample.setMaximumSize(QtCore.QSize(729, 580))
        PDL_Sample.setFocusPolicy(QtCore.Qt.TabFocus)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../../../../.designer/SANTEC.ICO"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        PDL_Sample.setWindowIcon(icon)
        
        self.groupBox = QtWidgets.QGroupBox(PDL_Sample)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 701, 141))
        self.groupBox.setObjectName("groupBox")
        self.groupBox_2 = QtWidgets.QGroupBox(self.groupBox)
        self.groupBox_2.setGeometry(QtCore.QRect(10, 20, 131, 111))
        self.groupBox_2.setObjectName("groupBox_2")
        self.rdo_tsl570 = QtWidgets.QRadioButton(self.groupBox_2)
        self.rdo_tsl570.setGeometry(QtCore.QRect(20, 30, 86, 16))
        self.rdo_tsl570.setObjectName("rdo_tsl570")
        self.rdo_tsl550 = QtWidgets.QRadioButton(self.groupBox_2)
        self.rdo_tsl550.setGeometry(QtCore.QRect(20, 60, 101, 16))
        self.rdo_tsl550.setObjectName("rdo_tsl550")
        self.groupBox_3 = QtWidgets.QGroupBox(self.groupBox)
        self.groupBox_3.setGeometry(QtCore.QRect(180, 20, 121, 111))
        self.groupBox_3.setObjectName("groupBox_3")
        self.rdo_tsl_gpib = QtWidgets.QRadioButton(self.groupBox_3)
        self.rdo_tsl_gpib.setGeometry(QtCore.QRect(20, 25, 86, 16))
        self.rdo_tsl_gpib.setObjectName("rdo_tsl_gpib")
        self.rdo_tsl_tcpip = QtWidgets.QRadioButton(self.groupBox_3)
        self.rdo_tsl_tcpip.setGeometry(QtCore.QRect(20, 55, 101, 16))
        self.rdo_tsl_tcpip.setObjectName("rdo_tsl_tcpip")
        self.rdo_tsl_usb = QtWidgets.QRadioButton(self.groupBox_3)
        self.rdo_tsl_usb.setGeometry(QtCore.QRect(20, 85, 86, 16))
        self.rdo_tsl_usb.setObjectName("rdo_tsl_usb")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(440, 20, 71, 16))
        self.label.setObjectName("label")
        self.txt_tsl_gpib_address = QtWidgets.QLineEdit(self.groupBox)
        self.txt_tsl_gpib_address.setGeometry(QtCore.QRect(440, 40, 81, 26))
        self.txt_tsl_gpib_address.setObjectName("txt_tsl_gpib_address")
        
        self.label_tsl_board = QtWidgets.QLabel(self.groupBox)
        self.label_tsl_board.setGeometry(QtCore.QRect(340, 20, 71, 16))
        self.label_tsl_board.setObjectName("label_tsl_board")
        self.txt_tsl_gpib_board = QtWidgets.QLineEdit(self.groupBox)
        self.txt_tsl_gpib_board.setGeometry(QtCore.QRect(340, 40, 81, 26))
        self.txt_tsl_gpib_board.setObjectName("txt_tsl_gpib_board")
        
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(440, 80, 71, 16))
        self.label_2.setObjectName("label_2")
        self.txt_tsl_ip = QtWidgets.QLineEdit(self.groupBox)
        self.txt_tsl_ip.setGeometry(QtCore.QRect(440, 100, 131, 26))
        self.txt_tsl_ip.setObjectName("txt_tsl_ip")
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(590, 80, 71, 16))
        self.label_3.setObjectName("label_3")
        self.txt_tsl_port = QtWidgets.QLineEdit(self.groupBox)
        self.txt_tsl_port.setGeometry(QtCore.QRect(590, 100, 71, 26))
        self.txt_tsl_port.setObjectName("txt_tsl_port")
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setGeometry(QtCore.QRect(340, 80, 81, 16))
        self.label_4.setObjectName("label_4")
        self.cmb_tsl_usb = QtWidgets.QComboBox(self.groupBox)
        self.cmb_tsl_usb.setGeometry(QtCore.QRect(340, 100, 91, 22))
        self.cmb_tsl_usb.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.cmb_tsl_usb.setObjectName("cmb_tsl_usb")
        
        
        self.groupBox_4 = QtWidgets.QGroupBox(PDL_Sample)
        self.groupBox_4.setGeometry(QtCore.QRect(10, 160, 701, 150))
        self.groupBox_4.setObjectName("groupBox_4")
        self.groupBox_5 = QtWidgets.QGroupBox(self.groupBox_4)
        self.groupBox_5.setGeometry(QtCore.QRect(10, 20, 131, 120))
        self.groupBox_5.setObjectName("groupBox_5")
        self.rdo_mpm_gpib = QtWidgets.QRadioButton(self.groupBox_5)
        self.rdo_mpm_gpib.setGeometry(QtCore.QRect(20, 30, 86, 16))
        self.rdo_mpm_gpib.setObjectName("rdo_mpm_gpib")
        self.rdo_mpm_tcpip = QtWidgets.QRadioButton(self.groupBox_5)
        self.rdo_mpm_tcpip.setGeometry(QtCore.QRect(20, 60, 101, 16))
        self.rdo_mpm_tcpip.setObjectName("rdo_mpm_tcpip")
        
        
        self.groupBox_device_1 = QtWidgets.QGroupBox(self.groupBox_4)
        self.groupBox_device_1.setGeometry(QtCore.QRect(180, 20, 230, 120))
        self.groupBox_device_1.setObjectName("groupBox_device_1")
        self.txt_mpm_port = QtWidgets.QLineEdit(self.groupBox_device_1)
        self.txt_mpm_port.setGeometry(QtCore.QRect(150, 40, 71, 26))
        self.txt_mpm_port.setObjectName("txt_mpm_port")
        self.txt_mpm_ip = QtWidgets.QLineEdit(self.groupBox_device_1)
        self.txt_mpm_ip.setGeometry(QtCore.QRect(10, 40, 131, 26))
        self.txt_mpm_ip.setObjectName("txt_mpm_ip")
        self.label_mpm_board = QtWidgets.QLabel(self.groupBox_device_1)
        self.label_mpm_board.setGeometry(QtCore.QRect(10, 70, 71, 16))
        self.label_mpm_board.setObjectName("label_5")
        self.txt_mpm_gpib_board = QtWidgets.QLineEdit(self.groupBox_device_1)
        self.txt_mpm_gpib_board.setGeometry(QtCore.QRect(10, 85, 81, 26))
        self.txt_mpm_gpib_board.setObjectName("txt_mpm_gpib_board")
        self.label_5 = QtWidgets.QLabel(self.groupBox_device_1)
        self.label_5.setGeometry(QtCore.QRect(100, 70, 71, 16))
        self.label_5.setObjectName("label_5")
        self.txt_mpm_gpib_address = QtWidgets.QLineEdit(self.groupBox_device_1)
        self.txt_mpm_gpib_address.setGeometry(QtCore.QRect(100, 85, 81, 26))
        self.txt_mpm_gpib_address.setObjectName("txt_mpm_gpib_address")
        self.label_7 = QtWidgets.QLabel(self.groupBox_device_1)
        self.label_7.setGeometry(QtCore.QRect(10, 25, 71, 16))
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.groupBox_device_1)
        self.label_8.setGeometry(QtCore.QRect(150, 25, 71, 16))
        self.label_8.setObjectName("label_8")
        
        self.groupBox_device_2 = QtWidgets.QGroupBox(self.groupBox_4)
        self.groupBox_device_2.setGeometry(QtCore.QRect(440, 20, 230, 120))
        self.groupBox_device_2.setObjectName("groupBox_device_2")
        #self.txt_mpm2_port = QtWidgets.QLineEdit(self.groupBox_device_2)
        #self.txt_mpm2_port.setGeometry(QtCore.QRect(150, 40, 71, 26))
        #self.txt_mpm2_port.setObjectName("txt_mpm2_port")
        #self.txt_mpm2_ip = QtWidgets.QLineEdit(self.groupBox_device_2)
        #self.txt_mpm2_ip.setGeometry(QtCore.QRect(10, 40, 131, 26))
        #self.txt_mpm2_ip.setObjectName("txt_mpm2_ip")
        #self.label_mpm2_gpib = QtWidgets.QLabel(self.groupBox_device_2)
        #self.label_mpm2_gpib.setGeometry(QtCore.QRect(10, 70, 71, 16))
        #self.label_mpm2_gpib.setObjectName("label_mpm2_gpib")
        #self.txt_mpm2_gpib_address = QtWidgets.QLineEdit(self.groupBox_device_2)
        #self.txt_mpm2_gpib_address.setGeometry(QtCore.QRect(10, 85, 81, 26))
        #self.txt_mpm2_gpib_address.setObjectName("txt_mpm2_gpib_address")
        #self.label_mpm2_IP = QtWidgets.QLabel(self.groupBox_device_2)
        #self.label_mpm2_IP.setGeometry(QtCore.QRect(10, 25, 71, 16))
        #self.label_mpm2_IP.setObjectName("label_mpm2_IP")
        #self.label_mpm2_PORT = QtWidgets.QLabel(self.groupBox_device_2)
        #self.label_mpm2_PORT.setGeometry(QtCore.QRect(150, 25, 71, 16))
        #self.label_mpm2_PORT.setObjectName("label_mpm2_PORT")
        self.btn_add_device = QtWidgets.QPushButton(self.groupBox_device_2)
        self.btn_add_device.setGeometry(QtCore.QRect(170, 30, 50, 26))
        self.btn_add_device.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_add_device.setObjectName("btn_add_device")

        self.btn_delete_device = QtWidgets.QPushButton(self.groupBox_device_2)
        self.btn_delete_device.setGeometry(QtCore.QRect(170, 60, 50, 26))
        self.btn_delete_device.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_delete_device.setObjectName("btn_delete_device")
        
        self.list_widget_1 = QtWidgets.QListWidget(self.groupBox_device_2)
        self.list_widget_1.setGeometry(QtCore.QRect(10, 30, 150, 80))
        self.list_widget_1.setObjectName("list_widget_1")
        
        
        self.PCUGroupBox = QtWidgets.QGroupBox(PDL_Sample)
        self.PCUGroupBox.setGeometry(QtCore.QRect(10, 320, 701, 150))
        self.PCUGroupBox.setObjectName("PCUGroupBox")
        self.PCUGroupBox_2 = QtWidgets.QGroupBox(self.PCUGroupBox)
        self.PCUGroupBox_2.setGeometry(QtCore.QRect(10, 20, 131, 111))
        self.PCUGroupBox_2.setObjectName("PCUGroupBox_2")
        self.rdo_pcu100 = QtWidgets.QRadioButton(self.PCUGroupBox_2)
        self.rdo_pcu100.setGeometry(QtCore.QRect(20, 30, 86, 16))
        self.rdo_pcu100.setObjectName("rdo_pcu100")
        self.rdo_pcu110 = QtWidgets.QRadioButton(self.PCUGroupBox_2)
        self.rdo_pcu110.setGeometry(QtCore.QRect(20, 60, 101, 16))
        self.rdo_pcu110.setObjectName("rdo_pcu110")
        self.PCUGroupBox_3 = QtWidgets.QGroupBox(self.PCUGroupBox)
        self.PCUGroupBox_3.setGeometry(QtCore.QRect(180, 20, 121, 111))
        self.PCUGroupBox_3.setObjectName("PCUGroupBox_3")
        self.rdo_pcu_gpib = QtWidgets.QRadioButton(self.PCUGroupBox_3)
        self.rdo_pcu_gpib.setGeometry(QtCore.QRect(20, 25, 86, 16))
        self.rdo_pcu_gpib.setObjectName("rdo_pcu_gpib")
        self.rdo_pcu_tcpip = QtWidgets.QRadioButton(self.PCUGroupBox_3)
        self.rdo_pcu_tcpip.setGeometry(QtCore.QRect(20, 55, 101, 16))
        self.rdo_pcu_tcpip.setObjectName("rdo_pcu_tcpip")
        self.rdo_pcu_usb = QtWidgets.QRadioButton(self.PCUGroupBox_3)
        self.rdo_pcu_usb.setGeometry(QtCore.QRect(20, 85, 86, 16))
        self.rdo_pcu_usb.setObjectName("rdo_pcu_usb")
        self.label_pcu = QtWidgets.QLabel(self.PCUGroupBox)
        self.label_pcu.setGeometry(QtCore.QRect(440, 20, 71, 16))
        self.label_pcu.setObjectName("label_pcu")
        self.txt_pcu_gpib_address = QtWidgets.QLineEdit(self.PCUGroupBox)
        self.txt_pcu_gpib_address.setGeometry(QtCore.QRect(440, 40, 81, 26))
        self.txt_pcu_gpib_address.setObjectName("txt_pcu_gpib_address")
        
        self.label_pcu_board = QtWidgets.QLabel(self.PCUGroupBox)
        self.label_pcu_board.setGeometry(QtCore.QRect(340, 20, 71, 16))
        self.label_pcu_board.setObjectName("label_pcu_board")
        self.txt_pcu_gpib_board = QtWidgets.QLineEdit(self.PCUGroupBox)
        self.txt_pcu_gpib_board.setGeometry(QtCore.QRect(340, 40, 81, 26))
        self.txt_pcu_gpib_board.setObjectName("txt_pcu_gpib_board")
        
        self.label_pcu_2 = QtWidgets.QLabel(self.PCUGroupBox)
        self.label_pcu_2.setGeometry(QtCore.QRect(440, 80, 71, 16))
        self.label_pcu_2.setObjectName("label_pcu_2")
        self.txt_pcu_ip = QtWidgets.QLineEdit(self.PCUGroupBox)
        self.txt_pcu_ip.setGeometry(QtCore.QRect(440, 100, 131, 26))
        self.txt_pcu_ip.setObjectName("txt_pcu_ip")
        self.label_pcu_3 = QtWidgets.QLabel(self.PCUGroupBox)
        self.label_pcu_3.setGeometry(QtCore.QRect(590, 80, 71, 16))
        self.label_pcu_3.setObjectName("label_pcu_3")
        self.txt_pcu_port = QtWidgets.QLineEdit(self.PCUGroupBox)
        self.txt_pcu_port.setGeometry(QtCore.QRect(590, 100, 71, 26))
        self.txt_pcu_port.setObjectName("txt_pcu_port")
        self.label_pcu_4 = QtWidgets.QLabel(self.PCUGroupBox)
        self.label_pcu_4.setGeometry(QtCore.QRect(340, 80, 81, 16))
        self.label_pcu_4.setObjectName("label_pcu_4")
        self.cmb_pcu_usb = QtWidgets.QComboBox(self.PCUGroupBox)
        self.cmb_pcu_usb.setGeometry(QtCore.QRect(340, 100, 91, 22))
        self.cmb_pcu_usb.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.cmb_pcu_usb.setObjectName("cmb_pcu_usb")
        
        self.groupBox_8 = QtWidgets.QGroupBox(PDL_Sample)
        self.groupBox_8.setGeometry(QtCore.QRect(10, 490, 130, 70))
        self.groupBox_8.setObjectName("groupBox_8")
        self.cmb_dev_number = QtWidgets.QComboBox(self.groupBox_8)
        self.cmb_dev_number.setGeometry(QtCore.QRect(10, 30, 91, 22))
        self.cmb_dev_number.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.cmb_dev_number.setObjectName("cmb_dev_number")
        self.btn_connect = QtWidgets.QPushButton(PDL_Sample)
        self.btn_connect.setGeometry(QtCore.QRect(200, 520, 150, 26))
        self.btn_connect.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_connect.setObjectName("btn_connect")
        self.btn_disconnect = QtWidgets.QPushButton(PDL_Sample)
        self.btn_disconnect.setGeometry(QtCore.QRect(370, 520, 150, 26))
        self.btn_disconnect.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_disconnect.setObjectName("btn_disconnect")

        self.retranslateUi(PDL_Sample)
        self.rdo_tsl550.clicked['bool'].connect(self.rdo_tsl_usb.setDisabled)
        self.rdo_tsl550.clicked['bool'].connect(self.rdo_tsl_tcpip.setDisabled)
        self.rdo_tsl570.clicked['bool'].connect(self.rdo_tsl_tcpip.setEnabled)
        self.rdo_tsl570.clicked['bool'].connect(self.rdo_tsl_usb.setEnabled)
        self.rdo_tsl_gpib.clicked['bool'].connect(self.txt_tsl_gpib_address.setEnabled)
        self.rdo_tsl_gpib.clicked['bool'].connect(self.txt_tsl_gpib_board.setEnabled)
        self.rdo_tsl_gpib.clicked['bool'].connect(self.txt_tsl_ip.setDisabled)
        self.rdo_tsl_tcpip.clicked['bool'].connect(self.txt_tsl_gpib_address.setDisabled)
        self.rdo_tsl_tcpip.clicked['bool'].connect(self.txt_tsl_gpib_board.setDisabled)
        self.rdo_tsl_gpib.clicked['bool'].connect(self.txt_tsl_port.setDisabled)
        self.rdo_tsl_gpib.clicked['bool'].connect(self.cmb_tsl_usb.setDisabled)
        self.rdo_tsl_tcpip.clicked['bool'].connect(self.cmb_tsl_usb.setDisabled)
        self.rdo_tsl_tcpip.clicked['bool'].connect(self.txt_tsl_ip.setEnabled)
        self.rdo_tsl_tcpip.clicked['bool'].connect(self.txt_tsl_port.setEnabled)
        self.rdo_tsl_usb.clicked['bool'].connect(self.txt_tsl_gpib_address.setDisabled)
        self.rdo_tsl_usb.clicked['bool'].connect(self.txt_tsl_gpib_board.setDisabled)
        self.rdo_tsl_usb.clicked['bool'].connect(self.cmb_tsl_usb.setEnabled)
        self.rdo_tsl_usb.clicked['bool'].connect(self.txt_tsl_ip.setDisabled)
        self.rdo_tsl_usb.clicked['bool'].connect(self.txt_tsl_port.setDisabled)
        self.rdo_tsl550.clicked['bool'].connect(self.rdo_tsl_gpib.setChecked)
        self.rdo_tsl550.clicked['bool'].connect(self.txt_tsl_ip.setDisabled)
        self.rdo_tsl550.clicked['bool'].connect(self.txt_tsl_port.setDisabled)
        self.rdo_tsl550.clicked['bool'].connect(self.txt_tsl_gpib_address.setEnabled)
        self.rdo_tsl550.clicked['bool'].connect(self.txt_tsl_gpib_board.setEnabled)
        self.rdo_tsl550.clicked['bool'].connect(self.cmb_tsl_usb.setDisabled)
        self.rdo_mpm_gpib.clicked['bool'].connect(self.txt_mpm_gpib_address.setEnabled)
        self.rdo_mpm_gpib.clicked['bool'].connect(self.txt_mpm_gpib_board.setEnabled)
        self.rdo_mpm_gpib.clicked['bool'].connect(self.txt_mpm_ip.setDisabled)
        self.rdo_mpm_gpib.clicked['bool'].connect(self.txt_mpm_port.setDisabled)
        self.rdo_mpm_tcpip.clicked['bool'].connect(self.txt_mpm_gpib_address.setDisabled)
        self.rdo_mpm_tcpip.clicked['bool'].connect(self.txt_mpm_gpib_board.setDisabled)
        self.rdo_mpm_tcpip.clicked['bool'].connect(self.txt_mpm_ip.setEnabled)
        self.rdo_mpm_tcpip.clicked['bool'].connect(self.txt_mpm_port.setEnabled)
        
        
        self.rdo_pcu100.clicked['bool'].connect(self.rdo_pcu_usb.setDisabled)
        self.rdo_pcu100.clicked['bool'].connect(self.rdo_pcu_tcpip.setDisabled)
        self.rdo_pcu110.clicked['bool'].connect(self.rdo_pcu_tcpip.setEnabled)
        self.rdo_pcu110.clicked['bool'].connect(self.rdo_pcu_usb.setEnabled)
        
        self.rdo_pcu_gpib.clicked['bool'].connect(self.txt_pcu_gpib_address.setEnabled)
        self.rdo_pcu_gpib.clicked['bool'].connect(self.txt_pcu_gpib_board.setEnabled)
        self.rdo_pcu_gpib.clicked['bool'].connect(self.txt_pcu_ip.setDisabled)
        self.rdo_pcu_tcpip.clicked['bool'].connect(self.txt_pcu_gpib_address.setDisabled)
        self.rdo_pcu_tcpip.clicked['bool'].connect(self.txt_pcu_gpib_board.setDisabled)
        self.rdo_pcu_gpib.clicked['bool'].connect(self.txt_pcu_port.setDisabled)
        self.rdo_pcu_gpib.clicked['bool'].connect(self.cmb_pcu_usb.setDisabled)
        self.rdo_pcu_tcpip.clicked['bool'].connect(self.cmb_pcu_usb.setDisabled)
        self.rdo_pcu_tcpip.clicked['bool'].connect(self.txt_pcu_ip.setEnabled)
        self.rdo_pcu_tcpip.clicked['bool'].connect(self.txt_pcu_port.setEnabled)
        self.rdo_pcu_usb.clicked['bool'].connect(self.txt_pcu_gpib_address.setDisabled)
        self.rdo_pcu_usb.clicked['bool'].connect(self.txt_pcu_gpib_board.setDisabled)
        self.rdo_pcu_usb.clicked['bool'].connect(self.cmb_pcu_usb.setEnabled)
        self.rdo_pcu_usb.clicked['bool'].connect(self.txt_pcu_ip.setDisabled)
        self.rdo_pcu_usb.clicked['bool'].connect(self.txt_pcu_port.setDisabled)
        
        self.rdo_pcu100.clicked['bool'].connect(self.rdo_pcu_gpib.setChecked)
        self.rdo_pcu100.clicked['bool'].connect(self.txt_pcu_ip.setDisabled)
        self.rdo_pcu100.clicked['bool'].connect(self.txt_pcu_port.setDisabled)
        self.rdo_pcu100.clicked['bool'].connect(self.txt_pcu_gpib_address.setEnabled)
        self.rdo_pcu100.clicked['bool'].connect(self.txt_pcu_gpib_board.setEnabled)
        self.rdo_pcu100.clicked['bool'].connect(self.cmb_pcu_usb.setDisabled)
        QtCore.QMetaObject.connectSlotsByName(PDL_Sample)

    def retranslateUi(self, PDL_Sample):
        _translate = QtCore.QCoreApplication.translate
        PDL_Sample.setWindowTitle(_translate("PDL_Sample", "Santec PDL STS Sample"))
        self.groupBox.setTitle(_translate("PDL_Sample", "TSL"))
        self.groupBox_2.setTitle(_translate("PDL_Sample", "Product"))
        self.rdo_tsl570.setText(_translate("PDL_Sample", "TSL-570"))
        self.rdo_tsl550.setText(_translate("PDL_Sample", "TSL-550/710"))
        self.groupBox_3.setTitle(_translate("PDL_Sample", "Communication"))
        self.groupBox_device_1.setTitle(_translate("PDL_Sample", "Device"))
        self.rdo_tsl_gpib.setText(_translate("PDL_Sample", "GPIB"))
        self.rdo_tsl_tcpip.setText(_translate("PDL_Sample", "TCP/IP"))
        self.rdo_tsl_usb.setText(_translate("PDL_Sample", "USB"))
        self.label.setText(_translate("PDL_Sample", "GPIB Address"))
        self.label_tsl_board.setText(_translate("PDL_Sample", "GPIB Board"))
        
        self.label_2.setText(_translate("PDL_Sample", "IP Address"))
        self.label_3.setText(_translate("PDL_Sample", "LAN Port"))
        self.label_4.setText(_translate("PDL_Sample", "USB Resource"))
        self.groupBox_4.setTitle(_translate("PDL_Sample", "MPM"))
        self.groupBox_5.setTitle(_translate("PDL_Sample", "Communication"))
        self.rdo_mpm_gpib.setText(_translate("PDL_Sample", "GPIB"))
        self.rdo_mpm_tcpip.setText(_translate("PDL_Sample", "TCP/IP"))
        self.label_7.setText(_translate("PDL_Sample", "IP Address"))
        self.label_8.setText(_translate("PDL_Sample", "LAN Port"))
        self.label_5.setText(_translate("PDL_Sample", "GPIB Address"))
        self.label_mpm_board.setText(_translate("PDL_Sample", "GPIB Board"))
        
        self.groupBox_device_2.setTitle(_translate("PDL_Sample", "MPM List"))
        #self.label_mpm2_IP.setText(_translate("IL_Sample", "IP Address"))
        #self.label_mpm2_PORT.setText(_translate("IL_Sample", "LAN Port"))
        #self.label_mpm2_gpib.setText(_translate("IL_Sample", "GPIB Address"))
        self.btn_add_device.setText(_translate("PDL_Sample", "Add"))
        self.btn_delete_device.setText(_translate("PDL_Sample", "Delete"))
        
        self.PCUGroupBox.setTitle(_translate("PDL_Sample", "PCU"))
        self.PCUGroupBox_2.setTitle(_translate("PDL_Sample", "Product"))
        self.rdo_pcu100.setText(_translate("PDL_Sample", "PCU-100"))
        self.rdo_pcu110.setText(_translate("PDL_Sample", "PCU-110"))
        self.PCUGroupBox_3.setTitle(_translate("PDL_Sample", "Communication"))
        self.rdo_pcu_gpib.setText(_translate("PDL_Sample", "GPIB"))
        self.rdo_pcu_tcpip.setText(_translate("PDL_Sample", "TCP/IP"))
        self.rdo_pcu_usb.setText(_translate("PDL_Sample", "USB"))
        
        self.label_pcu.setText(_translate("PDL_Sample", "GPIB Address"))
        self.label_pcu_board.setText(_translate("PDL_Sample", "GPIB Board"))
        self.label_pcu_2.setText(_translate("PDL_Sample", "IP Address"))
        self.label_pcu_3.setText(_translate("PDL_Sample", "LAN Port"))
        self.label_pcu_4.setText(_translate("PDL_Sample", "USB Resource"))

        self.groupBox_8.setTitle(_translate("PDL_Sample", "SPU"))
        self.btn_connect.setText(_translate("PDL_Sample", "Connect"))
        self.btn_disconnect.setText(_translate("PDL_Sample", "Disconnect"))

