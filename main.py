from flask import Flask
from flask import send_from_directory
from flask import flash, redirect, render_template, request, session, abort, url_for
import os
#import random
import factract
from card import make_card
from imgpil import create_imgs

app = Flask(__name__)
app.secret_key = os.urandom(16)


@app.errorhandler(400)
def badreq(e):
    return render_template('400.html')


@app.route('/')
def index():
    # return render_template('index.html')
    return render_template('index.html')
    # return "Deployed !!"


@app.route('/fact', methods=['GET', 'POST'])
def fact():
    global user_input
    user_input = request.form['user_input']
    user_input = user_input.title()
    img_url = factract.get_image(user_input)
    if img_url is 'False':
        return render_template('index.html', error='Disambiguation', user_input=user_input)
    if img_url is 'Error':
        return render_template('index.html', error='Exception', user_input=user_input)
    card_text = make_card(user_input)
    # print type(card_text)
    # print len(card_text)
    # print card_text
    flag = True
    if len(card_text) <= 2:
        flag = False
    text = factract.factract(user_input).decode('utf-8')
    if text == '':
        return "Working	"
    text = text.split('\n')
    return render_template('profile.html', text=text, flag=flag, img_url=img_url, user_input=user_input, card_text=card_text)


@app.route('/images', methods=['GET'])
def img():
    img_list = create_imgs(user_input)
    print(len(img_list))
    return render_template('image.html', images=img_list)


if __name__ == "__main__":
    app.run(debug=True)
