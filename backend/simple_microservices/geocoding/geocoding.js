import axios from "axios";

// Ensures that Google Maps API is loaded
export function loadGoogleMaps(apiKey) {
  return new Promise((resolve, reject) => {
    const script = document.createElement("script");
    script.src = `https://maps.googleapis.com/maps/api/js?key=${apiKey}&libraries=places`;
    script.onload = () => {
      resolve();
    };
    script.onerror = () => {
      reject(new Error("Failed to load Google Maps API script"));
    };
    document.head.appendChild(script);
  });
}
// Set up autocomplete when the Google Maps API has loaded

async function initAutocomplete(apiKey, vm) {
  await loadGoogleMaps(apiKey);

  const input = document.getElementById("autocomplete-input");
  const autocomplete = new google.maps.places.Autocomplete(input);

  // Set options for the autocomplete search box
  autocomplete.setFields(["place_id", "formatted_address"]);
  autocomplete.setTypes(["geocode"]);

  // Listen for changes to the input field
  autocomplete.addListener("place_changed", async () => {
    const place = autocomplete.getPlace();

    // Use the getPlacePredictions() function to get more autocomplete results
    const service = new google.maps.places.AutocompleteService();
    const request = {
      input: input.value,
      types: ["geocode"],
    };
    try {
      const results = await new Promise((resolve, reject) => {
        service.getPlacePredictions(request, (results, status) => {
          if (status === google.maps.places.PlacesServiceStatus.OK) {
            resolve(results);
          } else {
            reject(status);
          }
        });
      });
      const address = results[0].description;
      vm.geocodeResult = address; // parase address information to Vue

      // To parse the results to python 
      // Return address as a JSON object
      //   const jsonAddress = { address: address };

      //   // Make an HTTP POST request to the Python server
      //   const response = await fetch("http://localhost:5000/process_address", {
      //     method: "POST",
      //     headers: {
      //       "Content-Type": "application/json",
      //     },
      //     body: JSON.stringify(jsonAddress),
      //   });

      //   if (response.ok) {
      //     const data = await response.json();
      //     console.log(data);
      //   } else {
      //     throw new Error("HTTP error " + response.status);
      //   }
    } catch (error) {
      console.error(error);
    }
  });
}

async function geocode(address) {
  // Ensures that Address is no empty
  if ((address == null) | (address == "")) {
    return null;
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

      // Defining the PostalDistricts and PostalArea (I feel we can do this in SQL)
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
        "South": ["03", "04"],
        "South-East": ["01", "02", "06", "07"],
        "Central": ["08", "09", "10", "11", "12"],
      };

      // Preparing Data
      const postal_front = String(postalCode.slice(0, 2));

      // Finding the District based on the PostalCode
      let district = "";
      Object.keys(postalDistricts).forEach((key) => {
        // console.log(postalDistricts[key], key);
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

      return area;
    } catch (error) {
      console.log(error);
      console.log("no");
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
export { geocode, initAutocomplete };
