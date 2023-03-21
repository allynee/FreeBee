const express = require("express");
const app = express();
const port = 3001;
// const axios = require("axios");
const authentication = require("./authentication");

app.get("/:email/:password", async (req, res) => {
  const email = req.params.email;
  const password = req.params.password;
  // const email = "test@gmail.com"
  // const password = "test1234"
  const authStatus = await authentication.loginEmailPassword(email, password);
  console.log(authStatus)
  res.json(authStatus);
});

// Not completed yet
app.get("/google", async (req, res) => {
  console.log(authStatus)
  res.json(authStatus);
});

app.listen(port, () => {
  console.log(`Example app listening on port ${port}`);
});
