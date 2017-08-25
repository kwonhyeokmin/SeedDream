# -*- coding: utf-8 -*-
# Created by: PyQt5 UI code generator 5.8.2

from PyQt5 import QtCore, QtGui, QtWidgets
from sklearn import preprocessing

import Clustering
import Preprocess
import pandas as pd
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
from sklearn.cluster import KMeans
from matplotlib import pyplot as plt
import pyclust
from scipy.spatial.distance import cdist, pdist

# class for show pandas.DataFrame data.
class PandasModel(QtCore.QAbstractTableModel):
    def __init__(self, df = pd.DataFrame(), parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent=parent)
        self._df = df

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()

        if orientation == QtCore.Qt.Horizontal:
            try:
                return self._df.columns.tolist()[section]
            except (IndexError, ):
                return QtCore.QVariant()
        elif orientation == QtCore.Qt.Vertical:
            try:
                # return self.df.index.tolist()
                return self._df.index.tolist()[section]
            except (IndexError, ):
                return QtCore.QVariant()

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()

        if not index.isValid():
            return QtCore.QVariant()

        return QtCore.QVariant(str(self._df.ix[index.row(), index.column()]))

    def setData(self, index, value, role):
        row = self._df.index[index.row()]
        col = self._df.columns[index.column()]
        if hasattr(value, 'toPyObject'):
            # PyQt4 gets a QVariant
            value = value.toPyObject()
        else:
            # PySide gets an unicode
            dtype = self._df[col].dtype
            if dtype != object:
                value = None if value == '' else dtype.type(value)
        self._df.set_value(row, col, value)
        return True

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self._df.index)

    def columnCount(self, parent=QtCore.QModelIndex()):
        return len(self._df.columns)

    def sort(self, column, order):
        colname = self._df.columns.tolist()[column]
        self.layoutAboutToBeChanged.emit()
        self._df.sort_values(colname, ascending= order == QtCore.Qt.AscendingOrder, inplace=True)
        self._df.reset_index(inplace=True, drop=True)
        self.layoutChanged.emit()

# kmedoid elbow graph
def eblow_kmd(df, n):
    centroids = []
    for k in range(1, n):
        kdata = df.copy()
        kmd = pyclust.KMedoids(n_clusters=k)
        kmd.fit(df.values)
        centroids.append(kmd.centers_)
        kdata['cluster'] = kmd.labels_
    k_euclid = [cdist(df.values, cent) for cent in centroids]
    dist = [np.min(ke, axis=1) for ke in k_euclid]
    wcss = [sum(d ** 2) for d in dist]
    tss = sum(pdist(df.values) ** 2) / df.values.shape[0]
    bss = tss - wcss
    return bss

# kmeans elbow graph
def eblow_k(df, n):
    kMeansVar = []
    for k in range(1, n) :
        kdata = df.copy()
        km = KMeans(n_clusters=k).fit(df.values)
        kMeansVar.append(km)
        kdata['cluster'] = km.labels_
    centroids = [X.cluster_centers_ for X in kMeansVar]
    k_euclid = [cdist(df.values, cent) for cent in centroids]
    dist = [np.min(ke, axis=1) for ke in k_euclid]
    wcss = [sum(d**2) for d in dist]
    tss = sum(pdist(df.values)**2)/df.values.shape[0]
    bss = tss - wcss
    return bss

