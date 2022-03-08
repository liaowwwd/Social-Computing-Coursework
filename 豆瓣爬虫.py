

import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
import csv
import random
import time

def Rate(html):#return rate_list
    try:
        Rate_pattern = re.compile(r'<span class="rating_per">(.*?)</span>', re.S)
        rate_list = re.findall(Rate_pattern, html)
        return rate_list
    except:
        return ""

def Score(html):#retuen score_list(only one item)
    try:
        Score_pattern = re.compile(r'<strong class="ll rating_num" property="v:average">(.*?)</strong>', re.S)
        score_list = re.findall(Score_pattern, html)
        return score_list 
    except:
        return ""   

def Date(html):#retuen date_list(may have plenty of items)
    try:
        Date_pattern = re.compile(r'property="v:initialReleaseDate" content="(.*?)"', re.S)
        date_list = re.findall(Date_pattern, html)
        return date_list
    except:
        return "" 

def BoxUrl(html):#retuen url_list(may have plenty of items)
    time.sleep(random.randint(0,3)) 
    #记得手动检查一下每部电影是不是都有IMDb的链接
    try:
        #<span class="pl">IMDb链接:</span>
        Url_pattern = re.compile(r'IMDb.*?="(.*?)"', re.S)
        Url_list = re.findall(Url_pattern, html)
        return Url_list
    except:
        return ""
'''
<h4 class="inline">Cumulative Worldwide Gross:</h4>
'''
def Box(html):
    try:
        url_list = BoxUrl(html)
        box_html = GetHtml(url_list[0])
        Box_pattern = re.compile(r'Cumulative Worldwide Gross:</h4>(.*?)<', re.S)
        box_list = re.findall(Box_pattern, box_html)
        return box_list[0]
    except:
        return "unknown"


def Fans(movie_name, url):
    file_name = movie_name+"粉丝属性"
    with open(file_name+".csv","w",newline="") as csvfile: 
        writer = csv.writer(csvfile)
        writer.writerow(["姓名","评分","评论内容","地点"])
        
    Comment_page(file_name, url+'comments?sort=new_score&amp;status=P')
    for st in range(20,220,20):
      # https://movie.douban.com/subject/30170448/comments?start=40&limit=20&status=P&sort=new_score
       url_page = url+'comments?start='+str(st)+'&limit=20&status=P&sort=new_score'
       Comment_page(file_name, url_page)



def Comment_page(file_name, url):
    html = GetHtml(url)
    soup = BeautifulSoup(html, 'lxml')
    
    itemlist = soup.find_all('div', class_='comment-item')
    #print('item', itemlist)
    for item in itemlist:
        #print("item\n",item)
        #评分，未验证
        #<span class="allstar50 rating" title="力荐"></span>
        '''
        try:
            Star_pattern = re.compile(r'allstar(\d)0 rating', re.S)
            star = re.findall(Star_pattern, item)[0] #待验证
            print("star_list",star)
        except:
            print("un")
            star_list ="unknown"
        '''
        #姓名已验证，问题不大
        try:
            info = item.find('span', class_='comment-info')
            a_tag = info.find('a')
            span_tag = info.find_all('span')
            star = span_tag[1]['class'][0][7]#星级
            name = a_tag.text#名字
        except:
            star = "unknown"
            name = "unknown"
   
        #content 已验证 问题不大
        try:
            itemcomment = item.find('p', class_='comment-content')
            comment = itemcomment.find('span').text
        except:
            comment = "unkonwn"

        #userurl user_url = UserUrl(item)
        try:
            user_url = a_tag['href']
        except:
            user_url = ""
        #userlocation user_loc = UserLoc(user_url)
        try:
            html = GetHtml(user_url)
            soup = BeautifulSoup(html, 'html.parser')
            div_tag = soup.find('div', class_='user-info')
            location = div_tag.find('a').text
        except:
            location = "unknown"
            #地点已检查：问题不大
    

        with open(file_name+".csv","a", newline="") as csvfile: 
            writer = csv.writer(csvfile)
            #写入多行用writerows
            try:
                writer.writerow([name, star, comment, location])#有的地点是国外文字，写入会出错，这种情况就直接跳过
            except:
                ""

def GetHtml(url):
    time.sleep(random.randint(0,3))
    user_agents = ['Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36','Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1','Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50','Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11']
    pro=['27.124.36.152','64.64.249.95','27.102.113.33','103.118.41.81']
    headers = {'User-Agent':random.choice(user_agents)}
    cookies = dict(uuid='b18f0e70-8705-470d-bc4b-09a8da617e15',UM_distinctid='15d188be71d50-013c49b12ec14a-3f73035d-100200-15d188be71ffd')
    response = requests.get(url=url, proxies={'http':random.choice(pro)}, headers=headers)#, cookies=cookies
    #response.encoding = response.apparent_encoding
    response.encoding = 'utf-8'#为解决中文乱码所做尝试
    html = response.text
    return html

def OriginHtml():
    file_obj = open('douban.html', 'r',encoding='UTF-8')  # 以读方式打开文件名为douban.html的文件
    demo = file_obj.read()  # 把文件的内容全部读取出来并赋值给html变量
    file_obj.close()  # 关闭文件对象

    soup = BeautifulSoup(demo, 'html.parser')
    movies = soup.find('ul', id='feature-slide')
    for each in movies.find_all('li', class_="ui-slide-item"):
       all_a_tag = each.find_all('a')
       print(all_a_tag[1].text)#电影名称get
       #print(all_a_tag[0]['href'])#电影名称get
       topmovie(all_a_tag[0]['href'])

def Writecsv():
    with open("票房.csv","w",newline="") as csvfile: 
        writer = csv.writer(csvfile)
        writer.writerow(["电影名称","票房"])
       
    with open("评价分值.csv","w",newline="") as csvfile: 
        writer = csv.writer(csvfile)
        writer.writerow(["电影名称","总分","五星","四星","三星","二星","一星"])

if __name__ == "__main__":

    url = "https://movie.douban.com/awards/doubanfilm_annual/6/"
    url_list = []
    movie_list = []
    html = GetHtml(url)
    soup = BeautifulSoup(html, 'lxml')
    li_tag = soup.find_all('li', class_='ui-slide-item')
    for i in range(9,11):#这一些打算调一下
        li = li_tag[i]
        url_list.append(li.find('a')['href'])
        movie_list.append(li.find('p').find('a')['title'])
    print(movie_list)

    #Writecsv()       
    for i in range(0,len(url_list)):
        url = url_list[i]
        movie_name = movie_list[i]
        html = GetHtml(url)
        #该电影票房
        box = Box(html)  
        with open("票房.csv","a", newline="") as csvfile: 
            writer = csv.writer(csvfile)
            writer.writerow([movie_name,box])
        #该电影评价情况 
        rate_list = Rate(html)
        score_list = Score(html)
        with open("评价分值.csv","a", newline="") as csvfile: 
            writer = csv.writer(csvfile)
            writer.writerow([movie_name, score_list[0], rate_list[0], rate_list[1], rate_list[2], rate_list[3], rate_list[4]])   
        #该电影的粉丝属性
        Fans(movie_name, url)
     

