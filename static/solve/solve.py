from PIL import Image
import os
import zlib
from bitarray import bitarray

os.system('ffmpeg -y -i ../out.mp4 "frame_out%03d.png"')
frames = [f"frame_out{i:03d}.png" for i in range(1,73)]
# frames = [f"../frames/frame{i}.png" for i in range(72)]

WIDTH = 256 # from specs
HEIGHT = 256 # from specs
BIT_DEPTH = 2 # from specs
MULTIPLIER = 0b01010101 # by inspection
frame_len = 3 * BIT_DEPTH * WIDTH * HEIGHT # in bits
out = b""

for frame_id in frames:
    frame = bitarray(frame_len)
    img = Image.open(frame_id)
    pixels = img.load()
    offset = 0
    for y in range(HEIGHT):
        for x in range(WIDTH):
            px = [round(i/MULTIPLIER) for i in pixels[x, y]]
            for i in range(3):
                idx = offset * BIT_DEPTH + i * frame_len // 3
                for j in range(BIT_DEPTH):
                    bit = (px[i] >> (BIT_DEPTH - j - 1)) & 1
                    frame[idx + j] = bit
            offset += 1
    out += frame.tobytes()

open('out.bin', 'wb').write(out)
# Use binwalk to extract the zlib-compressed data
os.system('binwalk -e out.bin')
# Result is 9E4A.zlib

compressed = open('_out.bin.extracted/9E4A.zlib', 'rb').read()
data = zlib.decompress(compressed)
open('decompressed.bin', 'wb').write(data)

# turns out to be a tar archive
os.system('tar -xf decompressed.bin')

# flag is in /home/admin/Documents/not_social_security_number.txt