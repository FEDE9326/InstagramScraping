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
    if hashtag in ["covid", "corona", "covid19", "covid-19", "coronavirus"]:
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
        time.sleep(random.randrange(1,2,1))
    else:
        return post_links[:n_posts]
    
# Extract Info from a post collected with recent_posts function
# Info supported: img_link, detected content by Instagram AI, associated hashtags
def format_post(browser,post):
    browser.get(post)
    dict = {}
    dict["content"] = []
    try:
        for img in browser.find_elements_by_class_name("FFVAD"): #name of the img class
            dict["content"].extend(["text" if "text" in x else x for x in img.get_attribute("alt").split("Image may contain:")[-1].replace(" and ",",").replace(" ","").split(",")])
        span_tag = browser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/article/div[2]/div[1]/ul/div/li/div/div/div[2]/span')
        dict["hashtags"] = [a.text for a in span_tag.find_elements_by_tag_name('a')]
    except:
        print("Not able to locate the img")
    return dict


def main_function(hashtag, n_hashtags, filename):
    
    # Initializing WebDriver
    browser = Chrome(keep_alive = False)
    
    # Creating dataframe
    df = pd.DataFrame({"content":[], "hashtags":[]})
    
    # Retrieving the list of instagram posts
    posts = recent_posts(browser, hashtag, n_hashtags)
    
    # Retrieving information for every post
    index = 1
    for post in posts:
        df = df.append(format_post(browser,post), ignore_index=True)
        print("Analyzed post number " + str(index))
        index+=1
        time.sleep(random.randrange(1,4,1))
    
    # Deleting NaN entries
    df.dropna(inplace=True)
    
    # Dump dataframe into a file appending it and loading it
    df.to_csv(filename, mode = "a", header=False)
    df = pd.read_csv(filename, sep=",")
    
    # Calculating frequencies
    frequency_hashtag = Counter(hash for index, row in df.iterrows() for hash in literal_eval(row.hashtags) if hash[0] == "#")
    most_common_hashtag = frequency_hashtag.most_common()[1:20]
    
    # Plotting the results
    plt.figure(figsize=(30,20))
    plt.title("Hashtags related to #" + hashtag, fontsize=30)
    plt.bar(range(len(most_common_hashtag)), [x[1] for x in most_common_hashtag])
    plt.xticks(range(len(most_common_hashtag)), [x[0] for x in most_common_hashtag], rotation='55', fontsize=25)
    plt.yticks(fontsize=25)
    plt.savefig("hashtags")  
    
    frequency_content = Counter("people" if "people" in hash else hash for index, row in df.iterrows() for hash in literal_eval(row.content))
    most_common_content = [ x for x in frequency_content.most_common()[0:20] if x[0] != "" ] # removing posts with no hashtag
    plt.figure(figsize=(30,20))
    plt.title("Content of the images containing  #" + hashtag, fontsize=30)
    plt.bar(range(len(most_common_content)), [x[1] for x in most_common_content] )
    plt.xticks(range(len(most_common_content)), [x[0] if len(x[0]) < 15 else x[0][0:round((len(x[0])/2))]+"-\n"+x[0][round((len(x[0])/2)):] for x in most_common_content] , rotation='55', fontsize=25) # splitting in 2 the string in case of big length
    plt.yticks(fontsize=25)
    plt.savefig("content") 


if __name__ == "__main__":
    main_function("guitar", 300, "result_guitar.csv")


