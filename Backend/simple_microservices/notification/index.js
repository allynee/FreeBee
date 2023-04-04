// npm install express (to install expressjs)
process.env['NODE_TLS_REJECT_UNAUTHORIZED'] = 0

// const mail = require('./samplemail')
const mail = require('./emailing')
const express = require('express')
const app = express()
const port = 5005
// common for nodejs application ^
app.use(express.json())

app.get('/', (req, res) => {
    console.log("hello world")
    res.json({
        "hey": "there"
    })
})

app.get('/sendmail/:email?', async (req, res) => {
    // This is to check if email parameter contails anything
    console.log("Email API successfully called")
    console.log(req.body)
    //{
    //   email: 'lixuen.low.2021@scis.smu.edu.sg',
    //   subject: 'test from FreeBee',
    //   message: 'This is a test from FreeBee!'
    // }
    // console.log(req.params)
    // console.log(req.params.email)
    if (req.body != null && req.body != undefined && req.body != '' && req.body != ' ' && req.body != {}){
        console.log("sending mail ")
        console.log(req.body)
        email = req.body.email
        subject = req.body.subject
        message = req.body.message
        try {
            // This tries to send the email
            const result = await mail.sendingMail(email, subject, message);
            console.log(result)
            // res.status(200).send('ITS OKAY!!')
            // If the email sending is successful, it will return a string
            if (typeof result.response == 'string'){
                console.log('email sent ' + 250)
                let result = { result: "successful", statusCode: '250' };
                res.json(result);
                return result;
            }
            // if the email sending is unsuccessful, it will return result = undefined
        } catch (error) {
        // this is if there is an error with trying the sendmail function
        console.log('email not sent ' + 500)
        let result = { result: "internal error with samplemail.js", statusCode: '500' };
        res.json(result);
        return result;
        }
    }
    else{
        let result = { result: "invalid parsing", statusCode: '404' };
        res.json(result);
        return result;
    }
})


// app.listen(port, () => {
//     console.log(`Example app listening at http://localhost:${port}`)
// })
app.listen(port, '0.0.0.0', () => {
    console.log(`Example app listening at http://localhost:${port}`)
})