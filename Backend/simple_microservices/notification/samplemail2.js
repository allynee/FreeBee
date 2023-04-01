const nodemailer = require('nodemailer');
const transporter = nodemailer.createTransport({
    service: 'gmail',
    auth: {
      user: 'freebeedonotreply@gmail.com',
      pass: 'Freebee123!'
    }
  });
  const mailOptions = {
    from: 'freebeedonotreply@gmail.com',
    to: 'lixuen.low.2021@scis.smu.edu.sg',
    subject: 'Test email',
    text: 'This is a test email sent using Nodemailer'
  };
  transporter.sendMail(mailOptions, (error, info) => {
    if (error) {
      console.log(error);
    } else {
      console.log('Email sent: ' + info.response);
    }
  });