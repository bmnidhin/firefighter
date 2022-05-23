import React, { useState } from "react";
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import 'leaflet/dist/leaflet.css';


export default function NavmapView() {
    const [position, setPosition] = useState([8.919330, 76.633760]);
  return (
    <div >
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
      </MapContainer>
      ,
    </div>
  );
}
