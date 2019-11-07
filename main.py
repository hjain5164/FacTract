from flask import Flask
from flask import send_from_directory
from flask import flash, redirect, render_template, request, session, abort, url_for
import os
import factract
from card import make_card
import wikipedia

app = Flask(__name__)
app.secret_key = os.urandom(16)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search', methods=['GET', 'POST'])
def search():
    # global user_input
    user_input = request.form['user_input']
    search_list = wikipedia.search(user_input)
    length = len(search_list)
    return render_template('search.html', user_input=user_input, search_list=search_list)


@app.route('/fact', methods=['GET', 'POST'])
def fact():
    global user_input
    user_input = request.form['user_input']

    # To capitalize each word of the string
    user_input = user_input.title()

    # To get the image from Wikipedia
    img_url = factract.find_images(user_input)
    l = len(img_url)
    print img_url

    # Error handling if disambiguation occurs
    if img_url is 'False':
        search_list = wikipedia.search(user_input)
        length = len(search_list)
        return render_template('search.html', user_input=user_input,search_list=search_list)

    # Error handling if any other error occurs
    if img_url is 'Error':
        return render_template('index.html', error='Exception', user_input=user_input)



    # Create the flash Card if exits
    card_text = make_card(user_input)
    print '-----------------Card Text ------------------\n'
    print card_text
    flag = True
    if len(card_text) <= 2:
        flag = False

    # Extracts the important text from Wikipedia
    text = factract.factract(user_input).decode('utf-8')
    # if text == '':
    #     return "Working	"
    text = text.split('\n')
    print img_url
    return render_template('profile.html', text=text, length=l, flag=flag, img_url=img_url, user_input=user_input, card_text=card_text)


@app.errorhandler(404)
def badreq(e):
    return render_template('error.html', code=404)


@app.errorhandler(400)
def badreq(e):
    return render_template('error.html', code=400)


if __name__ == "__main__":
    app.run(debug=True)
