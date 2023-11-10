
#### 1.import ####

import os
import cv2
import numpy as np
from imutils import contours
import matplotlib.pyplot as plt
import glob
from tensorflow.keras.models import load_model
import pandas as pd
#from natsort import natsorted 


#### ２．set up pictures ####
input_file = "/Users/yusuke.s/Documents/GitHub/OCR_project/pictures/happy.png"

# 膨張処理の設定
#【横書き】大まかな文字領域の検出（ブロック検出）のための膨張処理（カーネルサイズ・膨張処理回数）の設定
block_kernel_hight = 5  # カーネルの縦の高さ
block_kernel_width = 5  # カーネルの横の幅
block_iterations = 4    # 膨張処理回数

# 輪郭のカット設定
# ブロック検出：文字領域検出した輪郭の「横幅」が、以下の範囲なら輪郭を残す
block_horizontal_height_minimum = 5  # 最小値（ピクセル）
block_horizontal_height_max = 1000   # 最大値（ピクセル）

# ブロック検出：文字領域検出した輪郭の「縦の高さ」が、以下の範囲なら輪郭を残す
block_vertical_height_minimum = 5  # 最小値（ピクセル）
block_vertical_height_max = 1000   # 最大値（ピクセル）



####  ４．大まかな文字領域の検出（ブロック検出） ####
# 画像から、ブロック検出をおこないます
# 「block_ROI_img〜.png」（ブロック検出画像）を作成します
# 「block_text-detection.png」（ブロック検出の結果を、元の画像に描画した画像）を作成します


# Process for detecting and extracting character regions from images
def block_contours (OCR_input_file):
  img = cv2.imread(OCR_input_file)
  width = 450
  height = 350
  img = cv2.resize(img, (width, height))

  # convert image to monochrome gray picture
  img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

  # convert to monochrome image
  retval, img_binary = cv2.threshold(img_gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

  # 白部分の膨張処理（Dilation）：モルフォロジー変換 - 2値画像を対象
  kernel = np.ones((block_kernel_hight, block_kernel_width),np.uint8) 
  img_dilation = cv2.dilate(img_binary,kernel,iterations = block_iterations)

  '''
  print('\n【Binarization】')

  # 膨張処理後の2値化画像の表示
  plt.imshow(cv2.cvtColor(img_dilation, cv2.COLOR_BGR2RGB))
  plt.show()
  '''

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

    #result.append([x, y, w, h])
    result.append([x_fix,y_fix,w_fix,h_fix])


  # 画面に矩形の輪郭を描画 （描画機能）
  for x, y, w, h in result:
      cv2.rectangle(img, (x, y), (x+w, y+h), (100, 255, 100), 3)

'''
  # 解説用のコメント（文字領域の輪郭検出・抽出）
  print('\n【Text detection・Contours】')

  # 文字領域の輪郭検出・抽出結果の表示
  plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
  plt.savefig('block_text-detection.png', dpi=300)
  plt.show()
'''


##excute block_contours
block_contours(input_file)

model = load_model("/Users/yusuke.s/Documents/GitHub/OCR_project/hiragana_recognition_cnn.h5")