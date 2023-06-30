#!/usr/bin/env python3


import math
import os
from io import BytesIO
from PIL import Image

MIN_WIDTH = 1000
MIN_HEIGHT = 500

MAX_SIZE = 500 * 10**3

file_list = [file for file in os.listdir('./') 
         if os.path.isfile(os.path.join('./', file))]

images = [Image.open(filename) for filename in file_list]
## remove the alpha channel AKA transparency
images_rgb = [im.convert('RGB') for im in images]

## RESIZE

images_resized = []

for im in images_rgb:
    width, height = im.size

    if width >= MIN_WIDTH and height >= MIN_HEIGHT:
        images_resized.append(im)
        continue
    scale = max(MIN_WIDTH/width, MIN_HEIGHT/height)
    new_size = (math.ceil(scale*width), math.ceil(scale*height))
    im_resized = im.resize(new_size)
    images_resized.append(im_resized)

## CONVERT

images_jpg = []

for im in images_resized:
    if im.format == "JPEG":
        images_jpg.append(im)
        continue
    with BytesIO() as f:
        try:
            im.save(f, format="JPEG")
            f.seek(0)
            im_jpg = Image.open(f)
            im_jpg.load()
            images_jpg.append(im_jpg)
        except OSError:
            print('cannot convert', im.filename)

## COMPRESS AND SAVE
for idx, im in enumerate(images_jpg):
    fsize = 0
    path = './output/' + os.path.splitext(dir_list[idx])[0] + '.jpg'
    ## get file size of image
    with BytesIO() as f:
        im.save(f, "JPEG", quality="keep")
        fsize = f.tell()

    if fsize <= MAX_SIZE:
        im.save(path, "JPEG")
        continue
    q = 95
    while fsize > MAX_SIZE:
        if(q == 0):
            print('could not compress', dir_list[idx])
            break
        with BytesIO() as f:
            im.save(f, "JPEG", optimize=True, quality=q) 
            fsize = f.tell()
        q -= 5
    if q != 0:
        im.save(path, "JPEG", optimize=True, quality=q)
