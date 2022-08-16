import os
import sys

from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import Qt

def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

form = resource_path('main.ui')
form_class = uic.loadUiType(form)[0]

form_word1 = resource_path('word1.ui')
form_word1window = uic.loadUiType(form_word1)[0]

form_word2 = resource_path('word2.ui')
form_word2window = uic.loadUiType(form_word2)[0]

#mainpage
class WindowClass(QMainWindow,QWidget, form_class):
    cus = 0
    border_s = 'border-color: rgb(255,255,182); \nbackground-color: rgb(170, 242, 248);\nborder-style: solid;\nborder-width: 2px;\nborder-radius: 10px;'
    border_b = 'border-color: rgb(170, 242, 248); \nbackground-color: rgb(170, 242, 248);\nborder-style: solid;\nborder-width: 2px;\nborder-radius: 10px;'
    
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.cus=0
        self.label_list=[]
        self.label_list.append(self.label_1)
        self.label_list.append(self.label_2)
        self.label_list.append(self.label_3)
        self.label_list.append(self.label_4)
        self.label_list[self.cus].setStyleSheet(self.border_s)

    def keyReleaseEvent(self,e):
        if e.key() == Qt.Key_W:
            if self.cus > 0:
                self.label_list[self.cus].setStyleSheet(self.border_b)
                self.cus-=1
                self.label_list[self.cus].setStyleSheet(self.border_s)
        elif e.key() == Qt.Key_S:
            if self.cus < 3:
                self.label_list[self.cus].setStyleSheet(self.border_b)
                self.cus+=1
                self.label_list[self.cus].setStyleSheet(self.border_s)
        elif e.key() == Qt.Key_F:
            if self.cus == 0:
                self.second = word1window()    
                self.second.show()              
                self.close()


#분류선택
class word1window(QDialog,QWidget,form_word1window):
    fract_name=[['전체','행동','감정'],['장소','사물']]
    x=0
    y=0
    pos=0 #스크롤 위치
    border_s = 'font: 20pt "AcadEref"; border-color: rgb(255,255,182); \nbackground-color: rgb(170, 242, 248);\nborder-style: solid;\nborder-width: 2px;\nborder-radius: 10px;'
    border_b = 'font: 20pt "AcadEref"; border-color: rgb(170,242,248); \nbackground-color: rgb(170, 242, 248);\nborder-style: solid;\nborder-width: 2px;\nborder-radius: 10px;'


    def __init__(self):
        super(word1window,self).__init__()
        self.initUi()
        self.label_list[0][0].setStyleSheet(self.border_s)
        self.show()

    def initUi(self):
        self.setupUi(self)
        self.label_list=[]
        formlayout = QGridLayout()
        #for index in range(100):
            #formlayout.addRow("button_{}".format(index), QPushButton(str(index)))
        for i in range(len(self.fract_name)):
            row_list=[]
            for j in range(len(self.fract_name[i])):
                label=QLabel(self.fract_name[i][j])
                label.setStyleSheet(self.border_b)
                formlayout.addWidget(label,i,j)
                row_list.append(label)
            self.label_list.append(row_list)
                
        widget = QWidget()
        widget.setLayout(formlayout) 
        self.scrollArea.setWidget(widget)
        self.scrollArea.setWidgetResizable(True)
        
 


    def keyPressEvent(self,e):
        
        if e.key() == Qt.Key_G:
            self.main = WindowClass()    
            self.main.show()
            self.close()
        elif e.key() == Qt.Key_S:
            if self.x < len(self.label_list)-1 and self.y < len(self.label_list[self.x])-1:
                self.label_list[self.x][self.y].setStyleSheet(self.border_b)
                self.x+=1
                self.label_list[self.x][self.y].setStyleSheet(self.border_s)
                if self.pos < 250:
                    self.pos+=50
                    self.scrollArea.verticalScrollBar().setSliderPosition(self.pos);
        elif e.key() == Qt.Key_W:
            if self.x > 0:
                self.label_list[self.x][self.y].setStyleSheet(self.border_b)
                self.x-=1
                self.label_list[self.x][self.y].setStyleSheet(self.border_s)
                if self.pos > 0:
                    self.pos-=20
                    self.scrollArea.verticalScrollBar().setSliderPosition(self.pos);
        elif e.key() == Qt.Key_D:
            if self.y < len(self.label_list[self.x])-1:
                self.label_list[self.x][self.y].setStyleSheet(self.border_b)
                self.y+=1
                self.label_list[self.x][self.y].setStyleSheet(self.border_s)
        elif e.key() == Qt.Key_A:
            if self.y > 0:
                self.label_list[self.x][self.y].setStyleSheet(self.border_b)
                self.y-=1
                self.label_list[self.x][self.y].setStyleSheet(self.border_s)

