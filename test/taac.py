import os
import sys
from gtts import gTTS
import pygame
from socket import *
from select import select
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from io import BytesIO
import base64
import ast
from hangul_utils import join_jamos

def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

#ui import
form = resource_path('main.ui')
form_class = uic.loadUiType(form)[0]

form_word1 = resource_path('word1.ui')
form_word1window = uic.loadUiType(form_word1)[0]

form_word2 = resource_path('word2.ui')
form_word2window = uic.loadUiType(form_word2)[0]

login_id = resource_path('loginid.ui')
login_id_window = uic.loadUiType(login_id)[0]

login_pw = resource_path('loginpw.ui')
login_pw_window = uic.loadUiType(login_pw)[0]

warning_text = resource_path('warning.ui')
warning_window = uic.loadUiType(warning_text)[0]

checksum = resource_path('checksum.ui')
checksum_window = uic.loadUiType(checksum)[0]

cud = resource_path('CUD.ui')
cud_window = uic.loadUiType(cud)[0]

picquiz = resource_path('game1.ui')
picquiz_window = uic.loadUiType(picquiz)[0]

wordquiz = resource_path('game2.ui')
wordquiz_window = uic.loadUiType(wordquiz)[0]

selectgame = resource_path('selectgame.ui')
selectgame_window = uic.loadUiType(selectgame)[0]

idnum=0

#mainpage
class WindowClass(QMainWindow,QWidget, form_class):
    global idnum
    cus = 0
    checkupdate = 0
    border_s = 'border-color: rgb(0,21,209); \nbackground-color: rgb(170, 242, 248);\nborder-style: solid;\nborder-width: 2px;\nborder-radius: 10px;'
    border_b = 'border-color: rgb(170, 242, 248); \nbackground-color: rgb(170, 242, 248);\nborder-style: solid;\nborder-width: 2px;\nborder-radius: 10px;'
    idCode = 0   
    def __init__(self):
        super().__init__()
        global idnum
        self.setupUi(self)
        self.cus=0
        self.label_list=[]
        self.label_list.append(self.label_1)
        self.label_list.append(self.label_3)
        self.label_list.append(self.label_4)
        self.label_list.append(self.label_5)
        self.label_list[self.cus].setStyleSheet(self.border_s)
        if idnum == 0:
            self.label_list[2].setText('로그인')
            self.label_list[3].hide()
            self.checkupdate = 0
        elif idnum > 0:
            self.label_list[2].setText('로그아웃')
            self.label_list[3].show()
            self.checkupdate = 1
            
    def keyReleaseEvent(self,e):
        global idnum
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
                self.second.showMaximized()
                self.close()
            if self.cus == 1:
                self.second = selectgamewindow()    
                self.second.showMaximized()
                self.close()
            elif self.cus == 2:
                if idnum == 0:
                    self.login = loginidwindow()   
                    self.login.showMaximized()
                    self.close()
                elif idnum > 0:
                    idnum = 0
                    self.label_list[3].setText('로그인')
                    self.label_list[4].hide()
            elif self.cus == 3 and self.checkupdate == 1:
                self.upin = selectfractwindow()   
                self.upin.showMaximized()
                self.close()

#단어조합게임
class wordquizwindow(QDialog,QWidget, wordquiz_window):
    x = 0
    y = 0
    score=0
    text = ''
    time=180
    word_name = []
    border_s = 'border-color: rgb(0,21,209); \nbackground-color: rgb(170, 242, 248);\nborder-style: solid;\nborder-width: 2px;\nborder-radius: 10px;'
    border_b = 'border-color: rgb(170, 242, 248); \nbackground-color: rgb(170, 242, 248);\nborder-style: solid;\nborder-width: 2px;\nborder-radius: 10px;'
    border_g = 'background-color: rgb(0, 255, 0);\nborder-radius: 30px;'
    border_gs = 'background-color: rgb(0, 255, 0);\nborder-radius: 30px;border-color: rgb(0,21,209);border-style: solid;\nborder-width: 2px'
    border_rs = 'background-color: rgb(255, 69, 69);\nborder-radius: 30px;border-color: rgb(0,21,209);border-style: solid;\nborder-width: 2px'
    border_r = 'background-color: rgb(255, 69, 69);\nborder-radius: 30px;'
  
    def __init__(self):
        super(wordquizwindow,self).__init__()
        self.dataImport()
        self.initUi()
        self.label_list[0][0].setStyleSheet(self.border_s)
        self.show()
        self.timer = QTimer(self)
        self.timer.start(1000)
        self.timer.timeout.connect(self.timeout)
        self.checklist=[]

    def initUi(self):
        self.setupUi(self)
        self.label_list=[]
        formlayout = QGridLayout()
        for i in range(len(self.word_name)):
            row_list=[]
            for j in range(len(self.word_name[i])):        
                label=QLabel(self.word_name[i][j])
                font1 = label.font()
                font1.setPointSize(18)
                label.setFont(font1)
                label.setAlignment(Qt.AlignCenter)
                label.setStyleSheet(self.border_b)
                formlayout.addWidget(label,i,j)
                row_list.append(label)
                
            self.label_list.append(row_list)
        row_list=[]
        row_list.append(self.check)
        row_list.append(self.remove)
        self.label_list.append(row_list)
        widget = QWidget()
        widget.setLayout(formlayout) 
        self.scrollArea.setWidget(widget)
        self.scrollArea.setWidgetResizable(True)

        

    def timeout(self):
        self.time-=1
        if self.time == 0:
            self.second = warningwindow(str(self.score)+'점')    
            self.second.exec()
            self.second = WindowClass()    
            self.second.showMaximized()
            self.close()
        self.time_label.setText("시간 "+str(self.time))
        
        
    def dataImport(self):    
        check=0
        sock.sendall(bytes("--cword--1"+"\n",'UTF-8'))
        data = sock.recv(1000000)
                    
        list2 = []
        a = str(data.decode())
        result = a[:-3]
        r = result.split('-')
        list_row = []
        for i in range(len(r)):
            if check == 7:
                check = 0
                list2.append(list_row)
                list_row=[]              
            list_row.append(r[i])
            check+=1
        list2.append(list_row)
        self.word_name = list2.copy()
        
    def keyReleaseEvent(self,e):
        if e.key() == Qt.Key_G:
            self.second = WindowClass()    
            self.second.showMaximized()
            self.close()
        elif e.key() == Qt.Key_S:
            if self.x < len(self.label_list)-2 and self.y < len(self.label_list[self.x+1]):
                self.label_list[self.x][self.y].setStyleSheet(self.border_b)
                self.x+=1                            
                self.label_list[self.x][self.y].setStyleSheet(self.border_s)
            elif self.x == len(self.label_list)-2:
                self.label_list[self.x][self.y].setStyleSheet(self.border_b)
                self.x+=1
                self.y=0
                self.label_list[self.x][self.y].setStyleSheet(self.border_gs)
        elif e.key() == Qt.Key_W:
            if self.x > 0 and self.x<7:
                self.label_list[self.x][self.y].setStyleSheet(self.border_b)
                self.x-=1              
                self.label_list[self.x][self.y].setStyleSheet(self.border_s)
            elif self.x==7 and self.y==0:
                self.label_list[self.x][self.y].setStyleSheet(self.border_g)
                self.x-=1              
                self.label_list[self.x][self.y].setStyleSheet(self.border_s)
            elif self.x==7 and self.y==1:
                self.label_list[self.x][self.y].setStyleSheet(self.border_r)
                self.x-=1              
                self.label_list[self.x][self.y].setStyleSheet(self.border_s)
        elif e.key() == Qt.Key_D:
            if self.y < len(self.label_list[self.x])-1 and self.x < 7:
                self.label_list[self.x][self.y].setStyleSheet(self.border_b)
                self.y+=1
                self.label_list[self.x][self.y].setStyleSheet(self.border_s)
            elif self.y < len(self.label_list[self.x])-1 and self.x == 7:
                self.label_list[self.x][self.y].setStyleSheet(self.border_g)
                self.y+=1
                self.label_list[self.x][self.y].setStyleSheet(self.border_rs)
        elif e.key() == Qt.Key_A:
            if self.y >0 and self.x<7:
                self.label_list[self.x][self.y].setStyleSheet(self.border_b)
                self.y-=1
                self.label_list[self.x][self.y].setStyleSheet(self.border_s)
            elif self.y >0 and self.x==7:
                self.label_list[self.x][self.y].setStyleSheet(self.border_r)
                self.y-=1
                self.label_list[self.x][self.y].setStyleSheet(self.border_gs)
        elif e.key() == Qt.Key_F:
            if self.x == 7 and self.y == 0:
                checktrue=0
                for i in range(len(self.checklist)):
                    if self.checklist[i]==self.text:
                        checktrue+=1
                if checktrue == 0 :
                    self.checklist.append(self.text)
                    sock.sendall(bytes("--wordCheck--"+self.text+"\n",'UTF-8'))
                    data = sock.recv(1000000)
                    a = str(data.decode())
                    result=a[:-2]
                    if result == '1':
                        self.score+=len(self.text)
                        self.second = warningwindow('있는단어')
                        self.second.exec()
                        self.score_label.setText("점수 "+str(self.score))
                    elif result == '0':
                        self.second = warningwindow('없는단어')    
                        self.second.exec()
                else:
                    self.second = warningwindow('이미입력한단어')    
                    self.second.exec()
            elif self.x == 7 and self.y == 1:
                self.text = ''
                self.text_label.setText(self.text)
            elif self.x < 7:
                self.text += self.word_name[self.x][self.y]
                self.text_label.setText(str(self.text))

                
#게임선택창
class selectgamewindow(QDialog,QWidget, selectgame_window):
    cus = 0
    border_s = 'border-color: rgb(0,21,209); \nbackground-color: rgb(170, 242, 248);\nborder-style: solid;\nborder-width: 2px;\nborder-radius: 10px;'
    border_b = 'border-color: rgb(170, 242, 248); \nbackground-color: rgb(170, 242, 248);\nborder-style: solid;\nborder-width: 2px;\nborder-radius: 10px;'
     
    def __init__(self):
        super(selectgamewindow,self).__init__()
        self.setupUi(self)
        self.cus=0
        self.label_list=[]
        self.label_list.append(self.game1)
        self.label_list.append(self.game2)
        self.label_list[self.cus].setStyleSheet(self.border_s)
        
    def keyReleaseEvent(self,e):
        if e.key() == Qt.Key_A:
            if self.cus > 0:
                self.label_list[self.cus].setStyleSheet(self.border_b)
                self.cus-=1
                self.label_list[self.cus].setStyleSheet(self.border_s)
        elif e.key() == Qt.Key_G:
            self.second = WindowClass()    
            self.second.showMaximized()
            self.close()
        elif e.key() == Qt.Key_D:
            if self.cus < 2:
                self.label_list[self.cus].setStyleSheet(self.border_b)
                self.cus+=1
                self.label_list[self.cus].setStyleSheet(self.border_s)
        elif e.key() == Qt.Key_F:
            if self.cus == 0:
                self.second = picgamewindow()    
                self.second.showMaximized()
                self.close()
            elif self.cus == 1:
                self.upin = wordquizwindow()   
                self.upin.showMaximized()
                self.close()
                
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

#단어수정(입력)
class updateword2window(QDialog,QWidget,login_pw_window):
    word_table = [['ㄱ','ㄴ','ㄷ','ㄹ','ㅁ','ㅂ','ㅅ'],
                  ['ㅇ','ㅈ','ㅊ','ㅋ','ㅌ','ㅍ','ㅎ'],
                  ['ㄲ','ㄸ','ㅃ','ㅆ','ㅉ'],
                  ['ㅏ','ㅓ','ㅗ','ㅜ','ㅡ','ㅣ','ㅒ'],
                  ['ㅑ','ㅕ','ㅛ','ㅠ','ㅐ','ㅔ','ㅖ']]
    cons_all= {'r':'ㄱ', 'R':'ㄲ', 's':'ㄴ', 'e':'ㄷ', 'E':'ㄸ', 'f':'ㄹ', 'a':'ㅁ', 'q':'ㅂ', 'Q':'ㅃ', 't':'ㅅ', 'T':'ㅆ',
           'd':'ㅇ', 'w':'ㅈ', 'W':'ㅉ', 'c':'ㅊ', 'z':'ㅋ', 'x':'ㅌ', 'v':'ㅍ', 'g':'ㅎ','k':'ㅏ', 'o':'ㅐ', 'i':'ㅑ', 'O':'ㅒ', 'j':'ㅓ', 'p':'ㅔ', 'u':'ㅕ', 'P':'ㅖ', 'h':'ㅗ', 'hk':'ㅘ', 'ho':'ㅙ', 'hl':'ㅚ',
           'y':'ㅛ', 'n':'ㅜ', 'b':'ㅠ',  'm':'ㅡ', 'l':'ㅣ'}            
    x=1
    y=0
    text=''
    idText=''
    label_text=''
    word=''
    border_s = 'font: 20pt "AcadEref"; border-color: rgb(0,21,209); \nbackground-color: rgb(170, 242, 248);\nborder-style: solid;\nborder-width: 2px;\nborder-radius: 10px;'
    border_b = 'font: 20pt "AcadEref"; border-color: rgb(170,242,248); \nbackground-color: rgb(170, 242, 248);\nborder-style: solid;\nborder-width: 2px;\nborder-radius: 10px;'
    border_g = 'background-color: rgb(0, 255, 0);\nborder-radius: 30px;'
    border_gs = 'background-color: rgb(0, 255, 0);\nborder-radius: 30px;border-color: rgb(0,21,209);border-style: solid;\nborder-width: 2px'
    border_rs = 'background-color: rgb(255, 69, 69);\nborder-radius: 30px;border-color: rgb(0,21,209);border-style: solid;\nborder-width: 2px'
    border_r = 'background-color: rgb(255, 69, 69);\nborder-radius: 30px;'
    def __init__(self,idText2,w_name):
        super(updateword2window,self).__init__()
        self.initUi()
        self.idText = idText2
        self.word=w_name
        self.label_list[1][0].setStyleSheet(self.border_s)
        self.show()

    def initUi(self):
        self.setupUi(self)
        self.label_2.setText('수정할 단어입력')
        self.label_3.setText('수정')
        self.label_list=[]
        row_list_init = [self.label_3,self.label_4]
        self.label_list.append(row_list_init)
        formlayout = QGridLayout()
        for i in range(5):
            row_list=[]
            for j in range(len(self.word_table[i])):
                label=QLabel(self.word_table[i][j])
                label.setStyleSheet(self.border_b)
                formlayout.addWidget(label,i,j)
                
                row_list.append(label)
            self.label_list.append(row_list)
        self.widget.setLayout(formlayout) 

    def keyReleaseEvent(self,e):
        global idnum
        if e.key() == Qt.Key_G:
            num=0
            self.login = selectfractwindow()   
            self.login.showMaximized()
            self.close()
        elif e.key() == Qt.Key_S:
            if self.x < len(self.label_list)-1 and self.y < len(self.label_list[self.x+1]):
                if self.x==0 and self.y==0:
                    self.label_list[self.x][self.y].setStyleSheet(self.border_g)
                elif self.x==0 and self.y==1:
                    self.label_list[self.x][self.y].setStyleSheet(self.border_r)
                else:
                    self.label_list[self.x][self.y].setStyleSheet(self.border_b)
                self.x+=1
                self.label_list[self.x][self.y].setStyleSheet(self.border_s)
        elif e.key() == Qt.Key_W:
            if self.x > 0 and self.y < len(self.label_list[self.x-1]):
                self.label_list[self.x][self.y].setStyleSheet(self.border_b)
                self.x-=1
                if self.x==0 and self.y==0:
                    self.label_list[self.x][self.y].setStyleSheet(self.border_gs)
                elif self.x==0 and self.y==1:
                    self.label_list[self.x][self.y].setStyleSheet(self.border_rs)
                else:
                    self.label_list[self.x][self.y].setStyleSheet(self.border_s)
        elif e.key() == Qt.Key_D:
            if self.y == len(self.label_list[self.x])-1:
                self.label_list[self.x][self.y].setStyleSheet(self.border_b)
                self.x=0
                self.y=0
                self.label_list[self.x][self.y].setStyleSheet(self.border_gs)
            if self.y < len(self.label_list[self.x])-1:
                if self.x==0:
                    if self.y==0:
                        self.label_list[self.x][self.y].setStyleSheet(self.border_g)
                        self.y+=1
                        self.label_list[self.x][self.y].setStyleSheet(self.border_rs)
                else:
                    self.label_list[self.x][self.y].setStyleSheet(self.border_b)
                    self.y+=1
                    self.label_list[self.x][self.y].setStyleSheet(self.border_s)
        elif e.key() == Qt.Key_A:
            if self.y==0:
                self.label_list[self.x][self.y].setStyleSheet(self.border_b)
                self.x=0
                self.y=0
                self.label_list[self.x][self.y].setStyleSheet(self.border_gs)
            if self.y > 0:
                if self.x==0:
                    if self.y==1:
                        self.label_list[self.x][self.y].setStyleSheet(self.border_r)
                        self.y-=1
                        self.label_list[self.x][self.y].setStyleSheet(self.border_gs)
                else:
                    self.label_list[self.x][self.y].setStyleSheet(self.border_b)
                    self.y-=1
                    self.label_list[self.x][self.y].setStyleSheet(self.border_s)
        elif e.key() == Qt.Key_F:
            if self.x >0:
                self.text = self.word_table[self.x-1][self.y]
                for key, value in self.cons_all.items():
                    if value == self.text:
                        self.label_text += key
                self.label.setText(jamo3(self.label_text))                
            elif self.x == 0 and self.y == 1:
                self.text = ''
                self.label_text = ''
                self.label.setText(self.text)
            elif self.x == 0 and self.y == 0:
                sock.sendall(bytes("--updateword--"+self.idText+"--"+self.label.text()+"--"+str(idnum)+"--"+self.word+"\n",'UTF-8'))
                data = sock.recv(10)
                a = str(data.decode())
                a = a[0:1]
                if int(a) == 0:
                    self.second = warningwindow('실패')    
                    self.second.exec()
                    self.main = selectfractwindow()    
                    self.main.showMaximized()
                    self.close()
                elif int(a) == 1:
                    self.second = warningwindow('수정 성공')    
                    self.second.exec()
                    self.main = selectfractwindow()    
                    self.main.showMaximized()
                    self.close()
                    
