const express = require("express");
const app = express();
const port = 3000;
// const axios = require("axios");
const geocoding = require("./geocoding");

app.get("/:address", async (req, res) => {

  const address = req.params.address;
  const geocodeResult = await geocoding.geocode(address);
  res.json(geocodeResult);
});
app.listen(port, () => {
  console.log(`Example app listening on port ${port}`);
});