#단어선택 및 출력
class word2window(QDialog,QWidget,form_word2window):
    fract_name=[['전체','행동','감정'],['장소','사물']]
    x=0
    y=0
    pos=0 #스크롤 위치 
    border_s = 'font: 20pt "AcadEref"; border-color: rgb(255,255,182); \nbackground-color: rgb(170, 242, 248);\nborder-style: solid;\nborder-width: 2px;\nborder-radius: 10px;'
    border_b = 'font: 20pt "AcadEref"; border-color: rgb(170,242,248); \nbackground-color: rgb(170, 242, 248);\nborder-style: solid;\nborder-width: 2px;\nborder-radius: 10px;'


    def __init__(self):
        super(word1window,self).__init__()
        self.initUi()
        self.label_list[0][0].setStyleSheet(self.border_s)
        self.show()

    def initUi(self):
        self.setupUi(self)
        self.label_list=[]
        formlayout = QGridLayout()
        #for index in range(100):
            #formlayout.addRow("button_{}".format(index), QPushButton(str(index)))
        for i in range(len(self.fract_name)):
            row_list=[]
            for j in range(len(self.fract_name[i])):
                label=QLabel(self.fract_name[i][j])
                label.setStyleSheet(self.border_b)
                formlayout.addWidget(label,i,j)
                row_list.append(label)
            self.label_list.append(row_list)
                
        widget = QWidget()
        widget.setLayout(formlayout) 
        self.scrollArea.setWidget(widget)
        self.scrollArea.setWidgetResizable(True)
        
 


    def keyPressEvent(self,e):
        
        if e.key() == Qt.Key_G:
            self.main = WindowClass()    
            self.main.show()
            self.close()
        elif e.key() == Qt.Key_S:
            if self.x < len(self.label_list)-1 and self.y < len(self.label_list[self.x])-1:
                self.label_list[self.x][self.y].setStyleSheet(self.border_b)
                self.x+=1
                self.label_list[self.x][self.y].setStyleSheet(self.border_s)
                if self.pos < 250:
                    self.pos+=50
                    self.scrollArea.verticalScrollBar().setSliderPosition(self.pos);
        elif e.key() == Qt.Key_W:
            if self.x > 0:
                self.label_list[self.x][self.y].setStyleSheet(self.border_b)
                self.x-=1
                self.label_list[self.x][self.y].setStyleSheet(self.border_s)
                if self.pos > 0:
                    self.pos-=20
                    self.scrollArea.verticalScrollBar().setSliderPosition(self.pos);
        elif e.key() == Qt.Key_D:
            if self.y < len(self.label_list[self.x])-1:
                self.label_list[self.x][self.y].setStyleSheet(self.border_b)
                self.y+=1
                self.label_list[self.x][self.y].setStyleSheet(self.border_s)
        elif e.key() == Qt.Key_A:
            if self.y > 0:
                self.label_list[self.x][self.y].setStyleSheet(self.border_b)
                self.y-=1
                self.label_list[self.x][self.y].setStyleSheet(self.border_s)
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()