#단어수정(선택)
class updatewordwindow(QDialog,QWidget,form_word1window):
    word_name=[]
    fract_code=''
    checksum = 0
    x=0
    y=0
    border_s = 'font: 20pt "AcadEref"; border-color: rgb(0,21,209); \nbackground-color: rgb(170, 242, 248);\nborder-style: solid;\nborder-width: 2px;\nborder-radius: 10px;'
    border_b = 'font: 20pt "AcadEref"; border-color: rgb(170,242,248); \nbackground-color: rgb(170, 242, 248);\nborder-style: solid;\nborder-width: 2px;\nborder-radius: 10px;'

    def __init__(self,f_code,w_name):
        super(updatewordwindow,self).__init__()
        self.word_name = w_name
        self.fract_code = f_code
        self.initUi()
        self.label_list[0][0].setStyleSheet(self.border_s)
        self.label.setText('수정할 단어 선택')
        self.show()

    def initUi(self):
        self.setupUi(self)
        self.label_list=[]
        formlayout = QGridLayout()
        for i in range(len(self.word_name)):
            row_list=[]
            for j in range(len(self.word_name[i])):        
                label=QLabel(self.word_name[i][j])
                label.setAlignment(Qt.AlignCenter)
                label.setStyleSheet(self.border_b)
                formlayout.addWidget(label,i,j)
                row_list.append(label)
                
            self.label_list.append(row_list)
        if 2 < len(self.label_list):
                for i in range(3,len(self.label_list)):
                    for j in range(len(self.label_list[i])):
                        self.label_list[i][j].hide()
                
        widget = QWidget()
        widget.setLayout(formlayout) 
        self.scrollArea.setWidget(widget)
        self.scrollArea.setWidgetResizable(True)
                       
    def keyReleaseEvent(self,e):        
        if e.key() == Qt.Key_G:
            self.second = selectfractwindow()    
            self.second.showMaximized()
            self.close()
        elif e.key() == Qt.Key_S:
            if self.x < len(self.label_list)-1 and self.y < len(self.label_list[self.x+1]):
                self.label_list[self.x][self.y].setStyleSheet(self.border_b)
                self.x+=1

                if len(self.label_list) > 2:
                    for i in range(0,len(self.label_list)):
                        for j in range(len(self.label_list[i])):
                            self.label_list[i][j].hide()

                    for i in range(self.x,self.x+2):
                        if i < len(self.label_list):
                            for j in range(len(self.label_list[i])):
                                self.label_list[i][j].show()
                else:
                    for i in range(2):
                        for j in range(len(self.label_list[i])):
                            self.label_list[i][j].show()
                            
                self.label_list[self.x][self.y].setStyleSheet(self.border_s)
        elif e.key() == Qt.Key_W:
            if self.x > 0:
                self.label_list[self.x][self.y].setStyleSheet(self.border_b)
                self.x-=1
                if self.y >= len(self.label_list[self.x]):
                    self.y = len(self.label_list[self.x])-1                    
               
                self.label_list[self.x][self.y].setStyleSheet(self.border_s)
                for i in range(0,len(self.label_list)):
                    for j in range(len(self.label_list[i])):
                        self.label_list[i][j].hide()
                for i in range(self.x,self.x+2):
                    if i < len(self.label_list):
                        for j in range(len(self.label_list[i])):
                            self.label_list[i][j].show()
                    
        elif e.key() == Qt.Key_D:
            if self.y < len(self.label_list[self.x])-1:
                self.label_list[self.x][self.y].setStyleSheet(self.border_b)
                self.y+=1
                self.label_list[self.x][self.y].setStyleSheet(self.border_s)
        elif e.key() == Qt.Key_A:
                self.label_list[self.x][self.y].setStyleSheet(self.border_b)
                self.y-=1
                self.label_list[self.x][self.y].setStyleSheet(self.border_s)
        elif e.key() == Qt.Key_F:
                self.main = updateword2window(self.fract_code,self.word_name[self.x][self.y])    
                self.main.showMaximized()
                self.close()
                
                    
#단어삭제
class delwordwindow(QDialog,QWidget,form_word1window):
    word_name=[]
    fract_code=''
    checksum = 0
    x=0
    y=0
    border_s = 'font: 20pt "AcadEref"; border-color: rgb(0,21,209); \nbackground-color: rgb(170, 242, 248);\nborder-style: solid;\nborder-width: 2px;\nborder-radius: 10px;'
    border_b = 'font: 20pt "AcadEref"; border-color: rgb(170,242,248); \nbackground-color: rgb(170, 242, 248);\nborder-style: solid;\nborder-width: 2px;\nborder-radius: 10px;'

    def __init__(self,f_code,w_name):
        super(delwordwindow,self).__init__()
        self.word_name = w_name
        self.fract_code = f_code
        self.initUi()
        self.label_list[0][0].setStyleSheet(self.border_s)
        self.label.setText('삭제할 단어 선택')
        self.show()

    def initUi(self):
        self.setupUi(self)
        self.label_list=[]
        formlayout = QGridLayout()
        for i in range(len(self.word_name)):
            row_list=[]
            for j in range(len(self.word_name[i])):        
                label=QLabel(self.word_name[i][j])
                label.setAlignment(Qt.AlignCenter)
                label.setStyleSheet(self.border_b)
                formlayout.addWidget(label,i,j)
                row_list.append(label)
                
            self.label_list.append(row_list)
        if 2 < len(self.label_list):
                for i in range(3,len(self.label_list)):
                    for j in range(len(self.label_list[i])):
                        self.label_list[i][j].hide()
                
        widget = QWidget()
        widget.setLayout(formlayout) 
        self.scrollArea.setWidget(widget)
        self.scrollArea.setWidgetResizable(True)
                       
    def keyReleaseEvent(self,e):
        global idnum
        if e.key() == Qt.Key_G:
            self.second = selectfractwindow()    
            self.second.showMaximized()
            self.close()
        elif e.key() == Qt.Key_S:
            if self.x < len(self.label_list)-1 and self.y < len(self.label_list[self.x+1]):
                self.label_list[self.x][self.y].setStyleSheet(self.border_b)
                self.x+=1

                if len(self.label_list) > 2:
                    for i in range(0,len(self.label_list)):
                        for j in range(len(self.label_list[i])):
                            self.label_list[i][j].hide()

                    for i in range(self.x,self.x+2):
                        if i < len(self.label_list):
                            for j in range(len(self.label_list[i])):
                                self.label_list[i][j].show()
                else:
                    for i in range(2):
                        for j in range(len(self.label_list[i])):
                            self.label_list[i][j].show()
                            
                self.label_list[self.x][self.y].setStyleSheet(self.border_s)
        elif e.key() == Qt.Key_W:
            if self.x > 0:
                self.label_list[self.x][self.y].setStyleSheet(self.border_b)
                self.x-=1
                if self.y >= len(self.label_list[self.x]):
                    self.y = len(self.label_list[self.x])-1                    
               
                self.label_list[self.x][self.y].setStyleSheet(self.border_s)
                for i in range(0,len(self.label_list)):
                    for j in range(len(self.label_list[i])):
                        self.label_list[i][j].hide()
                for i in range(self.x,self.x+2):
                    if i < len(self.label_list):
                        for j in range(len(self.label_list[i])):
                            self.label_list[i][j].show()
                    
        elif e.key() == Qt.Key_D:
            if self.y < len(self.label_list[self.x])-1:
                self.label_list[self.x][self.y].setStyleSheet(self.border_b)
                self.y+=1
                self.label_list[self.x][self.y].setStyleSheet(self.border_s)
        elif e.key() == Qt.Key_A:
                self.label_list[self.x][self.y].setStyleSheet(self.border_b)
                self.y-=1
                self.label_list[self.x][self.y].setStyleSheet(self.border_s)
        elif e.key() == Qt.Key_F:            
                sock.sendall(bytes("--delword--"+self.fract_code+"--"+self.word_name[self.x][self.y]+"--"+str(idnum)+"\n",'UTF-8'))
                data = sock.recv(10)
                a = str(data.decode())
                a = a[0:1]
                if int(a) == 0:
                    self.second = warningwindow('실패')    
                    self.second.exec()
                    self.main = selectfractwindow()    
                    self.main.showMaximized()
                    self.close()
                elif int(a) == 1:
                    self.second = warningwindow('삭제 성공')    
                    self.second.exec()
                    self.main = selectfractwindow()    
                    self.main.showMaximized()
                    self.close()
            
#단어추가
class addwordwindow(QDialog,QWidget,login_pw_window):
    word_table = [['ㄱ','ㄴ','ㄷ','ㄹ','ㅁ','ㅂ','ㅅ'],
                  ['ㅇ','ㅈ','ㅊ','ㅋ','ㅌ','ㅍ','ㅎ'],
                  ['ㄲ','ㄸ','ㅃ','ㅆ','ㅉ'],
                  ['ㅏ','ㅓ','ㅗ','ㅜ','ㅡ','ㅣ','ㅒ'],
                  ['ㅑ','ㅕ','ㅛ','ㅠ','ㅐ','ㅔ','ㅖ']]
    cons_all= {'r':'ㄱ', 'R':'ㄲ', 's':'ㄴ', 'e':'ㄷ', 'E':'ㄸ', 'f':'ㄹ', 'a':'ㅁ', 'q':'ㅂ', 'Q':'ㅃ', 't':'ㅅ', 'T':'ㅆ',
           'd':'ㅇ', 'w':'ㅈ', 'W':'ㅉ', 'c':'ㅊ', 'z':'ㅋ', 'x':'ㅌ', 'v':'ㅍ', 'g':'ㅎ','k':'ㅏ', 'o':'ㅐ', 'i':'ㅑ', 'O':'ㅒ', 'j':'ㅓ', 'p':'ㅔ', 'u':'ㅕ', 'P':'ㅖ', 'h':'ㅗ', 'hk':'ㅘ', 'ho':'ㅙ', 'hl':'ㅚ',
           'y':'ㅛ', 'n':'ㅜ', 'b':'ㅠ',  'm':'ㅡ', 'l':'ㅣ'}            
    x=1
    y=0
    text=''
    idText=''
    label_text=''
    border_s = 'font: 20pt "AcadEref"; border-color: rgb(0,21,209); \nbackground-color: rgb(170, 242, 248);\nborder-style: solid;\nborder-width: 2px;\nborder-radius: 10px;'
    border_b = 'font: 20pt "AcadEref"; border-color: rgb(170,242,248); \nbackground-color: rgb(170, 242, 248);\nborder-style: solid;\nborder-width: 2px;\nborder-radius: 10px;'
    border_g = 'background-color: rgb(0, 255, 0);\nborder-radius: 30px;'
    border_gs = 'background-color: rgb(0, 255, 0);\nborder-radius: 30px;border-color: rgb(0,21,209);border-style: solid;\nborder-width: 2px'
    border_rs = 'background-color: rgb(255, 69, 69);\nborder-radius: 30px;border-color: rgb(0,21,209);border-style: solid;\nborder-width: 2px'
    border_r = 'background-color: rgb(255, 69, 69);\nborder-radius: 30px;'
    def __init__(self,idText2):
        super(addwordwindow,self).__init__()
        self.initUi()
        self.idText = idText2
        self.label_list[1][0].setStyleSheet(self.border_s)
        self.show()

    def initUi(self):
        self.setupUi(self)
        self.label_2.setText('단어입력')
        self.label_3.setText('추가')
        self.label_list=[]
        row_list_init = [self.label_3,self.label_4]
        self.label_list.append(row_list_init)
        formlayout = QGridLayout()
        for i in range(5):
            row_list=[]
            for j in range(len(self.word_table[i])):
                label=QLabel(self.word_table[i][j])
                label.setStyleSheet(self.border_b)
                formlayout.addWidget(label,i,j)
                
                row_list.append(label)
            self.label_list.append(row_list)
        self.widget.setLayout(formlayout) 

    def keyReleaseEvent(self,e):
        global idnum
        if e.key() == Qt.Key_G:
            num=0
            self.login = selectfractwindow()   
            self.login.showMaximized()
            self.close()
        elif e.key() == Qt.Key_S:
            if self.x < len(self.label_list)-1 and self.y < len(self.label_list[self.x+1]):
                if self.x==0 and self.y==0:
                    self.label_list[self.x][self.y].setStyleSheet(self.border_g)
                elif self.x==0 and self.y==1:
                    self.label_list[self.x][self.y].setStyleSheet(self.border_r)
                else:
                    self.label_list[self.x][self.y].setStyleSheet(self.border_b)
                self.x+=1
                self.label_list[self.x][self.y].setStyleSheet(self.border_s)
        elif e.key() == Qt.Key_W:
            if self.x > 0 and self.y < len(self.label_list[self.x-1]):
                self.label_list[self.x][self.y].setStyleSheet(self.border_b)
                self.x-=1
                if self.x==0 and self.y==0:
                    self.label_list[self.x][self.y].setStyleSheet(self.border_gs)
                elif self.x==0 and self.y==1:
                    self.label_list[self.x][self.y].setStyleSheet(self.border_rs)
                else:
                    self.label_list[self.x][self.y].setStyleSheet(self.border_s)
        elif e.key() == Qt.Key_D:
            if self.y == len(self.label_list[self.x])-1:
                self.label_list[self.x][self.y].setStyleSheet(self.border_b)
                self.x=0
                self.y=0
                self.label_list[self.x][self.y].setStyleSheet(self.border_gs)
            if self.y < len(self.label_list[self.x])-1:
                if self.x==0:
                    if self.y==0:
                        self.label_list[self.x][self.y].setStyleSheet(self.border_g)
                        self.y+=1
                        self.label_list[self.x][self.y].setStyleSheet(self.border_rs)
                else:
                    self.label_list[self.x][self.y].setStyleSheet(self.border_b)
                    self.y+=1
                    self.label_list[self.x][self.y].setStyleSheet(self.border_s)
        elif e.key() == Qt.Key_A:
            if self.y==0:
                self.label_list[self.x][self.y].setStyleSheet(self.border_b)
                self.x=0
                self.y=0
                self.label_list[self.x][self.y].setStyleSheet(self.border_gs)
            if self.y > 0:
                if self.x==0:
                    if self.y==1:
                        self.label_list[self.x][self.y].setStyleSheet(self.border_r)
                        self.y-=1
                        self.label_list[self.x][self.y].setStyleSheet(self.border_gs)
                else:
                    self.label_list[self.x][self.y].setStyleSheet(self.border_b)
                    self.y-=1
                    self.label_list[self.x][self.y].setStyleSheet(self.border_s)
        elif e.key() == Qt.Key_F:
            if self.x >0:
                self.text = self.word_table[self.x-1][self.y]
                for key, value in self.cons_all.items():
                    if value == self.text:
                        self.label_text += key
                self.label.setText(jamo3(self.label_text))                
            elif self.x == 0 and self.y == 1:
                self.text = ''
                self.label_text = ''
                self.label.setText(self.text)
            elif self.x == 0 and self.y == 0:
                sock.sendall(bytes("--addword--"+self.idText+"--"+self.label.text()+"--"+str(idnum)+"\n",'UTF-8'))
                data = sock.recv(10)
                a = str(data.decode())
                a = a[0:1]
                if int(a) == 0:
                    self.second = warningwindow('실패')    
                    self.second.exec()
                    self.main = selectfractwindow()    
                    self.main.showMaximized()
                    self.close()
                elif int(a) == 1:
                    self.second = warningwindow('추가 성공')    
                    self.second.exec()
                    self.main = selectfractwindow()    
                    self.main.showMaximized()
                    self.close()
                    
