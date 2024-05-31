// src/lib/firebase.js
import { initializeApp } from "firebase/app";
import { getFirestore } from "firebase/firestore";

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
    apiKey: "AIzaSyBM_7VtPV6SQZinEM8vQAzOAqyzjdmfPAA",
    authDomain: "recetariopymes.firebaseapp.com",
    projectId: "recetariopymes",
    storageBucket: "recetariopymes.appspot.com",
    messagingSenderId: "1091262436525",
    appId: "1:1091262436525:web:3acc9ed197930e436a2224",
    measurementId: "G-E4MBL8DQP2"
  };

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const db = getFirestore(app);

export { db };