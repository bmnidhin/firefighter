import React from 'react'
import { styled } from '@mui/material/styles';
import Box from '@mui/material/Box';
import Paper from '@mui/material/Paper';
import Grid from '@mui/material/Grid';
import OpenIncidents from '../components/OpenIncidents';
import CameraFeed from '../components/CameraFeed';
import VehicleStatus from '../components/VehicleStatus';

export default function Homepage() {
  return (
    <div style={{margin:'30px'}}>
        <Box sx={{ flexGrow: 1 }}>
      <Grid container spacing={2}>
        <Grid item xs={12} sm={8} md={8}>
          <CameraFeed/>
        </Grid>
        <Grid item xs={12} sm={4} md={4}>
          <OpenIncidents/>
          <VehicleStatus/>
        </Grid>
      </Grid>
    </Box>
    </div>
  )
}
