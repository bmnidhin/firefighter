import React from 'react'
import { styled } from '@mui/material/styles';
import Box from '@mui/material/Box';
import Paper from '@mui/material/Paper';
import Grid from '@mui/material/Grid';
import GetCameraFeedId from './GetCameraFeedId';

const Item = styled(Paper)(({ theme }) => ({
  backgroundColor: theme.palette.mode === 'dark' ? '#1A2027' : '#fff',
  ...theme.typography.body2,
  padding: theme.spacing(1),
  textAlign: 'center',
  color: theme.palette.text.secondary,
}));
function CameraFeed() {
  return (
    <div>CameraFeed
       <Box sx={{ flexGrow: 1 }}>
      <Grid container spacing={2}>
        <Grid item xs={4}>
          <GetCameraFeedId id={'dell2'}/>
        </Grid>
        <Grid item xs={4}>
        <GetCameraFeedId id={'dell2'}/>
        </Grid>
        <Grid item xs={4}>
        <GetCameraFeedId id={'dell2'}/>
        </Grid>
        <Grid item xs={4}>
          <Item>xs=4</Item>
        </Grid>
      </Grid>
    </Box>
    </div>
  )
}

export default CameraFeed