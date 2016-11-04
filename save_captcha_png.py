#!/usr/bin/env python
# encoding: utf-8

# save_captcha_png.py
# Author     : jirui
# Date       : 2016/11/1


from PIL import Image
import StringIO
import os
from datetime import datetime


def save_captcha_png(ele):

    ele = find_getElementById("yourimageID")
    loc = ele.location
    size = ele.size
    left = loc['x']
    top = loc['y']
    width = size['width']
    height = size['height']
    box = (int(left), int(top), int(left + width), int(top + height))

    screenshot = ele.get_screenshot_as_png()
    img = Image.open(StringIO.StringIO(screenshot))
    area = img.crop(box)
    fp = os.path.join('路径', "captcha")
    if not os.path.exists(fp):
        os.makedirs(fp)
    filename = os.path.join(fp, datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '.png')

    area.save(filename, 'PNG')