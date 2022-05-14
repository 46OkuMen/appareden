import os
from PIL import Image


def crop(filename):
    img = Image.open(os.path.join('./img/portraits', filename))
    name = filename.split(".")[0]
    width, height = img.size

    imga = img.crop((0, 0, 160, 160))
    imga.save(os.path.join('./img/portraits/', filename.replace('.BMP', '.png')))

#crop('trauma-utk-derek.gif')

for portrait in [x for x in os.listdir('./img/portraits/') if x.endswith('.BMP')]:
	crop(portrait)
	#input()
	print(portrait)