#단어cud선택
class wordCUDwindow(QDialog,QWidget, cud_window):
    cus = 0
    fract_name=[]
    word_name=[]
    fract_code=[]
    x=0
    y=0
    border_s = 'border-color: rgb(0,21,209); \nbackground-color: rgb(170, 242, 248);\nborder-style: solid;\nborder-width: 2px;\nborder-radius: 10px;'
    border_b = 'border-color: rgb(170, 242, 248); \nbackground-color: rgb(170, 242, 248);\nborder-style: solid;\nborder-width: 2px;\nborder-radius: 10px;'
    idCode = 0   
    def __init__(self,f_name,w_name,f_code,x2,y2):
        super(wordCUDwindow,self).__init__()
        self.fract_name = f_name
        self.fract_code = f_code
        self.word_name = w_name
        self.x=x2
        self.y=y2
        self.setupUi(self)
        self.cus=0
        self.label_list=[]
        self.label_list.append(self.label_1)
        self.label_list.append(self.label_2)
        self.label_list.append(self.label_3)
        self.label_list[self.cus].setStyleSheet(self.border_s)
        
    def keyReleaseEvent(self,e):
        if e.key() == Qt.Key_W:
            if self.cus > 0:
                self.label_list[self.cus].setStyleSheet(self.border_b)
                self.cus-=1
                self.label_list[self.cus].setStyleSheet(self.border_s)
        elif e.key() == Qt.Key_G:
            self.second = selectfractwindow()    
            self.second.showMaximized()
            self.close()
        elif e.key() == Qt.Key_S:
            if self.cus < 2:
                self.label_list[self.cus].setStyleSheet(self.border_b)
                self.cus+=1
                self.label_list[self.cus].setStyleSheet(self.border_s)
        elif e.key() == Qt.Key_F:
            if self.cus == 0:
                self.second = addwordwindow(self.fract_code[self.x][self.y])    
                self.second.showMaximized()
                self.close()
            elif self.cus == 1:
                self.upin = updatewordwindow(self.fract_code[self.x][self.y],self.word_name[self.x][self.y])   
                self.upin.showMaximized()
                self.close()
            elif self.cus == 2:
                self.upin = delwordwindow(self.fract_code[self.x][self.y],self.word_name[self.x][self.y])   
                self.upin.showMaximized()
                self.close()
                
#분류수정(입력)
class updatefractwordwindow(QDialog,QWidget,login_pw_window):
    word_table = [['ㄱ','ㄴ','ㄷ','ㄹ','ㅁ','ㅂ','ㅅ'],
                  ['ㅇ','ㅈ','ㅊ','ㅋ','ㅌ','ㅍ','ㅎ'],
                  ['ㄲ','ㄸ','ㅃ','ㅆ','ㅉ'],
                  ['ㅏ','ㅓ','ㅗ','ㅜ','ㅡ','ㅣ','ㅒ'],
                  ['ㅑ','ㅕ','ㅛ','ㅠ','ㅐ','ㅔ','ㅖ']]
    cons_all= {'r':'ㄱ', 'R':'ㄲ', 's':'ㄴ', 'e':'ㄷ', 'E':'ㄸ', 'f':'ㄹ', 'a':'ㅁ', 'q':'ㅂ', 'Q':'ㅃ', 't':'ㅅ', 'T':'ㅆ',
           'd':'ㅇ', 'w':'ㅈ', 'W':'ㅉ', 'c':'ㅊ', 'z':'ㅋ', 'x':'ㅌ', 'v':'ㅍ', 'g':'ㅎ','k':'ㅏ', 'o':'ㅐ', 'i':'ㅑ', 'O':'ㅒ', 'j':'ㅓ', 'p':'ㅔ', 'u':'ㅕ', 'P':'ㅖ', 'h':'ㅗ', 'hk':'ㅘ', 'ho':'ㅙ', 'hl':'ㅚ',
           'y':'ㅛ', 'n':'ㅜ', 'b':'ㅠ',  'm':'ㅡ', 'l':'ㅣ'}            
    x=1
    y=0
    text=''
    idText=''
    label_text=''
    border_s = 'font: 20pt "AcadEref"; border-color: rgb(0,21,209); \nbackground-color: rgb(170, 242, 248);\nborder-style: solid;\nborder-width: 2px;\nborder-radius: 10px;'
    border_b = 'font: 20pt "AcadEref"; border-color: rgb(170,242,248); \nbackground-color: rgb(170, 242, 248);\nborder-style: solid;\nborder-width: 2px;\nborder-radius: 10px;'
    border_g = 'background-color: rgb(0, 255, 0);\nborder-radius: 30px;'
    border_gs = 'background-color: rgb(0, 255, 0);\nborder-radius: 30px;border-color: rgb(0,21,209);border-style: solid;\nborder-width: 2px'
    border_rs = 'background-color: rgb(255, 69, 69);\nborder-radius: 30px;border-color: rgb(0,21,209);border-style: solid;\nborder-width: 2px'
    border_r = 'background-color: rgb(255, 69, 69);\nborder-radius: 30px;'
    def __init__(self,idText2):
        super(updatefractwordwindow,self).__init__()
        self.initUi()
        self.idText = idText2
        self.label_list[1][0].setStyleSheet(self.border_s)
        self.show()

    def initUi(self):
        self.setupUi(self)
        self.label_2.setText('수정할 값 입력')
        self.label_3.setText('수정')
        self.label_list=[]
        row_list_init = [self.label_3,self.label_4]
        self.label_list.append(row_list_init)
        formlayout = QGridLayout()
        for i in range(5):
            row_list=[]
            for j in range(len(self.word_table[i])):
                label=QLabel(self.word_table[i][j])
                label.setStyleSheet(self.border_b)
                formlayout.addWidget(label,i,j)
                
                row_list.append(label)
            self.label_list.append(row_list)
        self.widget.setLayout(formlayout) 

    def keyReleaseEvent(self,e):
        global idnum
        if e.key() == Qt.Key_G:
            num=0
            self.login = selectfractwindow()   
            self.login.showMaximized()
            self.close()
        elif e.key() == Qt.Key_S:
            if self.x < len(self.label_list)-1 and self.y < len(self.label_list[self.x+1]):
                if self.x==0 and self.y==0:
                    self.label_list[self.x][self.y].setStyleSheet(self.border_g)
                elif self.x==0 and self.y==1:
                    self.label_list[self.x][self.y].setStyleSheet(self.border_r)
                else:
                    self.label_list[self.x][self.y].setStyleSheet(self.border_b)
                self.x+=1
                self.label_list[self.x][self.y].setStyleSheet(self.border_s)
        elif e.key() == Qt.Key_W:
            if self.x > 0 and self.y < len(self.label_list[self.x-1]):
                self.label_list[self.x][self.y].setStyleSheet(self.border_b)
                self.x-=1
                if self.x==0 and self.y==0:
                    self.label_list[self.x][self.y].setStyleSheet(self.border_gs)
                elif self.x==0 and self.y==1:
                    self.label_list[self.x][self.y].setStyleSheet(self.border_rs)
                else:
                    self.label_list[self.x][self.y].setStyleSheet(self.border_s)
        elif e.key() == Qt.Key_D:
            if self.y == len(self.label_list[self.x])-1:
                self.label_list[self.x][self.y].setStyleSheet(self.border_b)
                self.x=0
                self.y=0
                self.label_list[self.x][self.y].setStyleSheet(self.border_gs)
            if self.y < len(self.label_list[self.x])-1:
                if self.x==0:
                    if self.y==0:
                        self.label_list[self.x][self.y].setStyleSheet(self.border_g)
                        self.y+=1
                        self.label_list[self.x][self.y].setStyleSheet(self.border_rs)
                else:
                    self.label_list[self.x][self.y].setStyleSheet(self.border_b)
                    self.y+=1
                    self.label_list[self.x][self.y].setStyleSheet(self.border_s)
        elif e.key() == Qt.Key_A:
            if self.y==0:
                self.label_list[self.x][self.y].setStyleSheet(self.border_b)
                self.x=0
                self.y=0
                self.label_list[self.x][self.y].setStyleSheet(self.border_gs)
            if self.y > 0:
                if self.x==0:
                    if self.y==1:
                        self.label_list[self.x][self.y].setStyleSheet(self.border_r)
                        self.y-=1
                        self.label_list[self.x][self.y].setStyleSheet(self.border_gs)
                else:
                    self.label_list[self.x][self.y].setStyleSheet(self.border_b)
                    self.y-=1
                    self.label_list[self.x][self.y].setStyleSheet(self.border_s)
        elif e.key() == Qt.Key_F:
            if self.x >0:
                self.text = self.word_table[self.x-1][self.y]
                for key, value in self.cons_all.items():
                    if value == self.text:
                        self.label_text += key
                self.label.setText(jamo3(self.label_text))                
            elif self.x == 0 and self.y == 1:
                self.text = ''
                self.label_text = ''
                self.label.setText(self.text)
            elif self.x == 0 and self.y == 0:
                sock.sendall(bytes("--updateclass--"+self.idText+"--"+self.label.text()+"--"+str(idnum)+"\n",'UTF-8'))
                data = sock.recv(10)
                a = str(data.decode())
                a = a[0:1]
                if int(a) == 0:
                    self.second = warningwindow('실패')    
                    self.second.exec()
                    self.main = selectfractwindow()    
                    self.main.showMaximized()
                    self.close()
                elif int(a) == 1:
                    self.second = warningwindow('추가 성공')    
                    self.second.exec()
                    self.main = selectfractwindow()    
                    self.main.showMaximized()
                    self.close()
#분류수정선택
class updatefractwindow(QDialog,QWidget,form_word1window):
    fract_name=[]
    fract_code=[]
    checksum = 0
    x=0
    y=0
    border_s = 'font: 20pt "AcadEref"; border-color: rgb(0,21,209); \nbackground-color: rgb(170, 242, 248);\nborder-style: solid;\nborder-width: 2px;\nborder-radius: 10px;'
    border_b = 'font: 20pt "AcadEref"; border-color: rgb(170,242,248); \nbackground-color: rgb(170, 242, 248);\nborder-style: solid;\nborder-width: 2px;\nborder-radius: 10px;'

    def __init__(self,f_name,f_code):
        super(updatefractwindow,self).__init__()
        self.fract_name = f_name
        self.fract_code = f_code
        self.initUi()
        self.label_list[0][0].setStyleSheet(self.border_s)
        self.label.setText('수정할 분류 선택')
        self.show()

    def initUi(self):
        self.setupUi(self)
        self.label_list=[]
        formlayout = QGridLayout()
        for i in range(len(self.fract_name)):
            row_list=[]
            for j in range(len(self.fract_name[i])):        
                label=QLabel(self.fract_name[i][j])
                label.setAlignment(Qt.AlignCenter)
                label.setStyleSheet(self.border_b)
                formlayout.addWidget(label,i,j)
                row_list.append(label)
                
            self.label_list.append(row_list)
        if 2 < len(self.label_list):
                for i in range(3,len(self.label_list)):
                    for j in range(len(self.label_list[i])):
                        self.label_list[i][j].hide()
                
        widget = QWidget()
        widget.setLayout(formlayout) 
        self.scrollArea.setWidget(widget)
        self.scrollArea.setWidgetResizable(True)
                       
    def keyReleaseEvent(self,e):        
        if e.key() == Qt.Key_G:
            self.second = selectfractwindow()    
            self.second.showMaximized()
            self.close()
        elif e.key() == Qt.Key_S:
            if self.x < len(self.label_list)-1 and self.y < len(self.label_list[self.x+1]):
                self.label_list[self.x][self.y].setStyleSheet(self.border_b)
                self.x+=1

                if len(self.label_list) > 2:
                    for i in range(0,len(self.label_list)):
                        for j in range(len(self.label_list[i])):
                            self.label_list[i][j].hide()

                    for i in range(self.x,self.x+2):
                        if i < len(self.label_list):
                            for j in range(len(self.label_list[i])):
                                self.label_list[i][j].show()
                else:
                    for i in range(2):
                        for j in range(len(self.label_list[i])):
                            self.label_list[i][j].show()
                            
                self.label_list[self.x][self.y].setStyleSheet(self.border_s)
        elif e.key() == Qt.Key_W:
            if self.x > 0:
                self.label_list[self.x][self.y].setStyleSheet(self.border_b)
                self.x-=1
                if self.y >= len(self.label_list[self.x]):
                    self.y = len(self.label_list[self.x])-1                    
               
                self.label_list[self.x][self.y].setStyleSheet(self.border_s)
                for i in range(0,len(self.label_list)):
                    for j in range(len(self.label_list[i])):
                        self.label_list[i][j].hide()
                for i in range(self.x,self.x+2):
                    if i < len(self.label_list):
                        for j in range(len(self.label_list[i])):
                            self.label_list[i][j].show()
                    
        elif e.key() == Qt.Key_D:
            if self.y < len(self.label_list[self.x])-1:
                self.label_list[self.x][self.y].setStyleSheet(self.border_b)
                self.y+=1
                self.label_list[self.x][self.y].setStyleSheet(self.border_s)
        elif e.key() == Qt.Key_A:
                self.label_list[self.x][self.y].setStyleSheet(self.border_b)
                self.y-=1
                self.label_list[self.x][self.y].setStyleSheet(self.border_s)
        elif e.key() == Qt.Key_F:
            self.second = updatefractwordwindow(self.fract_code[self.x][self.y])
            self.second.showMaximized()
            self.close()
            
#분류삭제확인창
class delfractchecksumwindow(QDialog,QWidget,checksum_window):
    cus=1
    code=''
    border_g = 'background-color: rgb(0, 255, 0);\nborder-radius: 30px;'
    border_gs = 'background-color: rgb(0, 255, 0);\nborder-radius: 30px;border-color: rgb(0,21,209);border-style: solid;\nborder-width: 2px'
    border_rs = 'background-color: rgb(255, 69, 69);\nborder-radius: 30px;border-color: rgb(0,21,209);border-style: solid;\nborder-width: 2px'
    border_r = 'background-color: rgb(255, 69, 69);\nborder-radius: 30px;'
    def __init__(self,text,code2):
        super(delfractchecksumwindow,self).__init__()
        self.code = code2
        self.initUi()
        self.label_3.setText(text)
        self.show()
    def initUi(self):
        self.setupUi(self)
        self.label_2.setStyleSheet(self.border_rs)
        
    def keyReleaseEvent(self,e):
        global idnum
        if e.key() == Qt.Key_F:
            if self.cus == 0:
                sock.sendall(bytes("--delclass--"+str(idnum)+"--"+self.code+"\n",'UTF-8'))
                self.main = selectfractwindow()    
                self.main.showMaximized()
                self.close()
            elif self.cus == 1:
                self.main = selectfractwindow()    
                self.main.showMaximized()
                self.close()
        elif e.key() == Qt.Key_A:
            if self.cus == 1:
                self.label_2.setStyleSheet(self.border_r)
                self.cus = self.cus - 1
                self.label.setStyleSheet(self.border_gs)
        elif e.key() == Qt.Key_D:
            if self.cus == 0:
                self.label.setStyleSheet(self.border_g)
                self.cus = self.cus + 1
                self.label_2.setStyleSheet(self.border_rs)

