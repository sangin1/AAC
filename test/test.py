import os
import sys 
from select import select
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import base64
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt
import ast




form_class = uic.loadUiType("test.ui")[0]

class WindowClass(QMainWindow, form_class) :
    border_b = 'font: 20pt "AcadEref"; border-color: rgb(170,242,248); \nbackground-color: rgb(170, 242, 248);\nborder-style: solid;\nborder-width: 2px;\nborder-radius: 10px;'
    photo=[]
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.label_list=[]
        for i in range(10):
            pix = QPixmap()
            pix.load("img/"+str(i+1)+".jpg")
            pix_re=pix.scaled(300,200,Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
            self.photo.append(pix_re)
        
        formlayout = QGridLayout()

        for i in range(3):
            row_list=[]
            for j in range(2):
                box = QVBoxLayout()
                label=QLabel(str(i)+str(j))
                label.setAlignment(Qt.AlignHCenter)
                
                label2=QLabel(str(i+1)+str(j+1))
                label2.setPixmap(self.photo[j])
                label2.setAlignment(Qt.AlignHCenter)
                
                box.addWidget(label)
                box.addWidget(label2)

                widget = QWidget()
                widget.setLayout(box)
                widget.setStyleSheet(self.border_b)
                
                formlayout.addWidget(widget,i,j)
                row_list.append(widget)
                
            self.label_list.append(row_list)
                

        widget2 = QWidget()
        widget2.setLayout(formlayout) 
        self.scrollArea.setWidget(widget2)
        self.scrollArea.setWidgetResizable(True)

if __name__ == "__main__" :
    app = QApplication(sys.argv) 
    myWindow = WindowClass() 
    myWindow.show()
    app.exec_()
