const axios = require("axios");

async function geocode(address) {
  // Ensures that Address is no empty
  if ((address == null) | (address == "")) {
    return       {
      code: 400,
      address: null,
    };;
  } else {
    try {
      // Getting the data from Google Maps API based on the address given
      const response = await axios.get(
        `https://maps.googleapis.com/maps/api/geocode/json`,
        {
          params: {
            address: address,
            key: "AIzaSyCuYRt4DvWiVVLzsBaR8fyuU_vRz9zCn9I",
          },
        }
      );

      // Retrieves Latitude and Longitude
      const lat = response.data.results[0].geometry.location.lat;
      const lng = response.data.results[0].geometry.location.lng;
      // Calling PlaceId Function to get the PlaceId
      const place_id = await getPlaceId(lat, lng);

      // Calling PostalCode Function to get the PostalCode
      const postalCode = await getPostalCode(place_id);

      // Defining the PostalDistricts and PostalArea
      // prettier-ignore
      const postalDistricts = {
        "01": ["01", "02", "03", "04", "05", "06"],
        "02": ["07", "08"],
        "03": ["14", "15", "16"],
        "04": ["09", "10"],
        "05": ["11", "12", "13"],
        "06": ["17"],
        "07": ["18", "19"],
        "08": ["20", "21"],
        "09": ["22", "23"],
        "10": ["24", "25", "26", "27"],
        "11": ["28", "29", "30"],
        "12": ["31", "32", "33"],
        "13": ["34", "35", "36", "37"],
        "14": ["38", "39", "40", "41"],
        "15": ["42", "43", "44", "45"],
        "16": ["46", "47", "48"],
        "17": ["49", "50", "81"],
        "18": ["51", "52"],
        "19": ["53", "54", "55", "82"],
        "20": ["56", "57"],
        "21": ["58", "59"],
        "22": ["60", "61", "62", "63", "64"],
        "23": ["65", "66", "67", "68"],
        "24": ["69", "70", "71"],
        "25": ["72", "73"],
        "26": ["77", "78"],
        "27": ["75", "76"],
        "28": ["79", "80"],
      };

      //prettier-ignore
      const PostalArea = {
        "East": ["13", "14", "15", "16", "17", "18"],
        'West': ["05", "21", "22", "23", "24"],
        'North': ["19", "20", "25", "26", "27", "28"],
        "South": ["01","02","03", "04","06","07"],
        "Central": ["08", "09", "10", "11", "12"],
      };

      // Preparing Data
      const postal_front = String(postalCode.slice(0, 2));

      // Finding the District based on the PostalCode
      let district = "";
      Object.keys(postalDistricts).forEach((key) => {
        if (postalDistricts[key].includes(postal_front) === true) {
          district = key;
        }
      });

      // Finding the Area based on the District
      let area;
      Object.keys(PostalArea).forEach((key) => {
        if (PostalArea[key].includes(district) === true) {
          area = key;
        }
      });
      let return_json = {
        code: 200,
        address: address,
        area: area,
        district: district,
        postal_code: postalCode,
      };
      return return_json;
    } catch (error) {
      let return_json = {
        code: 400,
        address: null
      };
      return return_json
    }
  }

  // Gets the PlaceId based on the Latitude and Longitude
  async function getPlaceId(lat, lng) {
    try {
      const response = await axios.get(
        `https://maps.googleapis.com/maps/api/geocode/json`,
        {
          params: {
            latlng: `${lat},${lng}`,
            key: "AIzaSyCuYRt4DvWiVVLzsBaR8fyuU_vRz9zCn9I",
          },
        }
      );
      return response.data.results[0].place_id;
    } catch (error) {
      console.log(error);
    }
  }
}

async function getPostalCode(placeId) {
  try {
    const response = await axios.get(
      `https://maps.googleapis.com/maps/api/geocode/json`,
      {
        params: {
          place_id: placeId,
          key: "AIzaSyCuYRt4DvWiVVLzsBaR8fyuU_vRz9zCn9I",
        },
      }
    );
    // address_components would return the address components which consists of all the different details of the address
    const address_components = response.data.results[0].address_components;
    for (let i = 0; i < address_components.length; i++) {
      // finds the address components which is the postal code
      if (address_components[i].types == "postal_code") {
        return address_components[i].long_name;
      }
    }
  } catch (error) {
    console.log(error);
  }
}
module.exports = { geocode };
