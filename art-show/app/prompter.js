import readline from 'readline'

import { readFileSync } from 'fs'
import { randomInt } from 'crypto'

import { createCanvas } from 'canvas'

const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
})

const CHALLENGE_COUNT = 10
const TIMEOUT_MS = 60 * 1_000 // 1 minute

const CANVAS_SIZE = 450
const CHUNK_SIZE = 75
const MIN_FIGURE_SIZE = 15

class Chunk {
    constructor(fromX, fromY, toX, toY) {
        this.fromX = fromX
        this.fromY = fromY
        this.toX = toX
        this.toY = toY
    }
}

const shuffle = array => {
    for (let i = array.length - 1; i > 0; i--) {
        const j = randomInt(0, i + 1)
        { [array[i], array[j]] = [array[j], array[i]] }
    }
}

const generateImage = () => {
    const canvas = createCanvas(CANVAS_SIZE, CANVAS_SIZE)

    const ctx = canvas.getContext('2d')

    ctx.antialias = 'none' // we need precise drawing

    ctx.fillStyle = 'white'
    ctx.fillRect(0, 0, canvas.width, canvas.height)

    const chunks = new Set()

    for (let i = 0; i < canvas.width; i += CHUNK_SIZE) {
        for (let j = 0; j < canvas.height; j += CHUNK_SIZE) {
            chunks.add(new Chunk(i, j, i + CHUNK_SIZE, j + CHUNK_SIZE))
        }
    }

    const rgb = (r, g, b) => `rgb(${r}, ${g}, ${b})`

    const figureCount = randomInt(Math.ceil(chunks.size / 2), chunks.size)

    const figures = []

    const colorPool = Array.from({ length: figureCount - 1 }, () => {
        return Array.from({ length: 3 }, () => randomInt(32, 255))
    })

    colorPool.push(colorPool[0]) // duplicate a color

    // so that the duplicated color isn't predictable
    shuffle(colorPool)

    for (let i = 0; i < figureCount; i++) {
        // this technically isn't true random positioning since no
        // rectangle can transcend the bounds of its chunk

        const chunk = [...chunks][randomInt(0, chunks.size)]

        const [x, y] = [chunk.fromX, chunk.fromY]

        const [r, g, b] = colorPool.pop()

        ctx.fillStyle = rgb(r, g, b)
        ctx.strokeStyle = rgb(r, g, b)

        const figureX = randomInt(0, CHUNK_SIZE - MIN_FIGURE_SIZE)
        const figureW = randomInt(MIN_FIGURE_SIZE, CHUNK_SIZE - figureX)

        const figureY = randomInt(0, CHUNK_SIZE - MIN_FIGURE_SIZE)
        const figureH = randomInt(MIN_FIGURE_SIZE, CHUNK_SIZE - figureY)

        const [effectiveX, effectiveY] = [x + figureX, y + figureY]

        ctx.fillRect(effectiveX, effectiveY, figureW, figureH)

        figures.push([
            r, g, b,
            effectiveX, effectiveY,
            figureW, figureH
        ].join(','))

        chunks.delete(chunk) // don't reuse the chunk
    }

    return [canvas.toBuffer(), new Set(figures)]
}

const wrongAnswer = () => {
    console.log('WRONG')
    process.exit(1)
}

let isPrompting = false

const question = prompt => {
    isPrompting = true

    return new Promise(res => rl.question(prompt, answer => {
        isPrompting = false
        res(answer)
    }))
}

const timeout = setTimeout(() => {
    if (isPrompting) {
        console.log()
    }

    console.log('TIMEOUT')

    process.exit(1)
}, TIMEOUT_MS) // 1 minute

timeout.unref() // don't hold the event loop open

for (let i = 0; i < CHALLENGE_COUNT; i++) {
    const [image, answers] = generateImage()

    console.log('IMAGE ' + image.toString('base64'))

    const userAnswers = (await question('ANSWER ')).split('; ')

    for (const userAnswer of userAnswers) {
        if (!answers.delete(userAnswer)) { // rectangle is not correct
            wrongAnswer()
        }
    }

    if (answers.size) { // user missed some rectangles
        wrongAnswer()
    }
}

console.log('FLAG ' + readFileSync('../flag.txt', 'utf-8'))

rl.close()
