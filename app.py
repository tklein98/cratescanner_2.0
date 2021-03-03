from flask import Flask, flash, request, redirect, url_for, render_template
from scripts.price_scraper import get_price
from scripts.reviews_scraper import get_top3_reviews

app = Flask(__name__)

@app.route('/')
def index():
    price = get_price("zazie", "zen")
    return render_template('index.html', price=price)


@app.route('/result/', methods=['GET'])
def display_result():
    url = request.args.get("url")
    # run model: retrieve album and artist
    # add spotify widget
    # get price

    # get reviews

    #render template, and add variables to be passed to frontend as arguments
    return render_template('result.html')


if __name__ == '__main__':
    app.run()