#분류삭제
class delfractwindow(QDialog,QWidget,form_word1window):
    fract_name=[]
    fract_code=[]
    checksum = 0
    x=0
    y=0
    border_s = 'font: 20pt "AcadEref"; border-color: rgb(0,21,209); \nbackground-color: rgb(170, 242, 248);\nborder-style: solid;\nborder-width: 2px;\nborder-radius: 10px;'
    border_b = 'font: 20pt "AcadEref"; border-color: rgb(170,242,248); \nbackground-color: rgb(170, 242, 248);\nborder-style: solid;\nborder-width: 2px;\nborder-radius: 10px;'

    def __init__(self,f_name,f_code):
        super(delfractwindow,self).__init__()
        self.fract_name = f_name
        self.fract_code = f_code
        self.initUi()
        self.label_list[0][0].setStyleSheet(self.border_s)
        self.label.setText('삭제할 분류 선택')
        self.show()

    def initUi(self):
        self.setupUi(self)
        self.label_list=[]
        formlayout = QGridLayout()
        for i in range(len(self.fract_name)):
            row_list=[]
            for j in range(len(self.fract_name[i])):        
                label=QLabel(self.fract_name[i][j])
                label.setAlignment(Qt.AlignCenter)
                label.setStyleSheet(self.border_b)
                formlayout.addWidget(label,i,j)
                row_list.append(label)
                
            self.label_list.append(row_list)
        if 2 < len(self.label_list):
                for i in range(3,len(self.label_list)):
                    for j in range(len(self.label_list[i])):
                        self.label_list[i][j].hide()
                
        widget = QWidget()
        widget.setLayout(formlayout) 
        self.scrollArea.setWidget(widget)
        self.scrollArea.setWidgetResizable(True)
                       
    def keyReleaseEvent(self,e):        
        if e.key() == Qt.Key_G:
            self.second = selectfractwindow()    
            self.second.showMaximized()
            self.close()
        elif e.key() == Qt.Key_S:
            if self.x < len(self.label_list)-1 and self.y < len(self.label_list[self.x+1]):
                self.label_list[self.x][self.y].setStyleSheet(self.border_b)
                self.x+=1

                if len(self.label_list) > 2:
                    for i in range(0,len(self.label_list)):
                        for j in range(len(self.label_list[i])):
                            self.label_list[i][j].hide()

                    for i in range(self.x,self.x+2):
                        if i < len(self.label_list):
                            for j in range(len(self.label_list[i])):
                                self.label_list[i][j].show()
                else:
                    for i in range(2):
                        for j in range(len(self.label_list[i])):
                            self.label_list[i][j].show()
                            
                self.label_list[self.x][self.y].setStyleSheet(self.border_s)
        elif e.key() == Qt.Key_W:
            if self.x > 0:
                self.label_list[self.x][self.y].setStyleSheet(self.border_b)
                self.x-=1
                if self.y >= len(self.label_list[self.x]):
                    self.y = len(self.label_list[self.x])-1                    
               
                self.label_list[self.x][self.y].setStyleSheet(self.border_s)
                for i in range(0,len(self.label_list)):
                    for j in range(len(self.label_list[i])):
                        self.label_list[i][j].hide()
                for i in range(self.x,self.x+2):
                    if i < len(self.label_list):
                        for j in range(len(self.label_list[i])):
                            self.label_list[i][j].show()
                    
        elif e.key() == Qt.Key_D:
            if self.y < len(self.label_list[self.x])-1:
                self.label_list[self.x][self.y].setStyleSheet(self.border_b)
                self.y+=1
                self.label_list[self.x][self.y].setStyleSheet(self.border_s)
        elif e.key() == Qt.Key_A:
                self.label_list[self.x][self.y].setStyleSheet(self.border_b)
                self.y-=1
                self.label_list[self.x][self.y].setStyleSheet(self.border_s)
        elif e.key() == Qt.Key_F:
            self.second = delfractchecksumwindow('정말 삭제할까요?',self.fract_code[self.x][self.y])
            self.second.exec()
            self.close()
            
#분류추가(단어)
class addfractwordwindow(QDialog,QWidget,login_pw_window):
    word_table = [['ㄱ','ㄴ','ㄷ','ㄹ','ㅁ','ㅂ','ㅅ'],
                  ['ㅇ','ㅈ','ㅊ','ㅋ','ㅌ','ㅍ','ㅎ'],
                  ['ㄲ','ㄸ','ㅃ','ㅆ','ㅉ'],
                  ['ㅏ','ㅓ','ㅗ','ㅜ','ㅡ','ㅣ','ㅒ'],
                  ['ㅑ','ㅕ','ㅛ','ㅠ','ㅐ','ㅔ','ㅖ']]
    cons_all= {'r':'ㄱ', 'R':'ㄲ', 's':'ㄴ', 'e':'ㄷ', 'E':'ㄸ', 'f':'ㄹ', 'a':'ㅁ', 'q':'ㅂ', 'Q':'ㅃ', 't':'ㅅ', 'T':'ㅆ',
           'd':'ㅇ', 'w':'ㅈ', 'W':'ㅉ', 'c':'ㅊ', 'z':'ㅋ', 'x':'ㅌ', 'v':'ㅍ', 'g':'ㅎ','k':'ㅏ', 'o':'ㅐ', 'i':'ㅑ', 'O':'ㅒ', 'j':'ㅓ', 'p':'ㅔ', 'u':'ㅕ', 'P':'ㅖ', 'h':'ㅗ', 'hk':'ㅘ', 'ho':'ㅙ', 'hl':'ㅚ',
           'y':'ㅛ', 'n':'ㅜ', 'b':'ㅠ',  'm':'ㅡ', 'l':'ㅣ'}            
    x=1
    y=0
    text=''
    idText=''
    label_text=''
    border_s = 'font: 20pt "AcadEref"; border-color: rgb(0,21,209); \nbackground-color: rgb(170, 242, 248);\nborder-style: solid;\nborder-width: 2px;\nborder-radius: 10px;'
    border_b = 'font: 20pt "AcadEref"; border-color: rgb(170,242,248); \nbackground-color: rgb(170, 242, 248);\nborder-style: solid;\nborder-width: 2px;\nborder-radius: 10px;'
    border_g = 'background-color: rgb(0, 255, 0);\nborder-radius: 30px;'
    border_gs = 'background-color: rgb(0, 255, 0);\nborder-radius: 30px;border-color: rgb(0,21,209);border-style: solid;\nborder-width: 2px'
    border_rs = 'background-color: rgb(255, 69, 69);\nborder-radius: 30px;border-color: rgb(0,21,209);border-style: solid;\nborder-width: 2px'
    border_r = 'background-color: rgb(255, 69, 69);\nborder-radius: 30px;'
    def __init__(self,idText2):
        super(addfractwordwindow,self).__init__()
        self.initUi()
        self.idText = idText2
        self.label_list[1][0].setStyleSheet(self.border_s)
        self.show()

    def initUi(self):
        self.setupUi(self)
        self.label_2.setText('분류추가 단어입력')
        self.label_3.setText('추가')
        self.label_list=[]
        row_list_init = [self.label_3,self.label_4]
        self.label_list.append(row_list_init)
        formlayout = QGridLayout()
        for i in range(5):
            row_list=[]
            for j in range(len(self.word_table[i])):
                label=QLabel(self.word_table[i][j])
                label.setStyleSheet(self.border_b)
                formlayout.addWidget(label,i,j)
                
                row_list.append(label)
            self.label_list.append(row_list)
        self.widget.setLayout(formlayout) 

    def keyReleaseEvent(self,e):
        global idnum
        if e.key() == Qt.Key_G:
            num=0
            self.login = selectfractwindow()   
            self.login.showMaximized()
            self.close()
        elif e.key() == Qt.Key_S:
            if self.x < len(self.label_list)-1 and self.y < len(self.label_list[self.x+1]):
                if self.x==0 and self.y==0:
                    self.label_list[self.x][self.y].setStyleSheet(self.border_g)
                elif self.x==0 and self.y==1:
                    self.label_list[self.x][self.y].setStyleSheet(self.border_r)
                else:
                    self.label_list[self.x][self.y].setStyleSheet(self.border_b)
                self.x+=1
                self.label_list[self.x][self.y].setStyleSheet(self.border_s)
        elif e.key() == Qt.Key_W:
            if self.x > 0 and self.y < len(self.label_list[self.x-1]):
                self.label_list[self.x][self.y].setStyleSheet(self.border_b)
                self.x-=1
                if self.x==0 and self.y==0:
                    self.label_list[self.x][self.y].setStyleSheet(self.border_gs)
                elif self.x==0 and self.y==1:
                    self.label_list[self.x][self.y].setStyleSheet(self.border_rs)
                else:
                    self.label_list[self.x][self.y].setStyleSheet(self.border_s)
        elif e.key() == Qt.Key_D:
            if self.y == len(self.label_list[self.x])-1:
                self.label_list[self.x][self.y].setStyleSheet(self.border_b)
                self.x=0
                self.y=0
                self.label_list[self.x][self.y].setStyleSheet(self.border_gs)
            if self.y < len(self.label_list[self.x])-1:
                if self.x==0:
                    if self.y==0:
                        self.label_list[self.x][self.y].setStyleSheet(self.border_g)
                        self.y+=1
                        self.label_list[self.x][self.y].setStyleSheet(self.border_rs)
                else:
                    self.label_list[self.x][self.y].setStyleSheet(self.border_b)
                    self.y+=1
                    self.label_list[self.x][self.y].setStyleSheet(self.border_s)
        elif e.key() == Qt.Key_A:
            if self.y==0:
                self.label_list[self.x][self.y].setStyleSheet(self.border_b)
                self.x=0
                self.y=0
                self.label_list[self.x][self.y].setStyleSheet(self.border_gs)
            if self.y > 0:
                if self.x==0:
                    if self.y==1:
                        self.label_list[self.x][self.y].setStyleSheet(self.border_r)
                        self.y-=1
                        self.label_list[self.x][self.y].setStyleSheet(self.border_gs)
                else:
                    self.label_list[self.x][self.y].setStyleSheet(self.border_b)
                    self.y-=1
                    self.label_list[self.x][self.y].setStyleSheet(self.border_s)
        elif e.key() == Qt.Key_F:
            if self.x >0:
                self.text = self.word_table[self.x-1][self.y]
                for key, value in self.cons_all.items():
                    if value == self.text:
                        self.label_text += key
                self.label.setText(jamo3(self.label_text))                
            elif self.x == 0 and self.y == 1:
                self.text = ''
                self.label_text = ''
                self.label.setText(self.text)
            elif self.x == 0 and self.y == 0:
                sock.sendall(bytes("addclass--"+self.idText+"--"+self.label.text()+"--"+str(idnum)+"\n",'UTF-8'))
                data = sock.recv(10)
                a = str(data.decode())
                a = a[0:1]
                if int(a) == 1:
                    self.second = warningwindow('존재하는 분류')    
                    self.second.exec()
                    self.main = selectfractwindow()    
                    self.main.showMaximized()
                    self.close()
                elif int(a) == 0:
                    self.second = warningwindow('추가 성공')    
                    self.second.exec()
                    self.main = selectfractwindow()    
                    self.main.showMaximized()
                    self.close()
                    
#분류추가(분류)
class addfractwindow(QDialog,QWidget,login_pw_window):
    word_table = [['ㄱ','ㄴ','ㄷ','ㄹ','ㅁ','ㅂ','ㅅ'],
                  ['ㅇ','ㅈ','ㅊ','ㅋ','ㅌ','ㅍ','ㅎ'],
                  ['ㄲ','ㄸ','ㅃ','ㅆ','ㅉ'],
                  ['ㅏ','ㅓ','ㅗ','ㅜ','ㅡ','ㅣ','ㅒ'],
                  ['ㅑ','ㅕ','ㅛ','ㅠ','ㅐ','ㅔ','ㅖ']]
    cons_all= {'r':'ㄱ', 'R':'ㄲ', 's':'ㄴ', 'e':'ㄷ', 'E':'ㄸ', 'f':'ㄹ', 'a':'ㅁ', 'q':'ㅂ', 'Q':'ㅃ', 't':'ㅅ', 'T':'ㅆ',
           'd':'ㅇ', 'w':'ㅈ', 'W':'ㅉ', 'c':'ㅊ', 'z':'ㅋ', 'x':'ㅌ', 'v':'ㅍ', 'g':'ㅎ','k':'ㅏ', 'o':'ㅐ', 'i':'ㅑ', 'O':'ㅒ', 'j':'ㅓ', 'p':'ㅔ', 'u':'ㅕ', 'P':'ㅖ', 'h':'ㅗ', 'hk':'ㅘ', 'ho':'ㅙ', 'hl':'ㅚ',
           'y':'ㅛ', 'n':'ㅜ', 'b':'ㅠ',  'm':'ㅡ', 'l':'ㅣ'}            
    x=1
    y=0
    text=''
    label_text=''
    border_s = 'font: 20pt "AcadEref"; border-color: rgb(0,21,209); \nbackground-color: rgb(170, 242, 248);\nborder-style: solid;\nborder-width: 2px;\nborder-radius: 10px;'
    border_b = 'font: 20pt "AcadEref"; border-color: rgb(170,242,248); \nbackground-color: rgb(170, 242, 248);\nborder-style: solid;\nborder-width: 2px;\nborder-radius: 10px;'
    border_g = 'background-color: rgb(0, 255, 0);\nborder-radius: 30px;'
    border_gs = 'background-color: rgb(0, 255, 0);\nborder-radius: 30px;border-color: rgb(0,21,209);border-style: solid;\nborder-width: 2px'
    border_rs = 'background-color: rgb(255, 69, 69);\nborder-radius: 30px;border-color: rgb(0,21,209);border-style: solid;\nborder-width: 2px'
    border_r = 'background-color: rgb(255, 69, 69);\nborder-radius: 30px;'
    def __init__(self):
        super(addfractwindow,self).__init__()
        self.initUi()
        self.label_list[1][0].setStyleSheet(self.border_s)
        self.show()

    def initUi(self):
        self.setupUi(self)
        self.label_2.setText('분류추가 분류입력')
        self.label_3.setText('확인')
        self.label_list=[]
        row_list_init = [self.label_3,self.label_4]
        self.label_list.append(row_list_init)
        formlayout = QGridLayout()
        for i in range(5):
            row_list=[]
            for j in range(len(self.word_table[i])):
                label=QLabel(self.word_table[i][j])
                label.setStyleSheet(self.border_b)
                formlayout.addWidget(label,i,j)
                
                row_list.append(label)
            self.label_list.append(row_list)
        self.widget.setLayout(formlayout) 

    def keyReleaseEvent(self,e):
        global idnum
        if e.key() == Qt.Key_G:
            num=0
            self.login = selectfractwindow()   
            self.login.showMaximized()
            self.close()
        elif e.key() == Qt.Key_S:
            if self.x < len(self.label_list)-1 and self.y < len(self.label_list[self.x+1]):
                if self.x==0 and self.y==0:
                    self.label_list[self.x][self.y].setStyleSheet(self.border_g)
                elif self.x==0 and self.y==1:
                    self.label_list[self.x][self.y].setStyleSheet(self.border_r)
                else:
                    self.label_list[self.x][self.y].setStyleSheet(self.border_b)
                self.x+=1
                self.label_list[self.x][self.y].setStyleSheet(self.border_s)
        elif e.key() == Qt.Key_W:
            if self.x > 0 and self.y < len(self.label_list[self.x-1]):
                self.label_list[self.x][self.y].setStyleSheet(self.border_b)
                self.x-=1
                if self.x==0 and self.y==0:
                    self.label_list[self.x][self.y].setStyleSheet(self.border_gs)
                elif self.x==0 and self.y==1:
                    self.label_list[self.x][self.y].setStyleSheet(self.border_rs)
                else:
                    self.label_list[self.x][self.y].setStyleSheet(self.border_s)
        elif e.key() == Qt.Key_D:
            if self.y == len(self.label_list[self.x])-1:
                self.label_list[self.x][self.y].setStyleSheet(self.border_b)
                self.x=0
                self.y=0
                self.label_list[self.x][self.y].setStyleSheet(self.border_gs)
            if self.y < len(self.label_list[self.x])-1:
                if self.x==0:
                    if self.y==0:
                        self.label_list[self.x][self.y].setStyleSheet(self.border_g)
                        self.y+=1
                        self.label_list[self.x][self.y].setStyleSheet(self.border_rs)
                else:
                    self.label_list[self.x][self.y].setStyleSheet(self.border_b)
                    self.y+=1
                    self.label_list[self.x][self.y].setStyleSheet(self.border_s)
        elif e.key() == Qt.Key_A:
            if self.y==0:
                self.label_list[self.x][self.y].setStyleSheet(self.border_b)
                self.x=0
                self.y=0
                self.label_list[self.x][self.y].setStyleSheet(self.border_gs)
            if self.y > 0:
                if self.x==0:
                    if self.y==1:
                        self.label_list[self.x][self.y].setStyleSheet(self.border_r)
                        self.y-=1
                        self.label_list[self.x][self.y].setStyleSheet(self.border_gs)
                else:
                    self.label_list[self.x][self.y].setStyleSheet(self.border_b)
                    self.y-=1
                    self.label_list[self.x][self.y].setStyleSheet(self.border_s)
        elif e.key() == Qt.Key_F:
            if self.x >0:
                self.text = self.word_table[self.x-1][self.y]
                for key, value in self.cons_all.items():
                    if value == self.text:
                        self.label_text += key
                self.label.setText(jamo3(self.label_text))                
            elif self.x == 0 and self.y == 1:
                self.text = ''
                self.label_text = ''
                self.label.setText(self.text)
            elif self.x == 0 and self.y == 0:
                self.second = addfractwordwindow(self.label.text())    
                self.second.showMaximized()
                self.close()
                    
