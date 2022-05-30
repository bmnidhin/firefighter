import React, { useEffect, useState } from "react";
import Box from "@mui/material/Box";
import Card from "@mui/material/Card";
import CardActions from "@mui/material/CardActions";
import CardContent from "@mui/material/CardContent";
import Button from "@mui/material/Button";
import Typography from "@mui/material/Typography";
import { Link } from "react-router-dom";
import {db } from "../config/firebaseConfig";
import {collection, query, where, onSnapshot } from "firebase/firestore";
import Chip from '@mui/material/Chip';
import Stack from '@mui/material/Stack';
export default function VehicleStatus() {
  let [latest, setLatest] = useState([]);
  const getLatest = async () => {
    const q = query(collection(db, "vehicle")); // where("state", "==", "CA")
    const unsubscribe = onSnapshot(q, (querySnapshot) => {
        let mylatest = [];
        querySnapshot.forEach((doc) => {
          // doc.data() is never undefined for query doc snapshots
          // console.log(doc.id, " => ", doc.data());

          mylatest.push(doc.data());
        });
        setLatest(mylatest);
      })
    // console.log(mylatest);
  };
  useEffect(() => {
    getLatest();
  }, []);
  return (
    <div>
        <h2>Vehicle Status</h2>
      {latest.map((item, index) => (
      <Link to = {`/vehicle/${item.id}`} key={item.id}>  
      <Card sx={{ minWidth: 275 }}>
        <CardContent>
          <Typography sx={{ fontSize: 20 }} color="text.secondary" gutterBottom>
             {`${item.agent}`}
          </Typography>
          <Stack direction="row" spacing={1}>
          {item.classList.map((item, index) => (
            <Chip label={item} key={index} />
          ))}
          </Stack>
          <Typography sx={{ mb: 1.5 }} color="text.secondary">
            {item.onAction? "On Action": "Available"}
          </Typography>
          <Typography variant="body2">
          {`${item.location[0]}, ${item.location[1]}`}
            
          </Typography>
        </CardContent>
        <CardActions>
          <Button size="small">Learn More</Button>
        </CardActions>
      </Card>
      </Link>
      ))}
    </div>
  );
}
