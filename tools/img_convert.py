from PIL import Image
import os

for p in os.listdir('map'):
	if p.endswith('.BMP'):
		im = Image.open(os.path.join('map', p))
		im = im.crop([0, 0, 640, 384])
		im.save(os.path.join('map', p.replace('.BMP', '.PNG')))
