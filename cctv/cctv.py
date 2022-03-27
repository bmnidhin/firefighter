# Import required packages
import urllib.request
import cv2
import numpy as np
import sys
import pickle
import datetime
import boto3
import time
from multiprocessing import Pool
import pytz
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import logging
import argparse
import json
from object_detector import ObjectDetector
from object_detector import ObjectDetectorOptions
import utils

kinesis_client = boto3.client("kinesis")
rekog_client = boto3.client("rekognition")


####################### Setup Start ####################################################
dev = True
isKinesis = False
isIoTMessaging = False
url = ''
ipCamera = False
camera_index = 0 # 0 is usually the built-in webcam
capture_rate = 30 # Frame capture rate.. every X frames. Positive integer.
rekog_max_labels = 123
rekog_min_conf = 50.0

####################### Setup end ####################################################
AllowedActions = ['both', 'publish', 'subscribe']

# Custom MQTT message callback
def customCallback(client, userdata, message):
    print("Received a new message: ")
    print(message.payload)
    print("from topic: ")
    print(message.topic)
    print("--------------\n\n")


# Read in command-line parameters
parser = argparse.ArgumentParser()
parser.add_argument("-e", "--endpoint", action="store", default='a3fnw75gmb7w4v-ats.iot.us-west-2.amazonaws.com', required=True, dest="host", help="Your AWS IoT custom endpoint")
parser.add_argument("-r", "--rootCA", action="store", default='root-CA.crt',required=True, dest="rootCAPath", help="Root CA file path")
parser.add_argument("-c", "--cert", action="store",default='cctv-primary.cert.pem', dest="certificatePath", help="Certificate file path")
parser.add_argument("-k", "--key", action="store", default='cctv-primary.private.key',dest="privateKeyPath", help="Private key file path")
parser.add_argument("-p", "--port", action="store", dest="port", type=int, help="Port number override")
parser.add_argument("-w", "--websocket", action="store_true", dest="useWebsocket", default=False, help="Use MQTT over WebSocket")
parser.add_argument("-id", "--clientId", action="store", dest="clientId", default="basicPubSub",help="Targeted client id")
parser.add_argument("-t", "--topic", action="store", dest="topic", default="sdk/test/Python", help="Targeted topic")
parser.add_argument("-m", "--mode", action="store", dest="mode", default="both",help="Operation modes: %s"%str(AllowedActions))
parser.add_argument("-M", "--message", action="store", dest="message", default="Hello World!",help="Message to publish")
parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument( '--model',help='Path of the object detection model.',required=False,default='efficientdet_lite0.tflite')
parser.add_argument('--cameraId', help='Id of camera.', required=False, type=int, default=0)
parser.add_argument('--frameWidth',help='Width of frame to capture from camera.',required=False,type=int,default=640)
parser.add_argument('--frameHeight',help='Height of frame to capture from camera.',required=False,type=int,default=480)
parser.add_argument('--numThreads',help='Number of CPU threads to run the model.',required=False,type=int,default=4)
parser.add_argument('--enableEdgeTPU',help='Whether to run the model on EdgeTPU.',action='store_true',required=False,default=False)


args = parser.parse_args()
host = args.host
rootCAPath = args.rootCAPath
certificatePath = args.certificatePath
privateKeyPath = args.privateKeyPath
port = args.port
useWebsocket = args.useWebsocket
clientId = args.clientId
topic = args.topic
model = args.model
camera_id = int(args.cameraId)
width = args.frameWidth
height = args.frameHeight
num_threads=  int(args.numThreads)
enable_edgetpu = bool(args.enableEdgeTPU)

if args.mode not in AllowedActions:
    parser.error("Unknown --mode option %s. Must be one of %s" % (args.mode, str(AllowedActions)))
    exit(2)

if args.useWebsocket and args.certificatePath and args.privateKeyPath:
    parser.error("X.509 cert authentication and WebSocket are mutual exclusive. Please pick one.")
    exit(2)

if not args.useWebsocket and (not args.certificatePath or not args.privateKeyPath):
    parser.error("Missing credentials for authentication.")
    exit(2)

# Port defaults
if args.useWebsocket and not args.port:  # When no port override for WebSocket, default to 443
    port = 443
if not args.useWebsocket and not args.port:  # When no port override for non-WebSocket, default to 8883
    port = 8883

# Configure logging
logger = logging.getLogger("AWSIoTPythonSDK.core")
logger.setLevel(logging.DEBUG)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)

# Init AWSIoTMQTTClient
myAWSIoTMQTTClient = None
if useWebsocket:
    myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId, useWebsocket=True)
    myAWSIoTMQTTClient.configureEndpoint(host, port)
    myAWSIoTMQTTClient.configureCredentials(rootCAPath)
