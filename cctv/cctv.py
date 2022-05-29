# Import required packages
from tkinter import image_names
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
from VideoCapture import Device
import utils
import requests
if False:
    from object_detector import ObjectDetector
    from object_detector import ObjectDetectorOptions
    import utils

kinesis_client = boto3.client("kinesis")
rekog_client = boto3.client("rekognition")


####################### Setup Start ####################################################
dev = True
isKinesis = False
isIoTMessaging = False
url = './fire.mp4'
ipCamera = False
camera_index = 0  # 0 is usually the built-in webcam
capture_rate = 30  # Frame capture rate.. every X frames. Positive integer.
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
parser.add_argument("-e", "--endpoint", action="store", default='a3fnw75gmb7w4v-ats.iot.us-west-2.amazonaws.com',
                    required=True, dest="host", help="Your AWS IoT custom endpoint")
parser.add_argument("-r", "--rootCA", action="store", default='root-CA.crt',
                    required=True, dest="rootCAPath", help="Root CA file path")
parser.add_argument("-c", "--cert", action="store", default='cctv-primary.cert.pem',
                    dest="certificatePath", help="Certificate file path")
parser.add_argument("-k", "--key", action="store", default='cctv-primary.private.key',
                    dest="privateKeyPath", help="Private key file path")
parser.add_argument("-p", "--port", action="store",
                    dest="port", type=int, help="Port number override")
parser.add_argument("-w", "--websocket", action="store_true",
                    dest="useWebsocket", default=False, help="Use MQTT over WebSocket")
parser.add_argument("-id", "--clientId", action="store",
                    dest="clientId", default="basicPubSub", help="Targeted client id")
parser.add_argument("-t", "--topic", action="store", dest="topic",
                    default="sdk/test/Python", help="Targeted topic")
parser.add_argument("-m", "--mode", action="store", dest="mode",
                    default="both", help="Operation modes: %s" % str(AllowedActions))
parser.add_argument("-M", "--message", action="store", dest="message",
                    default="Hello World!", help="Message to publish")
parser = argparse.ArgumentParser(
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--model', help='Path of the object detection model.',
                    required=False, default='efficientdet_lite0.tflite')
parser.add_argument('--cameraId', help='Id of camera.',
                    required=False, type=int, default=0)
parser.add_argument('--frameWidth', help='Width of frame to capture from camera.',
                    required=False, type=int, default=640)
parser.add_argument('--frameHeight', help='Height of frame to capture from camera.',
                    required=False, type=int, default=480)
parser.add_argument('--numThreads', help='Number of CPU threads to run the model.',
                    required=False, type=int, default=4)
parser.add_argument('--enableEdgeTPU', help='Whether to run the model on EdgeTPU.',
                    action='store_true', required=False, default=False)


args = parser.parse_args()
isRaspberry = False
host = 'a3fnw75gmb7w4v-ats.iot.us-west-2.amazonaws.com'
rootCAPath = './keys/root-CA.crt'
certificatePath = './keys/dell2.cert.pem'
privateKeyPath = './keys/dell2.private.key'
port = 883
useWebsocket = False
clientId = "basicPubSub"
topic = "sdk/test/Python"
model = 'efficientdet_lite0.tflite'
classList = ['A', 'B', 'C']
camera_id = 'dell2'
width = 224
height = 224
num_threads = 4
enable_edgetpu = False
url = 'https://postman-echo.com/post'
responseUrl = 'https://postman-echo.com/get?foo1=bar1&foo2=bar2'
isRescuceOn = False
numberOfDistressCalls = 0
isRescueEnded = False
incidentNumber = 0


""" if args.mode not in AllowedActions:
    parser.error("Unknown --mode option %s. Must be one of %s" %
                 (args.mode, str(AllowedActions)))
    exit(2)

if args.useWebsocket and args.certificatePath and args.privateKeyPath:
    parser.error(
        "X.509 cert authentication and WebSocket are mutual exclusive. Please pick one.")
    exit(2)

if not args.useWebsocket and (not args.certificatePath or not args.privateKeyPath):
    parser.error("Missing credentials for authentication.")
    exit(2)

# Port defaults
if args.useWebsocket and not args.port:  # When no port override for WebSocket, default to 443
    port = 443
if not args.useWebsocket and not args.port:  # When no port override for non-WebSocket, default to 8883
    port = 8883 """

# Configure logging
logger = logging.getLogger("AWSIoTPythonSDK.core")
logger.setLevel(logging.DEBUG)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
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
    myAWSIoTMQTTClient.configureCredentials(
        rootCAPath, privateKeyPath, certificatePath)

# AWSIoTMQTTClient connection configuration
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
# Infinite offline Publish queueing
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)
myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

# Connect IoT Hub and send/Receive required message
# select source of video
# Get Image from IP Cam

# Get image from saved video
# Predict with model
# Send to Kinesis
# Send frame to Kinesis stream


