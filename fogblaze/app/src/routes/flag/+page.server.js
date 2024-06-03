import { readFileSync } from 'fs'

import { captchaGuard } from '$lib/guard.js'

export const load = ({ ...data }) => {
    captchaGuard(data)
    return { flag: readFileSync('../flag.txt', 'utf-8') }
}
