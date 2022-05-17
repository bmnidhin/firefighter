
# Camera Client

- [x] Capature with camera
- [x] Capture with ipcamera
- [] Detect fire
- [] Detect Class of fire
- [x] send frames to kinesis
- [] send cameraid to Kinesis
- [x] distress call to IoT Hub {cameraID, classOfFire,location }
- [] send HTTP req to central hub


# Raspi Camera Client

- [x] Capature with camera
- [x] Capture with ipcamera
- [] Detect fire
- [] Detect Class of fire
- [x] send frames to kinesis
- [] send cameraid to Kinesis
- [x] distress call to IoT Hub {cameraID, classOfFire,location }
- [] send HTTP req to central hub

# Frame Processor
- [] Get cameraid from metadata
- [x] process frames and detect labels
- [] send distress call with cameraId, class and Location
- [x] save image to s3
- [x] Save image data to DynamoDB

# Vehicle Client
- [] POST new fire
- [] GET all fire prone areas
- [] Get ongoing actions
- [] Receive Distress calls
- [] display distress reception
- [] Display route calculation

# Dashboard
- [x] Display frames
- [] Display Fire
- [] List Ongoing actions
- [] Display route