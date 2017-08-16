from romtools.disk import Disk
from rominfo import DEST_DISK
from PIL import Image
from bitstring import BitArray

d = Disk(DEST_DISK)
d.insert('ORTITLE.GEM', path_in_disk='TGL/OR')

NAMETAG_PALETTE = b'\x03\x33\x38\x40\xf4\x4d\x94\xfb\xac\xb9\xfd\x80\x21\x57\xd0\x66\x87\x3a\xcf\x8b\x80\x7f\xff\x00\x00'

def RGB_to_nybblebrg(color):
	red, blue, green = color
	b = blue & 0xf0
	r = red >> 4
	g = green & 0xf0
	return (b+r).to_bytes(1, byteorder='little') + g.to_bytes(1, byteorder='little')

print(RGB_to_nybblebrg((255, 0, 255)))

"""
img = Image.open('test.png')
width, height = img.size
blocks = img.size[0]//8
pix = img.load()

for x in range(width):
    for y in range(height):
        cpixel = pix[x, y]
        print(cpixel)

# TODO: Get a list of patterns from the blocks in the original image.

IMAGE_DATA_LOCATION = 0x100    # where pattern data ends and image data begins. TODO don't hardcode

with open('ORTITLE.GEM', 'wb') as f:
	f.write(b'Gem')
	f.write(b'\x02\x04\x00\x0e\x00')
	f.write(b'\x18\x00') # not sure what these bytes do
	f.write(height.to_bytes(2, byteorder='little'))
	f.write(IMAGE_DATA_LOCATION.to_bytes(2, byteorder='little'))
	f.write(b'\x00\x00\x00') # not sure about these either
	f.write(NAMETAG_PALETTE)   # for now
"""