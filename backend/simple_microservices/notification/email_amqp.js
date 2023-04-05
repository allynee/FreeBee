process.env['NODE_TLS_REJECT_UNAUTHORIZED'] = 0

const mail = require('./samplemail')
const express = require('express')
const app = express()
const port = 3000

const amqp = require('amqplib/callback_api');

amqp.connect('amqp://127.0.0.1', (err, connection) => { 
    if (err){
        throw err;
    }
    connection.createChannel((err, channel) => {
        if (err){
            throw err;
        }
        let queueName = "Subscribers";
        channel.assertQueue(queueName, { durable: true });
        channel.consume(queueName, (msg) => {
            console.log("receieved :" + msg.content.toString())
            channel.ack(msg);
            // convertAndSend(msg.content.toString())
        })
    })
})

function convertAndSend(aStringOfAnObj){
    const aJson = JSON.parse(aStringOfAnObj)
    console.log(aJson)
    console.log(aJson.Subscribers)
    for (let i = 0; i < aJson.Subscribers.length; i++){
        console.log(aJson.Subscribers[i].email)
        sendOneEmail(aJson.Subscribers[i].email)
    }
    // const email = aJson[0].email
    // console.log(email)
    // sendOneEmail(email)
}

async function sendOneEmail(email){
    if (email != null && email != undefined && email != '' && email != ' '){
        console.log("sending mail " + email)
        try {
            // This tries to send the email
            const result = await mail.sendMail(email);
            // console.log(result)
            // res.status(200).send('ITS OKAY!!')
            // If the email sending is successful, it will return a string
            if (typeof result.response == 'string'){
                console.log('email sent ' + 250)
                return JSON.parse(JSON.stringify({
                    message: 'email sent',
                    status: 250
                    //////RECENTLY FOUND ERROR THAT IF EMAIL IS TEMP@GMAIL (W0 .COM) IT STILL WORKS SMH
                }))
            }
        } catch (error) {
        // this is if there is an error with trying the sendmail function (e.g. wrong email format)
            console.log('email not sent ' + 500)
            return JSON.parse(JSON.stringify({
                message: 'internal error within samplemail.js',
                status: 500
            }));
            // res.status(500).send('internal error within samplemail.js')
        }
    }
    else{
        console.log('email param is empty ' + 404)
        return JSON.parse(JSON.stringify({
        // this is if there is no email parameter at all
            message: 'invalid email address',
            status: 404
        }));
    }
    // res.status(404).send('invalid email address')
}
