from PIL import Image, ImageDraw
import hashlib
import random
from datetime import datetime
import argparse
import time 

parser = argparse.ArgumentParser()
parser.add_argument("-seed", type=str, required=True, help="the seed string")
parser.add_argument("-path", type=str, default="image.png", help="path to the image. (Default is image.png)")
args = parser.parse_args()
seed = args.seed
path = args.path

def get_pixel(index):
  x = index % width
  y = index // width
  return (x,y)

image = Image.open(path).convert("RGBA")
draw = ImageDraw.Draw(image)
width, height = image.size
n = width * height
random.seed(hashlib.sha256(seed.encode('utf-8')).digest())
numbers = random.sample(range(n), n)

for i in range(0,len(numbers),2):
  x,y = get_pixel(numbers[i])
  r,g,b,a = image.getpixel((x,y))
  nx,ny = get_pixel(numbers[i+1])
  draw.point((x,y), (image.getpixel((nx,ny))))
  draw.point((nx,ny), (r,g,b,a))

image.save(f"images/{path[:-4]}_reversed.png")
with open(".history.txt", "a") as f:
  now = datetime.now()
  date = now.strftime("%d, %B, %Y %H:%M")
  f.write(f"{date} ~ seed:{seed}")
print("Success!")
