const nodemailer = require('nodemailer');


async function sendingMail(toMail, subject, content) {
  try{
      const transporter = nodemailer.createTransport({
        host: "smtp.gmail.com",
        port: 465,
        secure: true, // true for 465, false for other ports
        auth: {
          user: 'freebeedonotreply@gmail.com',
          pass: "ftfpmpnryokufxbz" // this pass is made for this project
        },
        tls: {
          // do not fail on invalid certs
          rejectUnauthorized: false
      }
      });

      const info = await transporter.sendMail({
        from: '"FreeBeeSg 🐝" <freebeedonotreply@gmail.com>',
        to: toMail,
        subject: subject,
        html: content,
      })
    console.log("Message sent: " + info.messageId);

  } catch (error){
    console.log(error);
    return error.response
  }
  
}



// toMail = 'lixuen.low.2021@scis.smu.edu.sg'
// subject = 'Test email2345678'
// html_content = "<h1>This is a sample email from FreeBeeSg</h1> \n <h2>Please do not reply to this email.</h2> \n <p>Thank you for using FreeBeeSg!</p>"

// sendingMail(toMail, subject, html_content)
// .catch(console.error);


module.exports = { sendingMail };


// const transporter = nodemailer.createTransport({
//     service: 'gmail',
//     auth: {
//       user: 'freebeedonotreply@gmail.com',
//       pass: 'Freebee123!'
//     }
//   });
//   const mailOptions = {
//     from: 'freebeedonotreply@gmail.com',
//     to: 'lixuen.low.2021@scis.smu.edu.sg',
//     subject: 'Test email',
//     text: 'This is a test email sent using Nodemailer'
//   };
//   transporter.sendMail(mailOptions, (error, info) => {
//     if (error) {
//       console.log(error);
//     } else {
//       console.log('Email sent: ' + info.response);
//     }
//   });