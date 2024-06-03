import { error } from '@sveltejs/kit'

import { getChallengeCount } from '$lib/captcha.js'

export const load = ({ url }) => {
    if (!getChallengeCount(url.searchParams.get('destination'))) {
        error(404, { message: 'Not Found' })
    }
}
