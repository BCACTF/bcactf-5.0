import { json } from '@sveltejs/kit'

import { randomUUID } from 'crypto'

import jwt from 'jsonwebtoken'

import {
    generateImage,
    calculateChallengeId,
    checkChallenge,
    generateWord,
    getChallengeCount
} from '$lib/captcha.js'
import { JWT_KEY } from '$lib/jwt-key.server.js'
import { addToBlacklist, isBlacklisted } from '$lib/blacklist.js'

export const POST = async ({ request }) => {
    const body = await request.json()

    const bodyIs = keys => {
        const bodyKeys = Object.keys(body)
        return keys.length === bodyKeys.length &&
            keys.every(key => bodyKeys.includes(key))
    }

    const word = generateWord()

    let captchaId
    let routeId
    let solved
    let total
    let expiresAt

    let done = false

    if (bodyIs(['routeId'])) {
        captchaId = randomUUID()
        routeId = body.routeId
        solved = 0
        total = getChallengeCount(body.routeId)

        if (!total) {
            return json({ error: 'Unknown route ID.' }, { status: 422 })
        }
    } else if (bodyIs(['captchaToken', 'word'])) {
        if (typeof body.word !== 'string' || body.word.length > 256) {
            return json({ error: 'Invalid word.' }, { status: 422 })
        }

        let captchaData

        try {
            captchaData = jwt.verify(body.captchaToken, JWT_KEY)
        } catch (error) {
            if (error.name === 'TokenExpiredError') {
                return json({
                    error: 'CAPTCHA is expired. Please start again.'
                }, { status: 410 })
            }
        }

        if (!captchaData || isBlacklisted(captchaData.captchaId)) {
            return json({
                error: 'Invalid CAPTCHA. Please start again.'
            }, { status: 403 })
        }

        if (!captchaData.challengeId) {
            return json({
                error: 'This CAPTCHA is already complete.'
            }, { status: 403 })
        }

        if (!checkChallenge(captchaData.challengeId, body.word)) {
            addToBlacklist(captchaData.captchaId, captchaData.exp)
            return json({
                error: 'CAPTCHA failed! Please start again.'
            }, { status: 403 })
        }

        captchaId = captchaData.captchaId
        routeId = captchaData.routeId
        solved = captchaData.solved + 1
        total = captchaData.total
        expiresAt = captchaData.exp

        done = solved === total
    } else {
        return json({ error: 'Unexpected request content!' }, { status: 422 })
    }

    const progress = { solved, total, done }

    const captchaData = {
        captchaId,
        routeId,
        challengeId: done ? null : calculateChallengeId(word),
        ...progress
    }

    const options = {}

    if (expiresAt && !done) {
        captchaData.exp = expiresAt
    } else {
        options.expiresIn = 60
    }

    return json({
        captchaToken: jwt.sign(captchaData, JWT_KEY, options),
        image: done ? null : generateImage(word),
        ...progress
    }, { status: 200 })
}
