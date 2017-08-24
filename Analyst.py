# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/kwon/Desktop/Analyst.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

import Clustering
import Preprocess


class Ui_MainWindow(object):
    global data
    def file_open(self):
        # read file
        path = QtWidgets.QFileDialog.getOpenFileName()[0]
        # if you select any file
        if not path == '':
            try: # if file is
                # preprocessing
                self.data = Preprocess.preprocess(path, True)
            except UnboundLocalError:
                self.data = Preprocess.preprocess(path, False)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setMaximumSize(QtCore.QSize(800, 600))

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(29, 29, 741, 501))
        self.tabWidget.setObjectName("tabWidget")
        self.Summary = QtWidgets.QWidget()
        self.Summary.setObjectName("Summary")
        self.groupBox = QtWidgets.QGroupBox(self.Summary)
        self.groupBox.setGeometry(QtCore.QRect(369, 0, 361, 461))
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayoutWidget_3 = QtWidgets.QWidget(self.groupBox)
        self.horizontalLayoutWidget_3.setGeometry(QtCore.QRect(10, 70, 341, 381))
        self.horizontalLayoutWidget_3.setObjectName("horizontalLayoutWidget_3")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_3)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setSpacing(2)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.graphBox = QtWidgets.QWidget(self.horizontalLayoutWidget_3)
        self.graphBox.setObjectName("graphBox")
        self.horizontalLayout_3.addWidget(self.graphBox)
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.groupBox)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 30, 341, 31))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.checkBoxLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.checkBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.checkBoxLayout.setObjectName("checkBoxLayout")
        self.groupBox_2 = QtWidgets.QGroupBox(self.Summary)
        self.groupBox_2.setGeometry(QtCore.QRect(10, 0, 361, 461))
        self.groupBox_2.setObjectName("groupBox_2")
        self.horizontalLayoutWidget_4 = QtWidgets.QWidget(self.groupBox_2)
        self.horizontalLayoutWidget_4.setGeometry(QtCore.QRect(10, 30, 341, 421))
        self.horizontalLayoutWidget_4.setObjectName("horizontalLayoutWidget_4")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_4)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setSpacing(2)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.dataBox = QtWidgets.QWidget(self.horizontalLayoutWidget_4)
        self.dataBox.setObjectName("dataBox")
        self.horizontalLayout_5.addWidget(self.dataBox)
        self.tabWidget.addTab(self.Summary, "")
        self.Clustering = QtWidgets.QWidget()
        self.Clustering.setObjectName("Clustering")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.Clustering)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(10, 10, 721, 441))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.widget = QtWidgets.QWidget(self.verticalLayoutWidget_2)
        self.widget.setObjectName("widget")
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.widget)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(0, 0, 224, 32))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.comboBox = QtWidgets.QComboBox(self.horizontalLayoutWidget_2)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.horizontalLayout_2.addWidget(self.comboBox)
        self.pushButton = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_2.addWidget(self.pushButton)
        self.verticalLayout_7.addWidget(self.widget)
        self.tabWidget.addTab(self.Clustering, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        #self.statusbar = QtWidgets.QStatusBar(MainWindow)
        #self.statusbar.setObjectName("statusbar")
        #MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menubar.addAction(self.menuFile.menuAction())

        # Text setting
        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        # function setting
        self.functionSetting(self)

    def functionSetting(self, Ui_MainWindow):
        Ui_MainWindow.pushButton.clicked.connect(Ui_MainWindow.on_click)
        Ui_MainWindow.actionOpen.triggered.connect(Ui_MainWindow.file_open)

    def on_click(self):
        clurTech = self.comboBox.currentText()
        if clurTech == 'kmeans':
            attribute = ['초장(cm)', '경경(mm)', '잎길이(cm)', '잎 폭(cm)', '잎 수 (개)']
            case = 0
            ksample, silhouette_score = Clustering.clustering(self.data, attribute, 14, case, 50)

        elif clurTech == 'kmedoid':
            print('kmedoid')

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.groupBox.setTitle(_translate("MainWindow", "Graph"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Data"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Summary), _translate("MainWindow", "Summary"))
        self.comboBox.setItemText(0, _translate("MainWindow", "kmeans"))
        self.comboBox.setItemText(1, _translate("MainWindow", "kmedoid"))
        self.pushButton.setText(_translate("MainWindow", "PushButton"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Clustering), _translate("MainWindow", "Clurstering"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionSave.setText(_translate("MainWindow", "Save"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

