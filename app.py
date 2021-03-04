from flask import Flask, flash, request, redirect, url_for, render_template
from scripts.price_scraper import get_price
from scripts.reviews_scraper import get_top3_reviews


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/result/', methods=['GET'])
def display_result():
    url = request.args.get("url")

    # run model: retrieve album and artist
    artist = "red hot chili peppers"
    album = "by the way"

    # add spotify widget
    album_id = "2UJcKiJxNryhL050F5Z1Fk"

    # get price
    price = get_price(artist, album)

    # get reviews

    reviews = get_top3_reviews(artist, album)

    #render template, and add variables to be passed to frontend as arguments
    return render_template('result.html', artist=artist, album=album, album_id=album_id, price=price, reviews=reviews)


if __name__ == '__main__':
    app.run()
