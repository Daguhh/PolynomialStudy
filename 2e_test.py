"""
================
Embedding In QT5
================

Simple Qt5 application embedding Matplotlib canvases

Copyright (C) 2005 Florent Rougon
              2006 Darren Dale
              2015 Jens H Nielsen

This file is an example program for Matplotlib. It may be used and
modified with no restriction; raw copies as well as modified versions
may be distributed without limitation.
"""

import sys
import os
import random
import matplotlib
# Make sure that we are using QT5

from collections import deque
matplotlib.use('Qt5Agg')
# Uncomment this line before running, it breaks sphinx-gallery builds
from PyQt5 import QtCore, QtWidgets

from numpy import arange, sin, pi
import numpy as np
import numpy.polynomial.polynomial as nppol
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar



from matplotlib.figure import Figure

progname = os.path.basename(sys.argv[0])
progversion = "0.1"

from MainWindow import Ui_MainWindow


class MyMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        #self.compute_initial_figure()

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self):
        pass


class MyStaticMplCanvas(MyMplCanvas):
    """Simple canvas with a sine plot."""

    def compute_initial_figure(self):
        t = arange(0.0, 3.0, 0.01)
        s = sin(2*pi*t)
        self.axes.plot(t, s)


class MyDynamicMplCanvas(MyMplCanvas):
    """A canvas that updates itself every second with a new plot."""

    def __init__(self, *args, **kwargs):
        MyMplCanvas.__init__(self, *args, **kwargs)
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update_figure)
        timer.start(1000)

    def compute_initial_figure(self):
        self.axes.plot([0, 1, 2, 3], [1, 2, 0, 4], 'r')

    def update_figure(self):
        # Build a list of 4 random integers between 0 and 10 (both inclusive)
        l = [random.randint(0, 10) for i in range(4)]
        self.axes.cla()
        self.axes.plot([0, 1, 2, 3], l, 'r')
        self.draw()

class PolynomeMplCanvas(MyMplCanvas):
    """A canvas that updates itself every second with a new plot."""

    def __init__(self, *args, **kwargs):
        MyMplCanvas.__init__(self, *args, **kwargs)
        #timer = QtCore.QTimer(self)
        #timer.timeout.connect(self.update_figure)
        #timer.start(1000)

    def compute_initial_figure(self):
        x = np.linspace(-20, 20, 40)
        y = x**2 + x + 1
        self.axes.plot(x,y)
        self.axes.set_xlim(-7,7)
        self.axes.set_ylim(-50,50)
        self.axes.grid()

        self.a=1
        self.b=1
        self.c=1

    def set_param(self,a,b,c):
        self.a=a
        self.b=b
        self.c=c

    def update_figure(self):
        # Build a list of 4 random integers between 0 and 10 (both inclusive)

        a=self.a
        b=self.b
        c=self.c

        x = np.linspace(-20, 20, 100)
        y = a*x**2 + b*x + c

        self.axes.cla()
        self.axes.plot(x, y)
        self.axes.grid()
        self.axes.set_xlim(-7,7)
        self.axes.set_ylim(-50,50)
        self.draw()

