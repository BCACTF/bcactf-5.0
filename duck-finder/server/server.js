import express from 'npm:express@4.18.2'
import 'npm:ejs@3.1.6'

if (!Deno.env.has('FLAG')) {
    throw new Error('flag is not configured')
}

const breeds = JSON.parse(Deno.readTextFileSync('breeds.json'))

const app = express()

app.use(express.urlencoded({ extended: true }))

app.set('view engine', 'ejs')

app.get('/', (_req, res) => {
    res.render('index', { breedNames: Object.keys(breeds) })
})

app.post('/', (req, res) => {
    for (const [breed, summary] of Object.entries(breeds)) {
        if (req.body?.breed?.toLowerCase() === breed.toLowerCase()) {
            res.render('search', {
                summary,
                notFound: false,
                ...req.body
            })
            return
        }
    }

    res.render('search', { notFound: true })
})

const server = app.listen(0, () => console.log(server.address().port))
