const scriptTheory = require('./libscript_theory_addon.node')
const crypto = require('crypto')

const ENCODED_FLAG = 'DZwOdRBBOBaBxZ7SdUHDqORNCSzNt2SkBDa5NH9xsGIGz8ufVijMgucC8fht'

const computeShifterAndValue = length => {
    // these routines are extracted straight from program.js

    const shifter = Buffer.alloc(length)

    for (let i = 0; i < shifter.length; i++) {
        const value = String(Math.abs(Math.E * i + 2 / 3 * 100))
        shifter[i] = Number(value.split('.')[1].slice(0, 2))
    }

    const value = [...shifter].map(value => value ** 2).reduce((a, b) => {
        return Math.max(a + Math.sqrt(b) - 2, 1)
    }, 0) % 200

    return [shifter, value]
}

const terraceBucket = (data, shifter, value) => {
    // undo bucket_terrace

    for (let i = 0; i < shifter.length; i++) {
        data[i] ^= shifter[i] ^ value
    }
}

const computeOilKey = () => {
    // just like in program.js, get the oil key

    // of course the flag will start with "bcactf"
    const oilKey = scriptTheory.bringOil('b'.charCodeAt(0))

    for (let i = 0; i < oilKey.length; i++) {
        oilKey[i] = Math.abs(oilKey[i] - i)
    }

    return oilKey
}

const accurateDiplomat = (data, oilKey) => {
    // reverse diplomat_accurate

    const iv = Buffer.alloc(16)

    // skip the first 4 bytes for the counter
    for (let i = 4; i < iv.length; i++) {
        iv[i] = 0x32
    }

    const cipher = crypto.createDecipheriv('chacha20', oilKey, iv)

    for (let i = 0; i < data.length; i++) {
        // because the lib calls reverse_bits
        const bits = [...data[i].toString(2).padStart(8, '0')]
        data[i] = parseInt(bits.reverse().join(''), 2)
    }

    return cipher.update(data).toString('utf-8')
}

const solve = () => {
    const data = Buffer.from(ENCODED_FLAG, 'base64')

    const [shifter, value] = computeShifterAndValue(data.length)
    const oilKey = computeOilKey()

    terraceBucket(data, shifter, value)

    console.log(accurateDiplomat(data, oilKey))
}

solve()