#분류cud선택
class cudfractwindow(QDialog,QWidget, cud_window):
    cus = 0
    fract_name=[]
    fract_code=[]
    border_s = 'border-color: rgb(0,21,209); \nbackground-color: rgb(170, 242, 248);\nborder-style: solid;\nborder-width: 2px;\nborder-radius: 10px;'
    border_b = 'border-color: rgb(170, 242, 248); \nbackground-color: rgb(170, 242, 248);\nborder-style: solid;\nborder-width: 2px;\nborder-radius: 10px;'
    idCode = 0   
    def __init__(self,f_name,f_code):
        super(cudfractwindow,self).__init__()
        self.fract_name = f_name
        self.fract_code = f_code
        self.setupUi(self)
        self.cus=0
        self.label_list=[]
        self.label_list.append(self.label_1)
        self.label_list.append(self.label_2)
        self.label_list.append(self.label_3)
        self.label_list[self.cus].setStyleSheet(self.border_s)
        self.label.setText('단어말하기 분류편집')
        self.label_list[0].setText('분류추가')
        self.label_list[1].setText('분류수정')
        self.label_list[2].setText('분류삭제')
        
    def keyReleaseEvent(self,e):
        if e.key() == Qt.Key_W:
            if self.cus > 0:
                self.label_list[self.cus].setStyleSheet(self.border_b)
                self.cus-=1
                self.label_list[self.cus].setStyleSheet(self.border_s)
        elif e.key() == Qt.Key_G:
            self.second = selectfractwindow()    
            self.second.showMaximized()
            self.close()
        elif e.key() == Qt.Key_S:
            if self.cus < 2:
                self.label_list[self.cus].setStyleSheet(self.border_b)
                self.cus+=1
                self.label_list[self.cus].setStyleSheet(self.border_s)
        elif e.key() == Qt.Key_F:
            if self.cus == 0:
                self.second = addfractwindow()    
                self.second.showMaximized()
                self.close()
            elif self.cus == 1:
                self.upin = updatefractwindow(self.fract_name,self.fract_code)   
                self.upin.showMaximized()
                self.close()
            elif self.cus == 2:
                self.upin = delfractwindow(self.fract_name,self.fract_code)   
                self.upin.showMaximized()
                self.close()
                
#단어편집 분류선택
class selectfractwindow(QDialog,QWidget,form_word1window):
    fract_name=[]
    fract_code=[]
    fract_name_ex=[]
    fract_code_ex=[]
    word_name=[]
    datatrue=0
    x=0
    y=0
    border_s = 'font: 20pt "AcadEref"; border-color: rgb(0,21,209); \nbackground-color: rgb(170, 242, 248);\nborder-style: solid;\nborder-width: 2px;\nborder-radius: 10px;'
    border_b = 'font: 20pt "AcadEref"; border-color: rgb(170,242,248); \nbackground-color: rgb(170, 242, 248);\nborder-style: solid;\nborder-width: 2px;\nborder-radius: 10px;'

    def __init__(self):
        super(selectfractwindow,self).__init__()
        self.dataImport()
        self.initUi()
        self.label_list[0][0].setStyleSheet(self.border_s)
        self.show()

    def initUi(self):
        self.setupUi(self)
        self.label_list=[]
        formlayout = QGridLayout()
        if self.datatrue == 0:
            row_list=[]
            label=QLabel(self.fract_name[0][0])
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet(self.border_b)
            formlayout.addWidget(label,0,0)
            row_list.append(label)
            self.label_list.append(row_list)
        else:
            for i in range(len(self.fract_name)):
                row_list=[]
                for j in range(len(self.fract_name[i])):        
                    label=QLabel(self.fract_name[i][j])
                    label.setAlignment(Qt.AlignCenter)
                    label.setStyleSheet(self.border_b)
                    formlayout.addWidget(label,i,j)
                    row_list.append(label)
                    
                self.label_list.append(row_list)

        if 2 < len(self.label_list):
                for i in range(3,len(self.label_list)):
                    for j in range(len(self.label_list[i])):
                        self.label_list[i][j].hide()
       
        widget = QWidget()
        widget.setLayout(formlayout) 
        self.scrollArea.setWidget(widget)
        self.scrollArea.setWidgetResizable(True)
        
    def dataImport(self):
        global idnum
        for i in range(2):
            if i == 0:
                check=1
                sock.sendall(bytes("--upin--"+str(idnum)+"\n",'UTF-8'))
                data = sock.recv(1000000)               
                list2 = []
                a = str(data.decode())
                list_row = []
                list_row.append("분류편집")
                if(a[:-2] == '0'):
                    self.datatrue = 0
                    list2.append(list_row)
                    self.fract_name = list2.copy()
                else:
                    self.datatrue = 1
                    result = a[:-2]
                    r = result.split('-')
                    for i in range(len(r)):
                        if check == 3:
                            check = 0
                            list2.append(list_row)
                            list_row=[]              
                        list_row.append(r[i])
                        check+=1
                    list2.append(list_row)
                    self.fract_name = list2.copy()
                    #전송 분류편집 형식 
                    check = 0
                    list4 = []
                    list_row=[]
                    for i in range(len(r)):
                        if check == 3:
                            check = 0
                            list4.append(list_row)
                            list_row=[]              
                        list_row.append(r[i])
                        check+=1
                    list4.append(list_row)
                    self.fract_name_ex = list4.copy()

                    #분류코드
                    data2 = sock.recv(1000000)               
                    list5 = []
                    a2 = str(data2.decode())
                    check = 1
                    list_row = []
                    list_row.append("분류편집")
                    result2 = a2[:-2]
                    r2 = result2.split('-')
                    for i in range(len(r2)):
                        if check == 3:
                            check = 0
                            list5.append(list_row)
                            list_row=[]              
                        list_row.append(r2[i])
                        check+=1
                    list5.append(list_row)
                    self.fract_code = list5.copy()
                    #전송 분류편집코드 형식
                    check = 0
                    list_row = []
                    list3 = []
                    for i in range(len(r2)):
                        if check == 3:
                            check = 0
                            list3.append(list_row)
                            list_row=[]              
                        list_row.append(r2[i])
                        check+=1
                    list3.append(list_row)
                    self.fract_code_ex = list3.copy()
                    
            elif i == 1 and self.datatrue == 1:
                check=0
                check_out = 0
                sock.sendall(bytes("--upin2--"+str(idnum)+"\n",'UTF-8'))
                data = sock.recv(1000000)
                list = []
                list_add = []
                a = str(data.decode())
                result = a[:-2]
                r = result.split('@')
                
                for i in range(len(r)):
                    word = r[i].split('-')
                    list_row = []
                    list_row_word=[]
                    
                    for j in range(len(word)):
                        if check == 3:
                            check = 0
                            list_row.append(list_row_word)
                            list_row_word=[]              
                        list_row_word.append(word[j])
                        check+=1                
                    list_row.append(list_row_word)
                    check=0

                    if check_out == 3:
                        check_out=0
                        list.append(list_add)
                        list_add = []
                        list_add.append(list_row)
                        check_out += 1
                    else:
                        list_add.append(list_row)
                        check_out += 1

                list.append(list_add)
                self.word_name=list.copy()
                       
    def keyReleaseEvent(self,e):
        
        if e.key() == Qt.Key_G:
            self.second = WindowClass()    
            self.second.showMaximized()
            self.close()
        elif e.key() == Qt.Key_S:
            if self.x < len(self.label_list)-1 and self.y < len(self.label_list[self.x+1]):
                self.label_list[self.x][self.y].setStyleSheet(self.border_b)
                self.x+=1

                if len(self.label_list) > 2:
                    for i in range(0,len(self.label_list)):
                        for j in range(len(self.label_list[i])):
                            self.label_list[i][j].hide()

                    for i in range(self.x,self.x+2):
                        if i < len(self.label_list):
                            for j in range(len(self.label_list[i])):
                                self.label_list[i][j].show()
                else:
                    for i in range(2):
                        for j in range(len(self.label_list[i])):
                            self.label_list[i][j].show()
                            
                self.label_list[self.x][self.y].setStyleSheet(self.border_s)
        elif e.key() == Qt.Key_W:
            if self.x > 0:
                self.label_list[self.x][self.y].setStyleSheet(self.border_b)
                self.x-=1
                if self.y >= len(self.label_list[self.x]):
                    self.y = len(self.label_list[self.x])-1                    
               
                self.label_list[self.x][self.y].setStyleSheet(self.border_s)
                for i in range(0,len(self.label_list)):
                    for j in range(len(self.label_list[i])):
                        self.label_list[i][j].hide()
                for i in range(self.x,self.x+2):
                    if i < len(self.label_list):
                        for j in range(len(self.label_list[i])):
                            self.label_list[i][j].show()
                    
        elif e.key() == Qt.Key_D:
            if self.y < len(self.label_list[self.x])-1:
                self.label_list[self.x][self.y].setStyleSheet(self.border_b)
                self.y+=1
                self.label_list[self.x][self.y].setStyleSheet(self.border_s)
        elif e.key() == Qt.Key_A:
                self.label_list[self.x][self.y].setStyleSheet(self.border_b)
                self.y-=1
                self.label_list[self.x][self.y].setStyleSheet(self.border_s)
        elif e.key() == Qt.Key_F:
            if self.x == 0 and self.y == 0:
                self.word2 = cudfractwindow(self.fract_name_ex, self.fract_code_ex)
                self.word2.showMaximized()
                self.close()
            else:
                self.word2 = wordCUDwindow(self.fract_name,self.word_name,self.fract_code,self.x,self.y)
                self.word2.showMaximized()
                self.close()
            
#회원가입(비밀번호)
class addpwwindow(QDialog,QWidget,login_pw_window):
    word_table = [['ㄱ','ㄴ','ㄷ','ㄹ','ㅁ','ㅂ','ㅅ'],
                  ['ㅇ','ㅈ','ㅊ','ㅋ','ㅌ','ㅍ','ㅎ'],
                  ['ㄲ','ㄸ','ㅃ','ㅆ','ㅉ'],
                  ['ㅏ','ㅓ','ㅗ','ㅜ','ㅡ','ㅣ','ㅒ'],
                  ['ㅑ','ㅕ','ㅛ','ㅠ','ㅐ','ㅔ','ㅖ']]
    cons_all= {'r':'ㄱ', 'R':'ㄲ', 's':'ㄴ', 'e':'ㄷ', 'E':'ㄸ', 'f':'ㄹ', 'a':'ㅁ', 'q':'ㅂ', 'Q':'ㅃ', 't':'ㅅ', 'T':'ㅆ',
           'd':'ㅇ', 'w':'ㅈ', 'W':'ㅉ', 'c':'ㅊ', 'z':'ㅋ', 'x':'ㅌ', 'v':'ㅍ', 'g':'ㅎ','k':'ㅏ', 'o':'ㅐ', 'i':'ㅑ', 'O':'ㅒ', 'j':'ㅓ', 'p':'ㅔ', 'u':'ㅕ', 'P':'ㅖ', 'h':'ㅗ', 'hk':'ㅘ', 'ho':'ㅙ', 'hl':'ㅚ',
           'y':'ㅛ', 'n':'ㅜ', 'b':'ㅠ',  'm':'ㅡ', 'l':'ㅣ'}            
    x=1
    y=0
    text=''
    idText=''
    label_text=''
    border_s = 'font: 20pt "AcadEref"; border-color: rgb(0,21,209); \nbackground-color: rgb(170, 242, 248);\nborder-style: solid;\nborder-width: 2px;\nborder-radius: 10px;'
    border_b = 'font: 20pt "AcadEref"; border-color: rgb(170,242,248); \nbackground-color: rgb(170, 242, 248);\nborder-style: solid;\nborder-width: 2px;\nborder-radius: 10px;'
    border_g = 'background-color: rgb(0, 255, 0);\nborder-radius: 30px;'
    border_gs = 'background-color: rgb(0, 255, 0);\nborder-radius: 30px;border-color: rgb(0,21,209);border-style: solid;\nborder-width: 2px'
    border_rs = 'background-color: rgb(255, 69, 69);\nborder-radius: 30px;border-color: rgb(0,21,209);border-style: solid;\nborder-width: 2px'
    border_r = 'background-color: rgb(255, 69, 69);\nborder-radius: 30px;'
    def __init__(self,idText2):
        super(addpwwindow,self).__init__()
        self.initUi()
        self.idText = idText2
        self.label_list[1][0].setStyleSheet(self.border_s)
        self.show()

    def initUi(self):
        self.setupUi(self)
        self.label_2.setText('회원가입 비밀번호')
        self.label_3.setText('가입')
        self.label_list=[]
        row_list_init = [self.label_3,self.label_4]
        self.label_list.append(row_list_init)
        formlayout = QGridLayout()
        for i in range(5):
            row_list=[]
            for j in range(len(self.word_table[i])):
                label=QLabel(self.word_table[i][j])
                label.setStyleSheet(self.border_b)
                formlayout.addWidget(label,i,j)
                
                row_list.append(label)
            self.label_list.append(row_list)
        self.widget.setLayout(formlayout) 

    def keyReleaseEvent(self,e):
        global idnum
        if e.key() == Qt.Key_G:
            num=0
            self.login = addidwindow()   
            self.login.showMaximized()
            self.close()
        elif e.key() == Qt.Key_S:
            if self.x < len(self.label_list)-1 and self.y < len(self.label_list[self.x+1]):
                if self.x==0 and self.y==0:
                    self.label_list[self.x][self.y].setStyleSheet(self.border_g)
                elif self.x==0 and self.y==1:
                    self.label_list[self.x][self.y].setStyleSheet(self.border_r)
                else:
                    self.label_list[self.x][self.y].setStyleSheet(self.border_b)
                self.x+=1
                self.label_list[self.x][self.y].setStyleSheet(self.border_s)
        elif e.key() == Qt.Key_W:
            if self.x > 0 and self.y < len(self.label_list[self.x-1]):
                self.label_list[self.x][self.y].setStyleSheet(self.border_b)
                self.x-=1
                if self.x==0 and self.y==0:
                    self.label_list[self.x][self.y].setStyleSheet(self.border_gs)
                elif self.x==0 and self.y==1:
                    self.label_list[self.x][self.y].setStyleSheet(self.border_rs)
                else:
                    self.label_list[self.x][self.y].setStyleSheet(self.border_s)
        elif e.key() == Qt.Key_D:
            if self.y == len(self.label_list[self.x])-1:
                self.label_list[self.x][self.y].setStyleSheet(self.border_b)
                self.x=0
                self.y=0
                self.label_list[self.x][self.y].setStyleSheet(self.border_gs)
            if self.y < len(self.label_list[self.x])-1:
                if self.x==0:
                    if self.y==0:
                        self.label_list[self.x][self.y].setStyleSheet(self.border_g)
                        self.y+=1
                        self.label_list[self.x][self.y].setStyleSheet(self.border_rs)
                else:
                    self.label_list[self.x][self.y].setStyleSheet(self.border_b)
                    self.y+=1
                    self.label_list[self.x][self.y].setStyleSheet(self.border_s)
        elif e.key() == Qt.Key_A:
            if self.y==0:
                self.label_list[self.x][self.y].setStyleSheet(self.border_b)
                self.x=0
                self.y=0
                self.label_list[self.x][self.y].setStyleSheet(self.border_gs)
            if self.y > 0:
                if self.x==0:
                    if self.y==1:
                        self.label_list[self.x][self.y].setStyleSheet(self.border_r)
                        self.y-=1
                        self.label_list[self.x][self.y].setStyleSheet(self.border_gs)
                else:
                    self.label_list[self.x][self.y].setStyleSheet(self.border_b)
                    self.y-=1
                    self.label_list[self.x][self.y].setStyleSheet(self.border_s)
        elif e.key() == Qt.Key_F:
            if self.x >0:
                self.text = self.word_table[self.x-1][self.y]
                for key, value in self.cons_all.items():
                    if value == self.text:
                        self.label_text += key
                self.label.setText(jamo3(self.label_text))                
            elif self.x == 0 and self.y == 1:
                self.text = ''
                self.label_text = ''
                self.label.setText(self.text)
            elif self.x == 0 and self.y == 0:
                sock.sendall(bytes("--addmember--"+self.idText+"--"+self.label.text()+"\n",'UTF-8'))
                data = sock.recv(10)
                a = str(data.decode())
                a = a[0:1]
                if int(a) == 1:
                    self.second = warningwindow('존재하는 아이디')    
                    self.second.exec()
                    self.main = addidwindow()    
                    self.main.showMaximized()
                    self.close()
                elif int(a) == 0:
                    self.second = warningwindow('가입 성공')    
                    self.second.exec()
                    self.main = WindowClass()    
                    self.main.showMaximized()
                    self.close()
                    
