# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'guiv4Window.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(887, 870)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.tableView_5 = QtWidgets.QTableView(self.centralwidget)
        self.tableView_5.setObjectName("tableView_5")
        self.gridLayout.addWidget(self.tableView_5, 5, 2, 1, 1)
        self.comboBox_2 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_2.setObjectName("comboBox_2")
        self.gridLayout.addWidget(self.comboBox_2, 3, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 3, 1, 1, 1)
        self.tableView_4 = QtWidgets.QTableView(self.centralwidget)
        self.tableView_4.setObjectName("tableView_4")
        self.gridLayout.addWidget(self.tableView_4, 5, 1, 1, 1)
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.gridLayout.addWidget(self.tableWidget, 2, 0, 1, 1)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout.addWidget(self.pushButton_2, 3, 2, 1, 1)
        self.tableView = QtWidgets.QTableView(self.centralwidget)
        self.tableView.setObjectName("tableView")
        self.gridLayout.addWidget(self.tableView, 2, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setObjectName("comboBox")
        self.gridLayout.addWidget(self.comboBox, 0, 0, 1, 1)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 0, 2, 1, 1)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 1, 1, 1)
        self.tableView_2 = QtWidgets.QTableView(self.centralwidget)
        self.tableView_2.setObjectName("tableView_2")
        self.gridLayout.addWidget(self.tableView_2, 2, 2, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 4, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 1, 1, 1, 1)
        self.tableView_3 = QtWidgets.QTableView(self.centralwidget)
        self.tableView_3.setObjectName("tableView_3")
        self.gridLayout.addWidget(self.tableView_3, 5, 0, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 4, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout.addWidget(self.label_5)
        self.radioButton = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton.setObjectName("radioButton")
        self.horizontalLayout.addWidget(self.radioButton)
        self.radioButton_2 = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton_2.setObjectName("radioButton_2")
        self.horizontalLayout.addWidget(self.radioButton_2)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 2, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_2.addWidget(self.label_8)
        self.radioButton_3 = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton_3.setObjectName("radioButton_3")
        self.horizontalLayout_2.addWidget(self.radioButton_3)
        self.radioButton_4 = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton_4.setObjectName("radioButton_4")
        self.horizontalLayout_2.addWidget(self.radioButton_4)
        self.gridLayout.addLayout(self.horizontalLayout_2, 4, 2, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 887, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_2.setText(_translate("MainWindow", "COM Port Board 2"))
        self.pushButton_2.setText(_translate("MainWindow", "Select"))
        self.label_3.setText(_translate("MainWindow", "LoRa Board Data"))
        self.pushButton.setText(_translate("MainWindow", "Select"))
        self.label.setText(_translate("MainWindow", "COM Port Board 1"))
        self.label_7.setText(_translate("MainWindow", "NEMO Detector Data"))
        self.label_4.setText(_translate("MainWindow", "NEMO Detector Data"))
        self.label_6.setText(_translate("MainWindow", "LoRa Board Data"))
        self.label_5.setText(_translate("MainWindow", "Histogram NEMO"))
        self.radioButton.setText(_translate("MainWindow", "Graph"))
        self.radioButton_2.setText(_translate("MainWindow", "Data"))
        self.label_8.setText(_translate("MainWindow", "Histogram"))
        self.radioButton_3.setText(_translate("MainWindow", "Graph"))
        self.radioButton_4.setText(_translate("MainWindow", "Data"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
