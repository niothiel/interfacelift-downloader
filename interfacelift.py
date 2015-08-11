from bs4 import BeautifulSoup
from tempfile import NamedTemporaryFile
from threading import Thread
import time
import requests
import re
import os

PAGE_TEMPLATE = 'https://interfacelift.com/wallpaper/downloads/date/any/index{}.html'
IMG_TEMPLATE = 'http://interfacelift.com/wallpaper/7yz4ma1/{padded_id}_{base}_{resolution}.jpg'
RESOLUTION = '2880x1800'
BASE_DIR = os.path.abspath(os.path.dirname(__name__))
DOWNLOAD_DIR = os.path.join(BASE_DIR, 'downloads')
REQUEST_HEADERS = {
  'User-Agent': 'imontoyou 1.0'
}

urls_to_download = []

if not os.path.exists(DOWNLOAD_DIR):
  os.mkdir(DOWNLOAD_DIR)

def get_urls_for_page(page):
  url = PAGE_TEMPLATE.format(page)
  r = requests.get(url)
  
  bs = BeautifulSoup(r.text)
  selects = bs.find_all('select')
  entries = filter(has_required_resolution, selects)
  urls = map(convert_to_url, entries)

  return urls

def has_required_resolution(select_tag):
  return RESOLUTION in select_tag.get_text()

def convert_to_url(select_tag):
  matches = re.search(r'\'(.*)\'.*\'(.*)\'', select_tag['onchange'])
  base, id_key =  matches.groups()
  padded_id = pad(id_key, 5)

  return IMG_TEMPLATE.format(padded_id=padded_id, base=base, resolution=RESOLUTION)

def pad(s, total_length):
  while len(s) < total_length:
    s = '0' + s

  return s

def download_url(url):
  file_name = url.split('/')[-1]
  download_path = os.path.join(DOWNLOAD_DIR, file_name)

  if os.path.exists(download_path):
    print 'Filename exists, skipping: {}'.format(file_name)
    return

  r = requests.get(url, stream=True, headers=REQUEST_HEADERS)
  temp_file = NamedTemporaryFile(delete=False)
  for chunk in r.iter_content(chunk_size=1024):
    if chunk:
      temp_file.write(chunk)
      temp_file.flush()
  temp_file.close()

  os.rename(temp_file.name, download_path)

  print 'Downloaded:', file_name

class DownloaderThread(Thread):
  def run(self):
    print 'Starting worker: ', self.name
    while True:
      if not urls_to_download:
        time.sleep(1)
        continue

      url = urls_to_download.pop()
      download_url(url)

if __name__ == '__main__':
  workers = [DownloaderThread() for x in range(4)]
  [worker.start() for worker in workers]

  page = 1
  while True:
    if len(urls_to_download) > 50:
      time.sleep(1)
      continue

    urls = get_urls_for_page(page)
    urls_to_download.extend(urls)
    page += 1