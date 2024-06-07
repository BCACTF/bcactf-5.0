import zlib
import os
from PIL import Image

WIDTH = 256
HEIGHT = 256
BIT_DEPTH = 2
MULTIPLIER = 0b01010101
filename = input("filename: ")
# read in data.tar to a bytes object
data = open(filename, "rb").read()

# compress with zlib
compressed = zlib.compress(data)

frame_len = 3 * BIT_DEPTH * WIDTH * HEIGHT // 8
compressed = os.urandom(frame_len - (len(compressed) % frame_len)) + compressed

n_frames = len(compressed) // frame_len

print(f"n_frames: {n_frames}")


def get_bit(byteobj, i):
    return (byteobj[i // 8] >> (7 - i % 8)) & 1


for frid in range(n_frames):
    frame = compressed[frid * frame_len : (frid + 1) * frame_len]
    img = Image.new("RGB", (WIDTH, HEIGHT))
    pixels = img.load()
    offset = 0
    for y in range(HEIGHT):
        for x in range(WIDTH):
            px = [0, 0, 0]
            for i in range(3):
                idx = offset * BIT_DEPTH + i * frame_len * 8 // 3
                for j in range(BIT_DEPTH):
                    px[i] += get_bit(frame, idx + j) << (BIT_DEPTH - j - 1)
                px[i] *= MULTIPLIER
            offset += 1
            pixels[x, y] = tuple(px)
    img.save(f"frames/frame{frid:03d}.png")

os.system(
    """ffmpeg -framerate 30 -pattern_type glob -i 'frames/*.png' \
            -metadata encoding_tool="StaticMaker https://shorturl.at/AUKZm" \
            -c:v libx264rgb -qp 12 out.mp4
    """)
