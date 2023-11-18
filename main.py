import ocr_handwritten
from flask import Flask, render_template, request
import base64
import requests
import random
import genanki
import atexit
import os 
import tensorflow as tf
import numpy as np
import hashlib
import base64

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Initialize my_deck as None
my_deck = None

@app.route('/', methods=['GET', 'POST'])
def home():
    global my_deck  # Move this line here

    user_input = None
    image_data = None
    search_result = None

    if request.method == "POST":
    # Check if 'file' is in the request
        if 'file' in request.files:
            file = request.files['file']
            if file:
                # Read the image file and encode it as base64
                file_64 = file
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(file_path)
                image_data = base64.b64encode(file_64.read()).decode('utf-8')
                ocr_handwritten.block_contours(file_path)
                os.remove(file_path)
                sha256_hash = "59292cd4f38367b7d35f169fe5398b770a5d06f9dc36f1b6a1f552d9f80e0ba1"
                base64_hash = base64.urlsafe_b64encode(bytes.fromhex(sha256_hash)).decode()
                #saved_model_path = f"models/{base64_hash}/"
                saved_model_path = "/Users/yusuke.s/Documents/GitHub/OCR_project/hiragana_recognition_cnn.h5"
                model = tf.keras.models.load_model(saved_model_path)
                processed_images = ocr_handwritten.process_images()
                predicted = model.predict(processed_images)
                predictions = np.argmax(predicted, axis=1)
                corresponding_labels = [folder[i] for i in predictions]
                user_input = ''.join(corresponding_labels)
                if user_input:
                    search_result = search_word_in_dictionary(user_input)
                    if my_deck is None:
                        my_deck = create_deck()
                    add_card_to_deck(my_deck, user_input, search_result)
        else:
            # Retrieve the user input from the keyboard 
            user_input = request.form.get("user_input")
            if user_input:
                search_result = search_word_in_dictionary(user_input)
                if my_deck is None:
                    my_deck = create_deck()
                add_card_to_deck(my_deck, user_input, search_result)

    return render_template("index.html", user_input=user_input, image_data=image_data, search_result=search_result)




# Function to search for words in the dictionary and retrieve meanings
def search_word_in_dictionary(word):
    response = requests.get(f"https://jisho.org/api/v1/search/words?keyword={word}")
    if response.status_code == 200:
        data = response.json()
        # Assuming that `data` contains the JSON data you posted
        meanings = []
        for entry in data['data']:
            senses = entry['senses']
            for sense in senses:
                eng_meaning = sense.get('english_definitions', [])
                meanings.append(eng_meaning)
        return meanings[0]
    else:
        return "Word not found or API error"


# Function to create and return a my_deck
def create_deck():
    sec_random = random.randrange(1 << 30, 1 << 31)
    my_deck = genanki.Deck(sec_random, 'English')
    return my_deck


# Function to add a card to the my_deck
def add_card_to_deck(my_deck, wor, defi):
    fir_random = random.randrange(1 << 30, 1 << 31)
    my_model = genanki.Model(fir_random, 'English',
                            fields=[
                                {'name': 'Question'},
                                {'name': 'Answer'},
                            ],
                            templates=[
                                {
                                    'name': 'Card 1',
                                    'qfmt': '{{Question}}',
                                    'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
                                },
                            ])
    my_note = genanki.Note(model=my_model, fields=[str(wor), str(defi)])
    my_deck.add_note(my_note)


# Function to write the my_deck to the output.apkg file
def write_deck_to_file():
    if my_deck:
        genanki.Package(my_deck).write_to_file('output.apkg')


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

atexit.register(write_deck_to_file)

if __name__ == '__main__':
    app.run()