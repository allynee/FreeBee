// npm install express (to install expressjs)

const express = require('express')
const app = express()
const port = 3000
// common for nodejs application ^

app.get('/', (req, res) => {
    console.log("hello world")
    res.json({
        "hey": "there"
    })
})

app.listen(port, () => {
    console.log(`Example app listening at http://localhost:${port}`)
})