import { WebSocketServer } from 'ws'
import { createServer } from 'http'
import { readFileSync } from 'fs'

import express from 'express'

const PORT = 3000

const WINNING_PATTERNS = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
]

const OPENING_RESPONSES = [4, 0, 4, 0, 0, 2, 4, 1, 4]

const app = express()

const server = createServer(app)

const wss = new WebSocketServer({
    noServer: true
})

const index = readFileSync('views/index.html', 'utf-8')
const flag = readFileSync('../flag.txt', 'utf-8')

app.get('/', (_req, res) => {
    res.send(index)
})

server.on('upgrade', (req, socket, head) => {
    wss.handleUpgrade(req, socket, head, ws => {
        wss.emit('connection', ws, req)
    })
})

const winDetect = board => {
    for (const [a, b, c] of WINNING_PATTERNS) {
        const player = board[a]

        if (player && board[b] === player && board[c] === player) {
            return player
        }
    }

    if (board.every(cell => cell)) {
        return 'tie'
    }

    return null
}

const minimax = (board, depth, alpha, beta, max) => {
    const score = {
        X: -10,
        O: 10,
        tie: 0
    }[winDetect(board)] ?? null

    if (score !== null) {
        return score - depth
    }

    let best = max ? -1000 : 1000

    for (let i = 0; i < 9; i++) {
        if (!board[i]) {
            board[i] = max ? 'O' : 'X'

            const score = minimax(board, depth + 1, alpha, beta, !max)

            if (max) {
                best = Math.max(best, score)
                alpha = Math.max(alpha, best)
            } else {
                best = Math.min(best, score)
                beta = Math.min(beta, best)
            }

            board[i] = ''

            if (beta <= alpha) {
                break
            }
        }
    }

    return best
}

wss.on('connection', ws => {
    const board = Array(9).fill('')

    const broadcastBoard = () => ws.send(JSON.stringify({
        packetId: 'board',
        board
    }))

    let isOpeningMove = true

    ws.on('message', message => {
        let packet

        try {
            packet = JSON.parse(message.toString())
        } catch {
            ws.send(JSON.stringify({
                packetId: 'gameOver',
                message: 'Malformed packet!'
            }))
            ws.close()

            return
        }

        switch (packet.packetId) {
            case 'move': {
                const { position } = packet

                if (typeof position !== 'number' || isNaN(position) || position < 0 ||
                    position >= 9 || board[position] === 'X') {
                    ws.send(JSON.stringify({
                        packetId: 'gameOver',
                        message: 'Invalid move!'
                    }))
                    ws.close()

                    return
                }

                board[position] = 'X'

                if (isOpeningMove) {
                    board[OPENING_RESPONSES[position]] = 'O'
                    isOpeningMove = false
                } else {
                    let bestScore = -1000
                    let bestMove = -1

                    for (let i = 0; i < 9; i++) {
                        if (!board[i]) {
                            board[i] = 'O'
                            const score = minimax(board, 0, -1000, 1000, false)
                            board[i] = ''

                            if (score > bestScore) {
                                bestScore = score
                                bestMove = i
                            }
                        }
                    }

                    board[bestMove] = 'O'
                }

                broadcastBoard()

                const winner = winDetect(board)

                if (winner === 'X') {
                    ws.send(JSON.stringify({
                        packetId: 'gameOver',
                        message: `You win! ${flag}`
                    }))
                    ws.close()
                } else if (winner === 'O') {
                    ws.send(JSON.stringify({
                        packetId: 'gameOver',
                        message: 'You lost! Better luck next time...'
                    }))
                    ws.close()
                } else if (winner === 'tie') {
                    ws.send(JSON.stringify({
                        packetId: 'gameOver',
                        message: 'Tie! Good, but not good enough...'
                    }))
                    ws.close()
                }

                break
            }

            default:
                ws.close()
        }
    })

    broadcastBoard()
})

server.listen(PORT, () => console.log(`Server listening on port ${PORT}`))
