import os
import pathlib
import hashlib

import requests
from PIL import Image

class ImageHandler(object):
    def __init__(self):
        self.width = 600
        self.height = 400

    # src  = https://domain.com/images/test.jpg
    # dest = /path/to/folder
    def download(self, src, folder, hashed=False):
        img_ext = pathlib.Path(src).suffix
        image_filename = hashlib.sha256(src.encode()).hexdigest() + img_ext if hashed else os.path.basename(src)
        save_to = '{}/{}'.format(folder, image_filename)
        img_data = requests.get(src).content
        with open(save_to, 'wb') as handler:
            handler.write(img_data)

        return save_to

    def resize(self, image_path, width=None, height=None, save_to=None, override=False):
        basewidth = isinstance(width, int) or self.width
        baseheight = isinstance(height, int) or self.height

        img = Image.open(image_path)
        if img.size[0] < basewidth:
            wpercent = (basewidth/float(img.size[0]))
            hsize = int((float(img.size[1]) * float(wpercent)))
            img = img.resize((basewidth, hsize), Image.ANTIALIAS)

        if img.size[1] < baseheight:
            wpercent = (baseheight/float(img.size[1]))
            wsize = int((float(img.size[0]) * float(wpercent)))
            img = img.resize((wsize, baseheight), Image.ANTIALIAS)

        ratio = float(img.size[0]) / float(img.size[1])

        y1 = (img.size[1] - baseheight) / 2
        y2 = y1 + baseheight
        x1 = (img.size[0] - basewidth) / 2
        x2 = x1 + basewidth

        if ratio > 1.5:
            w = int(float(img.size[1]) * 1.5)
            x1 = (img.size[0] - w) / 2
            x2 = x1 + w
            img = img.crop((x1, 0, x2, img.size[1]))
        else:
            h = int(float(img.size[0]) / 1.5)
            y1 = (img.size[1] - h) / 2
            y2 = y1 + h
            img = img.crop((0, y1, img.size[0], y2))


        save_as = None
        if isinstance(save_to, str):
            save_as = save_to

        if not save_as or override:
            save_as = image_path

        img.save(save_as)

    def info(self, image_path):
        img = Image.open(image_path)
        file_size = os.stat(image_path).st_size
        ext = pathlib.Path(image_path).suffix
        basename = os.path.basename(image_path)
        return {
            'basename': basename,
            'prefix': basename.split('.')[0],
            'suffix': ext,
            'size': file_size,
            'width': img.width,
            'height': img.height,
        }