else:
    myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId)
    myAWSIoTMQTTClient.configureEndpoint(host, port)
    myAWSIoTMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

# AWSIoTMQTTClient connection configuration
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

# Connect IoT Hub and send/Receive required message
# select source of video
# Get Image from IP Cam
cv2.namedWindow("Feed", cv2.WINDOW_AUTOSIZE)

# Get image from saved video
# Predict with model
# Send to Kinesis
#Send frame to Kinesis stream
def encode_and_send_frame(frame, frame_count, enable_kinesis=True, enable_rekog=False, write_file=False):
    try:
        #convert opencv Mat to jpg image
        #print "----FRAME---"
        retval, buff = cv2.imencode(".jpg", frame)

        img_bytes = bytearray(buff)

        utc_dt = pytz.utc.localize(datetime.datetime.now())
        now_ts_utc = (utc_dt - datetime.datetime(1970, 1, 1, tzinfo=pytz.utc)).total_seconds()

        frame_package = {
            'ApproximateCaptureTime' : now_ts_utc,
            'FrameCount' : frame_count,
            'ImageBytes' : img_bytes
        }

        if write_file:
            print("Writing file img_{}.jpg".format(frame_count))
            target = open("img_{}.jpg".format(frame_count), 'w')
            target.write(img_bytes)
            target.close()

        #put encoded image in kinesis stream
        if enable_kinesis:
            print("Sending image to Kinesis")
            response = kinesis_client.put_record(
                StreamName="FrameStream",
                Data=pickle.dumps(frame_package),
                PartitionKey="partitionkey"
            )
            print(response)

        if enable_rekog:
            response = rekog_client.detect_labels(
                Image={
                    'Bytes': img_bytes
                },
                MaxLabels=rekog_max_labels,
                MinConfidence=rekog_min_conf
            )
            print(response)

    except Exception as e:
        print(e)

def publish_to_iot():
     if args.mode == 'both' or args.mode == 'publish':
        message = {}
        message['message'] = args.message
        message['sequence'] = loopCount
        messageJson = json.dumps(message)
        myAWSIoTMQTTClient.publish(topic, messageJson, 1)
        if args.mode == 'publish':
            print('Published topic %s: %s\n' % (topic, messageJson))
        loopCount += 1
     time.sleep(1)

# Main

def main():
        # Variables to calculate FPS
    counter, fps = 0, 0
    start_time = time.time()

    # Start capturing video input from the camera
    cap = cv2.VideoCapture(camera_id)
    if ipCamera:
         imgResponse=urllib.request.urlopen(url) #connect with ipcamera
         cap = np.array(bytearray(imgResponse.read()), dtype=np.uint8)
    else:
        cap = cv2.VideoCapture(camera_id)     
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    # Visualization parameters
    row_size = 20  # pixels
    left_margin = 24  # pixels
    text_color = (0, 0, 255)  # red
    font_size = 1
    font_thickness = 1
    fps_avg_frame_count = 10

    # Initialize the object detection model
    options = ObjectDetectorOptions(
        num_threads=num_threads,
        score_threshold=0.3,
        max_results=3,
        enable_edgetpu=enable_edgetpu)
        
    detector = ObjectDetector(model_path=model, options=options)
    argv_len = len(sys.argv)
    capture_rate = 30
    if argv_len > 1 and sys.argv[1].isdigit():
        capture_rate = int(sys.argv[1])
    pool = Pool(processes=3)

    frame_count = 0
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        #cv2.resize(frame, (640, 360));
        # Image detection start
        counter += 1
        image = cv2.flip(image, 1)

        # Run object detection estimation using the model.
        detections = detector.detect(image)

        # Draw keypoints and edges on input image
        image = utils.visualize(image, detections)

        # Calculate the FPS
        if counter % fps_avg_frame_count == 0:
            end_time = time.time()
            fps = fps_avg_frame_count / (end_time - start_time)
            start_time = time.time()

        # Show the FPS
        fps_text = 'FPS = {:.1f}'.format(fps)
        text_location = (left_margin, row_size)
        cv2.putText(image, fps_text, text_location, cv2.FONT_HERSHEY_PLAIN,
                    font_size, text_color, font_thickness)
        #Image detection end
        if ret is False:
            break

        if frame_count % capture_rate == 0 and False:
            result = pool.apply_async(encode_and_send_frame, (frame, frame_count, True, False, False,))

        frame_count += 1

        # Receive messages from topic
        if args.mode == 'both' or args.mode == 'subscribe':
           myAWSIoTMQTTClient.subscribe(topic, 1, customCallback)
        time.sleep(2)

        # Display the resulting frame
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
    return

if __name__ == '__main__':
    main()