def encode_and_send_frame(frame, frame_count, cameraId, cameraLocation, enable_kinesis=True, enable_rekog=False, write_file=False):
    try:
        # convert opencv Mat to jpg image
        # print "----FRAME---"
        retval, buff = cv2.imencode(".jpg", frame)

        img_bytes = bytearray(buff)

        utc_dt = pytz.utc.localize(datetime.datetime.now())
        now_ts_utc = (utc_dt - datetime.datetime(1970, 1,
                      1, tzinfo=pytz.utc)).total_seconds()

        frame_package = {
            'ApproximateCaptureTime': 'steven grant',
            'FrameCount': frame_count,
            'CameraId': cameraId,
            'CameraLocation': cameraLocation,
            'ImageBytes': img_bytes
        }

        if write_file:
            print("Writing file img_{}.jpg".format(frame_count))
            target = open("img_{}.jpg".format(frame_count), 'w')
            target.write(img_bytes)
            target.close()

        # put encoded image in kinesis stream
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
    if ipCamera:
         # imgResponse=urllib.request.urlopen(url) #connect with ipcamera
        #  cap = cv2.VideoCapture(url)
        #  cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        #  cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        # devnum=0 means you are using the device set in 0 position probably your webcam
        cam = Device(devnum=0, showVideoWindow=0)
        # this return a PIL image but I don't know why the first is always black
        blackimg = cam.getImage()
        blackimg.show()  # try to check if you want
        image = cam.getImage()  # this is a real image PIL image
    else:
        cap = cv2.VideoCapture(camera_index)
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
    if isRaspberry:
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
    bytes = b''
    frame_count = 0
    while True:
        frame_jpg = b''

        # bytes += imgResponse.read(16384*2)
        # b = bytes.rfind(b'\xff\xd9')
        # a = bytes.rfind(b'\xff\xd8', 0, b-1)
        a = True
        b = True

        if a != -1 and b != -1:
            # print 'Found JPEG markers. Start {}, End {}'.format(a,b)

            # frame_jpg_bytes = bytes[a:b+2]
            # bytes = bytes[b+2:]

            if frame_count % capture_rate == 0:

                # You can perform any image pre-processing here using OpenCV2.
                # Rotating image 90 degrees to the left:
                # nparr = np.fromstring(frame_jpg_bytes, dtype=np.uint8)

                # Rotate 90 degrees counterclockwise
                # img_cv2_mat = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                # rotated_img = cv2.rotate(img_cv2_mat, cv2.ROTATE_90_COUNTERCLOCKWISE)

                # retval, frame = cv2.imencode(".jpg", rotated_img)

                # Image detection start
                counter += 1
                success, image = cap.read()
                isRescuceOn = False
                # Run object detection estimation using the model.
                if image is not None:
                    # Display the resulting frame
                    dim = (width, height)
                    image = cv2.resize(
                        image, dim, interpolation=cv2.INTER_AREA)
                    if isRaspberry:
                      detections = detector.detect(image)
                      print(detections, 'detections is detections')
                      # Draw keypoints and edges on input image
                    #   image = utils.visualize(image, detections)
                    else:
                      image, prediction = utils.myCustomPrediction(image)
                      fire, non_fire = prediction[0]
                      print(fire, "is the probability of fire")
                      if fire > 0.5 and not isRescuceOn:
                          classDetection = utils.myClassDetector(image)
                          predictedClassIndex = max(classDetection)
                          predictedClass = classList[predictedClassIndex]

                          myobj = {
                                'status': 'fire',  # fire, rescue, closed
                                'location': [8.919330, 76.633760],
                                'sender': camera_id,
                                'classOfFire':  predictedClass
                              }
                          response = requests.post(url, data=myobj)
                          if (response.status_code == 200):
                             print("The request was a success!")
                             print(response.json())
                             isRescuceOn = True
                             numberOfDistressCalls += 1
                             # Code here will only run if the request is successful
                          elif (response.status_code == 404):
                             print("Result not found!")
                             # Code here will react to failed
                    # check status of current operation
                    if isRescuceOn:
                        res = requests.get(responseUrl)
                        if (response.status_code == 200):
                            if (res.json()['status'] == 'closed'):
                                isRescuceOn = False
                                numberOfDistressCalls = 0
                                print("rescue is closed")
                             # Code here will only run if the request is successful
                        elif (response.status_code == 404):
                             print("Result not found!")
                    # Calculate the FPS
                    if counter % fps_avg_frame_count == 0:
                        end_time = time.time()
                        fps = fps_avg_frame_count / (end_time - start_time)
                        start_time = time.time()

                    # Show the FPS
                    fps_text = "fire :" + fire 
                    text_location = (left_margin, row_size)
                    cv2.putText(image, fps_text, text_location, cv2.FONT_HERSHEY_PLAIN,
                                font_size, text_color, font_thickness)
                    cv2.imshow('frame',image)           
                    # Image detection end 
                    # Send to Kinesis
                    if frame_count % capture_rate == 0 and isKinesis:
                       result = pool.apply_async(encode_and_send_frame, (image, frame_count,'dell-pc','tvm',True,False, False,))
                       print(result, 'result is result')	

       
                else:
                    print ("Frame is None")
             
                # Receive messages from topic
                if False:
                  myAWSIoTMQTTClient.subscribe(topic, 1, customCallback)
                time.sleep(2)

                # Display the resulting frame
                # cv2.imshow('frame', image)
                # cv2.waitKey(1) 
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
    return

if __name__ == '__main__':
    main()