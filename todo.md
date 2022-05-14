
# Camera Client

- [] Capature wit camera
- [] Capture with ipcamera
- [] Detect fire
- [] Detect Class of fire
- [] send frames to kinesis
- [] send cameraid to Kinesis
- [] distress call to IoT Hub {cameraID, classOfFire,location }
- [] send HTTP req to central hub

# Frame Processor
- [] Get cameraid from metadata
- [] process frames and detect labels
- [] send distress call with cameraId, class and Location
- [] save image to s3
- [] Save image data to DynamoDB

# Vehicle Client
- [] Receive Distress calls
- [] display distress reception
- [] Display route calculation

# Central Hub
- [] POST new fire
- [] GET all fire prone areas
- [] Get ongoing actions

# Dashboard

- [] Display frames
- [] Display Fire
- [] List Ongoing actions
- [] Display route