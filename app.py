from flask import Flask, request, render_template
from crate_scanner.scrapers.price_scraper import get_price
from crate_scanner.scrapers.reviews_scraper import get_top3_reviews
import os
from tensorflow.keras.models import Model
from tensorflow.keras.applications import VGG16
import numpy as np
from crate_scanner.albuminfo import matched_album
from crate_scanner.recommender import grab_rec
import json
import argparse
import pandas as pd

# Creating basemodel for vectorization
vgg16 = VGG16(weights='imagenet', include_top=True, pooling='max', input_shape=(224, 224, 3))
basemodel = Model(inputs=vgg16.input, outputs=vgg16.get_layer('flatten').output)

TEMPLATE_DIR = os.path.abspath('templates')
STATIC_DIR = os.path.abspath('static')

# loading images database
full_vectors = np.load('crate_scanner/data/VGG16_flatten_highres_array.npy', allow_pickle=True)
recommender_db = pd.read_csv('crate_scanner/data/recommendation_full_dataframe.csv')

app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)
app.debug = True


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/album-api/', methods=['GET'])
def return_data():
    url = request.args.get("url")
    # run model 1:artist, 2:album, 3:artist+album, 4: album_id, 5: album_cover
    album_info = matched_album(url, basemodel, full_vectors)

    # run model: retrieve album, artist and cover
    artist = album_info[1].lower()
    album = album_info[2].lower()
    cover_url = album_info[5]

    # add spotify widget
    album_id = album_info[4]

    # get price
    price = get_price(artist, album)[1]
    url_price = get_price(artist, album)[0]

    # get reviews
    reviews = get_top3_reviews(artist, album)

    #get recommendation_full_dataframe.csv
    rec = grab_rec(album_id,recommender_db)

    # get 1st recommended album
    rec_album_1 = rec[0][2]
    rec_artist_1 = rec[0][1]
    rec_img_1 = rec[0][0]

    # get 2nd
    rec_album_2 = rec[1][2]
    rec_artist_2 = rec[1][1]
    rec_img_2 = rec[1][0]

    # get 3rd
    rec_album_3 = rec[2][2]
    rec_artist_3 = rec[2][1]
    rec_img_3 = rec[2][0]

    data = {
      "artist": artist.title(),
      "album": album.title(),
      "cover_url": cover_url,
      "url_price": url_price,
      "album_id": album_id,
      "price": price,
      "reviews": reviews,
      "rec_album_1": rec_album_1,
      "rec_artist_1": rec_artist_1,
      "rec_img_1": rec_img_1,
      "rec_album_2": rec_album_2,
      "rec_artist_2": rec_artist_2,
      "rec_img_2": rec_img_2,
      "rec_album_3": rec_album_3,
      "rec_artist_3": rec_artist_3,
      "rec_img_3": rec_img_3,

    }

    response = app.response_class(
      response = json.dumps(data),
      status=200,
      mimetype='application/json'
      )

    return response



@app.route('/result/', methods=['GET'])
def display_result():
    url = request.args.get("url")

    return render_template('result.html', url=url)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type = int, default=80, help="Number of the port")
    parser.add_argument("--host", type = str, default='0.0.0.0', help="host url/adress")
    args = parser.parse_args()
    app.run(host=args.host, port=args.port)
