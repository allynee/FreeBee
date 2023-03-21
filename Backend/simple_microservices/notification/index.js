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

app.get('/sendmail/:email?', (req, res) => {
    // This is to check if email parameter contails anything
    if (req.params.email != null){
        console.log("sending mail " + req.params.email)
        try {
            // This tries to send the email
            result = mail.sendMail(req.params.email);
            // res.status(200).send('ITS OKAY!!')
            // If the email sending is successful, it will return a string
            if (typeof result == 'string'){
                res.json({
                    message: 'email sent',
                    status: 250
                    
                })
            }
            // if the email sending is unsuccessful, it will return result = undefined
            else{res.json({
                    message: 'Wrong email format',
                    status: 400
                })}
        } catch (error) {
        // this is if there is an error with trying the sendmail function
            res.json({
                message: 'internal error within samplemail.js',
                status: 500
            });
            // res.status(500).send('internal error within samplemail.js')
        }
    }
    res.json({
    // this is if there is no email parameter at all
        message: 'invalid email address',
        status: 404
    });
    // res.status(404).send('invalid email address')
})

app.listen(port, () => {
    console.log(`Example app listening at http://localhost:${port}`)
})