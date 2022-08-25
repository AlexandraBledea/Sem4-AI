from PIL import Image
from matplotlib import image
from matplotlib import pyplot
import os

img = Image.open('sunflower.jpg')

print(img.format)
print(img.mode)
print(img.size)

img.show()

data = image.imread('sunflower.jpg')
# summarize shape of the pixel array
print(data.dtype)
print(data.shape)

# display the array of pixels as an image

pyplot.imshow(data)
pyplot.show()

img_resized = img.resize((960, 540))
img_resized.show()

img_cropped = img.crop((900, 0, 1750, 750))
img_cropped.show()

img_grey = img.convert(mode='L')
img_grey.show()

# print(img.size)
