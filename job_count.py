import requests
import os
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from random import randint
from time import sleep

def main():
    #  C# =  C%23
    #  C++ = C%2B%2B
    languages_list = ["Swift","TypeScript","JavaScript", "React","Python","Django","AWS","Terraform", "Angular.js","Flask", "Django", "Kafka", "Pyramid", "SQL", "NoSQL", "RESTful", "CSS"]
    for term in languages_list:
        url = build_url(term)
        count = get_count(url)
        if term == "C%23" : term = "C#"
        if term == "C%2B%2B" : term = "C++"
        print(str(count)+" job posts in "+term+" Developer")
    


def build_url(term):
    base_url = 'https://www.indeed.com/jobs?q='+term+" Developer"+'&l='
    return base_url


def get_count(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    count_string = soup.find(id='searchCountPages').getText().strip()
    count = count_string.split(" ")[-2]
    #count = int(count.replace(',',''))
    return count


    


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