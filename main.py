from flask import Flask, render_template, request
import base64
import requests
import random
import genanki

app = Flask(__name__)
# Your route for the web application
@app.route('/', methods=['GET', 'POST'])
def home():
    user_input = None
    image_data = None
    search_result = None

    if request.method == "POST":
        # Check if 'file' is in the request
        if 'file' in request.files:
            file = request.files['file']
            if file:
                # Read the image file and encode it as base64
                image_data = base64.b64encode(file.read()).decode('utf-8')
   
            # Retrieve the user input from the form
        user_input = request.form.get("user_input")
        if user_input:
            search_result = search_word_in_dictionary(user_input)
            card_gen(user_input, search_result)
    return render_template("index.html", user_input=user_input, image_data=image_data, search_result=search_result)


# Function to search for words in the dictionary and retrieve meanings
def search_word_in_dictionary(word):
    response = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}")
    if response.status_code == 200:
        data = response.json()
        # Parse the response and extract meanings or relevant data
        # For example, you can access the data as data[0]["meanings"]
        definition = data[0]["meanings"][0]["definitions"][0]["definition"]
        return definition
    else:
        return "Word not found or API error"
    
def card_gen(wor, defi):
    fir_random = random.randrange(1 << 30, 1 << 31)
    sec_random = random.randrange(1 << 30, 1 << 31)
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
    my_note = genanki.Note(model=my_model, fields=[wor, defi])
    my_deck = genanki.Deck(sec_random, 'English')
    my_deck.add_note(my_note)
    genanki.Package(my_deck).write_to_file('output.apkg')
   


   

'''   
# Function to create a Quizlet set and add terms and definitions
def make_cards(accessToken, setName, terms, definitions):
    # Use Quizlet API to create a set
    # Iterate through terms and definitions and add them to the set
'''


if __name__ == '__main__':
    app.run()

"""
So far, codes works,
1.upload the picture from local 
2.display the picture on the same screen

from now, i'll work on the image processing using trained_model.
so, I'll back to here to integrate them

"""