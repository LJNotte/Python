# Python

## 1.爬虫
要求： 爬取豆瓣电影中：华语、欧美、韩国、日本每个标签下按照**评价排序的**全部电影，需要如下信息
1. 每个电影的电影名字、导演、编剧、主演、类型、国家、上映日期、片长、电影评分、以及每个电影的星级的百分比数据
2. 每个电影热门点评中的前100个评分及其评分人
3. 进入每个评分人的主页，爬取其看过的电影信息，以及对电影的评分
将上述数据分别存入数据库，整理为三张表

## 2、结合GUI的多线程实现
1）基于tkinter库创建一个scrolledtext，作为主线程
2）创建queue对象用于线程间交互数据
3）主线程内若干个生产者线程producer用于生成数据法你放入queue中
4）同时作为主线程的界面也是一个消费者线程，可以从queue中读取数据显示在界面上 
## 3、在完成上述内容的基础上，在scolledtext内显示抓取网页内容：
1）丰富界面内容，加若干个复选框，每个表示待抓取的的网址：加按钮，点击按钮开启后台线程爬取选中的网页内容
2）扩充生产者中的线程逻辑，从选取的网址抓取页面内容，将页面内容作为数据放在queue中
3）在消费者线程，读取queue中的数据，并在scrolledtext 中显示抓取的页面内容