# Main Window
class Ui_MainWindow(object):
    global data
    def file_open(self):
        # read file
        path = QtWidgets.QFileDialog.getOpenFileName()[0] # file path
        # remove previous checkBox group
        for i in range(self.checkBoxLayout.count()):
            self.checkBoxLayout.itemAt(i).widget().deleteLater()
        for i in range(self.checkBoxLayout_2.count()):
            self.checkBoxLayout_2.itemAt(i).widget().deleteLater()

        # if you select any file
        if not path == '':
            try: # if file is
                # preprocessing
                self.data = Preprocess.preprocess(path, True)
            except UnboundLocalError:
                try:
                    self.data = Preprocess.preprocess(path, False)
                except :
                    print('This file does not support. Please select vaild file.')
                    # add checkbox
            positions = [(i, j) for i in range(int(len(self.data.columns) / 4) + 1) for j in range(4)]
            for position, each in zip(positions, self.data.columns):
                self.checkBox = QtWidgets.QCheckBox(self.horizontalLayoutWidget)
                self.checkBox.setText(each)
                self.checkBoxLayout.addWidget(self.checkBox, *position)

            positions = [(i, j) for i in range(int(len(self.data.columns) / 6) + 1) for j in range(6)]
            for position, each in zip(positions, self.data.columns):
                self.checkBox_2 = QtWidgets.QCheckBox(self.verticalLayoutWidget_3)
                self.checkBox_2.setText(each)
                self.checkBoxLayout_2.addWidget(self.checkBox_2, *position)

            model = PandasModel(self.data)
            self.tableView.setModel(model)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setMaximumSize(QtCore.QSize(800, 600))
        # centralwidget
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        # tabWidget
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(29, 29, 741, 501))
        self.tabWidget.setObjectName("tabWidget")
        # Summary
        self.Summary = QtWidgets.QWidget()
        self.Summary.setObjectName("Summary")
        # groupBox
        self.groupBox = QtWidgets.QGroupBox(self.Summary)
        self.groupBox.setGeometry(QtCore.QRect(345, 0, 370, 460))
        self.groupBox.setObjectName("groupBox")
        self.groupBox_2 = QtWidgets.QGroupBox(self.Summary)
        self.groupBox_2.setGeometry(QtCore.QRect(20, 0, 300, 460))
        self.groupBox_2.setObjectName("groupBox_2")

        self.horizontalLayoutWidget_3 = QtWidgets.QWidget(self.groupBox_2)
        self.horizontalLayoutWidget_3.setGeometry(QtCore.QRect(10, 70, 341, 381))
        self.horizontalLayoutWidget_3.setObjectName("horizontalLayoutWidget_3")

        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_3)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")

        self.graphBox = QtWidgets.QWidget(self.horizontalLayoutWidget_3)
        self.graphBox.setObjectName("graphBox")
        self.horizontalLayout_3.addWidget(self.graphBox)
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.groupBox)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 40, 341, 31))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")

        self.checkBoxLayout = QtWidgets.QGridLayout(self.horizontalLayoutWidget)
        self.checkBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.checkBoxLayout.setObjectName("checkBoxLayout")
        self.horizontalLayoutWidget.setMinimumHeight(140)

        # graph option
        self.graphLayoutWidget = QtWidgets.QWidget(self.groupBox)
        self.graphLayout = QtWidgets.QHBoxLayout(self.graphLayoutWidget)
        self.graphLayout.setObjectName("graphLayout")
        self.graphLayoutWidget.setGeometry(QtCore.QRect(0, 10, 341, 40))

        # plot
        self.fig = plt.Figure()
        self.canvas = FigureCanvas(self.fig)
        self.plotLayoutWidget = QtWidgets.QWidget(self.groupBox)
        self.plotLayoutWidget.setMaximumHeight(260)
        self.plotLayout = QtWidgets.QVBoxLayout(self.plotLayoutWidget)
        self.plotLayout.addWidget(self.canvas)
        self.plotLayoutWidget.setGeometry(QtCore.QRect(1, 200, 370, 300))

        #clustering method comboBox
        self.comboBox = QtWidgets.QComboBox(self.graphLayoutWidget)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.graphLayout.addWidget(self.comboBox)

        self.pushButton_2 = QtWidgets.QPushButton(self.graphLayoutWidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.graphLayout.addWidget(self.pushButton_2)

        self.horizontalLayoutWidget_4 = QtWidgets.QWidget(self.groupBox_2)
        self.horizontalLayoutWidget_4.setGeometry(QtCore.QRect(10, 30, 341, 421))
        self.horizontalLayoutWidget_4.setObjectName("horizontalLayoutWidget_4")
        self.tableView = QtWidgets.QTableView(self.horizontalLayoutWidget_4)

        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_4)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setSpacing(2)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.horizontalLayout_5.addWidget(self.tableView)
        self.horizontalLayoutWidget_4.setMaximumWidth(280)

        # dataBox
        self.dataBox = QtWidgets.QWidget(self.horizontalLayoutWidget_4)
        self.dataBox.setObjectName("dataBox")
        self.horizontalLayout_5.addWidget(self.dataBox)
        self.tabWidget.addTab(self.Summary, "")
        # Clurstering
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

        # checkbox
        self.groupBox_3 = QtWidgets.QGroupBox(self.Clustering)
        self.groupBox_3.setObjectName("groupBox_3")
        self.groupBox_3.setGeometry(QtCore.QRect(10, 0, 710, 460))
        self.verticalLayoutWidget_3 = QtWidgets.QWidget(self.groupBox_3)

        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.groupBox_3)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(0, 0, 224, 32))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayoutWidget_2.setMinimumWidth(300)

        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")

        self.clusterComboBox = QtWidgets.QComboBox(self.horizontalLayoutWidget_2)
        self.clusterComboBox.setObjectName("clusterComboBox")
        self.clusterComboBox.addItem("")
        self.clusterComboBox.addItem("")

        self.horizontalLayout_2.addWidget(self.clusterComboBox)
        self.pushButton = QtWidgets.QPushButton(self.groupBox_3)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_2.addWidget(self.pushButton)

        self.label = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        self.label.setText("k value:")
        self.horizontalLayout_2.addWidget(self.label)

        self.kvalue = QtWidgets.QTextEdit(self.horizontalLayoutWidget_2)
        self.kvalue.setObjectName("kvalue")
        self.kvalue.setMaximumWidth(30)
        self.kvalue.setText("4")
        self.horizontalLayout_2.addWidget(self.kvalue)

        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(10, 25, 680, 100))
        self.checkBoxLayout_2 = QtWidgets.QGridLayout(self.verticalLayoutWidget_3)
        self.checkBoxLayout_2.setContentsMargins(0, 0, 0, 0)
        self.checkBoxLayout_2.setObjectName("checkBoxLayout_2")

        self.horizontalLayoutWidget_5 = QtWidgets.QWidget(self.groupBox_3)
        self.tableView_2 = QtWidgets.QTableView(self.horizontalLayoutWidget_5)
        self.horizontalLayout_6 = QtWidgets.QVBoxLayout(self.horizontalLayoutWidget_5)
        self.horizontalLayout_6.addWidget(self.tableView_2)
        self.horizontalLayoutWidget_5.setGeometry(QtCore.QRect(0, 120, 710, 300))
        self.label_2 = QtWidgets.QLabel(self.horizontalLayoutWidget_5)
        self.horizontalLayout_6.addWidget(self.label_2)

        self.verticalLayout_7.addWidget(self.widget)
        self.tabWidget.addTab(self.Clustering, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
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
        Ui_MainWindow.pushButton_2.clicked.connect(Ui_MainWindow.draw_click)

    def draw_click(self):
        try :
            df = self.data
            self.fig.clf()
            ax = self.fig.add_subplot(111)
            try:
                min_max_scaler = preprocessing.MinMaxScaler()
                if self.comboBox.currentText() == 'histogram':
                    for i in range(self.checkBoxLayout.count()):
                        if self.checkBoxLayout.itemAt(i).widget().isChecked():
                            attribute = self.checkBoxLayout.itemAt(i).widget().text()
                            ax.hist(self.data[str(attribute)], normed=1)
                elif self.comboBox.currentText() == 'scatter plot':
                    attribute = []
                    for i in range(self.checkBoxLayout.count()):
                        if self.checkBoxLayout.itemAt(i).widget().isChecked():
                            attribute.append(self.checkBoxLayout.itemAt(i).widget().text())
                    if len(attribute)==2:
                        ax.scatter(df[attribute[0]], df[attribute[1]], alpha=0.7, s=5)
                    else:
                        print('Please select two attribute.')
                elif self.comboBox.currentText() == 'elbow graph':
                    attribute = []
                    for i in range(self.checkBoxLayout.count()):
                        if self.checkBoxLayout.itemAt(i).widget().isChecked():
                            attribute.append(self.checkBoxLayout.itemAt(i).widget().text())

                    kdata = df[[x for x in attribute]]  # define attribute of clustering
                    x = kdata.values
                    x_scaled = min_max_scaler.fit_transform(x)
                    kdata = pd.DataFrame(x_scaled)

                    bss = eblow_k(kdata, 30)
                    ax.plot(bss)

                ax.grid()
                self.canvas.draw()

            except TypeError:
                print('len() of unsized object')
            except ValueError:
                print('Select another attribute.')
        except AttributeError:
            print('Please input data file.')

    def on_click(self):
        try:
            clurTech = self.clusterComboBox.currentText()
            attribute = []
            for i in range(self.checkBoxLayout.count()):
                if self.checkBoxLayout_2.itemAt(i).widget().isChecked():
                    attribute.append(self.checkBoxLayout_2.itemAt(i).widget().text())

            if clurTech == 'kmeans':
                case = 0
            elif clurTech == 'kmedoid':
                case = 1
            kvalue = self.kvalue.toPlainText()  # k value
            ksample, silhouette_score = Clustering.clustering(self.data, attribute, int(kvalue), case, 50)
            self.label_2.setText('silhouette score :' + str(silhouette_score))

            model = PandasModel(ksample)
            self.tableView_2.setModel(model)
        except AttributeError: # if there is no data for clustering
            print('Please input data.')

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.groupBox.setTitle(_translate("MainWindow", "Graph"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Data"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Summary), _translate("MainWindow", "Summary"))
        self.comboBox.setItemText(0, _translate("MainWindow", "histogram"))
        self.comboBox.setItemText(1, _translate("MainWindow", "scatter plot"))
        self.comboBox.setItemText(2, _translate("MainWindow", "elbow graph"))
        self.clusterComboBox.setItemText(0, _translate("MainWindow", "kmeans"))
        self.clusterComboBox.setItemText(1, _translate("MainWindow", "kmedoid"))

        self.pushButton.setText(_translate("MainWindow", "Clustering"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Clustering), _translate("MainWindow", "Clurstering"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.pushButton_2.setText(_translate("MainWindow", "Draw"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