class PolyMplCanvas(MyMplCanvas):
    """A canvas that updates itself every second with a new plot."""


    def __init__(self, *args, **kwargs):
        #MyMplCanvas.__init__(self, *args, **kwargs)
        super().__init__()


        self.fig_list = []
        self.figures_dct = {
            'ax2+bx+c' : (1,1,1),
            'ax2+bx'   : (0,1,1),
            'ax2+c'    : (1,0,1),
            'ax2'      : (0,0,1),
            'bx+c'     : (1,1,0),
            'bx'       : (0,1,0),
            'c'        : (1,0,0),
        }
        for k, v in self.figures_dct.items():
            self.figures_dct[k] = FigFig(self.axes, mask=v)
            self.fig_list.append(self.figures_dct[k])

        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update_figures)
        timer.start(1000)
        timer.setInterval(100)


    def show_plot(self, name, val):
        self.figures_dct[name].isShow = val
        if val == False:
            self.figures_dct[name].clear_figs()
        #self.fct = self.setFct(1,1,1)

    def set_params(self, *params):
        for fig in self.fig_list:
            fig.set_param(*params)


    def update_figures(self):
        #self.update_figure()
        for fig in self.fig_list:
            if fig.isShow:
                fig.update_figure()
        self.axes.set_xlim(-7,7)
        self.axes.set_ylim(-50,50)
        self.axes.grid(True)
        self.draw()

    def get_trace_buffer_size(self):
        size = self.fig_list[0].max_buffer
        return size

    def change_trace_buffer_size_4_all(self, max_buffer):

        for fig in self.fig_list:
            fig.clear_figs()
            print(f'new buffer = {max_buffer}')
            fig.max_buffer = max_buffer

class FigFig:

    @staticmethod
    def def_polyfct(*params):
        def poly(x):
            return nppol.polyval(x, params)
        return poly

    def __init__(self, axes, mask=(1,1,1)):
        self.axes = axes
        self.plot1 = list()
        self.mask = np.array(mask)
        self.setFct(1,1,1)
        self.isShow = False
        self.max_buffer = 30
        pass

    def setFct(self, *params):
        p = np.array(params) * self.mask
        self.fct = FigFig.def_polyfct(*p)
#        self.fct2 = PolyMplCanvas.def_polyfct(*params[:-1])

    def set_param(self, *params):
        self.setFct(*params)


    def compute_initial_figure(self):
        x = np.linspace(-20, 20, 40)
        y = self.fct(x)

        self.axes.plot(x,y)
        self.axes.set_xlim(-7,7)
        self.axes.set_ylim(-50,50)
        self.axes.grid(True)

    def update_figure(self):

        x = np.linspace(-20, 20, 100)
        y = self.fct(x)

#        max_buffer = 10
#        if len(self.axes.get_lines()) > max_buffer:
#            self.axes.get_lines().pop(0).remove()
#        for i, l in enumerate(self.axes.get_lines()):
#            l.set_linestyle('--')
#            c = (1/max_buffer)*(max_buffer-i)
#            l.set_color((c,c,c))
#
        max_buffer = self.max_buffer
        if len(self.plot1) > max_buffer:
            self.plot1.pop(0).remove()
        for i, l in enumerate(self.plot1):
            l.set_linestyle('--')
            c = (1/max_buffer)*(max_buffer-i)
            l.set_color((c,c,c))

        pp = self.axes.plot(x, y, 'k')
        self.plot1.append(pp[0])
#        self.axes.set_xlim(-7,7)
#        self.axes.set_ylim(-50,50)
#        self.axes.grid(True)
#        self.draw()

#        max_buffer = 10
#        if len(self.plot2) > max_buffer:
#            self.plot2.pop(0).remove()
#        for i, l in enumerate(self.plot2):
#            l.set_linestyle('--')
#            c = (1/max_buffer)*(max_buffer-i)
#            l.set_color((c,c,0))
#
#        pp = self.axes.plot(x, y2, 'r')
#        self.plot2.append(pp[0])
#        self.axes.set_xlim(-7,7)
#        self.axes.set_ylim(-50,50)
#        self.axes.grid(True)
#        self.draw()
#

    def clear_figs(self):
        while len(self.plot1):
            self.plot1.pop().remove()



class ApplicationWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)

        super(ApplicationWindow, self).__init__()
        self.setupUi(self)

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle("application main window")

 #       self.file_menu = QtWidgets.QMenu('&File', self)
 #       self.file_menu.addAction('&Quit', self.fileQuit,
 #                                QtCore.Qt.CTRL + QtCore.Qt.Key_Q)
 #       self.menuBar().addMenu(self.file_menu)
        self.actionQuitter.setShortcut(QtCore.Qt.CTRL + QtCore.Qt.Key_Q)
        self.actionQuitter.triggered.connect(self.close) #qApp.quit)
