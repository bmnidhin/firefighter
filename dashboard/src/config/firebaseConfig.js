import { initializeApp } from "firebase/app";
import { getFirestore } from "firebase/firestore";

const firebaseConfig = {
    apiKey: "AIzaSyCpx-9cASQi1I4aUPGPw-f6an3ujpfrQZw",
    authDomain: "firefighter-cf.firebaseapp.com",
    projectId: "firefighter-cf",
    storageBucket: "firefighter-cf.appspot.com",
    messagingSenderId: "191703712427",
    appId: "1:191703712427:web:ea37d39a87389f77fcadee",
    measurementId: "G-Q1FJHWYFML"
};

const app = initializeApp(firebaseConfig);
// const appCheck = firebase.appCheck();
// Pass your reCAPTCHA v3 site key (public key) to activate(). Make sure this
// key is the counterpart to the secret key you set in the Firebase console.
// appCheck.activate('6LchRbobAAAAABNv78_FAUlC4r7mW_vjl7Qo6AzI')
// if (!process.env.NODE_ENV || process.env.NODE_ENV === 'development') {
//   firebase.firestore().useEmulator("localhost", 8080);
//   firebase.storage().useEmulator("localhost", 9199);
//   firebase.functions().useEmulator("localhost", 5001);
// }

// firebase
//   .firestore()
//   .enablePersistence()
//   .catch((err) => {
//     if (err.code == "failed-precondition") {
//       // console.log("failed-precondition");
//       // ...
//     } else if (err.code == "unimplemented") {
//       // The current browser does not support all of the
//       // features required to enable persistence
//       // ...
//     }
//   });
export const db = getFirestore(app);

// export const fire = firebase;
// // export const auth = firebase.auth();
// // const messaging = firebase.messaging();
// export const firestore = firebase.firestore();
// export const FieldValue = firebase.firestore.FieldValue;
// export const storage = firebase.storage().ref();
// export const remoteConfig = firebase.remoteConfig();


// export const getToken = (setTokenFound) => {
//   return messaging
//     .getToken({
//       vapidKey:
//         "BAJSFoZTN0VNCWPU4wnP0XQzgSbIGeeLMFDNnSFmIKe6Fiy0H5lD_moo65vYniUQR7M2leOBCdD0m5wD1ZZUgGQ",
//     })
//     .then((currentToken) => {
//       if (currentToken) {
//         let date = new Date();
//         let tokenDoc = {
//           device: "Desktop",
//           token: currentToken,
//           lastUpdated: date,
//         };
//         let token = localStorage.getItem("token");
//         if (!token) {
//           localStorage.setItem("token", currentToken);
//           fire
//             .firestore()
//             .doc(
//               `users/${auth.currentUser.uid}/notificationTokens/${currentToken}`
//             )
//             .set(tokenDoc, { merge: true });
//         }
//         // console.log("current token for client: ", currentToken);
//         setTokenFound(true);
//         // Track the token -> client mapping, by sending to backend server
//         // show on the UI that permission is secured
//       } else {
//         // console.log(
//         //   "No registration token available. Request permission to generate one."
//         // );
//         setTokenFound(false);
//         // shows on the UI that permission is required
//       }
//     })
//     .catch((err) => {
//       // console.log("An error occurred while retrieving token. ", err);
//       // catch error while creating client token
//     });
// };

// export const onMessageListener = () =>
//   new Promise((resolve) => {
//     messaging.onMessage((payload) => {
//       resolve(payload);
//     });
//   });