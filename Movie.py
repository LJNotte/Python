# coding:utf-8

import json
from lxml import etree
import requests
import re
from bs4 import BeautifulSoup as bs


def Do_Login():
    s = requests.Session()
    url_login = 'http://accounts.douban.com/login'
    url_contacts = 'https://www.douban.com/contacts/list'

    formdata = {
        'source': 'index_nav',
        'redir': 'https://www.douban.com',
        'form_email': '22222',
        'form_password': '111111',
        'login': u'登录'
    }
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

    r = s.post(url_login, data=formdata, headers=headers)
    content = r.text

    soup = bs(content, 'lxml')
    captcha = soup.find('img', id='captcha_image')

    if captcha:
        captcha_url = captcha['src']
        re_captcha_id = r'<input type-"hidden" name="captcha-id" value="(.*?)"/'
        captcha_id = re.findall(re_captcha_id, content)
        print(captcha_id)
        print(captcha_url)
        captcha_text = input('Please input 验证码 : ')
        formdata['captcha-solution'] = captcha_text
        formdata['captcha-id'] = captcha_id
        r = s.post(url_login, data=formdata, headers=headers)



#获取每个页面的url
def Get_page_link():
    start_list = []
    for i in range(0, 1):
        url = 'https://movie.douban.com/j/search_subjects?type=movie&tag=%E5%8D%8E%E8%AF%AD&sort=rank&page_limit=20&page_start=' + str(i * 20)
        start_list.append(url)
    #print (start_list)
    return start_list

#获取每个电影的url
def Get_movie_link(url_list):
    for link in url_list:
         url = link;
         html = requests.get(url).text    #这里一般先打印一下html内容，看看是否有内容再继续。
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
                #'cover': item.get('cover')
                }
                result.append(film)
            print("++++++++++++++++++++++++++++++++++++++++++++++++++++")
            for i in  result:
                print (i)
                print ("\n")
    return result

#获取每个电影的信息
def Get_movie_Info(movie_url):
    movie_info = []
    for i in movie_url:
        movie = {}
        movie['title'] = i['title']
        movie['rate'] = i['rate']
        html = requests.get(i['url']).content
        page = etree.HTML(html)
        info = page.xpath("//*[@id='info']")[0]

        movie['director'] = info.xpath("./span[1]/span[2]/a/text()")[0]
        movie['screenwriter'] = info.xpath("./span[2]/span[2]/a/text()")[0]
        movie['actors'] = '/'.join(info.xpath("./span[3]/span[2]/a/text()"))
        movie['type'] = '/'.join(info.xpath("./span[@property='v:genre']/"
                                            "text()"))
        movie['initialReleaseDate'] = '/'. \
            join(info.xpath(".//span[@property='v:initialReleaseDate']/text()"))
        movie['runtime'] = \
            info.xpath(".//span[@property='v:runtime']/text()")[0]

        star = page.xpath("//*[@id='interest_sectl']")[0]
        movie['five_star'] = star.xpath("./div[1]/div[3]/div[1]/span[2]/text()")[0]
        movie['four_star'] = star.xpath("./div[1]/div[3]/div[2]/span[2]/text()")[0]
        movie['three_star'] = star.xpath("./div[1]/div[3]/div[3]/span[2]/text()")[0]
        movie['two_star'] = star.xpath("./div[1]/div[3]/div[4]/span[2]/text()")[0]
        movie['one_star'] = star.xpath("./div[1]/div[3]/div[5]/span[2]/text()")[0]

       # print (movie)
        movie_info.append(movie)
   # print ("=======================================================")
    return movie_info;

#获取每个电影评论的信息
def Get_Comment_Info(movie_url):
    comment_info = []
    for i in movie_url:
        comment = {}
        for j in range(0,1):
            url ="https://movie.douban.com/subject/" + str(i['id']) + "/comments?start="+str(j * 20)+"&limit=20&sort=new_score&status=P&percent_type="
            #url = "https://movie.douban.com/subject/1291546/comments?start=20&limit=20&sort=new_score&status=P&percent_type="
            #print (url)
            html = requests.get(url).content
            page = etree.HTML(html)

            info = page.xpath("//*[@id='comments']")[0]
            #print ("========================================== ")
           # print (info)
            for k in range(1,21):
                comment = {}
                comment ['name'] = info.xpath("./ div["+str(k) + "] / div[2] / h3 / span[2] / a /text()")[0]
                comment['href'] = info.xpath("./ div["+str(k) + "] / div[2] / h3 / span[2] / a /@href")[0]
                comment['content'] = info.xpath("./ div["+str(k) + "] / div[2] / p/text()")[0]
                #print (comment)
                comment_info.append(comment)

    return comment_info

def Get_User_Info(comment_info):
    user_info = []
    for i in comment_info:
        try:
            for j in range(0,6):
                url = i['href'] + "collect?start="+str(j * 15 )+"&sort=time&rating=all&filter=all&mode=grid"
                url = url.replace("www","movie")
                print ("user  : " + url)
                html = requests.get(url).content
                page = etree.HTML(html)

                info = page.xpath("//*[@id='content']/div[2]/div[1]/div[2]")[0]
                for k in range(1,16):
                    user = {}
                    user ['movie_title'] = info.xpath("./div["+str(k)+"]/div[2]/ul/li[1]/a/em/text()")[0]
                    user['movie_date'] = info.xpath("./ div["+str(k)+"] / div[2] / ul / li[3] / span/text()")[0]
                    user['movie_comment'] = info.xpath("./ div["+str(k)+"] /div[2]/ul/li[4]/span[1]/text()")[0]
                    print (user)
                    user_info.append(user)
        except IndexError:
             print ("no comment about film")

    return user_info



#爬取电影信息的主要逻辑函数
def Func_Craw_Movie():
   #1. 初始化部分
   url_list = []
   movie_list = []
   movie_info = []

   #2. 逻辑部分
   url_list = Get_page_link()
   movie_list = Get_movie_link(url_list)
   movie_info = Get_movie_Info(movie_list)

   #3. 检验
   for i in movie_info:
       print (i)
       print ("\n")




#爬取电影评论的逻辑函数
def Func_Craw_Comment():
   #1. 初始化部分
   url_list = []
   movie_list = []
   comment_info = []

   #2. 逻辑部分
   url_list = Get_page_link()
   movie_list = Get_movie_link(url_list)
   comment_info = Get_Comment_Info(movie_list)

   #3. 检验
   for i in comment_info:
       print (i)
       print ("\n")

#爬取电影评论的逻辑函数
def Func_Craw_User():
   #1. 初始化部分
   url_list = []
   movie_list = []
   comment_info = []
   user_info = []

   #2. 逻辑部分
   url_list = Get_page_link()
   movie_list = Get_movie_link(url_list)
   comment_info = Get_Comment_Info(movie_list)
   user_info =  Get_User_Info(comment_info)

   #3. 检验
   for i in user_info:
       print (i)
       print ("\n")

if __name__ == '__main__':
   # Do_Login()
    Func_Craw_User()