#
        self.actionA_propos.triggered.connect(self.about)


        self.function_list_layout = QtWidgets.QGridLayout()
        self.fonction_list_frame.setLayout(self.function_list_layout)
        self.function_list_size = 0

        figures_dct = {
            'ax2+bx+c' : (1,1,1),
            'ax2+bx'   : (0,1,1),
            'ax2+c'    : (1,0,1),
            'ax2'      : (0,0,1),
            'bx+c'     : (1,1,0),
            'bx'       : (0,1,0),
            'c'        : (1,0,0),
        }

        for k in figures_dct.keys():
            self.add_function_to_list(k)

#        self.add_function_to_list('ax2+bx+c')
#        self.add_function_to_list('ax2+bx')
#        self.add_function_to_list('ax2+c')
#        self.add_function_to_list('bx+c')
#        self.add_function_to_list('ax2')
#        self.add_function_to_list('bx')
#        self.add_function_to_list('c')
#        #self.fonction_list_frame.addWidget()
#        self.help_menu = QtWidgets.QMenu('&Help', self)
#        self.menuBar().addSeparator()
#        self.menuBar().addMenu(self.help_menu)

 #       self.help_menu.addAction('&About', self.about)

  #      self.main_widget = QtWidgets.QWidget(self)

   #     l = QtWidgets.QVBoxLayout(self.main_widget)
        #sc = MyStaticMplCanvas(self.main_widget, width=5, height=4, dpi=100)
        #dc = MyDynamicMplCanvas(self.main_widget, width=5, height=4, dpi=100)
        #self.sc = MyStaticMplCanvas(self.plot_area, width=5, height=4, dpi=100)
        #self.dc = MyDynamicMplCanvas(self.plot_area, width=5, height=4, dpi=100)
        self.tab_var_scene = self.addScene(self.tab_var_frame)
        self.tav_sign_scene = self.addScene(self.tab_sign_frame)

        #self.var_tab_area.resized.connect(self.add_var_table)
        self.add_var_table(self.tab_var_scene)

        self.a = 1
        self.b = 1
        self.c = 1

        self.polyplot = PolyMplCanvas(self.plot_area, width=5, height=4, dpi=100)
        self.addToolBar(QtCore.Qt.TopToolBarArea, NavigationToolbar(self.polyplot, self))
        l = QtWidgets.QVBoxLayout(self.plot_area)
        #l.addWidget(self.sc)
        #l.addWidget(self.dc)
        l.addWidget(self.polyplot)


        #self.main_widget.setFocus()
        #self.setCentralWidget(self.main_widget)

        #self.statusBar().showMessage("All hail matplotlib!", 2000)

        self.a_slider.sliderMoved.connect(self.change_parameter)
        self.b_slider.sliderMoved.connect(self.change_parameter)
        self.c_slider.sliderMoved.connect(self.change_parameter)

        self.actionFrameRate.triggered.connect(self.change_frame_rate)
        self.actionTaille4Trace.triggered.connect(self.change_trace_size)

    def change_frame_rate(self):
        pass

    def change_trace_size(self):
        val = self.get_new_buffer_size_value()
        self.polyplot.change_trace_buffer_size_4_all(val)

    def get_new_buffer_size_value(self, *args):

        buffer_size = self.polyplot.get_trace_buffer_size()
        dialog = AskSpinBox(buffer_size)
        #dialog.exec_()
        if dialog.exec_():
            new_buffer_size = dialog.get_values()
        else:
            new_buffer_size = dialog.cancel()
        return new_buffer_size

    def add_function_to_list(self, fct_name):

        checkbox = QtWidgets.QCheckBox(fct_name)
        #label = QtWidgets.QLabel(fct_name)
        checkbox.stateChanged.connect(self.toggle_plot_display)

        i = self.function_list_size
        self.function_list_layout.addWidget(checkbox,i,0,1,1)
        #self.function_list_layout.addWidget(label,i,1,1,2)

        self.function_list_size += 1

        return checkbox

    def toggle_plot_display(self, state):


        if state == QtCore.Qt.Checked:
            self.polyplot.show_plot(self.sender().text(), True)
        else:
            self.polyplot.show_plot(self.sender().text(), False)

    def add_var_table(self, scene):

        w, h = scene.width(), scene.height()
        w, h = scene.maframe.width(), scene.maframe.height()

        # H lines
        scene.addLine(0, 0, w, 0)
        scene.addLine(0, h/3, w, h/3)
        scene.addLine(0, h, w, h)

        # V lines
        scene.addLine(0, 0, 0, h)
        scene.addLine(w/6, 0, w/6, h)
        scene.addLine(w, 0, w, h)

    def addScene(self, frame):

        tab_var_layout = QtWidgets.QHBoxLayout(frame)
        scene = QtWidgets.QGraphicsScene()
        rect = (0, 0, frame.width(), frame.height())
        ##scene.setSceneRect(*rect)
        #scene.setSceneRect(frame.sceneRect())
        #scene.addText("Hello, world!")
        view = QtWidgets.QGraphicsView(scene)
        view.show()
        tab_var_layout.addWidget(view)
        frame.setLayout(tab_var_layout)
        #view.setSceneRect(*frame.frameRect().getRect())
        view.fitInView(*frame.frameRect().getRect())

        scene.maframe = frame

        return scene
       # self.scene = MyGraphicScene(self.layout)

       # self.view =QtWidgets.QGraphicsView(self.scene)
       # self.view.setScene(self.scene)
       # self.view.setCacheMode(QtWidgets.QGraphicsView.CacheBackground)
       # self.view.setMouseTracking(True)

       # self.layout.addWidget(self.view)



    def change_parameter(self):
        sender_name = self.sender().objectName()
        val = self.sender().value()
        if sender_name[0] == 'a':
            self.a_label.setText(f'a = {val}')
            self.a_label.setAlignment(QtCore.Qt.AlignCenter)
            self.a = int(val)
        elif sender_name[0] == 'b':
            self.b_label.setText(f'b = {val}')
            self.b_label.setAlignment(QtCore.Qt.AlignCenter)
            self.b = int(val)
        elif sender_name[0] == 'c':
            self.c_label.setText(f'c = {val}')
            self.c_label.setAlignment(QtCore.Qt.AlignCenter)
            self.c = int(val)

        self.polyplot.set_params(self.c, self.b, self.a)
        self.polyplot.update_figures()

    def fileQuit(self):
        self.close()

    def closeEvent(self, ce):
        self.fileQuit()

    def about(self):
        pass


class AskSpinBox(QtWidgets.QDialog):

    def __init__(self, val):
        super(QtWidgets.QDialog, self).__init__()
        self.layout = QtWidgets.QGridLayout(self) #QVBoxLayout(self)


        self.spinbox = QtWidgets.QSpinBox()
        self.spinbox.setRange(1,60)
        self.spinbox.setValue(val)
        self.layout.addWidget(self.spinbox, 1, 1, 1, 2)

        ok_btn = QtWidgets.QPushButton("Ok")
        ok_btn.clicked.connect(self.accept)

        cancel_btn = QtWidgets.QPushButton("Cancel")
        cancel_btn.clicked.connect(self.close)

        self.layout.addWidget(cancel_btn, 2, 1)
        self.layout.addWidget(ok_btn, 2, 2)

    def get_values(self):

        val = int(self.spinbox.value())
        return val

    def cancel(self):
        return 0

qApp = QtWidgets.QApplication(sys.argv)

aw = ApplicationWindow()
aw.setWindowTitle("%s" % progname)
aw.show()
sys.exit(qApp.exec_())
aw.exec_()
