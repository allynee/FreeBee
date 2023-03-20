process.env['NODE_TLS_REJECT_UNAUTHORIZED'] = 0

const mail = require('./samplemail')
const express = require('express')
const app = express()
const port = 3000

const amqplib = require('amqplib');

var amqp_url = process.env.CLOUDAMQP_URL || 'amqp://localhost:5672';
var amqp_setup = require('./amqp_setup');


async function init() {
    const connection = await amqp.connect(amqp_url)
   
    const q = "Notification"
    const channel = await connection.createChannel()
   
    await channel.assertQueue(q, { autoDelete: false })
   
    channel.prefetch(1)
   
    channel.consume(q, (msg) => {
     console.log("receieved msg from" + __file__)
     console.log(JSON.parse(msg.content))
     channel.ack(msg)
     sendOneEmail(JSON.parse(msg.content))
    })
   }

function sendOneEmail(email){
    if (email != null){
        console.log("sending mail " + email)
        try {
            // This tries to send the email
            result = mail.sendMail(email);
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
}

if( __name__ == "__main__"){
    console.log("\nThis is " + os.path.basename(__file__), end='')
    console.log(": monitoring routing key '{" + monitorBindingKey + "}' in exchange '{" + amqp_setup.exchangename + "}' ...")
    // call function num1
}