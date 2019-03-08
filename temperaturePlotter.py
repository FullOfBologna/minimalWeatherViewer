from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, QPushButton
from PyQt5.QtGui import QIcon
#******************************************************************
import matplotlib
matplotlib.use("Qt5Agg")
#******************************************************************
from PyQt5 import QtCore
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import random

from PyQt5.QtCore import QDate, QDateTime, QTime
from datetime import datetime, timedelta
import sys
import os
from numpy import arange, sin, pi 


class MyMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget ( as well as a FigureCanvasAgg, etc.) """

    def __init__(self,parent=None, width=5, height = 4, dpi=100):
        fig = Figure(figsize=(width,height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        self.compute_initial_figure()

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        def compute_initial_figure(self):
            pass

class MyStaticMplCanvas(MyMplCanvas):
    """Simple Canvas with Sin Plot"""

    def compute_initial_figure(self):
        t = arange(0.0,3.0, 0.01)
        s = sin(2*pi*t)
        self.axes.plot(t,s)

class MyDynamicMplCanvas(MyMplCanvas):
    """A canvas that updates itself every second with a new plot."""

    def __init__(self, *args, **kwargs):
        MyMplCanvas.__init__(self,*args,**kwargs)
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update_figure)
        timer.start(10)
        self.l = [random.randint(0,10)]
        self.xAxisCounter = -1.0

    def compute_initial_figure(self):
        self.axes.plot([0,1,2,3],[1,2,0,4],'r')

    def update_figure(self):
       """Build a list of 4 random integers between 0 and 10 (both incliusive) """

       lengthOfL = len(self.l)
       self.l.append(self.l[lengthOfL-1] + random.randint(-1000,1005)/1000.0)
       self.xAxisCounter += 1
       if self.xAxisCounter>=100:
#           self.l.pop(0)
           x = arange(0.0,len(self.l),1.0)
           self.axes.set_xlim(self.xAxisCounter-100,self.xAxisCounter)
       elif len(self.l)>=1:
           x = arange(0.0,len(self.l),1.0)
       else:
           x = arange(0.0,1.0,1.0)

       self.axes.plot(x,self.l,'r')
       self.draw()

class ApplicationWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle("Application Main Window")

        self.file_menu = QMenu('&File',self)
        self.file_menu.addAction('&Quit',self.fileQuit,QtCore.Qt.CTRL + QtCore.Qt.Key_Q)

#        self.menuBar().addMenu(self.file_menu)

#        self.help_menu = QMenu('&Help',self)

        self.main_widget = QWidget(self)

        l = QVBoxLayout(self.main_widget)
#        sc = MyStaticMplCanvas(self.main_widget, width=5, height=4, dpi=100)
        dc = MyDynamicMplCanvas(self.main_widget, width=5, height=4, dpi=100)
#        l.addWidget(sc)
        l.addWidget(dc)
        
        l.setContentsMargins(0,0,0,0)

        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)
        
        self.main_widget.setWindowFlags(QtCore.Qt.FramelessWindowHint);

#       self.statusBar().showMessage("All hail matplotlib!",2000)

    def fileQuit(self):
        self.close()

    def closeEvent(self,ce):
        self.fileQuit()

    def about(self):
        QMessageBox.about(self, "About","filler text")
       

qApp = QApplication(sys.argv)

aw = ApplicationWindow()
aw.setWindowTitle("Hello World")
aw.show()
sys.exit(qApp.exec_())
