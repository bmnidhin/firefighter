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
const axios = require("axios");
// Automatically allow cross-origin requests
app.use(cors({ origin: true }));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));

// build multiple CRUD interfaces:
app.post("/fire", async (req, res) => {
  const status = req.body.status;
  const location = req.body.location;
  const timestamp = FieldValue.serverTimestamp();
  const sender = req.body.sender || "camera"; // sender id
  const classOfFire = req.body.class || "";

  let fireRef = db.collection("fire").doc();
  fireDoc = { status, location, timestamp, classOfFire, sender, id: sender };
  let vehicles = await db.collection("vehicle").where("classList", "array-contains", classOfFire).get(); //TODO: add query if needed
  let allVehicles = [];

  vehicles.forEach((doc) => {
    allVehicles.push(doc.data());
  });
  let distanceArr = []
  let shortest = allVehicles.forEach((vehicle) => {
    let xVehicle = vehicle.location[0];
    let yVehicle = vehicle.location[1];

    let xFire = location[0];
    let yFire = location[1];

    let dist = Math.sqrt(Math.pow(xVehicle - xFire, 2) + Math.pow(yVehicle - yFire, 2));
    distanceArr.push(dist);

  })
  let shortestDist = Math.min(...distanceArr);
 /// find index of shortest distance
  let shortestIndex = distanceArr.indexOf(shortestDist);
  let shortestVehicle = allVehicles[shortestIndex];
  console.log(shortestVehicle,"is the shortest vehicle");
  console.log(distanceArr, "is the distance array");
  await axios
    .post(
      "https://l1z09jhovb.execute-api.us-west-2.amazonaws.com/default/alertVehicle",
      {
        event: classOfFire,
        source: location,
        incidentId: sender,
        shortestVehicle: shortestVehicle || "not available",
      }
    )
    .then(function (response) {
      console.log(response);
    })
    .catch(function (error) {
      console.log(error);
    });
    try{
    await db
    .collection(`vehicle`)
    .doc(shortestVehicle.id || "abc-powder-1")
    .set({onAction:true}, { merge: true })
    .then((newDoc) => {
     console.log("vehicle on action");
    })
    .catch((err) => {
      console.log(`error${err}`);
    });
  }catch(err){
    console.log(err);
  }

  await db
    .collection(`fire`)
    .doc(sender)
    .set(fireDoc, { merge: true })
    .then((newDoc) => {
      res.status(201).send(`Created a new incident: ${fireRef.id}`);
    })
    .catch((err) => {
      res.status(500).send(`error${err}`);
    });

  // query all nearby vehicles with class name availability and assign one

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
app.post("/vehicle", async (req, res) => {
  const status = req.body.status;
  const currentLocation = req.body.location;
  const timestamp = FieldValue.serverTimestamp();
  const sender = req.body.sender || "camera";
  const classOfFire = req.body.class;

  let vehicleRef = db.collection("vehicle").doc();
  fireDoc = {
    status,
    currentLocation,
    timestamp,
    classOfFire,
    sender,
    id: vehicleRef.id,
    isActive: false,
    dealingIncident: null,
  };
  await db
    .collection(`vehicle`)
    .doc(vehicleRef.id)
    .set(fireDoc, { merge: true })
    .then((newDoc) => {
      res.status(201).send(`Created a new vehicle: ${vehicleRef.id}`);
    })
    .catch((err) => {
      res.status(500).send(`error${err}`);
    });
});
// get all vehicles
app.get("/vehicle", async (req, res) => {
  let result = await db.collection("vehicle").get(); //TODO: add query if needed
  let response = [];

  result.forEach((doc) => {
    response.push(doc.data());
  });

  return res.send({ vehicles: response });
});
// update status of a vehicle
app.post("/vehicle/:id", async (req, res) => {
  const status = req.body.status;
  const currentLocation = req.body.currentLocation;
  const timestamp = FieldValue.serverTimestamp();
  const isActive = req.body.isActive || false;
  const dealingIncident = req.body.dealingIncident || null;

  fireDoc = { status, currentLocation, timestamp, isActive, dealingIncident };
  await db
    .collection(`vehicle`)
    .doc(req.params.id)
    .set(fireDoc, { merge: true })
    .then((newDoc) => {
      res.status(201).send(`Updated vehicle: ${req.params.id}`);
    })
    .catch((err) => {
      res.status(500).send(`error${err}`);
    });
});
// Expose Express API as a single Cloud Function:
exports.widgets = functions.https.onRequest(app);
