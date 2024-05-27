import { redirect } from '@sveltejs/kit'

import jwt from 'jsonwebtoken'

import { JWT_KEY } from '$lib/jwt-key.server.js'

const captchaGuard = ({ url, route }) => {
    const token = url.searchParams.get('token')

    const { id: routeId } = route

    try {
        const captchaData = jwt.verify(token, JWT_KEY)
        if (captchaData.done && captchaData.routeId === routeId) {
            return
        }
    } catch {}

    redirect(307, '/captcha?destination=' + routeId)
}

export { captchaGuard }
