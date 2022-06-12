import sys
from PyQt5 import QtWidgets, QtSql
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QAbstractItemView
from copy import deepcopy

import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision
import torchvision.datasets as dset
import torchvision.transforms as transforms
import torch.optim as optim
import torchvision.models as models
import PIL.Image as Image
import numpy as np
import threading
import cv2
import os
import time
import subprocess
import locale
import codecs


from 变换 import Ui_change
from 历史 import Ui_video
from 主界面 import Ui_main
from 关于 import Ui_infor


from PyQt5 import QtCore, QtGui
import pymssql

import tkinter as tk
from tkinter.filedialog import *
from PIL import Image


class opmain(QtWidgets.QMainWindow):

    def __init__(self):
        super(opmain, self).__init__()

        self.ui = Ui_main()  #  这句话是实例化类
        self.ui.setupUi(self)  #  这句话相当于设置控件
        QtWidgets.QWidget.__init__(self)
        self.ui = Ui_main()
        self.ui.setupUi(self)

    def open(self):  # 被调用的类需要再编写一个open函数
        # self.setGeometry(300, 300, 300, 220)
        self.setWindowTitle('人像动漫化')
        # self.move(300, 300)
        self.setWindowIcon(QIcon('图标.ico'))
        self.showFullScreen()
    def warn(self,str):
        reply = QtWidgets.QMessageBox.warning(self, '警告', str)

