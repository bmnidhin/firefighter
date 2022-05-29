
from typing import List
from keras.models import load_model
from PIL import Image, ImageOps
import numpy as np
import cv2
import numpy as np
from object_detector import Detection

_MARGIN = 10  # pixels
_ROW_SIZE = 10  # pixels
_FONT_SIZE = 1
_FONT_THICKNESS = 1
_TEXT_COLOR = (0, 0, 255)  # red

def myCustomPrediction(image):
  # Load the model
  model = load_model('./models/keras_model.h5')

# Create the array of the right shape to feed into the keras model
# The 'length' or number of images you can put into the array is
# determined by the first position in the shape tuple, in this case 1.
  data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
# Replace this with the path to your image
  # image = Image.open('<IMAGE_PATH>')
#resize the image to a 224x224 with the same strategy as in TM2:
#resizing the image to be at least 224x224 and then cropping from the center
  # size = (224, 224)
  # image = ImageOps.fit(image, size, Image.ANTIALIAS)

#turn the image into a numpy array
  image_array = np.asarray(image)
# Normalize the image
  normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
# Load the image into the array
  data[0] = normalized_image_array

# run the inference
  prediction = model.predict(data)
  print(prediction)
  return [image,prediction]

def myClassDetector(image):
  # Load the model
  model = load_model('./models/flower_detector.h5')

# Create the array of the right shape to feed into the keras model
# The 'length' or number of images you can put into the array is
# determined by the first position in the shape tuple, in this case 1.
  data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
# Replace this with the path to your image
  # image = Image.open('<IMAGE_PATH>')
#resize the image to a 224x224 with the same strategy as in TM2:
#resizing the image to be at least 224x224 and then cropping from the center
  # size = (224, 224)
  # image = ImageOps.fit(image, size, Image.ANTIALIAS)

#turn the image into a numpy array
  image_array = np.asarray(image)
# Normalize the image
  normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
# Load the image into the array
  data[0] = normalized_image_array

# run the inference
  prediction = model.predict(data)
  print(prediction)
  return [image,prediction]

def visualize(
    image: np.ndarray,
    detections: List[Detection],
) -> np.ndarray:
  """Draws bounding boxes on the input image and return it.
  Args:
    image: The input RGB image.
    detections: The list of all "Detection" entities to be visualize.
  Returns:
    Image with bounding boxes.
  """
  for detection in detections:
    # Draw bounding_box
    start_point = detection.bounding_box.left, detection.bounding_box.top
    end_point = detection.bounding_box.right, detection.bounding_box.bottom
    cv2.rectangle(image, start_point, end_point, _TEXT_COLOR, 3)

    # Draw label and score
    category = detection.categories[0]
    class_name = category.label
    probability = round(category.score, 2)
    result_text = class_name + ' (' + str(probability) + ')'
    text_location = (_MARGIN + detection.bounding_box.left,
                     _MARGIN + _ROW_SIZE + detection.bounding_box.top)
    cv2.putText(image, result_text, text_location, cv2.FONT_HERSHEY_PLAIN,
                _FONT_SIZE, _TEXT_COLOR, _FONT_THICKNESS)

  return image