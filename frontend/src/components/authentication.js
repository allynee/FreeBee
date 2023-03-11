import firebase from "firebase/compat/app";
import "firebase/compat/auth";

const firebaseConfig = {
  apiKey: "AIzaSyDR1Tf3bAMUUHyksaUsiZWyPvzOqw62d0I",
  authDomain: "esdddtest.firebaseapp.com",
  projectId: "esdddtest",
  storageBucket: "esdddtest.appspot.com",
  messagingSenderId: "444566927588",
  appId: "1:444566927588:web:fcbb1cdf23c6c5e5ca54f1",
};

firebase.initializeApp(firebaseConfig);

const auth = firebase.auth();

function signInWithGoogle() {
  const googleProvider = new firebase.auth.GoogleAuthProvider();
  auth
    .signInWithPopup(googleProvider)
    .then(() => {
      window.location.assign("https://www.google.com");
      console.log("Signed in");
    })
    .catch((error) => {
      console.log(error);
      console.log("Error signing in");
    });
}

export { signInWithGoogle };
