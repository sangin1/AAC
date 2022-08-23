import os
import sys
import pyttsx3
from socket import *
from select import select
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PIL import Image
from io import BytesIO
import base64
import matplotlib.pyplot as plt
import ast
from hangul_utils import join_jamos

def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

form = resource_path('main.ui')
form_class = uic.loadUiType(form)[0]

form_word1 = resource_path('word1.ui')
form_word1window = uic.loadUiType(form_word1)[0]

form_word2 = resource_path('word2.ui')
form_word2window = uic.loadUiType(form_word2)[0]

login_id = resource_path('loginid.ui')
loin_id_window = uic.loadUiType(login_id)[0]

idnum=0

#mainpage
class WindowClass(QMainWindow,QWidget, form_class):
    cus = 0
    border_s = 'border-color: rgb(0,21,209); \nbackground-color: rgb(170, 242, 248);\nborder-style: solid;\nborder-width: 2px;\nborder-radius: 10px;'
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

        #이미지추가 예시
        #self.pix=QPixmap('img/1.PNG')
        #self.label_list[0].setPixmap(self.pix)

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
            elif self.cus == 3:
                self.login = loginidwindow()   
                self.login.show()
                self.close()

#로그인(아이디)
class loginidwindow(QDialog,QWidget,loin_id_window):
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
                formlayout.addWidget(label,i,j)
                
                row_list.append(label)
            self.label_list.append(row_list)
        self.widget.setLayout(formlayout) 

    def keyPressEvent(self,e):
        if e.key() == Qt.Key_G:
            self.second = WindowClass()    
            self.second.show()
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

#분류선택
class word1window(QDialog,QWidget,form_word1window):
    fract_name=[]
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
                for i in range(3,len(self.label_list)):
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
                sock.sendall(bytes(str(i+1)+"--"+str(idnum)+"\n",'UTF-8'))
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
            elif i == 1:
                check=0
                check_out = 0
                sock.sendall(bytes(str(i+1)+"--"+str(idnum)+"\n",'UTF-8'))
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
                sock.sendall(bytes(str(i+1)+"--"+str(idnum)+"\n",'UTF-8'))
                data2 = sock.recv(100000)
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
                       
    def keyPressEvent(self,e):
        
        if e.key() == Qt.Key_G:
            self.second = WindowClass()    
            self.second.show()
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
            self.word2.show()
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
        self.show()
        self.engine = pyttsx3.init()

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
                label.setAlignment(Qt.AlignHCenter)
                
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
        
    def keyPressEvent(self,e):
        
        if e.key() == Qt.Key_G:
            self.word2 = word1window()
            self.word2.show()
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
                self.engine.say(self.text)
                self.engine.runAndWait()
            elif self.x == 0 and self.y == 1:
                self.text = ''
                self.text_label.setText(self.text)
        
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
    sock.connect(('localhost',6000));
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()
    sock.close()
