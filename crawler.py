import requests
from bs4 import BeautifulSoup
import urllib.request
import datetime
import csv
from crawler_utils import *

# VARIABLE
website_name = 'http://f319.com/'
start_date = datetime.datetime.strptime("01-03-2020", "%d-%m-%Y")
end_date = datetime.datetime.now()
data = [['thread_url', 'thread_name', 'title?', 'content', 'created_date']]
max_pages = 10000
#
def get_comments(thread_url, title, website_name, comments_data):
  thread = urllib.request.urlopen(thread_url)
  thread_soup = BeautifulSoup(thread, 'lxml')
  comments = thread_soup.findAll('div', class_='messageInfo')
  for comment in comments:
    if comment.find('blockquote', class_='messageText ugc baseHtml').find('div', class_='bbCodeBlock bbCodeQuote') is not None:
     continue
    else:
      cmt = []
      comment_content = comment.find('blockquote', class_='messageText ugc baseHtml').text.strip().replace('\n', '.').replace('\t', '')
      created_date = comment.find('a', class_='datePermalink').text[:10]
      cmt.extend([thread_url, title, 'N', comment_content, created_date])
      comments_data.append(cmt)
      # print(created_date, comment_content)
  if thread_soup.find('a', string="Tiếp >"):
    next_page_button_url = thread_soup.findAll('a', class_='text')[-1]
    thread_url = website_name + next_page_button_url['href']
    return get_comments(thread_url, title, website_name, comments_data)
  else:
    return
#
def get_thread_urls(page_url):
  page = urllib.request.urlopen(page_url)
  soup = BeautifulSoup(page, 'lxml')
  all_threads= soup.findAll('div', class_='titleText')
  all_thread_urls = find_thread_urls(all_threads, website_name, start_date, end_date)
  return all_thread_urls
#
def f319_crawler(page_url, website_name, max_pages, start_date, end_date, data, page_number=0):
  page = urllib.request.urlopen(page_url)
  soup = BeautifulSoup(page, 'lxml')
  #
  all_thread_urls = get_thread_urls(page_url)
  for thread_url in all_thread_urls:
    title_data = []
    comments_data = []
    thread = urllib.request.urlopen(thread_url)
    thread_soup = BeautifulSoup(thread, 'lxml')
    title = thread_soup.find('div', class_='titleBar').find('h1').text
    title_date = get_title_date(thread_soup)
    title_data.extend([thread_url, title, 'Y', title, title_date])
    print(title)
    comments = get_comments(thread_url, title, website_name, comments_data)
    data.append(title_data)
    data.extend(comments_data)
  #
  next_page_button_url = soup.findAll('a', class_='text')[-1]
  page_url = website_name + next_page_button_url['href']
  print(page_url)
  page_number = page_number + 1
  if page_number > max_pages:
    return print("Max pages reaches, end crawl")
  else:
    return f319_crawler(page_url, website_name, max_pages, start_date, end_date, data, page_number)
f319_crawler(website_name, website_name, max_pages, start_date, end_date, data)
print(data[:10])
# with open('data.csv', 'w', encoding='utf-8-sig', newline='') as file:
#   writer = csv.writer(file, delimiter='#')
#   writer.writerows(data)
with open('data.txt', 'w', encoding='utf-8-sig', newline='') as file:
  writer = csv.writer(file, delimiter='#')
  writer.writerows(data)
