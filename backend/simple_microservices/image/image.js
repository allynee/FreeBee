const { initializeApp } = require("firebase/app");
const { ref: dbref, getDatabase, push } = require("firebase/database");
const { ref: stRef,getStorage, uploadBytes } = require("firebase/storage");

const firebaseConfig = initializeApp({
  apiKey: "AIzaSyD5ESzYYAhQhq7fecEJZofuXqjZTzSHRus",
  authDomain: "esdeeznutz.firebaseapp.com",
  databaseURL: "https://esdeeznutz-default-rtdb.firebaseio.com",
  projectId: "esdeeznutz",
  storageBucket: "esdeeznutz.appspot.com",
  messagingSenderId: "74897120396",
  appId: "1:74897120396:web:ab4510df9dcce9a7296fa9",
});

const db = getDatabase(firebaseConfig);

const storage = getStorage();

async function createListingFirebase(image) {
  try {
    const data = await push(dbref(db, "Listing"), {
      image: image.originalname,
    });
    const key = data.key;
    const filename = image.originalname;
    let ext = filename.slice(filename.lastIndexOf("."));
    const imageUpload = await uploadBytes(
      stRef(storage, "listings/" + key + ext),
      image.buffer
    );
    // const imageUrl = await getDownloadURL(
    //   stRef(storage, "listings/" + key + ext)
    // );
    const imageUrl = `https://firebasestorage.googleapis.com/v0/b/esdeeznutz.appspot.com/o/listings%2F${
      key + ext
    }?alt=media&token=d96a1b6f-e4a2-42d1-a06b-c9331d4490a4`;
    console.log(imageUrl);
    let return_response = {
      statusCode: 200,
      authStatus: "Success",
      listingid: key,
      extension: ext,
    };

    return return_response;
  } catch (error) {
    let return_response = {
      statusCode: 403,
      authStatus: "Failed to upload image",
    };
  }
}

module.exports = {
  createListingFirebase,
};
