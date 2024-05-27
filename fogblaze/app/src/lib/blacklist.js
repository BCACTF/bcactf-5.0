const blacklist = new Map()

const cleanupSymbol = Symbol.for('fogblazeBlacklistCleanup')

if (globalThis[cleanupSymbol]) {
    clearInterval(globalThis[cleanupSymbol])
}

globalThis[cleanupSymbol] = setInterval(() => {
    for (const [captchaId, expires] of blacklist) {
        if (expires * 1_000 < Date.now()) {
            blacklist.delete(captchaId)
        }
    }
}, 30_000)

const addToBlacklist = (captchaId, expires) => blacklist.set(captchaId, expires)

const isBlacklisted = captchaId => blacklist.has(captchaId)

export { addToBlacklist, isBlacklisted }
