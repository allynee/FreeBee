// npm install express (to install expressjs)
process.env['NODE_TLS_REJECT_UNAUTHORIZED'] = 0

const mail = require('./samplemail')
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

app.get('/sendmail', (req, res) => {
    console.log("sending mail")
    try {
        mail.sendMail();
        res.status(200).send('ITS OKAY!!')
    } catch (error) {
        res.status(404).send('ERROR! ERROR!')
    }
    // res.json({
    //     "hey": "there"
    // })
})

app.listen(port, () => {
    console.log(`Example app listening at http://localhost:${port}`)
})