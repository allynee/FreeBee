const { initializeApp } = require("firebase/app");
require("firebase/compat/auth");

jwt = require("jsonwebtoken");

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
  apiKey: "AIzaSyDR1Tf3bAMUUHyksaUsiZWyPvzOqw62d0I",
  authDomain: "esdddtest.firebaseapp.com",
  projectId: "esdddtest",
  storageBucket: "esdddtest.appspot.com",
  messagingSenderId: "444566927588",
  appId: "1:444566927588:web:fcbb1cdf23c6c5e5ca54f1",
});

const auth = getAuth(firebaseConfig);

const provider = new GoogleAuthProvider();

async function loginEmailPassword(email, password) {
  try {
    const userCredential = await signInWithEmailAndPassword(
      auth,
      email,
      password
    );
    // Signed in
    const user = userCredential._tokenResponse.idToken;
    // setCookie(user, 1);
    if (checkAuthStatus()) {
      let access = await checkAccess(user);
      // let return_json = { result: user };

      return access;
    } else {
      console.log("LOG IN FAILED");
      let return_json = { result: "Unsuccessful" };
      return return_json;
    }
  } catch (error) {
    console.log(error);
    let return_json = { result: "Unsuccessful" };
    return return_json;
  }
}

// Function will login using google and return a UID
async function signInWithGoogle() {
  try {
    // This gives you a Google Access Token. You can use it to access the Google API.
    const result = await signInWithPopup(auth, provider);
    const credential = GoogleAuthProvider.credentialFromResult(result);
    console.log(credential)
    const token = credential.idToken;
    setCookie(token, 1);
    let return_json = { accessToken: token };
    return return_json;
  } catch (error) {
    // Handle Errors here.
    const errorCode = error.code;
    console.log(errorCode);
  }
}

function signUp(email, password) {
  // not done
  createUserWithEmailAndPassword(auth, email, password)
    .then((userCredential) => {
      // Signed in
      const user = userCredential.user;
      // ...
    })
    .catch((error) => {
      const errorCode = error.code;
      const errorMessage = error.message;
      // ..
    });
}

async function checkAuthStatus() {
  const authChange = await onAuthStateChanged(auth, (user) => {
    if (user) {
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
  // const endpoint = `https://www.googleapis.com/oauth2/v3/tokeninfo?access_token=${token}`;
  // const response = await fetch(endpoint, {
  //   method: 'GET',
  //   headers: {
  //     "Content-Type": "application/json"
  //   },
  // });
  // if (!response.ok) {
  //   throw new Error("Network response was not ok");
  // }
  // let return_json = { authStatus: "Success" };
  // return return_json;
  const decodedToken = jwt.decode(token, { complete: true });
  const response = decodedToken.payload.user_id
  let return_json = { uid : response}
  return return_json;
}

// Frontend function
// Set cookie function
// function setCookie(accessToken, time) {
//   var expires = "";
//   if (time) {
//     var date = new Date();
//     date.setTime(date.getTime() + time * 60 * 1000);
//     expires = "; expires=" + date.toUTCString();
//   }
//   document.cookie = "accessToken=" + accessToken + ";" + expires;
// }

// Get cookie function
// function getCookie() {
//   var nameEQ = "accessToken=";
//   var ca = document.cookie.split(";");
//   for (var i = 0; i < ca.length; i++) {
//     var c = ca[i];
//     while (c.charAt(0) == " ") c = c.substring(1, c.length);
//     if (c.indexOf(nameEQ) == 0) {
//       return c.substring(nameEQ.length, c.length);
//     }
//   }
//   return null;
// }

module.exports = {
  signInWithGoogle,
  loginEmailPassword,
  checkAccess,
  // setCookie,
  // getCookie,
};
