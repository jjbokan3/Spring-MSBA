# python script to scrape comedy transcripts
# site: http://scrapsfromtheloft.com/stand-up-comedy-scripts/

# importing requisite packages
import time
import requests

from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

import pandas as pd

# pointing to the browser driver
driver_path = "chrome driver path goes here"

# creating the service variable
s = Service(driver_path)

# SCRAPSFROMTHELOFT comedy transcripts link
comedy_transcripts = "https://scrapsfromtheloft.com/stand-up-comedy-scripts/"

# opening a browser
browser = webdriver.Chrome(service=s)
# navigating to the SCRAPSFROMTHELOFT comedy transcripts page
browser.get(comedy_transcripts)
time.sleep(5)
# getting the page source
base_page = browser.page_source
# passing it to BS to parse the tree
base_page_soup = BeautifulSoup(base_page, 'lxml')
# getting the grid containing the links to each comedy transcript
transcript_link_list = base_page_soup.find("div", {"class": "elementor-posts-container elementor-posts elementor-posts--skin-classic elementor-grid"})
# getting the links to each transcript from the transcript_link_list
transcript_urls = [x.find("a")["href"] for x in transcript_link_list.find_all("article")]
#%%
# initializing empty lists to store the data
unique_id, title, date, description, text, link = [], [], [], [], [], []

# creating a loop to iterate through each transcript link
for url in transcript_urls:
    print(url)
    # collecting requisite elements from each page:
    # - the last element of the URL as a unique ID
    # - the title of the transcript
    # - the post date
    # - the transcript in its entirety
    # - the url to the transcript
    # using the requests package to get the page source
    t = requests.get(url)
    # chillen
    time.sleep(3)
    # passing the page source to BS to parse the html tree
    t_soup = BeautifulSoup(t.text, 'lxml')
    # getting the unique identifier from the URL
    unique_id.append(url.split("/")[-2])
    # getting the title of the transcript
    title.append(t_soup.find("h1", {"class": "elementor-heading-title elementor-size-default"}).text)
    print(title[-1])
    # getting the date of the post
    date.append(t_soup.find("span", {"class": "elementor-icon-list-text elementor-post-info__item elementor-post-info__item--type-date"}).text)
    # the text is contained in a series of p tags with the style "text-align: justify;"
    # getting the p tags
    p_tags = t_soup.find_all("p", {"style": "text-align: justify;"})
    # getting the text from each p tag
    p_text = [x.text for x in p_tags]
    # joining the text from each p tag into a single string
    text.append(" ".join(p_text))
    # saving the URL for DQC
    link.append(url)

browser.close()

#%%
comedy_dict = {'link': link,
               'unique_id': unique_id,
               'date': date,
               'title': title,
               'text': text}
comedy_df = pd.DataFrame(comedy_dict)
comedy_df.to_csv("directory for the data goes here", sep = "\t", index=False)