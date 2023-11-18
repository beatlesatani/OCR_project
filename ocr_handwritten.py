#### 1.import ####

import os
import cv2
import numpy as np
from imutils import contours
import matplotlib.pyplot as plt
import glob
import tensorflow as tf
from tensorflow.keras.models import load_model
import pandas as pd

#Inport the picture
input_file = "your image path"


# Process for detecting and extracting character regions from images
def block_contours(OCR_input_file):
# setting for morphological dilation
  block_kernel_hight = 5  # height of kernel
  block_kernel_width = 5  # width of kernel
  block_iterations = 4    # num of iteration
  #height range of rectangle area
  block_horizontal_height_minimum = 5  
  block_horizontal_height_max = 1000  
  #width range of rectangle area
  block_vertical_height_minimum = 5  
  block_vertical_height_max = 1000 

  #image size preprocessing
  img = cv2.imread(OCR_input_file)
  width = 450
  height = 350
  img = cv2.resize(img, (width, height))
  # convert image to monochrome gray picture
  img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  # convert to monochrome image
  retval, img_binary = cv2.threshold(img_gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

  # morphological dilation for binary image
  kernel = np.ones((block_kernel_hight, block_kernel_width),np.uint8) 
  img_dilation = cv2.dilate(img_binary,kernel,iterations = block_iterations)

  # detect contour
  #cnts: coordinates of contour,  hierarchy: how to detect contour
  #cv2.RETR_EXTERNAL：return the most external contour.
  #cv2.CHAIN_APPROX_SIMPLE : do not contain all pointns on the contour to reduce data size.leaves only their end points.

  cnts, hierarchy = cv2.findContours(img_dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
  cnts, hierarchy = contours.sort_contours(cnts, method='left-to-right')

  # first setting of ROI
  block_ROI_index = 0

  # convert contour coordinates to the list
  result = []
  for contour in cnts:
    x, y, w, h = cv2.boundingRect(contour)
    # remove too large area / too small area
    if not block_vertical_height_minimum < w < block_vertical_height_max:
      continue
    if not block_horizontal_height_minimum < h < block_horizontal_height_max:
      continue

    x_fix = x-15
    y_fix = y-18
    w_fix = w+40
    h_fix = h+40

    # extract  (capture rectangle and each image is in the rectangle)
    block_ROI = img[y_fix:y_fix+h_fix, x_fix:x_fix+w_fix]
    cv2.imwrite('block_ROI_img{}.png'.format(block_ROI_index), block_ROI)
    block_ROI_index += 1

##excute block_contours
#block_contours(input_file)


def process_images():
    im_size = 32
    im_color = 1

    # List to store the processed images
    result = []
    file_list = glob.glob("block_ROI_img*.png")
    image_files = sorted(file_list)

    # Loop through the image files
    for i, image_file in enumerate(image_files):
        # Load the image using OpenCV
        img = cv2.imread(image_file)
        # Invert the colors of the processed image
        img = 255 - img
        # Convert the image to grayscale and resize it to 32x32
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img_resized = cv2.resize(img_gray, (im_size, im_size))

        # Append the label (i) and the processed image to the result list
        result.append([i, img_resized])

    new_image = []
    for d in result:
        (num, img) = d
        img = img.astype('float').reshape(im_size, im_size, im_color) / 255
        new_image.append(img)
    new_image = np.array(new_image)

    # Delete processed images
    file_list = glob.glob("block_ROI_img*png")
    for file in file_list:
        os.remove(file)

    return new_image


folder = ['あ', 'い', 'う', 'え', 'お',
          'か', 'き', 'く', 'け', 'こ',
          'さ', 'し', 'す', 'せ', 'そ',
          'た', 'ち', 'つ', 'て', 'と',
          'な', 'に', 'ぬ', 'ね', 'の',
          'は', 'ひ', 'ふ', 'へ', 'ほ',
          'ま', 'み', 'む', 'め', 'も',
          'や', 'ゆ', 'よ',
          'ら', 'り', 'る', 'れ', 'ろ',
          'わ', 'ん', 'を']

#When use functions in main.py, comment out this part
'''
block_contours (input_file)
saved_model_path = "your model path" 
model = tf.keras.models.load_model(saved_model_path)
processed_images = process_images()
predicted = model.predict(processed_images)
predictions = np.argmax(predicted, axis=1)
corresponding_labels = [folder[i] for i in predictions]
outcome = ''.join(corresponding_labels)
print(outcome)
'''

