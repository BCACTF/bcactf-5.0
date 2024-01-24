#!/usr/bin/env -S deno run

// ChaCha20 works by XORing the plaintext with a stream generated from
// the (key, nonce) pair. Since this pair is reused for encrypting the
// secret message and the user's message, the following operations can be
// performed to reveal the secret plaintext given the secret ciphertext:
// 1. user_ciphertext = user_plaintext ⊕ stream
// 2. stream = user_plaintext ⊕ user_ciphertext
// 3. secret_plaintext = stream ⊕ secret_ciphertext

const fromHex = (hex: string) => hex.match(/.{2}/g)!.map(byte => parseInt(byte, 16))

const secretMsg = fromHex(prompt('Enter secret message:')!)

console.log('Enter this as your message: ' + '1'.repeat(secretMsg.length))

const encryptedUserMsg = fromHex(prompt('Enter encrypted user message:')!)

const decryptedSecretMsg = secretMsg
    .map((v, i) => v ^ encryptedUserMsg[i])
    .map(v => String.fromCharCode(v ^ '1'.charCodeAt(0)))
    .join('')

console.log('Decrypted secret message: ' + decryptedSecretMsg)
