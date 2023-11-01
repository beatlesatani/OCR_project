from flask import Flask, render_template, request
import base64

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST' and 'file' in request.files:
        file = request.files['file']
        if file:
            # Read the image file and encode it as base64
            image_data = base64.b64encode(file.read()).decode('utf-8')
            return render_template('index.html', image_data=image_data)
    return render_template('index.html', image_data=None)

if __name__ == '__main__':
    app.run()


"""
So far, codes works,
1.upload the picture from local 
2.display the picture on the same screen

from now, i'll work on the image processing using trained_model.
so, I'll back to here to integrate them

"""