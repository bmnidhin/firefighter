
# Camera Client

- [x] Capature with camera
- [x] Capture with ipcamera
- [x] Detect fire
- [] Detect Class of fire
- [x] send frames to kinesis
- [x] send cameraid to Kinesis
- [x] distress call to IoT Hub {cameraID, classOfFire,location }
- [x] send HTTP req to central hub


# Raspi Camera Client

- [x] Capature with camera
- [x] Capture with ipcamera
- [] Detect fire
- [] Detect Class of fire
- [x] send frames to kinesis
- [] send cameraid to Kinesis
- [x] distress call to IoT Hub {cameraID, classOfFire,location }
- [x] send HTTP req to central hub

# Frame Processor
- [x] Get cameraid from metadata
- [x] process frames and detect labels
- [x] send distress call with cameraId, class and Location
- [x] save image to s3
- [x] Save image data to DynamoDB

# Vehicle Client
- [] POST new fire
- [] GET all fire prone areas
- [] Get ongoing actions
- [] Receive Distress calls
- [] display distress reception
- [] Display route calculation

# Server
- [x] CURD Fire
- [] alert vehicle
# Dashboard
- [x] Display frames
- [x] Display Fire
- [x] List Ongoing actions
- [] Display route
- [] Mobile View