class opchange(QtWidgets.QMainWindow):

    def __init__(self):
        self.t=0
        self.ch=0
        super(opchange, self).__init__()
        self.ui = Ui_change()  #  这句话是实例化类
        self.timer_camera = QTimer()
        self.ui.setupUi(self)  #  这句话相当于设置控件
        QtWidgets.QWidget.__init__(self)
        self.ui = Ui_change()
        self.ui.setupUi(self)
        self.type=0
        self.filepath=''

    def open(self):  # 被调用的类需要再编写一个open函数
        # self.setGeometry(300, 300, 300, 220)
        self.setWindowTitle('人像动漫化')
        # self.move(300, 300)
        self.setWindowIcon(QIcon('图标.ico'))
        self.showFullScreen()
        self.list()

    def warn(self,str):
        reply = QtWidgets.QMessageBox.warning(self, '警告', str)

    def clickshow(self):
        self.ch=0
        root = Tk()
        root.withdraw()
        self.filepath = askopenfilename()
        self.ch=0
        if self.filepath != None:
            if self.filepath[-4:] in [".mp4", ".flv", ".avi", ".mkv"]:
                self.t=1
                self.cap = cv2.VideoCapture(self.filepath)
                self.type=1
                self.slotStart()
            elif self.filepath[-4:] in [".jpg", ".png", ".bmp"] or self.filepath[-5:] in [".tiff"]:
                self.slotStop()
                self.ui.show.setPixmap(QPixmap(self.filepath))
                self.ui.show.setScaledContents(True)
                self.type=2
                self.t=0
            elif self.filepath!='':
                self.warn('仅支持图片和视频格式')
                self.type=0
        self.ui.address.setText(self.filepath)
        self.ui.address.setWordWrap(True)

    def list(self):
        import os
        files = os.listdir('model')  # 得到文件夹下的所有文件名称
        if files=='':
            files='无'

        slm = QStringListModel() # 创建mode
        slm.setStringList(files)  # 将数据设置到model
        self.ui.model.setModel(slm)  ##绑定 listView 和 model

    def warn(self,str):
        reply = QtWidgets.QMessageBox.warning(self, '警告', str)

    def slotStart(self):
        """ Slot function to start the progamme
        """

        self.timer_camera.start(100)
        self.timer_camera.timeout.connect(self.openFrame)
        if self.ch==1:
            self.timer_camera.timeout.connect(self.openFrame2)
    def slotStop(self):
        """ Slot function to stop the programme
        """
        if self.t==0:
            return
        elif self.t==1:
            self.timer_camera.stop()   # 停止计时器
            self.t=2
        else:
            self.timer_camera.start(100)
            self.timer_camera.timeout.connect(self.openFrame)
            if self.ch == 1:
                self.timer_camera.timeout.connect(self.openFrame2)
            self.t=1

    def openFrame(self):
        """ Slot function to capture frame and process it
        """

        ret,frame = self.cap.read()

        if(self.cap.isOpened()):
            ret, frame = self.cap.read()
            if ret:
                gray= cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                gray= cv2.cvtColor(gray, cv2.COLOR_BGR2RGB)

                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                height, width, bytesPerComponent = frame.shape
                bytesPerLine = bytesPerComponent * width

                q_image = QImage(frame.data,  width, height, bytesPerLine,
                                 QImage.Format_RGB888).scaled(self.ui.show.width(), self.ui.show.height())
                self.ui.show.setPixmap(QPixmap.fromImage(q_image))
            else:
                self.cap.release()
                self.timer_camera.stop()   # 停止计时器

    def openFrame2(self):
        """ Slot function to capture frame and process it
        """

        ret,frame = self.cap2.read()

        if(self.cap2.isOpened()):
            ret, frame = self.cap2.read()
            if ret:
                gray= cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                gray= cv2.cvtColor(gray, cv2.COLOR_BGR2RGB)

                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                height, width, bytesPerComponent = frame.shape
                bytesPerLine = bytesPerComponent * width

                q_image = QImage(frame.data,  width, height, bytesPerLine,
                                 QImage.Format_RGB888).scaled(self.ui.result.width(), self.ui.result.height())
                self.ui.result.setPixmap(QPixmap.fromImage(q_image))
            else:
                self.cap2.release()
                self.timer_camera.stop()   # 停止计时器
    def resultwhat(self):
        if self.type==0:
            self.warn("请先选择文件")
            return
        elif self.type==1:
            tp='video2anime.py'
        else:
            tp='picture.py'



        print('python '+tp+' --checkpoint model/'+self.ui.model.currentText()+' --input_dir '+self.filepath+' --output_dir history --device cpu')
        #result=os.popen('python '+tp+' --checkpoint face_paint_512_v2_0.pt --input_dir '+'test'+' --output_dir history --device cpu')

        self.warn("程序即将运行请稍候，运行过程可能会未响应")
        ps = subprocess.Popen('python '+tp+' --checkpoint model/'+self.ui.model.currentText()+' --input_file '+self.filepath+' --output_dir history --device cpu', stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)

        while True:
            data = ps.stdout.readline()
            if data == b'':
                if ps.poll() is not None:
                    break
            else:
                print(data)


        if self.filepath[-4:] in [".mp4", ".flv", ".avi", ".mkv"]:
            self.ch=1
            self.cap2 = cv2.VideoCapture('history/'+self.filepath.split("/")[-1])
            self.slotStart()
        elif self.filepath[-4:] in [".jpg", ".png", ".bmp"] or self.filepath[-5:] in [ ".tiff"]:
            print('history/'+self.filepath.split("/")[-1])
            self.ui.result.setPixmap(QPixmap('history/'+self.filepath.split("/")[-1]))
            self.ui.result.setScaledContents(True)


