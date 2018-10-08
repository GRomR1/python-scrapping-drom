import os
import sys
from PIL import Image

logo = Image.open('logo/logo_min200.png')
# logo = logo.resize((int(logo.width * 0.2), int(logo.height * 0.2)), Image.LANCZOS)
# logo.show()
# print(logo.format, logo.size, logo.mode)
path = 'product_images'

def add_logo_to_image(filename, code='0'):
    if filename.endswith('.jpg') or filename.endswith('.png'):
        im = Image.open(filename)
        # im.show()
        im.paste(logo, (im.width - logo.width, im.height - logo.height), logo)
        # image.paste(logo, (imageWidth - logoWidth, imageHeight - logoHeight), logo)
        # im.show()
        im.save("{}/{}.jpg".format(path, code))
        print('Added watermark to ' + filename)

add_logo_to_image('images/1518005907891_default.jpg')

# for filename in os.listdir(path):
#     if (filename.endswith('.jpg') or filename.endswith('.png')) and (filename != lgo):
#
#         image = Image.open(path + '/' + filename)
#         imageWidth = image.width
#         imageHeight = image.height
#
#         try:
#             if pos == 'topleft':
#                 image.paste(logo, (0, 0), logo)
#             elif pos == 'topright':
#                 image.paste(logo, (imageWidth - logoWidth, 0), logo)
#             elif pos == 'bottomleft':
#                 image.paste(logo, (0, imageHeight - logoHeight), logo)
#             elif pos == 'bottomright':
#                 image.paste(logo, (imageWidth - logoWidth, imageHeight - logoHeight), logo)
#             elif pos == 'center':
#                 image.paste(logo, ((imageWidth - logoWidth)/2, (imageHeight - logoHeight)/2), logo)
#             else:
#                 print('Error: ' + pos + ' is not a valid position')
#                 print('Usage: watermark.py \'image path\' \'logo path\' [topleft, topright, bottomleft, bottomright, center]')
#
#             image.save(path + '/' + filename)
#             print('Added watermark to ' + path + '/' + filename)
#
#         except:
#             image.paste(logo, ((imageWidth - logoWidth)/2, (imageHeight - logoHeight)/2), logo)
#             image.save(path + '/' + filename)
#             print('Added default watermark to ' + path + '/' + filename)