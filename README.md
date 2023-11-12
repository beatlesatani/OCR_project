# OCR Project

## 1. CNN Handwritten Recognition

### Overview
This component focuses on detecting Hiragana characters using a CNN model. The dataset is sourced from ETL文字データベース, and the model is trained with a modified size of 32x32 images.

### Model Architecture
- Feature Extraction: Kernel size=3, Strides=1, Filters=32, Activation=ReLU
- Pooling: MaxPooling2D
- Optimizer: RMSprop()
- Loss Function: Sparse Categorical Crossentropy
- Accuracy: 100%

[Link to Notebook](link_to_cnn_handwritten_recognition_notebook)

## 2. OCR Model

### Overview
The OCR model detects contours and generates character images for the CNN model to process. Initially attempted without pyocr, it faced issues with connected lines in characters. The morphological dilation transformation in OpenCV solved this problem.

### Model Details
- Contour Detection
- Morphological Dilation
- Adjusting Rectangle Area for Image Generation

[OCR_1.ipynb](https://github.com/beatlesatani/OCR_project/blob/main/OCR_1.ipynb)
[OCR_2.ipynb](https://github.com/beatlesatani/OCR_project/blob/main/OCR_2.ipynb)

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

[Link to Notebook](link_to_ocr_model_notebook)

