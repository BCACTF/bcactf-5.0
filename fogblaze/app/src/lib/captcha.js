import { createHash, randomInt, timingSafeEqual } from 'crypto'

import { createCanvas } from 'canvas'

const ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

const generateWord = () => {
    let word = ''

    for (let i = 0; i < 4; i++) {
        word += ALPHABET[randomInt(ALPHABET.length)]
    }

    return word
}

const getFgColor = bgColor => {
    const [r, g, b] = bgColor
    const luminance =  0.2126 * r + 0.7152 * g + 0.0722 * b
    return luminance > 128 ? [0, 0, 0] : [255, 255, 255]
}

const rgb = (r, g, b) => `rgb(${r}, ${g}, ${b})`

const generateImage = word => {
    const canvas = createCanvas(180, 75)
    const ctx = canvas.getContext('2d')

    const bgColor = Array.from({ length: 3 }, () => randomInt(255))
    ctx.fillStyle = rgb(bgColor)
    ctx.fillRect(0, 0, canvas.width, canvas.height)

    const fgColor = getFgColor(bgColor)
    ctx.fillStyle = rgb(fgColor)
    ctx.strokeStyle = rgb(fgColor)

    ctx.textBaseline = 'middle'

    ctx.font = '50px Roboto'

    let offset = randomInt(20)

    for (const char of word) {
        const rotation = randomInt(-6, 6) * (Math.PI / 180)
        ctx.rotate(rotation)

        ctx[randomInt(2) === 1 ? 'strokeText' : 'fillText'](
            char,
            offset,
            canvas.height / 2 + randomInt(-3, 3)
        )

        const { width } = ctx.measureText(char)
        offset += Math.round(width + randomInt(5, 10))

        ctx.rotate(-rotation)
    }

    const lineCount = randomInt(2, 6)

    for (let i = 0; i < lineCount; i++) {
        ctx.beginPath()
        ctx.moveTo(randomInt(offset), randomInt(canvas.height))
        ctx.lineTo(randomInt(offset), randomInt(canvas.height))
        ctx.stroke()
    }

    return canvas.toDataURL()
}

const getChallengeCount = routeId => {
    switch (routeId) {
        case '/':
            return 2
        case '/flag':
            return 75
        case '/lorem-ipsum':
            return 30
        default:
            return null
    }
}

const calculateChallengeId = word => createHash('md5')
    .update(word)
    .digest('hex')

const checkChallenge = (challengeId, guessedWord) => timingSafeEqual(...[
    challengeId,
    calculateChallengeId(guessedWord)
].map(data => Buffer.from(data, 'hex')))

export {
    generateWord,
    generateImage,
    calculateChallengeId,
    checkChallenge,
    getChallengeCount
}