class opvideo(QtWidgets.QMainWindow):

    def __init__(self):
        super(opvideo, self).__init__()
        QtWidgets.QWidget.__init__(self)
        self.ui = Ui_video()
        self.ui.setupUi(self)
        self.ui.choices.currentIndexChanged.connect(self.choose)  # 点击下拉列表，触发对应事件
        self.timer_camera = QTimer()
        self.t=0
        self.type=0

    def open(self):  # 被调用的类需要再编写一个open函数
        # self.setGeometry(300, 300, 300, 220)
        self.setWindowTitle('人像动漫化')
        # self.move(300, 300)
        self.setWindowIcon(QIcon('图标.ico'))
        self.showFullScreen()
        self.list()


    def warn(self,str):
        reply = QtWidgets.QMessageBox.warning(self, '警告', str)

    def list(self):
        import os
        files = os.listdir('history')  # 得到文件夹下的所有文件名称
        if files=='':
            files='无'
        else:
            files=['请选择']+files
        slm = QStringListModel() # 创建mode
        slm.setStringList(files)  # 将数据设置到model
        self.ui.choices.setModel(slm)  ##绑定 listView 和 model

    def choose(self):

        if self.ui.choices.currentText()=='无' or self.ui.choices.currentText()=='未选择':

            return
        else:
            if self.ui.choices.currentText()[-3:] == 'mp4' or self.ui.choices.currentText()[-3:] == 'avi':
                self.type=1
                self.t = 1
                self.cap = cv2.VideoCapture('history/'+self.ui.choices.currentText())
                self.slotStart()
            else:
                if self.type==1:
                    self.cap.release()
                    self.timer_camera.stop()  # 停止计时器
                self.type=2
                self.ui.show.setPixmap(QPixmap('history/'+self.ui.choices.currentText()))
                self.ui.show.setScaledContents(True)



    def slotStart(self):
        """ Slot function to start the progamme
        """

        self.timer_camera.start(100)
        self.timer_camera.timeout.connect(self.openFrame)

    def slotStop(self):
        """ Slot function to stop the programme
        """
        if self.t==0 or self.type==2 or self.type==0:
            return
        elif self.t==1:
            self.timer_camera.stop()   # 停止计时器
            self.t=2
        else:
            self.timer_camera.start(100)
            self.timer_camera.timeout.connect(self.openFrame)
            self.t=1

    def openFrame(self):
        """ Slot function to capture frame and process it
        """

        ret,frame = self.cap.read()
        if(self.cap.isOpened()):
            ret, frame = self.cap.read()
            if ret:
                gray= cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                gray= cv2.cvtColor(gray, cv2.COLOR_BGR2RGB)

                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                height, width, bytesPerComponent = frame.shape
                bytesPerLine = bytesPerComponent * width

                q_image = QImage(frame.data,  width, height, bytesPerLine,
                                 QImage.Format_RGB888).scaled(self.ui.show.width(), self.ui.show.height())
                self.ui.show.setPixmap(QPixmap.fromImage(q_image))
            else:
                self.cap.release()
                self.timer_camera.stop()   # 停止计时器



class opinfor(QtWidgets.QMainWindow):

    def __init__(self):
        super(opinfor, self).__init__()

        self.ui = Ui_infor()  #  这句话是实例化类

        self.ui.setupUi(self)  #  这句话相当于设置控件
        QtWidgets.QWidget.__init__(self)
        self.ui = Ui_infor()
        self.ui.setupUi(self)

    def open(self):  # 被调用的类需要再编写一个open函数
        # self.setGeometry(300, 300, 300, 220)
        self.setWindowTitle('人像动漫化')
        # self.move(300, 300)
        self.setWindowIcon(QIcon('图标.ico'))
        self.show()
    def warn(self,str):
        reply = QtWidgets.QMessageBox.warning(self, '警告', str)





if __name__ == '__main__':
    image_size = (1440, 810)
    data_transform = transforms.Compose([
        transforms.RandomHorizontalFlip(),
        transforms.Resize(image_size),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
    ])
    #train_data = dset.ImageFolder(root="train", transform=data_transform)
    #model = torch.load('resnext101_92.5.pkl', map_location='cpu')
    #model.eval()


    app = QtWidgets.QApplication(sys.argv)

    change=opchange()
    video=opvideo()
    main=opmain()
    infor=opinfor()

    main.open()

    change.ui.showwhat.clicked.connect(change.clickshow)
    change.ui.resultwhat.clicked.connect(change.resultwhat)
    change.ui.stop.clicked.connect(change.slotStop)
    change.ui.back.clicked.connect(main.open)
    change.ui.back.clicked.connect(change.close)

    main.ui.video.clicked.connect(video.open)
    main.ui.change.clicked.connect(change.open)

    video.ui.back.clicked.connect(main.open)
    video.ui.back.clicked.connect(video.close)
    video.ui.stop.clicked.connect(video.slotStop)

    infor.ui.close.clicked.connect(infor.close)

    main.ui.closesys.clicked.connect(main.close)

    main.ui.infor.clicked.connect(infor.open)
    sys.exit(app.exec_())