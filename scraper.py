# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 12:27:18 2020

@author: fede9326
"""

import pandas as pd
import time
import random
from selenium.webdriver import Chrome
from collections import Counter
from ast import literal_eval
import matplotlib.pyplot as plt

# Scrape n_posts from instagram with the input hashtag 
def recent_posts(browser, hashtag, n_posts):
    url = "https://www.instagram.com/explore/tags/" + hashtag + "/"
    browser.get(url)
    browser.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div/ul/li[1]/button').click()
    post = 'https://www.instagram.com/p/'
    post_links = []
    while len(post_links) < n_posts:
        links = [a.get_attribute('href') for a in browser.find_elements_by_tag_name('a')]
        for link in links:
            if post in link and link not in post_links:
                post_links.append(link)
        scroll_down = "window.scrollTo(0, document.body.scrollHeight);"
        browser.execute_script(scroll_down)
        time.sleep(random.randrange(1,4,1))
    else:
        return post_links[:n_posts]
    
# Extract Info from a post collected with recent_posts function
# Info supported: img_link, detected content by Instagram AI, associated hashtags
def format_post(browser,post):
    browser.get(post)
    dict = {}
    try:
        img_tag = browser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/article/div[1]/div/div/div[1]/img')
        #dict["img_link"] = img_tag.get_attribute("src")
        dict["content"] = [ "text" if "text" in x else x for x in img_tag.get_attribute("alt").split("Image may contain:")[-1].replace(" and ",",").replace(" ","").split(",") ]
        span_tag = browser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/article/div[2]/div[1]/ul/div/li/div/div/div[2]/span')
        dict["hashtags"] = [a.text for a in span_tag.find_elements_by_tag_name('a')]
    except:
        print("Trying another xpath for the image")
        try:
            img_tag = browser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/article/div[1]/div/div[1]/div[2]/div/div/div/ul/li[2]/div/div/div/div[1]/div[1]/img')
            #dict["img_link"] = img_tag.get_attribute("src")
            dict["content"] = [ "text" if "text" in x else x for x in img_tag.get_attribute("alt").split("Image may contain:")[-1].replace(" and ",",").replace(" ","").split(",") ]
            span_tag = browser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/article/div[2]/div[1]/ul/div/li/div/div/div[2]/span')
        except:
            print("Not able to lacate the img")
            
    return dict

browser = Chrome(keep_alive = False)
df = pd.DataFrame({"content":[], "hashtags":[]})
posts = recent_posts(browser,"covid", 200)
for post in posts:
    df = df.append(format_post(browser,post), ignore_index=True)
    time.sleep(random.randrange(1,4,1))

df.dropna(inplace=True)
        
df.to_csv("result.csv", mode = "a", header=False)
df = pd.read_csv("result.csv", sep=",")

frequency_hashtag = Counter(hash for index, row in df.iterrows() for hash in literal_eval(row.hashtags) if hash[0] == "#")
most_common_hashtag = frequency_hashtag.most_common()[1:30]
plt.figure(figsize=(30,15))
plt.bar(range(len(most_common_hashtag)), [x[1] for x in most_common_hashtag] )
plt.xticks(range(len(most_common_hashtag)), [x[0] for x in most_common_hashtag], rotation='70', fontsize=18)
plt.savefig("hashtags")  

frequency_content = Counter("people" if "people" in hash else hash for index, row in df.iterrows() for hash in literal_eval(row.content))
most_common_content = frequency_content.most_common()[0:18]
plt.figure(figsize=(20,15))
plt.bar(range(len(most_common_content)), [x[1] for x in most_common_content] )
plt.xticks(range(len(most_common_content)), [x[0] for x in most_common_content], rotation='70', fontsize=18)
plt.savefig("content") 




