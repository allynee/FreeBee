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
        let queueName = "letterbox";
        channel.assertQueue(queueName, { durable: false });
        channel.consume(queueName, (msg) => {
            console.log("receieved :" + msg.content.toString())
            channel.ack(msg);
            sendOneEmail(msg.content.toString())
        })
    })
})

function sendOneEmail(email){
    console.log("sending mail " + email)
    if (email != null){
        console.log("sending mail " + email)
        try {
            // This tries to send the email
            result = mail.sendMail(email);
            console.log(result)
            result.then((result) => {
                // res.status(200).send('ITS OKAY!!')
                // If the email sending is successful, it will return a string
                if (typeof result == 'string'){
                    console.log('email sent ' + 250)
                    return JSON.parse(JSON.stringify({
                        message: 'email sent',
                        status: 250
                        
                    }))
                }
                // if the email sending is unsuccessful, it will return result = undefined
                else{
                    console.log('email not sent ' + 400)
                    return JSON.parse(JSON.stringify({
                        message: 'Wrong email format',
                        status: 400
                    }))
                }
            })
        } catch (error) {
        // this is if there is an error with trying the sendmail function
            console.log('email not sent ' + 500)
            return JSON.parse(JSON.stringify({
                message: 'internal error within samplemail.js',
                status: 500
            }));
            // res.status(500).send('internal error within samplemail.js')
        }
    }
    console.log('email not sent ' + 404)
    return JSON.parse(JSON.stringify({
    // this is if there is no email parameter at all
        message: 'invalid email address',
        status: 404
    }));
    // res.status(404).send('invalid email address')
}

// if( __name__ == "__main__"){
//     console.log("\nThis is " + os.path.basename(__file__), end='')
//     console.log(": monitoring routing key '{" + monitorBindingKey + "}' in exchange '{" + amqp_setup.exchangename + "}' ...")
//     // call function num1
// }