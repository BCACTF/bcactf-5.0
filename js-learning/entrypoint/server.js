import { join } from 'path'
import { spawn } from 'child_process'

import express from 'express'
import httpProxy from 'http-proxy'

const proxyRequest = (req, res) => {
    try {
        const proxy = httpProxy.createProxyServer({})

        proxy.on('error', (_err, _req, res) => {
            if (res.headersSent) {
                return
            }

            res.status(500).send('Internal Server Error')
        })

        const child = spawn('deno', [
            'run',
            '--allow-env',
            '--allow-read=.',
            '--allow-net=0.0.0.0:0',
            'server.js'
        ], {
            cwd: join(process.cwd(), '../server'),
            env: { ...process.env, NO_COLOR: 1 }
        })

        child.stdout.once('data', data => {
            const port = Number(data.toString('utf-8'))
            proxy.web(req, res, { target: `http://127.0.0.1:${port}` })
        })

        const killTimeout = setTimeout(() => child.kill('SIGKILL'), 5_000)

        proxy.on('end', () => {
            clearTimeout(killTimeout)
            child.kill('SIGKILL')
        })
    } catch {
        res.status(500).send('Internal Server Error')
    }
}

const app = express()

app.get('/', proxyRequest)
app.get('/script.js', proxyRequest)
app.get('/style.css', proxyRequest)

app.post('/check', proxyRequest)

app.listen(3000)

process.on('uncaughtException', () => {})
