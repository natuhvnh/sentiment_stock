import datetime

def find_thread_urls(threads, website_name, start_date, end_date):
  """
  Return thread_urls have created date btw date_start and date_end
  """
  thread_urls = []
  for thread in threads:
    if thread.find('abbr', class_='DateTime today') is not None and thread.find('abbr', class_='DateTime today')['data-datestring'] is not None:
      created_date = thread.find('abbr', class_='DateTime today')['data-datestring']
      created_date = datetime.datetime.strptime(created_date, "%d/%m/%Y")
      if start_date <= created_date <= end_date:
        thread_url = thread.find('a')['href']
        thread_url = website_name + thread_url
        thread_urls.append(thread_url)
    elif thread.find('abbr', class_='DateTime') is not None and thread.find('abbr', class_='DateTime')['data-datestring'] is not None:
      created_date = thread.find('abbr', class_='DateTime')['data-datestring']
      created_date = datetime.datetime.strptime(created_date, "%d/%m/%Y")
      if start_date <= created_date <= end_date:
        thread_url = thread.find('a')['href']
        thread_url = website_name + thread_url
        thread_urls.append(thread_url)     
    elif thread.find('span', class_='DateTime').text:
      created_date = thread.find('span', class_='DateTime').text
      created_date = datetime.datetime.strptime(created_date, "%d/%m/%Y")
      if start_date <= created_date <= end_date:
        thread_url = thread.find('a')['href']
        thread_url = website_name + thread_url
        thread_urls.append(thread_url)
  return thread_urls
#
def get_title_date(thread_soup):
  if thread_soup.find('abbr', class_='DateTime') is not None:
    title_date = thread_soup.find('abbr', class_='DateTime')['data-datestring']
  else:
    title_date = thread_soup.find('span', class_='DateTime').text
  return title_date

