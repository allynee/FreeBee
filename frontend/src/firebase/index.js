import { initializeApp} from 'firebase/app'
import { 
    getFirestore, 
} from 'firebase/firestore'

const firebaseConfig = {
    apiKey: "AIzaSyA9pWcQLY3cm-4YEm-5yTrIY0AQFbHWVp8",
    authDomain: "wad2-petfinder.firebaseapp.com",
    projectId: "wad2-petfinder",
    storageBucket: "wad2-petfinder.appspot.com",
    messagingSenderId: "1079295116811",
    appId: "1:1079295116811:web:1cf6e519a8d736eb16a90e"
  };


//initialise firebase app  
initializeApp(firebaseConfig)
const db=getFirestore()

export default db
//initialise services
// // export default getFirestore()

// // //collection ref
// // const userRef=collection(db, 'Users')

// // //get collection data
// // getDocs(userRef)
// // .then((snapshot)=>{
// //     console.log(snapshot.docs)
// // })