#회원가입(아이디)
class addidwindow(QDialog,QWidget,login_pw_window):
    word_table = [['ㄱ','ㄴ','ㄷ','ㄹ','ㅁ','ㅂ','ㅅ'],
                  ['ㅇ','ㅈ','ㅊ','ㅋ','ㅌ','ㅍ','ㅎ'],
                  ['ㄲ','ㄸ','ㅃ','ㅆ','ㅉ'],
                  ['ㅏ','ㅓ','ㅗ','ㅜ','ㅡ','ㅣ','ㅒ'],
                  ['ㅑ','ㅕ','ㅛ','ㅠ','ㅐ','ㅔ','ㅖ']]
    cons_all= {'r':'ㄱ', 'R':'ㄲ', 's':'ㄴ', 'e':'ㄷ', 'E':'ㄸ', 'f':'ㄹ', 'a':'ㅁ', 'q':'ㅂ', 'Q':'ㅃ', 't':'ㅅ', 'T':'ㅆ',
           'd':'ㅇ', 'w':'ㅈ', 'W':'ㅉ', 'c':'ㅊ', 'z':'ㅋ', 'x':'ㅌ', 'v':'ㅍ', 'g':'ㅎ','k':'ㅏ', 'o':'ㅐ', 'i':'ㅑ', 'O':'ㅒ', 'j':'ㅓ', 'p':'ㅔ', 'u':'ㅕ', 'P':'ㅖ', 'h':'ㅗ', 'hk':'ㅘ', 'ho':'ㅙ', 'hl':'ㅚ',
           'y':'ㅛ', 'n':'ㅜ', 'b':'ㅠ',  'm':'ㅡ', 'l':'ㅣ'}            
    x=1
    y=0
    text=''
    label_text=''
    border_s = 'font: 20pt "AcadEref"; border-color: rgb(0,21,209); \nbackground-color: rgb(170, 242, 248);\nborder-style: solid;\nborder-width: 2px;\nborder-radius: 10px;'
    border_b = 'font: 20pt "AcadEref"; border-color: rgb(170,242,248); \nbackground-color: rgb(170, 242, 248);\nborder-style: solid;\nborder-width: 2px;\nborder-radius: 10px;'
    border_g = 'background-color: rgb(0, 255, 0);\nborder-radius: 30px;'
    border_gs = 'background-color: rgb(0, 255, 0);\nborder-radius: 30px;border-color: rgb(0,21,209);border-style: solid;\nborder-width: 2px'
    border_rs = 'background-color: rgb(255, 69, 69);\nborder-radius: 30px;border-color: rgb(0,21,209);border-style: solid;\nborder-width: 2px'
    border_r = 'background-color: rgb(255, 69, 69);\nborder-radius: 30px;'
    def __init__(self):
        super(addidwindow,self).__init__()
        self.initUi()
        self.label_list[1][0].setStyleSheet(self.border_s)
        self.show()

    def initUi(self):
        self.setupUi(self)
        self.label_2.setText('회원가입 아이디')
        self.label_3.setText('확인')
        self.label_list=[]
        row_list_init = [self.label_3,self.label_4]
        self.label_list.append(row_list_init)
        formlayout = QGridLayout()
        for i in range(5):
            row_list=[]
            for j in range(len(self.word_table[i])):
                label=QLabel(self.word_table[i][j])
                label.setStyleSheet(self.border_b)
                formlayout.addWidget(label,i,j)
                
                row_list.append(label)
            self.label_list.append(row_list)
        self.widget.setLayout(formlayout) 

    def keyReleaseEvent(self,e):
        global idnum
        if e.key() == Qt.Key_G:
            num=0
            self.login = loginidwindow()   
            self.login.showMaximized()
            self.close()
        elif e.key() == Qt.Key_S:
            if self.x < len(self.label_list)-1 and self.y < len(self.label_list[self.x+1]):
                if self.x==0 and self.y==0:
                    self.label_list[self.x][self.y].setStyleSheet(self.border_g)
                elif self.x==0 and self.y==1:
                    self.label_list[self.x][self.y].setStyleSheet(self.border_r)
                else:
                    self.label_list[self.x][self.y].setStyleSheet(self.border_b)
                self.x+=1
                self.label_list[self.x][self.y].setStyleSheet(self.border_s)
        elif e.key() == Qt.Key_W:
            if self.x > 0 and self.y < len(self.label_list[self.x-1]):
                self.label_list[self.x][self.y].setStyleSheet(self.border_b)
                self.x-=1
                if self.x==0 and self.y==0:
                    self.label_list[self.x][self.y].setStyleSheet(self.border_gs)
                elif self.x==0 and self.y==1:
                    self.label_list[self.x][self.y].setStyleSheet(self.border_rs)
                else:
                    self.label_list[self.x][self.y].setStyleSheet(self.border_s)
        elif e.key() == Qt.Key_D:
            if self.y == len(self.label_list[self.x])-1:
                self.label_list[self.x][self.y].setStyleSheet(self.border_b)
                self.x=0
                self.y=0
                self.label_list[self.x][self.y].setStyleSheet(self.border_gs)
            if self.y < len(self.label_list[self.x])-1:
                if self.x==0:
                    if self.y==0:
                        self.label_list[self.x][self.y].setStyleSheet(self.border_g)
                        self.y+=1
                        self.label_list[self.x][self.y].setStyleSheet(self.border_rs)
                else:
                    self.label_list[self.x][self.y].setStyleSheet(self.border_b)
                    self.y+=1
                    self.label_list[self.x][self.y].setStyleSheet(self.border_s)
        elif e.key() == Qt.Key_A:
            if self.y==0:
                self.label_list[self.x][self.y].setStyleSheet(self.border_b)
                self.x=0
                self.y=0
                self.label_list[self.x][self.y].setStyleSheet(self.border_gs)
            if self.y > 0:
                if self.x==0:
                    if self.y==1:
                        self.label_list[self.x][self.y].setStyleSheet(self.border_r)
                        self.y-=1
                        self.label_list[self.x][self.y].setStyleSheet(self.border_gs)
                else:
                    self.label_list[self.x][self.y].setStyleSheet(self.border_b)
                    self.y-=1
                    self.label_list[self.x][self.y].setStyleSheet(self.border_s)
        elif e.key() == Qt.Key_F:
            if self.x >0:
                self.text = self.word_table[self.x-1][self.y]
                for key, value in self.cons_all.items():
                    if value == self.text:
                        self.label_text += key
                self.label.setText(jamo3(self.label_text))                
            elif self.x == 0 and self.y == 1:
                self.text = ''
                self.label_text = ''
                self.label.setText(self.text)
            elif self.x == 0 and self.y == 0:
                if self.label.text() == '':
                    self.second = warningwindow('빈 아이디')    
                    self.second.exec()
                else:
                    self.main = addpwwindow(self.label.text())    
                    self.main.showMaximized()
                    self.close()
                    
#로그인(아이디)
class loginidwindow(QDialog,QWidget,login_id_window):
    word_table = [['ㄱ','ㄴ','ㄷ','ㄹ','ㅁ','ㅂ','ㅅ'],
                  ['ㅇ','ㅈ','ㅊ','ㅋ','ㅌ','ㅍ','ㅎ'],
                  ['ㄲ','ㄸ','ㅃ','ㅆ','ㅉ'],
                  ['ㅏ','ㅓ','ㅗ','ㅜ','ㅡ','ㅣ','ㅒ'],
                  ['ㅑ','ㅕ','ㅛ','ㅠ','ㅐ','ㅔ','ㅖ']]
    cons_all= {'r':'ㄱ', 'R':'ㄲ', 's':'ㄴ', 'e':'ㄷ', 'E':'ㄸ', 'f':'ㄹ', 'a':'ㅁ', 'q':'ㅂ', 'Q':'ㅃ', 't':'ㅅ', 'T':'ㅆ',
           'd':'ㅇ', 'w':'ㅈ', 'W':'ㅉ', 'c':'ㅊ', 'z':'ㅋ', 'x':'ㅌ', 'v':'ㅍ', 'g':'ㅎ','k':'ㅏ', 'o':'ㅐ', 'i':'ㅑ', 'O':'ㅒ', 'j':'ㅓ', 'p':'ㅔ', 'u':'ㅕ', 'P':'ㅖ', 'h':'ㅗ', 'hk':'ㅘ', 'ho':'ㅙ', 'hl':'ㅚ',
           'y':'ㅛ', 'n':'ㅜ', 'b':'ㅠ',  'm':'ㅡ', 'l':'ㅣ'}
               
    x=1
    y=0
    text=''
    label_text=''
    border_s = 'font: 20pt "AcadEref"; border-color: rgb(0,21,209); \nbackground-color: rgb(170, 242, 248);\nborder-style: solid;\nborder-width: 2px;\nborder-radius: 10px;'
    border_b = 'font: 20pt "AcadEref"; border-color: rgb(170,242,248); \nbackground-color: rgb(170, 242, 248);\nborder-style: solid;\nborder-width: 2px;\nborder-radius: 10px;'
    border_g = 'background-color: rgb(0, 255, 0);\nborder-radius: 30px;'
    border_gs = 'background-color: rgb(0, 255, 0);\nborder-radius: 30px;border-color: rgb(0,21,209);border-style: solid;\nborder-width: 2px'
    border_rs = 'background-color: rgb(255, 69, 69);\nborder-radius: 30px;border-color: rgb(0,21,209);border-style: solid;\nborder-width: 2px'
    border_r = 'background-color: rgb(255, 69, 69);\nborder-radius: 30px;'
    border_blues = 'background-color: rgb(85, 170, 255);\nborder-radius: 30px;border-color: rgb(0,21,209);border-style: solid;\nborder-width: 2px'
    border_blue = 'background-color: rgb(85, 170, 255);\nborder-radius: 30px;'
    def __init__(self):
        super(loginidwindow,self).__init__()
        self.initUi()
        self.label_list[1][0].setStyleSheet(self.border_s)
        self.show()

    def initUi(self):
        self.setupUi(self)
        self.label_list=[]
        row_list_init = [self.label_2,self.label_3,self.label_4]
        self.label_list.append(row_list_init)
        formlayout = QGridLayout()
        for i in range(5):
            row_list=[]
            for j in range(len(self.word_table[i])):
                label=QLabel(self.word_table[i][j])
                label.setStyleSheet(self.border_b)
                label.setAlignment(Qt.AlignCenter)
                formlayout.addWidget(label,i,j)
                
                row_list.append(label)
            self.label_list.append(row_list)
        self.widget.setLayout(formlayout) 

    def keyReleaseEvent(self,e):
        if e.key() == Qt.Key_G:
            num=0
            self.second = WindowClass()    
            self.second.showMaximized()
            self.close()
        elif e.key() == Qt.Key_S:
            if self.x < len(self.label_list)-1 and self.y < len(self.label_list[self.x+1]):
                if self.x==0 and self.y==0:
                    self.label_list[self.x][self.y].setStyleSheet(self.border_g)
                elif self.x==0 and self.y==1:
                    self.label_list[self.x][self.y].setStyleSheet(self.border_r)
                elif self.x==0 and self.y==2:
                    self.label_list[self.x][self.y].setStyleSheet(self.border_blue)
                else:
                    self.label_list[self.x][self.y].setStyleSheet(self.border_b)
                self.x+=1
                self.label_list[self.x][self.y].setStyleSheet(self.border_s)
        elif e.key() == Qt.Key_W:
            if self.x > 0 and self.y < len(self.label_list[self.x-1]):
                self.label_list[self.x][self.y].setStyleSheet(self.border_b)
                self.x-=1
                if self.x==0 and self.y==0:
                    self.label_list[self.x][self.y].setStyleSheet(self.border_gs)
                elif self.x==0 and self.y==1:
                    self.label_list[self.x][self.y].setStyleSheet(self.border_rs)
                elif self.x==0 and self.y==2:
                    self.label_list[self.x][self.y].setStyleSheet(self.border_blues)
                else:
                    self.label_list[self.x][self.y].setStyleSheet(self.border_s)
        elif e.key() == Qt.Key_D:
            if self.y == len(self.label_list[self.x])-1:
                self.label_list[self.x][self.y].setStyleSheet(self.border_b)
                self.x=0
                self.y=0
                self.label_list[self.x][self.y].setStyleSheet(self.border_gs)
            if self.y < len(self.label_list[self.x])-1:
                if self.x==0:
                    if self.y==0:
                        self.label_list[self.x][self.y].setStyleSheet(self.border_g)
                        self.y+=1
                        self.label_list[self.x][self.y].setStyleSheet(self.border_rs)
                    elif self.y==1:
                        self.label_list[self.x][self.y].setStyleSheet(self.border_r)
                        self.y+=1
                        self.label_list[self.x][self.y].setStyleSheet(self.border_blues)
                else:
                    self.label_list[self.x][self.y].setStyleSheet(self.border_b)
                    self.y+=1
                    self.label_list[self.x][self.y].setStyleSheet(self.border_s)
        elif e.key() == Qt.Key_A:
            if self.y==0:
                self.label_list[self.x][self.y].setStyleSheet(self.border_b)
                self.x=0
                self.y=0
                self.label_list[self.x][self.y].setStyleSheet(self.border_gs)
            if self.y > 0:
                if self.x==0:
                    if self.y==1:
                        self.label_list[self.x][self.y].setStyleSheet(self.border_r)
                        self.y-=1
                        self.label_list[self.x][self.y].setStyleSheet(self.border_gs)
                    elif self.y==2:
                        self.label_list[self.x][self.y].setStyleSheet(self.border_blue)
                        self.y-=1
                        self.label_list[self.x][self.y].setStyleSheet(self.border_rs)
                else:
                    self.label_list[self.x][self.y].setStyleSheet(self.border_b)
                    self.y-=1
                    self.label_list[self.x][self.y].setStyleSheet(self.border_s)
        elif e.key() == Qt.Key_F:
            if self.x >0:
                self.text = self.word_table[self.x-1][self.y]
                for key, value in self.cons_all.items():
                    if value == self.text:
                        self.label_text += key
                self.label.setText(jamo3(self.label_text))
            elif self.x == 0 and self.y == 1:
                self.text = ''
                self.label_text = ''
                self.label.setText(self.text)
            elif self.x == 0 and self.y == 0:
                self.second = loginpwwindow(self.label.text())    
                self.second.showMaximized()
                self.close()
            elif self.x == 0 and self.y == 2:
                self.second = addidwindow()    
                self.second.showMaximized()
                self.close()

