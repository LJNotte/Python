from tkinter import *
from tkinter import scrolledtext
import requests
import json

url_list = []
mes_list = []
def Craw_movie():
    ind = 0
    for i in url_list:
        print ("link   " + i)
        scr.insert(END, mes_list[ind] + " 推荐的前20名电影如下 ： \n")
        ind += 1
        html = requests.get(i).text  # 这里一般先打印一下html内容，看看是否有内容再继续。
        # print (html)
        movie = json.loads(html)
        result = []
        if movie and 'subjects' in movie.keys():
            for item in movie.get('subjects'):
                film = {
                    'rate': item.get('rate'),
                    'title': item.get('title'),
                    'url': item.get('url'),
                    'id': item.get('id'),
                }
                result.append(film)
                #    print("++++++++++++++++++++++++++++++++++++++++++++++++++++")
                # for i in  result:
                #    print (i)i
                #    print ("\n")
                scr.insert(END,film['title'] + " " + film['rate'] + " " + film['url'] + '\n')
        scr.insert(END, "======================================================================= \n\n\n\n")

def MyEvent1():
     url = "https://movie.douban.com/j/search_subjects?type=movie&tag=%E5%8D%8E%E8%AF%AD&sort=rank&page_limit=20&page_start=0"
     url_list.append(url)
     mes_list.append('华语')


def MyEvent2():
    url = "https://movie.douban.com/j/search_subjects?type=movie&tag=%E6%AC%A7%E7%BE%8E&sort=rank&page_limit=20&page_start=0"
    url_list.append(url)
    mes_list.append('欧美')


def MyEvent3():
    url = "https://movie.douban.com/j/search_subjects?type=movie&tag=%E9%9F%A9%E5%9B%BD&sort=rank&page_limit=20&page_start=0"
    url_list.append(url)
    mes_list.append('韩国')


def MyEvent4():
    url = "https://movie.douban.com/j/search_subjects?type=movie&tag=%E6%97%A5%E6%9C%AC&sort=rank&page_limit=20&page_start=0"
    url_list.append(url)
    mes_list.append('日本')

def cls():
    mes_list = []
    url_list = []
    scr.delete(0.0, END)

#list1=["hhh","aaa"]
#str = list1[1]
#print(str)
top=Tk()
top.wm_title("多线程爬虫 + GUI")
top.geometry("600x500+300+200")

c1=Checkbutton(top,text="华语",command= MyEvent1)
c1.pack()

c2=Checkbutton(top,text="欧美",command= MyEvent2)
c2.pack()

c3=Checkbutton(top,text="韩国",command= MyEvent3)
c3.pack()

c4 = Checkbutton(top,text="日本",command=MyEvent4)
c4.pack()

button = Button(top, text='获取', font=('微软雅黑', 10), command=Craw_movie)
button.pack()   # 设置其在界面中出现的位置  column代表列   row 代表行
button = Button(top, text='清除', font=('微软雅黑', 10), command=cls)
button.pack()   # 设置其在界面中出现的位置  column代表列   row 代表行
# 滚动文本框
scrolW = 150 # 设置文本框的长度
scrolH = 80 # 设置文本框的高度
scr = scrolledtext.ScrolledText(top, width=scrolW, height=scrolH)
scr.pack()


top.mainloop()
