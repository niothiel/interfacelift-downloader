import interfacelift
import os
from PIL import Image

def is_valid_image_file(path):
  try:
    print 'Verifying:', path.split('/')[-1]
    im = Image.open(path)
    im.verify()
    return interfacelift.RESOLUTION == '{}x{}'.format(*im.size)
  except:
    return False

download_contents = os.listdir(interfacelift.DOWNLOAD_DIR)
download_contents = [os.path.join(interfacelift.DOWNLOAD_DIR, f) for f in download_contents]
image_files = filter(lambda f: os.path.isfile(f) and f.endswith('.jpg'), download_contents)

valid_files = set(filter(is_valid_image_file, image_files))
invalid_files = set(image_files).difference(valid_files)
print invalid_files

for f in invalid_files:
  os.remove(f)