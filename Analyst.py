# -*- coding: utf-8 -*-
# Created by: PyQt5 UI code generator 5.8.2
from PyQt5 import QtCore, QtWidgets
from sklearn import preprocessing
import Clustering
import Preprocess
import pandas as pd
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
from sklearn.cluster import KMeans
from matplotlib import pyplot as plt
from scipy.spatial.distance import cdist, pdist
import sys

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

# kmeans elbow graph
def eblow_k(df, n):
    kMeansVar = []
    for k in range(1, n) :
        kdata = df.copy()
        km = KMeans(n_clusters=k).fit(df.values)
        kMeansVar.append(km)
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
    # method for file open
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
            # add checkbox(summary)
            positions = [(i, j) for i in range(int(len(self.data.columns) / 4) + 1) for j in range(4)]
            for position, each in zip(positions, self.data.columns):
                self.checkBox = QtWidgets.QCheckBox(self.checkBoxLayoutWidget)
                self.checkBox.setText(each)
                self.checkBoxLayout.addWidget(self.checkBox, *position)
            # add checkbox(clustering)
            positions = [(i, j) for i in range(int(len(self.data.columns) / 6) + 1) for j in range(6)]
            for position, each in zip(positions, self.data.columns):
                self.checkBox_2 = QtWidgets.QCheckBox(self.verticalLayoutWidget_3)
                self.checkBox_2.setText(each)
                self.checkBoxLayout_2.addWidget(self.checkBox_2, *position)
            # show data in DataFrame form on summary tab
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
        self.Summary = QtWidgets.QWidget()
        self.Summary.setObjectName("Summary")
        self.Clustering = QtWidgets.QWidget()
        self.Clustering.setObjectName("Clustering")
        self.tabWidget.addTab(self.Summary, "")
        self.tabWidget.addTab(self.Clustering, "")

        ## Summary Tab
        # groupBox
        self.leftBox_Summary = QtWidgets.QGroupBox(self.Summary)
        self.leftBox_Summary.setGeometry(QtCore.QRect(20, 0, 300, 460))
        self.leftBox_Summary.setObjectName("leftBox_Summary")
        self.rightBox_Summary = QtWidgets.QGroupBox(self.Summary)
        self.rightBox_Summary.setGeometry(QtCore.QRect(345, 0, 370, 460))
        self.rightBox_Summary.setObjectName("rightBox_Summary")

        # left group box
        self.summaryDataLayoutWidget = QtWidgets.QWidget(self.leftBox_Summary)
        self.summaryDataLayoutWidget.setGeometry(QtCore.QRect(10, 70, 341, 381))
        self.summaryDataLayoutWidget.setObjectName("summaryDataLayoutWidget")

        self.tableLayoutWidget = QtWidgets.QWidget(self.leftBox_Summary)
        self.tableLayoutWidget.setGeometry(QtCore.QRect(10, 30, 341, 421))
        self.tableLayoutWidget.setObjectName("tableLayoutWidget")
        self.tableView = QtWidgets.QTableView(self.tableLayoutWidget)

        self.tableLayout = QtWidgets.QHBoxLayout(self.tableLayoutWidget)
        self.tableLayout.setContentsMargins(0, 0, 0, 0)
        self.tableLayout.setSpacing(2)
        self.tableLayout.setObjectName("horizontalLayout_5")
        self.tableLayout.addWidget(self.tableView)
        self.tableLayoutWidget.setMaximumWidth(280)

        # right group box
        # graphLayout
        self.graphLayoutWidget = QtWidgets.QWidget(self.rightBox_Summary)
        self.graphLayout = QtWidgets.QVBoxLayout(self.graphLayoutWidget)
        self.graphLayout.setObjectName("graphLayout")
        self.graphLayoutWidget.setMaximumWidth(375)
        # option box
        self.optionGraphWidget = QtWidgets.QWidget(self.graphLayoutWidget)
        self.optionGraphLayout = QtWidgets.QHBoxLayout(self.optionGraphWidget)
        self.optionGraphLayout.setObjectName("optionGraphLayout")
        self.optionGraphLayout.setContentsMargins(0, 10, 0, 0)
        self.graphLayout.addWidget(self.optionGraphWidget)
        # option comboBox
        self.comboBox = QtWidgets.QComboBox(self.optionGraphWidget)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.optionGraphLayout.addWidget(self.comboBox)
        # draw button
        self.drawButton = QtWidgets.QPushButton(self.optionGraphWidget)
        self.drawButton.setObjectName("drawButton")
        self.optionGraphLayout.addWidget(self.drawButton)
        # plot
        self.plotLayoutWidget = QtWidgets.QWidget(self.graphLayoutWidget)
        self.plotLayoutWidget.setObjectName("plotLayoutWidget")
        self.plotLayout = QtWidgets.QVBoxLayout(self.plotLayoutWidget)
        self.plotLayout.setObjectName("plotLayout")
        self.fig = plt.Figure()
        self.canvas = FigureCanvas(self.fig)
        self.plotLayout.addWidget(self.canvas)
        self.plotLayout.setContentsMargins(0, 0, 0, 0)
        self.plotLayoutWidget.setMinimumHeight(250)
        self.plotLayoutWidget.setMaximumHeight(250)
        self.graphLayout.addWidget(self.plotLayoutWidget)
        # Summary checkBox
        self.checkBoxLayoutWidget = QtWidgets.QWidget(self.graphLayoutWidget)
        self.checkBoxLayoutWidget.setObjectName("checkBoxLayoutWidget")
        self.checkBoxLayout = QtWidgets.QGridLayout(self.checkBoxLayoutWidget)
        self.checkBoxLayout.setObjectName("checkBoxLayout")
        self.checkBoxLayoutWidget.setMinimumHeight(100)
        self.checkBoxLayoutWidget.setMaximumHeight(100)
        self.checkBoxLayout.setContentsMargins(0, 0 ,0 ,0)
        self.graphLayout.addWidget(self.checkBoxLayoutWidget)

        ## Clurstering
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.Clustering)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(10, 10, 721, 441))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.widget = QtWidgets.QWidget(self.verticalLayoutWidget_2)
        self.widget.setObjectName("widget")
        # checkbox
        self.centerBox_Clustering = QtWidgets.QGroupBox(self.Clustering)
        self.centerBox_Clustering.setObjectName("centerBox_Clustering")
        self.centerBox_Clustering.setGeometry(QtCore.QRect(10, 0, 710, 460))
        self.verticalLayoutWidget_3 = QtWidgets.QWidget(self.centerBox_Clustering)

        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.centerBox_Clustering)
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
        self.clusteringButton = QtWidgets.QPushButton(self.centerBox_Clustering)
        self.clusteringButton.setObjectName("clusteringButton")
        self.horizontalLayout_2.addWidget(self.clusteringButton)

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

        self.horizontalLayoutWidget_5 = QtWidgets.QWidget(self.centerBox_Clustering)
        self.tableView_2 = QtWidgets.QTableView(self.horizontalLayoutWidget_5)
        self.horizontalLayout_6 = QtWidgets.QVBoxLayout(self.horizontalLayoutWidget_5)
        self.horizontalLayout_6.addWidget(self.tableView_2)
        self.horizontalLayoutWidget_5.setGeometry(QtCore.QRect(0, 120, 710, 300))
        self.label_2 = QtWidgets.QLabel(self.horizontalLayoutWidget_5)
        self.horizontalLayout_6.addWidget(self.label_2)

        self.verticalLayout_7.addWidget(self.widget)
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
        Ui_MainWindow.clusteringButton.clicked.connect(Ui_MainWindow.clustering_click)
        Ui_MainWindow.actionOpen.triggered.connect(Ui_MainWindow.file_open)
        Ui_MainWindow.drawButton.clicked.connect(Ui_MainWindow.draw_click)

    def draw_click(self):
        try :
            df = self.data
            self.fig.clf()
            ax = self.fig.add_subplot(111)
            try:
                min_max_scaler = preprocessing.MinMaxScaler()
                if self.comboBox.currentText() == 'histogram': # histogram
                    for i in range(self.checkBoxLayout.count()):
                        if self.checkBoxLayout.itemAt(i).widget().isChecked():
                            attribute = self.checkBoxLayout.itemAt(i).widget().text()
                            ax.hist(self.data[str(attribute)], normed=1)
                elif self.comboBox.currentText() == 'scatter plot': # scatter plot
                    attribute = [] # attribute for drawing scatter plot
                    for i in range(self.checkBoxLayout.count()):
                        if self.checkBoxLayout.itemAt(i).widget().isChecked():
                            attribute.append(self.checkBoxLayout.itemAt(i).widget().text())
                    if len(attribute)==2: # check attribute
                        ax.scatter(df[attribute[0]], df[attribute[1]], alpha=0.7, s=5)
                        pearson = np.corrcoef(df[attribute[0]], df[attribute[1]])

                    else:
                        print('Please select two attribute.')
                elif self.comboBox.currentText() == 'elbow graph': # elbow graph
                    attribute = []
                    for i in range(self.checkBoxLayout.count()):
                        if self.checkBoxLayout.itemAt(i).widget().isChecked():
                            attribute.append(self.checkBoxLayout.itemAt(i).widget().text())
                    kdata = df[[x for x in attribute]]  # define attribute of clustering
                    x = kdata.values
                    x_scaled = min_max_scaler.fit_transform(x)
                    kdata = pd.DataFrame(x_scaled)
                    bss = eblow_k(kdata, 30)
                    ax.xaxis.set_ticks(np.arange(1, 31, 3))
                    ax.plot(bss)
                ax.grid()
                self.canvas.draw()
            except TypeError:
                print('len() of unsized object')
            except ValueError:
                print('Select another attribute.')
        except AttributeError:
            print('Please input data file.')

    def clustering_click(self):
        try:
            clurTech = self.clusterComboBox.currentText()
            attribute = []
            for i in range(self.checkBoxLayout.count()):
                if self.checkBoxLayout_2.itemAt(i).widget().isChecked():
                    attribute.append(self.checkBoxLayout_2.itemAt(i).widget().text())
            if len(attribute)>1:
                if clurTech == 'kmeans':
                    case = 0
                elif clurTech == 'kmedoid':
                    case = 1
                kvalue = self.kvalue.toPlainText()  # k value
                ksample, silhouette_score = Clustering.clustering(self.data, attribute, int(kvalue), case, 50)
                self.label_2.setText('silhouette score :' + str(silhouette_score))

                model = PandasModel(ksample)
                self.tableView_2.setModel(model)
            else:
                print('Please select one attribute at least.')
        except AttributeError: # if there is no data for clustering
            print('Please input data.')

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.rightBox_Summary.setTitle(_translate("MainWindow", "Graph"))
        self.leftBox_Summary.setTitle(_translate("MainWindow", "Data"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Summary), _translate("MainWindow", "Summary"))
        self.comboBox.setItemText(0, _translate("MainWindow", "histogram"))
        self.comboBox.setItemText(1, _translate("MainWindow", "scatter plot"))
        self.comboBox.setItemText(2, _translate("MainWindow", "elbow graph"))
        self.clusterComboBox.setItemText(0, _translate("MainWindow", "kmeans"))
        self.clusterComboBox.setItemText(1, _translate("MainWindow", "kmedoid"))

        self.clusteringButton.setText(_translate("MainWindow", "Clustering"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Clustering), _translate("MainWindow", "Clurstering"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.drawButton.setText(_translate("MainWindow", "Draw"))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

