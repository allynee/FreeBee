// node image_api.js

const cors = require("cors");
const express = require("express");
const multer = require("multer");
const bodyParser = require("body-parser");
const app = express();
const port = 3002;
app.use(cors(), bodyParser.json());
const upload = multer();

// const axios = require("axios");
const imageFn = require("./image");

app.post("/image", async (req, res) => {
  const image = req.body
  const authStatus = await imageFn.createListingFirebase(image);
  res.json(authStatus);
});

app.get("/image", async (req, res) => {
  const authStatus = imageFn.getImageUrl();
  res.json(authStatus);
});

app.listen(port, () => {
  console.log(`Example app listening on port ${port}`);
});