#로그인(비밀번호)
class loginpwwindow(QDialog,QWidget,login_pw_window):
    word_table = [['ㄱ','ㄴ','ㄷ','ㄹ','ㅁ','ㅂ','ㅅ'],
                  ['ㅇ','ㅈ','ㅊ','ㅋ','ㅌ','ㅍ','ㅎ'],
                  ['ㄲ','ㄸ','ㅃ','ㅆ','ㅉ'],
                  ['ㅏ','ㅓ','ㅗ','ㅜ','ㅡ','ㅣ','ㅒ'],
                  ['ㅑ','ㅕ','ㅛ','ㅠ','ㅐ','ㅔ','ㅖ']]
    cons_all= {'r':'ㄱ', 'R':'ㄲ', 's':'ㄴ', 'e':'ㄷ', 'E':'ㄸ', 'f':'ㄹ', 'a':'ㅁ', 'q':'ㅂ', 'Q':'ㅃ', 't':'ㅅ', 'T':'ㅆ',
           'd':'ㅇ', 'w':'ㅈ', 'W':'ㅉ', 'c':'ㅊ', 'z':'ㅋ', 'x':'ㅌ', 'v':'ㅍ', 'g':'ㅎ','k':'ㅏ', 'o':'ㅐ', 'i':'ㅑ', 'O':'ㅒ', 'j':'ㅓ', 'p':'ㅔ', 'u':'ㅕ', 'P':'ㅖ', 'h':'ㅗ', 'hk':'ㅘ', 'ho':'ㅙ', 'hl':'ㅚ',
           'y':'ㅛ', 'n':'ㅜ', 'b':'ㅠ',  'm':'ㅡ', 'l':'ㅣ'}            
    x=1
    y=0
    text=''
    idText=''
    label_text=''
    border_s = 'font: 20pt "AcadEref"; border-color: rgb(0,21,209); \nbackground-color: rgb(170, 242, 248);\nborder-style: solid;\nborder-width: 2px;\nborder-radius: 10px;'
    border_b = 'font: 20pt "AcadEref"; border-color: rgb(170,242,248); \nbackground-color: rgb(170, 242, 248);\nborder-style: solid;\nborder-width: 2px;\nborder-radius: 10px;'
    border_g = 'background-color: rgb(0, 255, 0);\nborder-radius: 30px;'
    border_gs = 'background-color: rgb(0, 255, 0);\nborder-radius: 30px;border-color: rgb(0,21,209);border-style: solid;\nborder-width: 2px'
    border_rs = 'background-color: rgb(255, 69, 69);\nborder-radius: 30px;border-color: rgb(0,21,209);border-style: solid;\nborder-width: 2px'
    border_r = 'background-color: rgb(255, 69, 69);\nborder-radius: 30px;'
    def __init__(self,idText2):
        super(loginpwwindow,self).__init__()
        self.initUi()
        self.idText = idText2
        self.label_list[1][0].setStyleSheet(self.border_s)
        self.show()

    def initUi(self):
        self.setupUi(self)
        self.label_list=[]
        row_list_init = [self.label_3,self.label_4]
        self.label_list.append(row_list_init)
        formlayout = QGridLayout()
        for i in range(5):
            row_list=[]
            for j in range(len(self.word_table[i])):
                label=QLabel(self.word_table[i][j])
                label.setStyleSheet(self.border_b)
                label.setAlignment(Qt.AlignCenter)
                formlayout.addWidget(label,i,j)
                
                row_list.append(label)
            self.label_list.append(row_list)
        self.widget.setLayout(formlayout) 

    def keyReleaseEvent(self,e):
        global idnum
        if e.key() == Qt.Key_G:
            num=0
            self.login = loginidwindow()   
            self.login.showMaximized()
            self.close()
        elif e.key() == Qt.Key_S:
            if self.x < len(self.label_list)-1 and self.y < len(self.label_list[self.x+1]):
                if self.x==0 and self.y==0:
                    self.label_list[self.x][self.y].setStyleSheet(self.border_g)
                elif self.x==0 and self.y==1:
                    self.label_list[self.x][self.y].setStyleSheet(self.border_r)
                else:
                    self.label_list[self.x][self.y].setStyleSheet(self.border_b)
                self.x+=1
                self.label_list[self.x][self.y].setStyleSheet(self.border_s)
        elif e.key() == Qt.Key_W:
            if self.x > 0 and self.y < len(self.label_list[self.x-1]):
                self.label_list[self.x][self.y].setStyleSheet(self.border_b)
                self.x-=1
                if self.x==0 and self.y==0:
                    self.label_list[self.x][self.y].setStyleSheet(self.border_gs)
                elif self.x==0 and self.y==1:
                    self.label_list[self.x][self.y].setStyleSheet(self.border_rs)
                else:
                    self.label_list[self.x][self.y].setStyleSheet(self.border_s)
        elif e.key() == Qt.Key_D:
            if self.y == len(self.label_list[self.x])-1:
                self.label_list[self.x][self.y].setStyleSheet(self.border_b)
                self.x=0
                self.y=0
                self.label_list[self.x][self.y].setStyleSheet(self.border_gs)
            if self.y < len(self.label_list[self.x])-1:
                if self.x==0:
                    if self.y==0:
                        self.label_list[self.x][self.y].setStyleSheet(self.border_g)
                        self.y+=1
                        self.label_list[self.x][self.y].setStyleSheet(self.border_rs)
                else:
                    self.label_list[self.x][self.y].setStyleSheet(self.border_b)
                    self.y+=1
                    self.label_list[self.x][self.y].setStyleSheet(self.border_s)
        elif e.key() == Qt.Key_A:
            if self.y==0:
                self.label_list[self.x][self.y].setStyleSheet(self.border_b)
                self.x=0
                self.y=0
                self.label_list[self.x][self.y].setStyleSheet(self.border_gs)
            if self.y > 0:
                if self.x==0:
                    if self.y==1:
                        self.label_list[self.x][self.y].setStyleSheet(self.border_r)
                        self.y-=1
                        self.label_list[self.x][self.y].setStyleSheet(self.border_gs)
                else:
                    self.label_list[self.x][self.y].setStyleSheet(self.border_b)
                    self.y-=1
                    self.label_list[self.x][self.y].setStyleSheet(self.border_s)
        elif e.key() == Qt.Key_F:
            if self.x >0:
                self.text = self.word_table[self.x-1][self.y]
                for key, value in self.cons_all.items():
                    if value == self.text:
                        self.label_text += key
                self.label.setText(jamo3(self.label_text))                
            elif self.x == 0 and self.y == 1:
                self.text = ''
                self.label_text = ''
                self.label.setText(self.text)
            elif self.x == 0 and self.y == 0:
                sock.sendall(bytes("--login--"+self.idText+"--"+self.label.text()+"\n",'UTF-8'))
                data = sock.recv(10)
                a = str(data.decode())
                a = a[0:1]
                if int(a) == 0:
                    idnum = int(a)
                    self.second = warningwindow('로그인 실패')    
                    self.second.exec()
                    self.main = WindowClass()    
                    self.main.showMaximized()
                    self.close()
                elif int(a) > 0:
                    idnum = int(a)
                    self.second = warningwindow('로그인 성공')    
                    self.second.exec()
                    self.main = WindowClass()    
                    self.main.showMaximized()
                    self.close()          
                

#단어말하기 분류선택
class word1window(QDialog,QWidget,form_word1window):
    fract_name=[]
    fract_code=[]
    word_name=[]
    image_name=[]
    x=0
    y=0
    border_s = 'font: 20pt "AcadEref"; border-color: rgb(0,21,209); \nbackground-color: rgb(170, 242, 248);\nborder-style: solid;\nborder-width: 2px;\nborder-radius: 10px;'
    border_b = 'font: 20pt "AcadEref"; border-color: rgb(170,242,248); \nbackground-color: rgb(170, 242, 248);\nborder-style: solid;\nborder-width: 2px;\nborder-radius: 10px;'

    def __init__(self):
        super(word1window,self).__init__()
        self.dataImport()
        self.initUi()
        self.label_list[0][0].setStyleSheet(self.border_s)
        self.show()

    def initUi(self):
        self.setupUi(self)
        self.label_list=[]
        formlayout = QGridLayout()
        for i in range(len(self.fract_name)):
            row_list=[]
            for j in range(len(self.fract_name[i])):        
                label=QLabel(self.fract_name[i][j])
                label.setAlignment(Qt.AlignCenter)
                label.setStyleSheet(self.border_b)
                formlayout.addWidget(label,i,j)
                row_list.append(label)
                
            self.label_list.append(row_list)
            
        if 2 < len(self.label_list):
                for i in range(2,len(self.label_list)):
                    for j in range(len(self.label_list[i])):
                        self.label_list[i][j].hide()
                
        widget = QWidget()
        widget.setLayout(formlayout) 
        self.scrollArea.setWidget(widget)
        self.scrollArea.setWidgetResizable(True)
        
    def dataImport(self):        
        for i in range(3):
            if i == 0:
                check=0
                sock.sendall(bytes("--"+str(i+1)+"--"+str(idnum)+"\n",'UTF-8'))
                data = sock.recv(1000000)
                    
                list2 = []
                a = str(data.decode())
                result = a[:-2]
                r = result.split('-')
                list_row = []
                for i in range(len(r)):
                    if check == 3:
                        check = 0
                        list2.append(list_row)
                        list_row=[]              
                    list_row.append(r[i])
                    check+=1
                list2.append(list_row)
                self.fract_name = list2.copy()

                sock.sendall(bytes("--12--"+str(idnum)+"\n",'UTF-8'))
                data2 = sock.recv(1000000)               
                list3 = []
                a2 = str(data2.decode())
                check = 0
                result2 = a2[:-2]
                r2 = result2.split('-')
                self.fract_code = r2.copy()
            elif i == 1:
                check=0
                check_out = 0
                sock.sendall(bytes("--"+str(i+1)+"--"+str(idnum)+"\n",'UTF-8'))
                data = sock.recv(1000000)
                list = []
                list_add = []
                a = str(data.decode())
                result = a[:-2]
                r = result.split('@')
                
                for i in range(len(r)):
                    word = r[i].split('-')
                    list_row = []
                    list_row_word=[]
                    
                    for j in range(len(word)):
                        if check == 3:
                            check = 0
                            list_row.append(list_row_word)
                            list_row_word=[]              
                        list_row_word.append(word[j])
                        check+=1                
                    list_row.append(list_row_word)
                    check=0

                    if check_out == 3:
                        check_out=0
                        list.append(list_add)
                        list_add = []
                        list_add.append(list_row)
                        check_out += 1
                    else:
                        list_add.append(list_row)
                        check_out += 1

                list.append(list_add)
                self.word_name=list.copy()
            elif i == 2:
                check3=0
                check_out3 = 0
                a=''
                sock.sendall(bytes("--"+str(i+1)+"--"+str(idnum)+"\n",'UTF-8'))
                data2 = sock.recv(10000)
                sock.sendall(bytes("--32--"+str(idnum)+"\n",'UTF-8'))
                while True:
                    data = sock.recv(100000)
                    a = a + data.decode()
                    if len(a)>=int(data2):
                        break

                list3 = []
                list_add3 = []
                result3 = a[:-2]
                
                r3 = result3.split('@')
                
                for i in range(len(r3)):
                    word3 = r3[i].split('-')
                    list_row3 = []
                    list_row_word3=[]
                    
                    for j in range(len(word3)):
                        if check3 == 3:
                            check3 = 0
                            list_row3.append(list_row_word3)
                            list_row_word3=[]              
                        list_row_word3.append(word3[j])
                        check3+=1                
                    list_row3.append(list_row_word3)
                    check3=0

                    if check_out3 == 3:
                        check_out3=0
                        list3.append(list_add3)
                        list_add3 = []
                        list_add3.append(list_row3)
                        check_out3 += 1
                    else:
                        list_add3.append(list_row3)
                        check_out3 += 1

                list3.append(list_add3)
                self.image_name=list3.copy()
                       
    def keyReleaseEvent(self,e):
        
        if e.key() == Qt.Key_G:
            self.second = WindowClass()    
            self.second.showMaximized()
            self.close()
        elif e.key() == Qt.Key_S:
            if self.x < len(self.label_list)-1 and self.y < len(self.label_list[self.x+1]):
                self.label_list[self.x][self.y].setStyleSheet(self.border_b)
                self.x+=1

                if len(self.label_list) > 2:
                    for i in range(0,len(self.label_list)):
                        for j in range(len(self.label_list[i])):
                            self.label_list[i][j].hide()

                    for i in range(self.x,self.x+2):
                        if i < len(self.label_list):
                            for j in range(len(self.label_list[i])):
                                self.label_list[i][j].show()
                else:
                    for i in range(2):
                        for j in range(len(self.label_list[i])):
                            self.label_list[i][j].show()
                            
                self.label_list[self.x][self.y].setStyleSheet(self.border_s)
        elif e.key() == Qt.Key_W:
            if self.x > 0:
                self.label_list[self.x][self.y].setStyleSheet(self.border_b)
                self.x-=1
                if self.y >= len(self.label_list[self.x]):
                    self.y = len(self.label_list[self.x])-1                    
               
                self.label_list[self.x][self.y].setStyleSheet(self.border_s)
                for i in range(0,len(self.label_list)):
                    for j in range(len(self.label_list[i])):
                        self.label_list[i][j].hide()
                for i in range(self.x,self.x+2):
                    if i < len(self.label_list):
                        for j in range(len(self.label_list[i])):
                            self.label_list[i][j].show()
                    
        elif e.key() == Qt.Key_D:
            if self.y < len(self.label_list[self.x])-1:
                self.label_list[self.x][self.y].setStyleSheet(self.border_b)
                self.y+=1
                self.label_list[self.x][self.y].setStyleSheet(self.border_s)
        elif e.key() == Qt.Key_A:
                self.label_list[self.x][self.y].setStyleSheet(self.border_b)
                self.y-=1
                self.label_list[self.x][self.y].setStyleSheet(self.border_s)
        elif e.key() == Qt.Key_F:
            self.word2 = word2window(self.word_name,self.image_name,self.x,self.y)
            self.word2.showMaximized()
            self.close()

