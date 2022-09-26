from flask import Flask, request, render_template
from crate_scanner.scrapers.price_scraper import get_price
from crate_scanner.scrapers.reviews_scraper import get_top3_reviews
import os
from tensorflow.keras.models import Model
# from tensorflow.keras.applications import VGG16
import tensorflow as tf
import numpy as np
from crate_scanner.albuminfo import matched_album
from crate_scanner.albuminfo import make_prediction
from crate_scanner.recommender import grab_rec
import json
import argparse
import pandas as pd
import re

# Creating basemodel for vectorization

# model_new = tf.keras.applications.resnet50.ResNet50(
#     include_top=True,
#     weights='imagenet',
#     input_tensor=None,
#     input_shape=None,
#     pooling=None,
#     classes=1000,
# )

# basemodel = Model(inputs=model_new.input, outputs=model_new.get_layer('avg_pool').output)

basemodel = tf.keras.models.load_model('crate_scanner/data/resnet50_avg_model.h5')
TEMPLATE_DIR = os.path.abspath('templates')
STATIC_DIR = os.path.abspath('static')

# loading images database
database = np.load('crate_scanner/data/resnet50_preprocessing.npy', allow_pickle=True)
recommender_db = pd.read_csv('crate_scanner/data/recommendation_full_dataframe.csv')

app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/album-api/', methods=['GET'])
def return_data():
    url = request.args.get("url")
    # run model 1:artist, 2:album, 3:artist+album, 4: album_id, 5: album_cover
    album_info = make_prediction(basemodel,url, database)
    print('prediction:',album_info)
    # run model: retrieve album, artist and cover
    cleaned = album_info.lower().replace(".jpg", "")
    # artist = album_info[1].lower().replace("'", "")
    # album = album_info[2].lower().replace("'", "")
    # album = re.sub("[\(\[].*?[\)\]]", "", album)

    split = cleaned.split('_')
    album = split[0]
    artist = split[1]
    print('album',album,'artist',artist)
    cover_url = album_info[5]

    # add spotify widget
    # album_id = album_info[4]
    album_id = '1C2h7mLntPSeVYciMRTF4a'
    # get price
    price = '20'
    # format(get_price(artist, album)[1], '.2f')
    url_price = 'www.google.com'
    # get_price(artist, album)[0]

    print('price:',price)
    # get reviews
    reviews = get_top3_reviews(artist, album)

    #get recommendation_full_dataframe.csv
    rec = grab_rec(album_id,recommender_db)

    # get 1st recommended album
    rec_album_1 = rec[0][2].replace("'", "")
    rec_artist_1 = rec[0][1].replace("'", "")
    rec_img_1 = rec[0][0]

    # get 2nd
    rec_album_2 = rec[1][2].replace("'", "")
    rec_artist_2 = rec[1][1].replace("'", "")
    rec_img_2 = rec[1][0]

    # get 3rd
    rec_album_3 = rec[2][2].replace("'", "")
    rec_artist_3 = rec[2][1].replace("'", "")
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
