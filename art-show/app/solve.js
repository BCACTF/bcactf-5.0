// There isn't much to see here; any valid algorithm to find
// the rectangles will suffice. In this case, I search through
// the image pixel-by-pixel to find a non-white pixel, which
// indicates that a rectangle has begun, and then I peek right
// until I once again hit a white pixel to determine the width.
// Repeating the same process except vertically gives the height.
// After a rectangle is found, its constituent pixels are replaced
// with white pixels so the algorithm does not try to map the
// same rectangle multiple times.

import { createCanvas, loadImage } from 'canvas'

import readline from 'readline'

const CANVAS_SIZE = 450

const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
})

const question = prompt => new Promise(res => rl.question(prompt, res))

const canvas = createCanvas(CANVAS_SIZE, CANVAS_SIZE)

const ctx = canvas.getContext('2d')

const img = await loadImage(Buffer.from(await question('PNG Base64: '), 'base64'))
ctx.drawImage(img, 0, 0)

const isWhite = ([r, g, b]) => r === 255 && g === 255 && b === 255

const pixels = []

{
    const { data } = ctx.getImageData(0, 0, canvas.width, canvas.height)

    let line = []

    // break the linear data into a 2d array
    for (let i = 0; i < data.length; i += 4) {
        if (line.length >= CANVAS_SIZE) {
            pixels.push(line)
            line = []
        }

        // we don't need data[i + 3] (alpha)
        line.push([data[i], data[i + 1], data[i + 2]])
    }

    pixels.push(line)
}

const figures = []

for (let x = 0; x < CANVAS_SIZE; x++) {
    for (let y = 0; y < CANVAS_SIZE; y++) {
        const [r, g, b] = pixels[y][x]

        // either no rectangle or already seen
        if (isWhite([r, g, b])) {
            continue
        }

        let width
        let height

        // explore right
        for (let sx = x; sx < CANVAS_SIZE; sx++) {
            if (isWhite(pixels[y][sx])) {
                width = sx - x
                break
            }
        }

        // explore down
        for (let sy = y; sy < CANVAS_SIZE; sy++) {
            if (isWhite(pixels[sy][x])) {
                height = sy - y
                break
            }
        }

        for (let i = 0; i < width; i++) {
            for (let j = 0; j < height; j++) {
                // mark the whole shape as visited
                pixels[y + j][x + i] = [255, 255, 255]
            }
        }

        figures.push(`${r},${g},${b},${x},${y},${width},${height}`)
    }
}

console.log(figures.join('; '))

rl.close()
