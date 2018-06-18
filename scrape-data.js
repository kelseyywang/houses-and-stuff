//child_process reference: https://www.sohamkamani.com/blog/2015/08/21/python-nodejs-comm/
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
let spawn = require("child_process").spawn,
  py = spawn("python", ["run_scraper.py"]),
  dataString = "";

py.stdout.on("data", function(data) {
  dataString += data.toString();
});

py.stdout.on("end", function() {
  console.log("Data scraped =", dataString);
  let deleonUpdates = {};
  dataJson = JSON.parse(dataString);
  for (let key in dataJson) {
    deleonUpdates[`Deleon listings/${key}`] = dataJson[key];
  }
  firebase
    .database()
    .ref()
    .update(deleonUpdates);
});
py.stdin.end();
