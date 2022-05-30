import React from 'react'
import { styled } from '@mui/material/styles';
import Box from '@mui/material/Box';
import Grid from '@mui/material/Grid';
import NavmapView from '../components/NavmapView';
import IncidentLogs from '../components/IncidentLogs';
import { useParams} from "react-router-dom";
import GetCameraFeedId from '../components/GetCameraFeedId';

export default function IncidentPage(props) {
  let { id } = useParams();
  return (
    <div style={{margin:'30px'}}>
        <Box sx={{ flexGrow: 1 }}>
      <Grid container spacing={2}>
        <Grid item xs={8}>
          <NavmapView id= {id}/>
        </Grid>
        <Grid item xs={4}>
         <IncidentLogs/>
         <GetCameraFeedId id={'dell2'}/>
        </Grid>
      </Grid>
    </Box>
    </div>
  )
}
