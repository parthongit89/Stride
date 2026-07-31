// Firebase Web SDK Initialization & Google Sign-In Handler
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-app.js";
import { getAuth, GoogleAuthProvider, signInWithPopup } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-auth.js";

const firebaseConfig = {
  apiKey: "AIzaSyA2Kgdzerip50cMSQev4NXEbQ72P4oYGRU",
  authDomain: "stride-59051.firebaseapp.com",
  projectId: "stride-59051",
  storageBucket: "stride-59051.firebasestorage.app",
  messagingSenderId: "608022732803",
  appId: "1:608022732803:web:00b51aa2e68baa26082e36",
  measurementId: "G-GQNM2DYPMH"
};

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const provider = new GoogleAuthProvider();

window.signInWithGoogle = function() {
    const btn = document.getElementById('btn-google-login');
    if (btn) btn.disabled = true;

    signInWithPopup(auth, provider)
        .then((result) => {
            const user = result.user;
            fetch('/auth/firebase-login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    email: user.email,
                    name: user.displayName,
                    uid: user.uid
                })
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    window.location.href = data.redirect;
                } else {
                    alert(data.message || 'Firebase login failed.');
                    if (btn) btn.disabled = false;
                }
            })
            .catch(err => {
                console.error("Backend login error:", err);
                if (btn) btn.disabled = false;
            });
        })
        .catch((error) => {
            console.error("Firebase Auth Error:", error);
            alert("Google Sign-In failed: " + error.message);
            if (btn) btn.disabled = false;
        });
};
