from flask import Flask
from flask import send_from_directory
from flask import flash, redirect, render_template, request, session, abort, url_for
import os
import factract
from card import make_card


app = Flask(__name__)
app.secret_key = os.urandom(16)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/fact', methods=['GET', 'POST'])
def fact():
    global user_input
    user_input = request.form['user_input']

    # To capitalize each word of the string
    user_input = user_input.title()

    # To get the image from Wikipedia
    img_url = factract.get_image(user_input)

    # Error handling if disambiguation occurs
    if img_url is 'False':
        return render_template('index.html', error='Disambiguation', user_input=user_input)

    # Error handling if any other error occurs
    if img_url is 'Error':
        return render_template('index.html', error='Exception', user_input=user_input)

    # Create the flash Card if exits
    card_text = make_card(user_input)
    flag = True
    if len(card_text) <= 2:
        flag = False

    # Extracts the important text from Wikipedia
    text = factract.factract(user_input).decode('utf-8')
    if text == '':
        return "Working	"
    text = text.split('\n')
    return render_template('profile.html', text=text, flag=flag, img_url=img_url, user_input=user_input, card_text=card_text)


@app.errorhandler(404)
def badreq(e):
    return render_template('error.html', code=404)


@app.errorhandler(400)
def badreq(e):
    return render_template('error.html', code=400)


if __name__ == "__main__":
    app.run(debug=True)
