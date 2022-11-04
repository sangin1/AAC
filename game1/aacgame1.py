import os
import sys
import pygame
from select import select
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import ast
from io import BytesIO

def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

warning_text = resource_path('warning.ui')
warning_window = uic.loadUiType(warning_text)[0]

picquiz = resource_path('game1.ui')
picquiz_window = uic.loadUiType(picquiz)[0]

form = resource_path('mainstart.ui')
form_class = uic.loadUiType(form)[0]

#메시지 창
class warningwindow(QDialog,QWidget,warning_window):
    def __init__(self,text):
        super(warningwindow,self).__init__()
        self.initUi()
        self.label_3.setText(text)
        self.show()

    def initUi(self):
        self.setupUi(self)
        
    def keyReleaseEvent(self,e):
        if e.key() == Qt.Key_F:
            self.close()

class WindowClass(QMainWindow,QWidget, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
            
    def keyReleaseEvent(self,e):
        if e.key() == Qt.Key_F:
            self.second = picgamewindow()    
            self.second.showMaximized()
            self.close()
            
                
#그림퀴즈
class picgamewindow(QDialog,QWidget,picquiz_window):
    border_s = 'font: 20pt "AcadEref"; border-color: rgb(0,21,209); \nbackground-color: rgb(85, 255, 255);\nborder-style: solid;\nborder-width: 2px;\nborder-radius: 10px;'
    border_b = 'font: 20pt "AcadEref"; border-color: rgb(85, 255, 255); \nbackground-color: rgb(85, 255, 255);\nborder-style: solid;\nborder-width: 2px;\nborder-radius: 10px;'
    answer=[2,4,1,1,3,2,4,4,3,2]
    quiz=[['사자','호랑이','치타','고양이'],['열기구','애드벌룬','비행기','비행선'],
          ['코끼리','코뿔소','하마','기린'],['송이버섯','표고버섯','송로버섯','능이버섯'],
          ['요트','수상스키','공기부양정','구명보트'],['도토리','솔방울','호두','잣'],
          ['까치','제비','참새','까마귀'],['라일락','개나리','코스모스','장미'],
          ['고무나무','사랑초','산세베리아','죽순'],['가오리','거북이','이구아나','도롱뇽']]
    photo=[]
    an_num=0
    an_score=0
    label_list=[]
    x=0
    y=0
    def __init__(self):
        super(picgamewindow,self).__init__()
        self.initUi()
        self.show()

    def initUi(self):
        self.setupUi(self)
        self.label_list.clear()
        for i in range(10):
            pix = QPixmap()
            pix.load("img/"+str(i+1)+".jpg")
            pix_re=pix.scaled(400,300,Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
            self.photo.append(pix_re)
        self.pic.setPixmap(self.photo[self.an_num])
        self.pic.setAlignment(Qt.AlignCenter)
        self.now.setText(str(self.an_num+1)+' / 10')
        self.score.setText('점수 '+str(self.an_score))
        label_list1=[]
        label_list2=[]
        label_list1.append(self.an1)
        label_list1.append(self.an2)
        label_list2.append(self.an3)
        label_list2.append(self.an4)
        self.label_list.append(label_list1)
        self.label_list.append(label_list2)
        self.label_list[0][0].setText(self.quiz[self.an_num][0])
        self.label_list[0][1].setText(self.quiz[self.an_num][1])
        self.label_list[1][0].setText(self.quiz[self.an_num][2])
        self.label_list[1][1].setText(self.quiz[self.an_num][3])
        self.label_list[0][0].setStyleSheet(self.border_s)
        
    def keyReleaseEvent(self,e):
        if e.key() == Qt.Key_F:
            if self.an_num >= 9:
                if self.answer[self.an_num] == 1 and self.x == 0 and self.y == 0:
                    self.an_score = self.an_score + 1
                elif self.answer[self.an_num] == 2 and self.x == 0 and self.y == 1:
                    self.an_score = self.an_score + 1
                elif self.answer[self.an_num] == 3 and self.x == 1 and self.y == 0:
                    self.an_score = self.an_score + 1
                elif self.answer[self.an_num] == 4 and self.x == 1 and self.y == 1:
                    self.an_score = self.an_score + 1
                self.second = warningwindow(str(self.an_score)+'점')    
                self.second.exec()
                self.main = WindowClass()    
                self.main.showMaximized()
                self.close()
            else:
                if self.answer[self.an_num] == 1 and self.x == 0 and self.y == 0:
                    self.an_score = self.an_score + 1
                elif self.answer[self.an_num] == 2 and self.x == 0 and self.y == 1:
                    self.an_score = self.an_score + 1
                elif self.answer[self.an_num] == 3 and self.x == 1 and self.y == 0:
                    self.an_score = self.an_score + 1
                elif self.answer[self.an_num] == 4 and self.x == 1 and self.y == 1:
                    self.an_score = self.an_score + 1
                self.an_num = self.an_num+1
                self.pic.setPixmap(self.photo[self.an_num])
                self.pic.setAlignment(Qt.AlignCenter)
                self.now.setText(str(self.an_num+1)+' / 10')
                self.score.setText('점수 '+str(self.an_score))
                self.label_list[0][0].setText(self.quiz[self.an_num][0])
                self.label_list[0][1].setText(self.quiz[self.an_num][1])
                self.label_list[1][0].setText(self.quiz[self.an_num][2])
                self.label_list[1][1].setText(self.quiz[self.an_num][3])
                self.label_list[self.x][self.y].setStyleSheet(self.border_b)
                self.x=0
                self.y=0
                self.label_list[0][0].setStyleSheet(self.border_s)
        elif e.key() == Qt.Key_G:
            self.second = warningwindow(str(self.an_score)+'점')    
            self.second.exec()
            self.second = WindowClass()    
            self.second.showMaximized()
            self.close()
        elif e.key() == Qt.Key_S:
            if self.x == 0 :
                self.label_list[self.x][self.y].setStyleSheet(self.border_b)
                self.x+=1                            
                self.label_list[self.x][self.y].setStyleSheet(self.border_s)
        elif e.key() == Qt.Key_W:
            if self.x == 1:
                self.label_list[self.x][self.y].setStyleSheet(self.border_b)
                self.x-=1
                self.label_list[self.x][self.y].setStyleSheet(self.border_s)                    
        elif e.key() == Qt.Key_D:
            if self.y == 0:
                self.label_list[self.x][self.y].setStyleSheet(self.border_b)
                self.y+=1
                self.label_list[self.x][self.y].setStyleSheet(self.border_s)
        elif e.key() == Qt.Key_A:
            if self.y == 1:
                self.label_list[self.x][self.y].setStyleSheet(self.border_b)
                self.y-=1
                self.label_list[self.x][self.y].setStyleSheet(self.border_s)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.showMaximized()
    app.exec_()
