// THIS IS A SAMPLE FOR SENDING EMAILS USING NODEMAILER AND GOOGLE API
// npm install googleapis nodemailer
// THIS IS IN APP.JS WHEN TESTED

const nodemailer = require('nodemailer');
const { google } = require('googleapis');

const CLIENT_ID = '406765810173-lial73q96ehf1bm3c2num3q4870df64l.apps.googleusercontent.com';
const CLIENT_SECRET = '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';
const REDIRECT_URI = 'https://developers.google.com/oauthplayground';
const REFRESH_TOKEN = '1//04c1KdrptPhA3CgYIARAAGAQSNwF-L9Ir185THrwzqwIZmVZiHrO44nsX2RRsKKFpBl_8-uuObVh9-F-mWAJgNISfmWJc_MKeg34';
// const OAuth2 = google.auth.OAuth2;

//access token will expire aft awhile so have to recreate it
const oAuth2Client = new google.auth.OAuth2(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI);
oAuth2Client.setCredentials({ refresh_token: REFRESH_TOKEN });

// can pass in parameters to sendMail function
async function sendMail(){
    try{
        const accessToken = await oAuth2Client.getAccessToken();
        const transport = nodemailer.createTransport({
            service: 'gmail',
            auth: {
                type: 'OAuth2',
                user: 'FreeBeeDoNotReply@gmail.com',
                clientId: CLIENT_ID,
                clientSecret: CLIENT_SECRET,
                refreshToken: REFRESH_TOKEN,
                accessToken: accessToken 
            }
        });

        const mailOptions = {
            from: 'FreeBeeSg <FreeBeeDoNotReply@gmail.com>',
            to: 'lixuen.low.2021@smu.edu.sg',
            subject: 'SAMPLE EMAIL from FreeBeeSg2',
            text: 'This is a sample email from FreeBeeSg \n Please do not reply to this email. \n Thank you for using FreeBeeSg!',
            html: '<h1>This is a sample email from FreeBeeSg</h1> \n <h2>Please do not reply to this email.</h2> \n <p>Thank you for using FreeBeeSg!</p>'
        };

        //this returns a promise
        const result = await transport.sendMail(mailOptions)
        return result
        
    } catch (error){
        return error
    }
}

// sendMail().then(result => console.log('Email sent...', result))
// .catch(error => console.log(error.message));
// node app.js TO RUN THE THING

module.exports = { sendMail };

// error message: self signed certificate in certificate chain
// // solution 'set NODE_TLS_REJECT_UNAUTHORIZED=0' in terminal (this is for windows)