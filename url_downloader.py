import interfacelift
import json
import os

JSON_PATH = 'urls.json'

def write_urls():
  print 'Writing urls: ', len(urls)
  formatted_urls = sorted(list(urls))
  with open(JSON_PATH, 'w') as fout:
    json.dump(formatted_urls, fout, indent=2)

if os.path.exists(JSON_PATH):
  with open(JSON_PATH, 'r') as fin:
    urls = set(json.load(fin))
else:
  urls = set()

page = 1
while True:
  page_urls = interfacelift.get_urls_for_page(page)
  urls.update(set(page_urls))
  page += 1

  print 'Page:', page
  if page % 10 == 0:
    write_urls()