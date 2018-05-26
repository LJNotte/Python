# coding:utf-8
from tkinter import *
from tkinter import scrolledtext
import threading
import time
import queue

myqueue = queue.Queue()

class Producer(threading.Thread):
    def __init__(self, threadname):
        threading.Thread.__init__(self, name = threadname)
    def run(self):
        global myqueue
        myqueue.put(self.getName())
        text.insert(END,self.getName() + ' put ' +  self.getName() + ' to queue.\n')
        time.sleep(0.1)

class Consumer(threading.Thread):
    def __init__(self, threadname):
        threading.Thread.__init__(self, name = threadname)
    def run(self):
        global myqueue
        text.insert(END,self.getName() + ' get ' +  myqueue.get() + ' from queue.\n')

def fun():
    plist = []
    clist = []

    for i in range(10):
        p = Producer('Producer' + str(i))
        plist.append(p)
        c = Consumer('Consumer' + str(i))
        clist.append(c)
    for i in plist:
        i.start()
       # i.join()
    for i in clist:
        i.start()
       # i.join()
    #text.insert(END,  ' get ' +  ' from queue. \n')


root = Tk()
root.title('多线程实例——生产者和消费者问题')  # 窗口标题
root.geometry('400x500+200+200')  # 窗口呈现位置

textlabel = Label(root)
textlabel.grid(row=0, column=0,sticky=E+W)
scrolW = 40 # 设置文本框的长度
scrolH = 25 # 设置文本框的高度
text = scrolledtext.ScrolledText(root, width=scrolW, height=scrolH)
text.grid(row=0, column=0,sticky=E+W)
button = Button(root, text='点击继续', font=('微软雅黑', 10), command=fun)
button.grid()
var = StringVar()  # 设置变量
label = Label(root, font=('微软雅黑', 10), fg='red', textvariable=var)
label.grid()



root.mainloop()
