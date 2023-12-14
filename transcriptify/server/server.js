import { readFileSync } from 'fs'

import puppeteer from 'puppeteer'
import express from 'express'

const PORT = 3000

const browser = puppeteer.launch({
    headless: 'new',
    args: ['--no-sandbox']
})

const app = express()

app.use(express.json())

const flag = readFileSync('../flag.txt', 'utf-8')

const views = ['index', 'viewtranscript'].map(name => {
    return [name, readFileSync(`views/${name}.html`, 'utf-8')]
}).reduce((a, b) => (a[b[0]] = b[1], a), {})

app.get('/', (_req, res) => {
    res.send(views.index)
})

const wrapped = callback => (req, res, next) => callback(req, res, next).catch(next)
const sleep = ms => new Promise(res => setTimeout(res, ms))

app.get('/viewtranscript', wrapped(async (req, res) => {
    let transcript

    try {
        transcript = JSON.parse(req.query.transcript)

        if (typeof transcript.studentName !== 'string') {
            throw new TypeError()
        }
    } catch {
        res.status(400).send('Bad Request')
        return
    }

    const time = String(Math.round(new Date().getTime() / 1_000))
    const nonce = Buffer.from(
        time.slice(0, -1) + (Number(time.at(-1)) >= 5 ? '5' : '0') + '000',
        'utf-8'
    ).toString('base64')

    res
        .set('Content-Security-Policy', `default-src 'self'; script-src 'nonce-${nonce}'`)
        .send(views.viewtranscript
                .replace('{nonce}', nonce)
                .replace('{studentName}', transcript.studentName ?? ''))
}))

const VIEW_TRANSCRIPT_URL = `http://localhost:${PORT}/viewtranscript`

app.get('/pdftranscript', wrapped(async (req, res) => {
    await sleep(2_500)

    const { transcript } = req.query

    const context = await (await browser).createIncognitoBrowserContext()

    const page = await context.newPage()

    await page.setRequestInterception(true)

    page.on('request', request => {
        if (request.isInterceptResolutionHandled()) {
            return
        }

        const url = new URL(request.url())

        if (url.href.startsWith(VIEW_TRANSCRIPT_URL)) {
            request.continue()
        } else {
            request.abort()
        }
    })

    const load = async () => {
        try {
            const url = new URL(VIEW_TRANSCRIPT_URL)

            await page.goto(url)

            await page.evaluate(flag => {
                localStorage.setItem('flag', flag)
            }, flag)

            url.searchParams.set('transcript', transcript)

            await page.goto(url)

            await sleep(1_000)

            const pdf = await page.pdf({
                pageRanges: '1',
                timeout: 1_500
            })
            res.contentType('application/pdf').send(pdf)

            await context.close()
        } catch {}
    }

    await Promise.race([load(), await sleep(3_500)])

    if (!context.closed) {
        await context.close()
    }

    if (!res.headersSent) {
        res.status(500).send('PDF generation failed')
    }
}))

app.listen(PORT, () => console.log(`Server listening on port ${PORT}`))
