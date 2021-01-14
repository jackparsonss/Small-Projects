import firebase from 'firebase'

const firebaseConfig = {
  apiKey: "AIzaSyChPDX_ZZW5TgdxLnjX5kUN9j84zLBg_MA",
  authDomain: "whatsapp-clone-ba0de.firebaseapp.com",
  databaseURL: "https://whatsapp-clone-ba0de.firebaseio.com",
  projectId: "whatsapp-clone-ba0de",
  storageBucket: "whatsapp-clone-ba0de.appspot.com",
  messagingSenderId: "174199684775",
  appId: "1:174199684775:web:f533fe4256c654c480e582",
  measurementId: "G-HX675VP67J"
};

const firebaseApp = firebase.initializeApp(firebaseConfig);
const auth = firebase.auth();
const provider = new firebase.auth.GoogleAuthProvider();

export {auth, provider};