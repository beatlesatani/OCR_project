# OCR Project

## 1. CNN Handwritten Recognition

### Overview
This component focuses on detecting Hiragana characters using a CNN model. The dataset is sourced from ETL文字データベース, and the model is trained with a modified size of 32x32 images.

### Model Architecture
1.CNN model
- Feature Extraction: Kernel size=3, Strides=1, Filters=32, Activation=ReLU
- Pooling: MaxPooling2D
- Optimizer: RMSprop()
- Loss Function: Sparse Categorical Crossentropy
- Accuracy: 98.11%
2. AlexNet model
- 5 convolutional layers.
- 3 fully connected layers
- Optimizer: RMSprop()
- Loss Function: Sparse Categorical Crossentropy
- Accuracy: 99.38%

[Notebook for recognition model](https://github.com/beatlesatani/OCR_project/blob/d14516a2c8d4bba47315db06f539d93973656dc7/recognition_modeling.ipynb)

## 2. OCR Model

### Overview
The OCR model detects contours and generates character images for the CNN model to process. Initially attempted without pyocr, it faced issues with connected lines in characters. The morphological dilation transformation in OpenCV solved this problem.

### Model Details
- Contour Detection
- Morphological Dilation
- Adjusting Rectangle Area for Image Generation

[OCR_1.ipynb](https://github.com/beatlesatani/OCR_project/blob/main/OCR_1.ipynb) (basic OCR model without adjustment),

[OCR_2.ipynb](https://github.com/beatlesatani/OCR_project/blob/main/OCR_2.ipynb) (OCR model with adjustment such as morphological Dilation, adjusting rectangle area)

## 3. Model Deployment

### Transporting Models to Local Environment
Models built on Ubuntu VM and Colab are made available for local use, addressing issues with M1 chip MacBooks using Miniforge and virtual environments.

## 4. Automated Flashcard Generator

### Overview
An automated flashcard generator that uses the Jisho API to retrieve word meanings. Flashcards are then exported into an Anki deck (output.apkg) for easy import.

### Usage
1. Input words or use a picture for word retrieval.
2. Jisho API fetches word meanings.
3. Anki flashcards are generated and exported.

[Link to Jisho API](https://jisho.org/)
[Link to Anki API](https://ankiweb.net/shared/info/2055492159)



