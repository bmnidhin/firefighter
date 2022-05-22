const express = require("express");
const cors = require("cors");
const functions = require("firebase-functions");
const admin = require("firebase-admin");
const firebaseHelper = require("firebase-functions-helper");
const bodyParser = require("body-parser");
const app = express();
admin.initializeApp(functions.config().firebase);
const db = admin.firestore();
const FieldValue = require("firebase-admin").firestore.FieldValue;

// Automatically allow cross-origin requests
app.use(cors({ origin: true }));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));

// build multiple CRUD interfaces:
app.post("/fire", async (req, res) => {
  const status = req.body.status;
  const location = req.body.location;
  const timestamp = FieldValue.serverTimestamp();
  const sender = req.body.sender || "camera";
  const classOfFire = req.body.class || "";

  let fireRef = db.collection("fire").doc();
  fireDoc = { status, location, timestamp, classOfFire, sender, id: fireRef.id };
  await db
    .collection(`fire`)
    .doc(fireDoc.id)
    .set(fireDoc, { merge: true })
    .then((newDoc) => {
      res.status(201).send(`Created a new incident: ${fireRef.id}`);
    })
    .catch((err) => {
      res.status(500).send(`error${err}`);
    });

    // query all nearby vehicles with class name and assign one
    
    // send lambda to topic


});

// get all fires
app.get("/fire", async (req, res) => {
  let result = await db.collection("fire").get(); //TODO: add query if needed
  let response = [];

  result.forEach((doc) => {
    response.push(doc.data());
  });

  return res.send({ incidents: response });
});
// get status of an incident
app.get("/fire/:id", async (req, res) => {
    let result = await db.collection("fire").doc(req.params.id).get(); //TODO: add query if needed
    return res.send({ incident: result.data() });
  });
// update status of an incident
app.post("/fire/:id", async (req, res) => {
  const status = req.body.status;
  const location = req.body.location;
  const timestamp = FieldValue.serverTimestamp();
  const sender = req.body.sender || "camera";
  const classOfFire = req.body.class || "";

  fireDoc = { status, location, timestamp, sender, classOfFire };
  await db
    .collection(`fire`)
    .doc(req.params.id)
    .set(fireDoc, { merge: true })
    .then((newDoc) => {
      res.status(201).send(`Updated incident: ${req.params.id}`);
    })
    .catch((err) => {
      res.status(500).send(`error${err}`);
    });
});
// onboard a vehicle
// get all vehicles
// update status of a vehicle

// Expose Express API as a single Cloud Function:
exports.widgets = functions.https.onRequest(app);
