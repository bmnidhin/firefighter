import React from 'react'
import { styled } from '@mui/material/styles';
import Box from '@mui/material/Box';
import Grid from '@mui/material/Grid';
import NavmapView from '../components/NavmapView';
import IncidentLogs from '../components/IncidentLogs';


export default function IncidentPage() {
  return (
    <div style={{margin:'30px'}}>
        <Box sx={{ flexGrow: 1 }}>
      <Grid container spacing={2}>
        <Grid item xs={8}>
          <NavmapView/>
        </Grid>
        <Grid item xs={4}>
            ssss
         <IncidentLogs/>
        </Grid>
      </Grid>
    </Box>
    </div>
  )
}
