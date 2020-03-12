import sys
import os
from os import path
import pandas as pd
import numpy as np
from itertools import zip_longest
from pandas import DataFrame
from csv import reader
#we store the pulls instead of the matricies because the matricies are sparse, but extremely large compared to the pull files
#for around 100kb of pull data we need around 3000kb for the associated matrix

path_tags_master = os.path.join(os.getcwd(),'csv_files/tags_master.txt')
tags_global = []

def main():
    init_vals()
    get_corr_matrix()

def get_corr_matrix():
    p = os.path.join(os.getcwd(),'csv_files\daily_post_pulls')
    posts = get_posts(p)
    print("number of posts :: "+str(len(posts)))

    tag_list = []
    for p in posts:
        p_list = [0]*len(tags_global)
        for tag in tags_global:
            if tag in p:
                p_list[tags_global.index(tag)] = 1
        tag_list.append(p_list)
    df = DataFrame(tag_list, columns=tags_global)
    corr_df = df.corr()
    corr_df = corr_df.fillna(0)
    print(corr_df)
    print(corr_df[corr_df['.net'] > .01])


def init_vals():
    global tags_global
    if path.isfile(path_tags_master):
        print('global tags avaliable')
        df = pd.read_table(path_tags_master)
        to_list = df['0'].to_list()
        tags_global = to_list
    else:
        print('global tags not avaliable')

def get_posts(p):
    posts = []
    file_paths = []
    if path.exists(p):
        print('daily folder present') #continue
        #walk directiory, add files to list of lists for all posts
        for file in os.walk(p):
            for sub_path in file[2]:
                file_paths.append(file[0]+'/'+sub_path)
        for file_p in file_paths:
            print('walking...'+file_p)
            with open (file_p, 'r') as file_obj:
                csv_reader = reader(file_obj)
                for key_set in list(csv_reader):
                    posts.append(key_set)
            
    else:
        print('no daily folder, breaking out')
        return -1
    return posts

main()
