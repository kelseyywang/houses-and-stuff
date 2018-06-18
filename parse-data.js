let firebase = require("firebase");
let firebaseFile = require("./firebase-file");

let config = {
  apiKey: firebaseFile.FIREBASE_KEY,
  authDomain: "houses-and-stuff.firebaseapp.com",
  databaseURL: "https://houses-and-stuff.firebaseio.com",
  projectId: "houses-and-stuff",
  storageBucket: "houses-and-stuff.appspot.com"
};

firebase.initializeApp(config);

//Get data from firebase
let value;
firebase
  .database()
  .ref(`/Non-Deleon listings/`)
  .once("value", snapshot => {
    value = JSON.stringify(snapshot.val());
  })
  .then(() => {
    let spawn = require("child_process").spawn,
      py = spawn("python", ["play_with_data.py"]),
      data = value,
      dataString = "";

    py.stdout.on("data", function(data) {
      dataString += data;
    });

    py.stdout.on("end", function() {
      console.log("Returned from play_with_data:", dataString);
    });
    py.stdin.write(value);
    py.stdin.end();
  });
