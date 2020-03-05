import requests
import os
import os.path
from os import path
import time
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd

date = datetime.utcnow().strftime("%Y-%m-%d")
print(date)
tags_global = []
post_lists_list = []
path_tags_master = os.path.join(os.getcwd(),'csv_files/tags_master.txt')
path_tags_posts = os.path.join(os.getcwd(),'csv_files/tags_posts_'+date+'.txt')

url = 'https://stackoverflow.com/jobs?sort=p&pg=1'
def main():
     global path_tags_master
     global path_tags_posts
     global url
     i=0

     init_vals()
     #25 cycles will typically get us either in the last 24hours or a little bit over
     #so we only need to run this once a day to get our data
     while(i<25):
         i+=1
         print(i)
         url = 'https://stackoverflow.com/jobs?sort=i&pg='+str(i)
         parse_page(url)
        
     df = pd.DataFrame(tags_global)
     df.to_csv(r''+path_tags_master, index=None)

     df = pd.DataFrame(post_lists_list)
     df.to_csv(r''+path_tags_posts, index=None)


def init_vals():
    global path_tags_master
    global path_tags_posts
    global tags_global
    global post_lists_list
    if path.exists(os.path.join(os.getcwd(),'csv_files')):
        print('folder present')
    else:
        print('building folder')
        os.mkdir(os.path.join(os.getcwd(),'csv_files'))

    if path.isfile(path_tags_master):
        print('global tags avaliable')
        df = pd.read_table(path_tags_master)
        to_list = df['0'].to_list()
        tags_global = to_list
    else:
        print('global tags not avaliable')
    
    if path.isfile(path_tags_posts):
        print('tags by post available')
        df = pd.read_table(path_tags_posts)
        to_list = df.values.tolist()
        new_list = []
        for ls in to_list:
            a = ls[0].split(',')
            new_item = []
            for item in a:
                new_item.append(item)
            new_list.append(new_item)
        post_lists_list = new_list
    else:
        print('tags by post not available')

def parse_page(url):
    global tags_global
    global post_lists_list
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    posts = soup.findAll("div",{"data-jobid":True})
    for post in posts:
        soup2 = BeautifulSoup(str(post), 'html.parser')
        tags = soup2.find_all("a", {"class":"post-tag job-link no-tag-menu"})
        postList = []
        for tag in tags:
            if tag.getText() not in tags_global:
                print('new tag! '+str(tag.getText()))
                tags_global.append(tag.getText())
            postList.append(tag.getText())

        #the below lines only exist to test and make sure that we are infact getting around 24hrs of jobs with our cycles
        #it also delays the bot from scraping so quickly, which is good for not irritating stack-overflow
        soup3 = BeautifulSoup(str(post),'html.parser')
        grid_cells = soup3.find_all("div",{"class":"mt8 fs-caption fc-black-500 grid gs8 gsx fw-wrap"})
        for grid_cell in grid_cells:
            for line in grid_cell.getText().split("\n"):
                if 'ago' in line:
                    print(line)
        post_lists_list.append(postList)

main()
