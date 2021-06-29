"""
In this example, we demonstrate how to create simple camera viewer using Opencv3 and PyQt5

Author: Berrouba.A
Last edited: 21 Feb 2018
"""

# import system module
import sys

# import some PyQt5 modules
from PyQt5.QtWidgets import QApplication, QProgressBar
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QImage, QPaintDevice, QPainter
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QRect, QTimer

# import Opencv module
import cv2
# import libraries useb by lumenera camera
import time
from lucam import Lucam
lucam = Lucam(1)

#import the libraries for Baseline of the Telescope

from alpaca import Telescope
scope=Telescope('127.0.0.1:11111',0)

# behavior of the program

from ui_main_window import *

#create popup window
class MyPopup(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.progressbar()

    def progressbar(self):
        self.pbar=QProgressBar(self)
        self.pbar.setGeometry(30,40,200,25)
        self.setGeometry(300,300,280,170)
        self.setWindowTitle("Capturando... ")
        self.pbar.show()


class MainWindow(QWidget):
    # class constructor
    def __init__(self):
        # call QWidget constructor
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # create a timer
        self.timer = QTimer()
        self.timer2 = QTimer()
        # set timer timeout callback function
        self.timer.timeout.connect(self.viewCam)
        self.timer2.timeout.connect(self.viewCam2)
        # set control_bt callback clicked  function
        self.ui.control_bt.clicked.connect(self.controlTimer)
        self.ui.control_bt2.clicked.connect(self.controlTimer2)
        self.w=None


    # view camera
    def viewCam(self):
        # read image in BGR format
        ret, image = self.cap.read()
        # convert image to RGB format
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # image= cv2.cvtColor(image,cv2.COLOR_RGB2HSV)
    
        # get image infos
        height, width, channel = image.shape
        step = channel * width
        # create QImage from image
        qImg = QImage(image.data, width, height, step, QImage.Format_RGB888)
        # show image in img_label
        self.ui.image_label.setPixmap(QPixmap.fromImage(qImg))
    #view Camera2
    def viewCam2(self):
        # n = numero de Fotos que se quiere
        n = 5
        scope.findhome()
        print('im at home')
        for counter in range (n) :
            # Creating a Counter
            print(counter)
            #moving the scope
            #scope.abortslew()
            if scope.connected():
                # Taking the snapshot
                capture = lucam.TakeSnapshot()
                # Saving the SnapShot
                lucam.SaveImage(capture, 'az'+str(scope.azimuth())+'alt'+str(scope.altitude())+'.jpg')
                #move the base
                time.sleep(0.5)
                scope.moveaxis(1,1)
                time.sleep(0.5)
                scope.abortslew()
                self.w.pbar.setValue(counter*100/4)
            else:
                print('No está conectado el Telescopio')
            if counter==4:
                self.timer2.stop()
                self.cap2.release()
                self.ui.control_bt2.setText("Captura finalizada")
                time.sleep(1)
                self.w.destroy()
                self.ui.control_bt2.setText("Tomar Captura")
        return
            
        


    # start/stop timer
    def controlTimer(self):
        # if timer is stopped
        if not self.timer.isActive():
            # create video capture
            self.cap = cv2.VideoCapture(1)
            # start timer
            self.timer.start(20)
            # update control_bt text
            self.ui.control_bt.setText("Stop")
        # if timer is started
        else:
            # stop timer
            self.timer.stop()
            # release video capture
            self.cap.release()
            # update control_bt text
            self.ui.control_bt.setText("Start")
            
    def controlTimer2(self):
        # if timer is stopped
        if not self.timer2.isActive():
            # create video capture
            self.cap2 = cv2.VideoCapture(2)
            # start timer
            self.timer2.start(20)
            # update control_bt text
            self.ui.control_bt2.setText("Capturando")
            self.w = MyPopup()
            self.w.show()

        # if timer is started
        else:
            # stop timer
            self.timer2.stop()
            # release video capture
            self.cap2.release()
            # update control_bt text
            self.ui.control_bt2.setText("Tomar Captura")

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # create and show mainWindow
    mainWindow = MainWindow()
    mainWindow.show()

    sys.exit(app.exec_())