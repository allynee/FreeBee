// THIS IS A SAMPLE FOR SENDING EMAILS USING NODEMAILER AND GOOGLE API
// npm install googleapis nodemailer
// THIS IS IN APP.JS WHEN TESTED
process.env['NODE_TLS_REJECT_UNAUTHORIZED'] = 0


const nodemailer = require('nodemailer');
const { google } = require('googleapis');

const CLIENT_ID = '373101173117-5q491oac5dk1mc5nglja1qb2dre4qnk9.apps.googleusercontent.com';
const CLIENT_SECRET = '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';
const REDIRECT_URI = 'https://developers.google.com/oauthplayground';
const REFRESH_TOKEN = '1//04XWkQuHf31ZzCgYIARAAGAQSNwF-L9IrUdkns84aHxt9XUgBac_-JqCfldFs-Mq2XpRbWCozT8Ibm5pdKmznPj2YJlpfWFdWj6w';
// const OAuth2 = google.auth.OAuth2;

//access token will expire aft awhile so have to recreate it
const oAuth2Client = new google.auth.OAuth2(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI);
oAuth2Client.setCredentials({ refresh_token: REFRESH_TOKEN });


// to = 'lixuen.low.2021@smu.edu.sg',
// subject = 'SAMPLE EMAIL from FreeBeeSg2',
// text = 'This is a sample email from FreeBeeSg \n Please do not reply to this email. \n Thank you for using FreeBeeSg!',
// html = '<h1>This is a sample email from FreeBeeSg</h1> \n <h2>Please do not reply to this email.</h2> \n <p>Thank you for using FreeBeeSg!</p>'
// sendingMail(to, subject, html)
// can pass in parameters to sendMail function
async function sendingMail(toMail, subject, content){
    // toMail = 'lixuen.low.2021@smu.edu.sg',
    // subject = 'SAMPLE EMAIL from FreeBeeSg2',
    // content = '<h1>This is a sample email from FreeBeeSg</h1> \n <h2>Please do not reply to this email.</h2> \n <p>Thank you for using FreeBeeSg!</p>'
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
            to: toMail,
            subject: subject,
            html: content
        };

        //this returns a promise
        // const result = await transport.sendMail(mailOptions)
        const result = await transport.sendMail(mailOptions)
        console.log(result);
        return result;

        
    } catch (error){
        console.log(error);
        return error.response
    }
}
// sendMail('lixuen.low.2021@scis.smu.edu.sg').then(result => console.log('Email sent...', result))
// .catch(error => console.log(error.message));
// node app.js TO RUN THE THING

module.exports = { sendingMail };

// error message: self signed certificate in certificate chain
// // solution 'set NODE_TLS_REJECT_UNAUTHORIZED=0' in terminal (this is for windows)

// error message: 400: Invalid Credentials
// refresh token expires every 7 days