import React, { useState,useEffect } from "react";
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import 'leaflet/dist/leaflet.css';
import {db } from "../config/firebaseConfig";
import { doc, getDoc } from "firebase/firestore";

export default function NavmapView(props) {
  const [position, setPosition] = useState([8.919330, 76.633760]);
  let [latest, setLatest] = useState([]);
  const getLatest = async () => {
    const docRef = doc(db, "fire", props.id);
    const docSnap = await getDoc(docRef);
    if (docSnap.exists()) {
      setLatest(docSnap.data());
      console.log("Document data:", docSnap.data());
      setPosition([parseFloat(docSnap.data().location[0]),parseFloat((docSnap.data().location[1]))])
    }
  };
  useEffect(() => {
    getLatest();
  }, []);
   
  return (
    <div >
      {JSON.stringify(position)}
      {latest.location &&(
      <MapContainer center={position} zoom={18} scrollWheelZoom={true} style={{height:"90vh", width:'100%'}}>
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        <Marker position={position}>
          <Popup>
            A pretty CSS3 popup. <br /> Easily customizable.
          </Popup>
        </Marker>
      </MapContainer>)}
      ,
    </div>
  );
}
