// (run with deno)

// The secret message and the user's message are encrypted with the
// same (key, nonce) tuple, which completely defeats the security of
// ChaCha20. Essentially, E(secret_msg) ⊕ E(user_msg) = secret_msg ⊕ user_msg
// ...where E is obviously ChaCha20. Since the user message is controlled
// by the attacker, it is trivial to retrieve the secret message thus:
// (secret_msg ⊕ user_msg) ⊕ user_msg = secret_msg

const fromHex = (hex: string) => hex.match(/.{2}/g)!.map(byte => parseInt(byte, 16))

const secretMsg = fromHex(prompt('Enter secret message:')!)

console.log('Enter this as your message: ' + '1'.repeat(secretMsg.length))

const encryptedUserMsg = fromHex(prompt('Enter encrypted user message:')!)

const decryptedSecretMsg = secretMsg
    .map((v, i) => v ^ encryptedUserMsg[i])
    .map(v => String.fromCharCode(v ^ '1'.charCodeAt(0)))
    .join('')

console.log('Decrypted secret message: ' + decryptedSecretMsg)