#단어선택 및 출력
class word2window(QDialog,QWidget,form_word2window):    
    x=1
    y=0
    fract_x = 0
    fract_y = 0
    word_name1 =[]
    image_name1 =[]
    text = ''
    pos=0 #스크롤 위치 
    border_s = 'font: 20pt "AcadEref"; border-color: rgb(0,21,209); \nbackground-color: rgb(170, 242, 248);\nborder-style: solid;\nborder-width: 2px;\nborder-radius: 10px;'
    border_b = 'font: 20pt "AcadEref"; border-color: rgb(170,242,248); \nbackground-color: rgb(170, 242, 248);\nborder-style: solid;\nborder-width: 2px;\nborder-radius: 10px;'
    border_g = 'background-color: rgb(0, 255, 0);\nborder-radius: 30px;'
    border_gs = 'background-color: rgb(0, 255, 0);\nborder-radius: 30px;border-color: rgb(0,21,209);border-style: solid;\nborder-width: 2px'
    border_rs = 'background-color: rgb(255, 69, 69);\nborder-radius: 30px;border-color: rgb(0,21,209);border-style: solid;\nborder-width: 2px'
    border_r = 'background-color: rgb(255, 69, 69);\nborder-radius: 30px;'
    def __init__(self,word_name,image_name,x,y):
        super(word2window,self).__init__()
        self.word_name1 = word_name.copy()
        self.image_name1 = image_name.copy()
        self.fract_x = x
        self.fract_y = y
        self.initUi()
        self.label_list[1][0].setStyleSheet(self.border_s)
        pygame.mixer.init()
        self.show()

    def initUi(self):
        self.setupUi(self)
        self.label_list=[]
        row_list_init = [self.sound,self.remove]
        self.label_list.append(row_list_init)
        formlayout = QGridLayout()
        for i in range(len(self.word_name1[self.fract_x][self.fract_y])):
            row_list=[]
            for j in range(len(self.word_name1[self.fract_x][self.fract_y][i])):
                if self.image_name1[self.fract_x][self.fract_y][i][j]=='null':
                    ss="b\'iVBORw0KGgoAAAANSUhEUgAAArgAAAI0CAIAAAB50M3bAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAm1SURBVHhe7duxahRhGEDR3RVjiJUQAqYxZfAB9P3LxDIQi2BlYRohYCQJODNO1oCF3sLFajin2Bn2Bf7L93+znqZpBQDwN5unJwDAH4QCAJCEAgCQhAIAkIQCAJCEAgCQhAIAkIQCAJCEAgCQhAIAkIQCAJCEAgCQhAIAkIQCAJCEAgCQhAIAkIQCAJCEAgCQhAIAkIQCAJCEAgCQhAIAkIQCAJCEAgCQhAIAkIQCAJCEAgCQhAIAkIQCAJCEAgCQhAIAkIQCAJCEAgCQhAIAkIQCAJCEAgCQhAIAkIQCAJCEAgCQhAIAkIQCAJCEAgCQhAIAkIQCAJCEAgCQhAIAkIQCAJCEAgCQhAIAkIQCAJCEAgCQhAIAkIQCAJCEAgCQhAIAkIQCAJCEAgCQhAIAkIQCAJCEAgCQhAIAkIQCAJCEAgCQhAIAkIQCAJCEAgCQhAIAkIQCAJCEAgCQhAIAkIQCAJCEAgCQhAIAkIQCAJCEAgCQhAIAkIQCAJCEAgCQhAIAkIQCAJCEAgCQhAIAkIQCAJCEAgCQhAIAkIQCAJCEAgCQhAIAkIQCAJCEAgCQhAIAkIQCAJCEAgCQhAIAkIQCAJCEAgCQhAIAkIQCAJCEAgCQhAIAkIQCAJCEAgCQhAIAkIQCAJCEAgCQhAIAkIQCAJCEAgCQhAIAkIQCAJCEAgCQhAIAkIQCAJCEAgCQhAIAkIQCAJCEAgCQhAIAkIQCAJCEAgCQhAIAkIQCAJCEAgCQhAIAkIQCAJCEAgCQhAIAkIQCAJCEAgCQhAIAkIQCAJCEAgCQhAIAkIQCAJCEAgCQhAIAkIQCAJCEAgCQhAIAkIQCAJCEAgCQhAIAkIQCAJCEAgCQhAIAkIQCAJCEAgCQhAIAkIQCAJCEAgCQhAIAkIQCAJCEAgCQhAIAkIQCAJCEAgCQhAIAkIQCAJCEAgCQhAIAkIQCAJCEAgCQhAIAkIQCAJCEAgCQhAIAkIQCAJCEAgCQhAIAkIQCAJCEAgCQhAIAkIQCAJCEAgCQhAIAkIQCAJCEAgCQhAIAkIQCAJCEAgCQhAIAkIQCAJCEAgCQhAIAkIQCAJCEAgCQhAIAkIQCAJCEAgCQhAIAkIQCAJCEAgCQhAIAkIQCAJCEAgCQhAIAkIQCAJCEAgCQhAIAkIQCAJCEAgCQhAIAkIQCAJCEAgCQhAIAkIQCAJCEAgCQhAIAkIQCAJCEAgCQhAIAkIQCAJCEAgCQhAIAkIQCAJCEAgCQhAIAkIQCAJCEAgCQhAIAkIQCAJCEAgCQhAIAkIQCAJCEAgCQhAIAkIQCAJCEAgCQhAIAkIQCAJCEAgCQhAIAkIQCAJCEAgCQhAIAkIQCAJCEAgCQhAIAkIQCAJCEAgCQhAIAkIQCAJCEAgCQhAIAkIQCAJCEAgCQhAIAkIQCAJCEAgCQhAIAkIQCAJCEAgCQhAIAkIQCAJCEAgCQ1tM0Pb0CAAsyH/Hj+HjKbzbr2a8//5VQAIAFGobh9vbuy/XXORGOjw8PDvafbXa5RnD1AABLM03TXAlnZ5eraTX8GD6cf7y/f9htNGCiAABLMwzj1dXn+eX09M38e3Hx6eDl/snJ6x2GCiYKALBA6/XvWcA4TuuVHQUAYOvx6uH73fnZ5dHRq7kSbm6+vXv/dv/F3g4rjUIBABZoGMf7u4fr7TLj6+PDvb3nuy0zCgUAWKb5iB+3p/z260hXDwDA/2aZEQBIQgEASEIBAEhCAQBIQgEASEIBAEhCAQBIQgEASEIBAEhCAQBIQgEASEIBAEhCAQBIQgEASEIBAEhCAQBIQgEASEIBAEhCAQBIQgEASEIBAEhCAQBIQgEASEIBAEhCAQBIQgEASEIBAEhCAQBIQgEASEIBAEhCAQBIQgEASEIBAEhCAQBIQgEASEIBAEhCAQBIQgEASEIBAEhCAQBIQgEASEIBAEhCAQBIQgEASEIBAEhCAQBIQgEASEIBAEhCAQBIQgEASEIBAEhCAQBIQgEASEIBAEhCAQBIQgEASEIBAEhCAQBIQgEASEIBAEhCAQBIQgEASEIBAEhCAQBIQgEASEIBAEhCAQBIQgEASEIBAEhCAQBIQgEASEIBAEhCAQBIQgEASEIBAEhCAQBIQgEASEIBAEhCAQBIQgEASEIBAEhCAQBIQgEASEIBAEhCAQBIQgEASEIBAEhCAQBIQgEASEIBAEhCAQBIQgEASEIBAEhCAQBIQgEASEIBAEhCAQBIQgEASEIBAEhCAQBIQgEASEIBAEhCAQBIQgEASEIBAEhCAQBIQgEASEIBAEhCAQBIQgEASEIBAEhCAQBIQgEASEIBAEhCAQBIQgEASEIBAEhCAQBIQgEASEIBAEhCAQBIQgEASEIBAEhCAQBIQgEASEIBAEhCAQBIQgEASEIBAEhCAQBIQgEASEIBAEhCAQBIQgEASEIBAEhCAQBIQgEASEIBAEhCAQBIQgEASEIBAEhCAQBIQgEASEIBAEhCAQBIQgEASEIBAEhCAQBIQgEASEIBAEhCAQBIQgEASEIBAEhCAQBIQgEASEIBAEhCAQBIQgEASEIBAEhCAQBIQgEASEIBAEhCAQBIQgEASEIBAEhCAQBIQgEASEIBAEhCAQBIQgEASEIBAEhCAQBIQgEASEIBAEhCAQBIQgEASEIBAEhCAQBIQgEASEIBAEhCAQBIQgEASEIBAEhCAQBIQgEASEIBAEhCAQBIQgEASEIBAEhCAQBIQgEASEIBAEhCAQBIQgEASEIBAEhCAQBIQgEASEIBAEhCAQBIQgEASEIBAEhCAQBIQgEASEIBAEhCAQBIQgEASEIBAEhCAQBIQgEASEIBAEhCAQBIQgEASEIBAEhCAQBIQgEASEIBAEhCAQBIQgEASEIBAEhCAQBIQgEASEIBAEhCAQBIQgEASEIBAEhCAQBIQgEASEIBAEhCAQBIQgEASEIBAEhCAQBIQgEASEIBAEhCAQBIQgEASEIBAEhCAQBIQgEASEIBAEhCAQBIQgEASEIBAEhCAQBIQgEASEIBAEhCAQBIQgEASEIBAEhCAQBIQgEASEIBAEhCAQBIQgEASEIBAEhCAQBIQgEASEIBAEhCAQBIQgEASEIBAEhCAQBIQgEASEIBAEhCAQBIQgEASEIBAEhCAQBIQgEASEIBAEhCAQBIQgEASEIBAEhCAQBIQgEASEIBAEhCAQBIQgEASEIBAEhCAQBIQgEASEIBAEhCAQBIQgEASEIBAEhCAQBIQgEASEIBAEhCAQBIQgEASEIBAEhCAQBIQgEASEIBAEhCAQBIQgEASEIBAEhCAQBIQgEACKvVT+EWbNG26YEZAAAAAElFTkSuQmCC\'"
                    imagen=QImage()
                    data = ast.literal_eval(ss)
                    bytearr = QByteArray.fromBase64(data)
                    imagen.loadFromData( bytearr, 'PNG' )
                    pix = QPixmap.fromImage(imagen)
                    pix_re=pix.scaled(120,165,Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
                else:
                    imagen=QImage()
                    ss="b\'"+self.image_name1[self.fract_x][self.fract_y][i][j]+"\'"
                    data = ast.literal_eval(ss)
                    bytearr = QByteArray.fromBase64(data)
                    imagen.loadFromData( bytearr, 'PNG' )
                    pix = QPixmap.fromImage(imagen)
                    pix_re=pix.scaled(120,165,Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        
                box = QVBoxLayout()
                label=QLabel(self.word_name1[self.fract_x][self.fract_y][i][j])
                label.setAlignment(Qt.AlignCenter)
                
                label2=QLabel()
                label2.setAlignment(Qt.AlignHCenter)
                label2.setPixmap(pix_re)
                label2.setAlignment(Qt.AlignHCenter)
                
                box.addWidget(label2)
                box.addWidget(label)

                widget = QWidget()
                widget.setLayout(box)
                widget.setStyleSheet(self.border_b)
                formlayout.addWidget(widget,i,j)
                row_list.append(widget)
                
            self.label_list.append(row_list)
            
        if 2 < len(self.label_list):
                for i in range(3,len(self.label_list)):
                    for j in range(len(self.label_list[i])):
                        self.label_list[i][j].hide()        
        widget2 = QWidget()
        widget2.setLayout(formlayout) 
        self.scrollArea.setWidget(widget2)
        self.scrollArea.setWidgetResizable(True)
        
    def keyReleaseEvent(self,e):
        
        if e.key() == Qt.Key_G:
            self.word2 = word1window()
            self.word2.showMaximized()
            self.deleteLater()
        elif e.key() == Qt.Key_S:
            if self.x < len(self.label_list)-1 and self.y < len(self.label_list[self.x+1]):
                if self.x==0 and self.y==0:
                    self.label_list[self.x][self.y].setStyleSheet(self.border_g)
                elif self.x==0 and self.y==1:
                    self.label_list[self.x][self.y].setStyleSheet(self.border_r)
                else:
                    self.label_list[self.x][self.y].setStyleSheet(self.border_b)
                self.x+=1
                
                for i in range(1,len(self.label_list)):
                    for j in range(len(self.label_list[i])):
                        self.label_list[i][j].hide()
                
                for i in range(self.x,self.x+2):
                    if i < len(self.label_list):
                        for j in range(len(self.label_list[i])):
                            self.label_list[i][j].show()

                if len(self.label_list) > 2:
                    if self.x == len(self.label_list)-1 and self.x > 1:
                        for j in range(len(self.label_list[self.x-1])):
                                self.label_list[self.x-1][j].show()
                            
                self.label_list[self.x][self.y].setStyleSheet(self.border_s)
        elif e.key() == Qt.Key_W:
            if self.x > 0:
                self.label_list[self.x][self.y].setStyleSheet(self.border_b)
                self.x-=1
                if self.y >= len(self.label_list[self.x]):
                    self.y = len(self.label_list[self.x])-1
                if self.x==0 and self.y==0:
                    self.label_list[self.x][self.y].setStyleSheet(self.border_gs)
                    for i in range(1,len(self.label_list)):
                        for j in range(len(self.label_list[i])):
                            self.label_list[i][j].hide()
                    for i in range(self.x+1,self.x+3):
                        if i < len(self.label_list):
                            for j in range(len(self.label_list[i])):
                                self.label_list[i][j].show()
                elif self.x==0 and self.y==1:
                    self.label_list[self.x][self.y].setStyleSheet(self.border_rs)
                    for i in range(1,len(self.label_list)):
                        for j in range(len(self.label_list[i])):
                            self.label_list[i][j].hide()
                    for i in range(self.x+1,self.x+3):
                        if i < len(self.label_list):
                            for j in range(len(self.label_list[i])):
                                self.label_list[i][j].show()                    
                else:
                    self.label_list[self.x][self.y].setStyleSheet(self.border_s)
                    for i in range(1,len(self.label_list)):
                        for j in range(len(self.label_list[i])):
                            self.label_list[i][j].hide()
                    for i in range(self.x,self.x+2):
                        if i < len(self.label_list):
                            for j in range(len(self.label_list[i])):
                                self.label_list[i][j].show()
                    
        elif e.key() == Qt.Key_D:
            if self.y == len(self.label_list[self.x])-1:
                self.label_list[self.x][self.y].setStyleSheet(self.border_b)
                self.x=0
                self.y=0
                self.label_list[self.x][self.y].setStyleSheet(self.border_gs)
            if self.y < len(self.label_list[self.x])-1:
                if self.x==0:
                    if self.y==0:
                        self.label_list[self.x][self.y].setStyleSheet(self.border_g)
                        self.y+=1
                        self.label_list[self.x][self.y].setStyleSheet(self.border_rs)
                else:
                    self.label_list[self.x][self.y].setStyleSheet(self.border_b)
                    self.y+=1
                    self.label_list[self.x][self.y].setStyleSheet(self.border_s)
        elif e.key() == Qt.Key_A:
            if self.y==0:
                self.label_list[self.x][self.y].setStyleSheet(self.border_b)
                self.x=0
                self.y=0
                self.label_list[self.x][self.y].setStyleSheet(self.border_gs)
            if self.y > 0:
                if self.x==0:
                    if self.y==1:
                        self.label_list[self.x][self.y].setStyleSheet(self.border_r)
                        self.y-=1
                        self.label_list[self.x][self.y].setStyleSheet(self.border_gs)
                else:
                    self.label_list[self.x][self.y].setStyleSheet(self.border_b)
                    self.y-=1
                    self.label_list[self.x][self.y].setStyleSheet(self.border_s)
        elif e.key() == Qt.Key_F:
            if self.x >0:
                self.text += self.word_name1[self.fract_x][self.fract_y][self.x-1][self.y]
                self.text_label.setText(str(self.text))
            elif self.x == 0 and self.y == 0:
                at = gTTS(text=self.text,lang="ko")
                at.save("ta.mp3")
                pygame.mixer.music.load("ta.mp3")
                pygame.mixer.music.play()
                while(pygame.mixer.music.get_busy()):
                    b=0
                pygame.mixer.music.unload()
            elif self.x == 0 and self.y == 1:
                self.text = ''
                self.text_label.setText(self.text)

#자모결합함수                
def jamo3(text2):
    cons = {'r':'ㄱ', 'R':'ㄲ', 's':'ㄴ', 'e':'ㄷ', 'E':'ㄸ', 'f':'ㄹ', 'a':'ㅁ', 'q':'ㅂ', 'Q':'ㅃ', 't':'ㅅ', 'T':'ㅆ',
           'd':'ㅇ', 'w':'ㅈ', 'W':'ㅉ', 'c':'ㅊ', 'z':'ㅋ', 'x':'ㅌ', 'v':'ㅍ', 'g':'ㅎ'}
    vowels = {'k':'ㅏ', 'o':'ㅐ', 'i':'ㅑ', 'O':'ㅒ', 'j':'ㅓ', 'p':'ㅔ', 'u':'ㅕ', 'P':'ㅖ', 'h':'ㅗ', 'hk':'ㅘ', 'ho':'ㅙ', 'hl':'ㅚ',
           'y':'ㅛ', 'n':'ㅜ', 'nj':'ㅝ', 'np':'ㅞ', 'nl':'ㅟ', 'b':'ㅠ',  'm':'ㅡ', 'ml':'ㅢ', 'l':'ㅣ'}
    cons_double = {'rt':'ㄳ', 'sw':'ㄵ', 'sg':'ㄶ', 'fr':'ㄺ', 'fa':'ㄻ', 'fq':'ㄼ', 'ft':'ㄽ', 'fx':'ㄾ', 'fv':'ㄿ', 'fg':'ㅀ', 'qt':'ㅄ'}
    cons_all= {'r':'ㄱ', 'R':'ㄲ', 's':'ㄴ', 'e':'ㄷ', 'E':'ㄸ', 'f':'ㄹ', 'a':'ㅁ', 'q':'ㅂ', 'Q':'ㅃ', 't':'ㅅ', 'T':'ㅆ',
           'd':'ㅇ', 'w':'ㅈ', 'W':'ㅉ', 'c':'ㅊ', 'z':'ㅋ', 'x':'ㅌ', 'v':'ㅍ', 'g':'ㅎ','k':'ㅏ', 'o':'ㅐ', 'i':'ㅑ', 'O':'ㅒ', 'j':'ㅓ', 'p':'ㅔ', 'u':'ㅕ', 'P':'ㅖ', 'h':'ㅗ', 'hk':'ㅘ', 'ho':'ㅙ', 'hl':'ㅚ',
           'y':'ㅛ', 'n':'ㅜ', 'b':'ㅠ',  'm':'ㅡ', 'l':'ㅣ'}
    result = ''
    vc = ''
    for t in text2:
        if t in cons :
            vc+='c'
        elif t in vowels:
            vc+='v'
        else:
            vc+='!'
    vc = vc.replace('cvv', 'fVV').replace('cv', 'fv').replace('cc', 'dd')
    i = 0
    while i < len(text2):
        v = vc[i]
        t = text2[i]
        j = 1
        try:
            if v == 'f' or v == 'c':  
                result+=cons[t]
            elif v == 'V':
                result+=vowels[text2[i:i+2]]
                j+=1
            elif v == 'v':
                result+=vowels[t]
            elif v == 'd':
                result+=cons_double[text2[i:i+2]]
                j+=1
            else:
                result+=t
        except:
            print(t)
            if t in cons_all:
                result+=cons_all[t]
            else:
                result+=t                   
        i += j
    return join_jamos(result)
    
if __name__ == '__main__':
    sock = socket(AF_INET,SOCK_STREAM)
    sock.connect(('aszx1234.duckdns.org',6000));
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.showMaximized()
    app.exec_()
    sock.close()
