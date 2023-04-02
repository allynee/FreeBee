// node auth_api.js


const cors = require("cors");
const express = require("express");
const multer = require("multer");
const bodyParser = require("body-parser");
const app = express();
const port = 3001;
app.use(cors(), bodyParser.json());
const upload = multer();
// const axios = require("axios");
const authentication = require("./authentication");

app.get("/login/:email/:password", async (req, res) => {
  const email = req.params.email;
  const password = req.params.password;
  // const email = "test@gmail.com"
  // const password = "test1234"
  const authStatus = await authentication.loginEmailPassword(email, password);
  console.log(authStatus);
  res.json(authStatus);
});

app.get("/auth/checkaccess/:token", async (req, res) => {
  const token = req.params.token;
  const authStatus = await authentication.checkAccess(token);
  res.json(authStatus);
});

app.post("/register", async (req, res) => {
  console.log(req.body);
  const email = req.body.email;
  const password = req.body.password;
  const role = req.body.role;
  const name = req.body.name;
  const authStatus = await authentication.signUp(email, password, role, name);
  res.json(authStatus);
});

app.get("/signout", async (req, res) => {
  const authStatus = await authentication.signOutAccount();
  res.json(authStatus);
});

app.listen(port, () => {
  console.log(`Example app listening on port ${port}`);
});
