from socket import *
from select import select
import sys

sock = socket(AF_INET,SOCK_STREAM)
sock.connect(('localhost',6000));

for i in range(2):
    if i == 0:
        check=0
        sock.sendall(bytes(str(i+1)+"--aa\n",'UTF-8'))
        data = sock.recv(1024)
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
        print(list2)
    elif i == 1:
        check=0
        check_out = 0
        sock.sendall(bytes(str(i+1)+"--aa\n",'UTF-8'))
        data = sock.recv(1024)
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
        print(list)




sock.close()
