import requests
import os
import os.path
from os import path
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from random import randint
from time import sleep
from datetime import datetime
import pandas as pd
from pandas import DataFrame
from random import randint
from time import sleep

import os
import os.path
from os import path
date = datetime.utcnow().strftime("%Y-%m-%d")
path_tags_count = os.path.join(os.getcwd(),'csv_files/daily_count_pulls/tags_count_'+date+'.txt')
path_tags_master = os.path.join(os.getcwd(),'csv_files/tags_master.txt')

def main():
    #  C# =  C%23
    #  C++ = C%2B%2B
    languages_list = get_tag_master_list()
    tag_label_list = []
    tag_count_list = []
    global path_tags_count
    for term in languages_list:
        if "+" in term : term.replace("+","%2B")
        if "#" in term : term.replace("+","%23")
        if '-' in term:
            term = term.replace('-','+')
        else:
            term = term+"+Developer"
        url = build_url(term)
        count = get_count(url)

        
        tag_count_list.append(count)
        tag_label_list.append(term)
        print(str(count)+" job posts in "+term)
    df = DataFrame(tag_count_list, index=tag_label_list)
    df.to_csv(path_tags_count)
    

def build_url(term):
    if('/jobs' in term):
        term = term.replace('&from=sug','')
        term = term+'&l='
        base_url = 'https://www.indeed.com'+term
        return base_url
    else:
        base_url = 'https://www.indeed.com/jobs?q='+term+'&l='
        return base_url

def get_count(url):
    #do a good turn, don't request bomb indeed
    #sleep(randint(5,20))

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    temp =soup.find(id='searchCountPages')

    if temp is None:
        print('None type passed')
        #check for autocomplete, otherwise, return 0
        try:
            temp = soup.find('li').find('a')['href']
        except:
            #no suggested searches, return0
            return 0

        temp_url = build_url(temp)
        print('Getting count for suggestion...')
        return get_count(temp_url)    
    else:
        print('Counting...')
        count_string = soup.find(id='searchCountPages').getText().strip()
        count = count_string.split(" ")[-2]
        #count = int(count.replace(',',''))
        return count

def get_tag_master_list():
    global path_tags_master
    p_to_count_folder = os.path.join(os.getcwd(),'csv_files/daily_count_pulls')

    if path.exists(p_to_count_folder):
        print('daily tag count folder present')
    else:
        print('building daily tag count folder')
        os.mkdir(p_to_count_folder)

    if path.isfile(path_tags_master):
        print('global tags avaliable')
        df = pd.read_table(path_tags_master)
        to_list = df['0'].to_list()
        return to_list
    else:
        print('global tags not avaliable')
    
    
main()



# salary finding functionality, I will wait till indeed approves my API access instead of hamfisting this functionality
# logic is preserved for future reference

# if(soup.find(id='filter-salary-estimate-menu') == None):
#         print("BROKEN")

#     while (soup.find(id='filter-salary-estimate-menu') == None):
#         print("BROKEN")
#         response = requests.get(base_url)
#         soup = BeautifulSoup(response.content, 'html.parser')

#     rays = soup.find(id='filter-salary-estimate-menu').getText().strip().split(")")
#     parsd = []
#     number_of_jobs = []
#     wages = []
#     for ray in rays:
#         txt = ray.replace("$","").replace("+\xa0(", "-")
#         if(txt == ""):
#             break
#         wage = txt.split("-")[0]
#         raw_amount = txt.split("-")[1]
#         wages.append(wage)
#         number_of_jobs.append(raw_amount)

#     #print(wages)
#     print(number_of_jobs)
    
#     buckets = []
#     for bucket in wages:
#         if(wages.index(bucket) == 0):
#             buckets.append("0-"+bucket)
#         elif(wages.index(bucket) == len(wages)-1):
#             buckets.append(bucket+"+")
#         else:
#             ind = wages.index(bucket)
#             buckets.append(wages[ind-1]+"-"+bucket)

#     print(buckets)