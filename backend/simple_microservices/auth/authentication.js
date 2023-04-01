const { initializeApp } = require("firebase/app");
require("firebase/compat/auth");

jwt = require("jsonwebtoken");

const axios = require("axios");

const { ref: dbref, set, getDatabase } = require("firebase/database");

const {
  ref: stRef,
  getStorage,
  uploadBytes,
  getDownloadURL,
} = require("firebase/storage");

const {
  getAuth,
  onAuthStateChanged,
  signOut,
  createUserWithEmailAndPassword,
  signInWithEmailAndPassword,
  GoogleAuthProvider,
  signInWithPopup,
} = require("firebase/auth");

const firebaseConfig = initializeApp({
  apiKey: "AIzaSyD5ESzYYAhQhq7fecEJZofuXqjZTzSHRus",
  authDomain: "esdeeznutz.firebaseapp.com",
  databaseURL: "https://esdeeznutz-default-rtdb.firebaseio.com",
  projectId: "esdeeznutz",
  storageBucket: "esdeeznutz.appspot.com",
  messagingSenderId: "74897120396",
  appId: "1:74897120396:web:ab4510df9dcce9a7296fa9",
});

const auth = getAuth(firebaseConfig);

const db = getDatabase(firebaseConfig);

const storage = getStorage();

// const provider = new GoogleAuthProvider();

async function loginEmailPassword(email, password) {
  try {
    console.log(email, password);
    console.log("login");
    const userCredential = await signInWithEmailAndPassword(
      auth,
      email,
      password
    );
    // Signed in
    const user = userCredential._tokenResponse.idToken;
    const uid = userCredential._tokenResponse.localId;
    // setCookie(user, 1);
    if (checkAuthStatus()) {
      const response = await axios.get(
        "https://esdeeznutz-default-rtdb.firebaseio.com/UserData/" +
          uid +
          "/.json"
      );
      const role = response.data.role;
      const name = response.data.name;
      let access = {
        accessToken: user,
        statusCode: "200",
        uid: uid,
        role: role,
        name: name,
      };
      // let return_json = { result: user };
      return access;
    } else {
      console.log("LOG IN FAILED");
      let return_json = { result: "Unsuccessful", statusCode: "401" };
      return return_json;
    }
  } catch (error) {
    console.log(error);
    let return_json = { result: "Unsuccessful", statusCode: "401" };
    return return_json;
  }
}

// Function will login using google and return a UID
// async function signInWithGoogle() {
//   try {
//     // This gives you a Google Access Token. You can use it to access the Google API.
//     const result = await signInWithPopup(auth, provider);
//     const credential = GoogleAuthProvider.credentialFromResult(result);
//     console.log(credential);
//     const token = credential.idToken;
//     setCookie(token, 1);
//     let return_json = { accessToken: token };
//     return return_json;
//   } catch (error) {
//     // Handle Errors here.
//     const errorCode = error.code;
//     console.log(errorCode);
//   }
// }

async function signUp(email, password, role, name) {
  try {
    const response = await createUserWithEmailAndPassword(
      auth,
      email,
      password
    );
    // Signed in
    const uid = response.user.uid;
    const accessToken = response.user.accessToken;

    set(dbref(db, "UserData/" + uid), {
      role: role,
      name: name,
    }).catch((error) => {
      console.log(error);
    });

    let userData = {
      uid: uid,
      authStatus: "Sign Up Success",
      accessToken: accessToken,
      statusCode: "200",
    };
    console.log(userData);
    return userData;
  } catch (error) {
    let userData = {
      authStatus: "Sign Up Failed",
      statusCode: "200",
      errorMessage: error.code,
    };
    console.log(userData);
    return userData;
  }
}

//

async function checkAuthStatus() {
  const authChange = await onAuthStateChanged(auth, (user) => {
    if (user) {
      console.log("yes");
      // User is signed in, see docs for a list of available properties
      // https://firebase.google.com/docs/reference/js/firebase.User
      // ...
      return true;
    } else {
      // User is signed out
      // ...
    }
    if (authChange) {
      return true;
    }
  });
}

async function checkAccess(token) {
  // const cookie = await getCookie();
  try {
    const decodedToken = jwt.decode(token, { complete: true });
    const uid = decodedToken.payload.user_id;
    const role = await getUser(uid);
    // get back uid code and success message
    let return_json = {
      uid: uid,
      statusCode: "200",
      role: role,
      authStatus: "Success",
    };
    return return_json;
  } catch (error) {
    let return_json = {
      statusCode: "403",
      authStatus: "Unauthorized User",
    };
    return return_json;
  }
}

async function getUser(uid) {
  try {
    const response = await axios.get(
      "https://esdeeznutz-default-rtdb.firebaseio.com/UserData/" +
        uid +
        "/.json"
    );
    let role = response.data.role;
    return role;
  } catch (error) {
    console.log(error);
  }
}

async function signOutAccount() {
  try {
    const response = await auth.signOut();
    return response;
  } catch (error) {
    console.log(error);
  }
}

module.exports = {
  // signInWithGoogle,
  loginEmailPassword,
  checkAccess,
  // setCookie,
  // getCookie,
  signUp,
  signOutAccount,
};
