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
let descStr = "";

//Get descs from Non Deleon listings
let nd_obj;
firebase
  .database()
  .ref(`/Non-Deleon listings/`)
  .once("value", snapshot => {
    nd_obj = snapshot.val();
    let keys = Object.keys(nd_obj);
    for (let k of keys) {
      if (nd_obj[k]["desc"].length > 30) {
        descStr += ". " + nd_obj[k]["desc"];
      } else {
        console.log(
          "Inadequate description for " + k + ": " + nd_obj[k]["desc"]
        );
      }
    }
  })
  .then(() => {
    //Get descs from Deleon listings
    let d_obj;
    firebase
      .database()
      .ref(`/Deleon listings/`)
      .once("value", snapshot => {
        d_obj = snapshot.val();
        let descStr = "";
        let keys = Object.keys(d_obj);
        for (let k of keys) {
          let attributes = Object.keys(d_obj[k]);
          for (let a of attributes) {
            if (a.includes("desc:") && !a.includes("中文")) {
              if (d_obj[k][a].length > 30) {
                descStr += ". " + d_obj[k][a];
              } else {
                console.log(
                  "Inadequate description for " + k + ": " + d_obj[k][a]
                );
              }
            }
          }
        }
        let descStrUpdate = {};
        descStrUpdate["allDescStr"] = descStr;
        firebase
          .database()
          .ref()
          .update(descStrUpdate);
        console.log("descStr is " + descStr);
      });
  });
