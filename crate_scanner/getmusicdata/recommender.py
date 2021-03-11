import numpy as np
import pandas as pd
from sklearn.neighbors import KNeighborsRegressor
from crate_scanner.getmusicdata.dataprocessing import *
from crate_scanner.getmusicdata.getmetadata import *
from sklearn.preprocessing import MinMaxScaler



def album_recommender(album_dataset, recommender_output_path):

    recommender_dataset = album_dataset

    non_numerical_cols = ['artists', 'album_cover', 'album_name', 'album_id', 'first_track_id', 'album']

    X = recommender_dataset.drop(columns=non_numerical_cols).copy()
    y_tempo = X['tempo']

    #Intantiate MinMaxScaler() and fit/transofrm each column
    minmax = MinMaxScaler()
    X['danceability']= minmax.fit(X[["danceability"]]).transform(X[["danceability"]])
    X['energy']= minmax.fit(X[["energy"]]).transform(X[["energy"]])
    X['speechiness']= minmax.fit(X[["speechiness"]]).transform(X[["speechiness"]])
    X['acousticness']= minmax.fit(X[["acousticness"]]).transform(X[["acousticness"]])
    X['instrumentalness']= minmax.fit(X[["instrumentalness"]]).transform(X[["instrumentalness"]])
    X['liveness']= minmax.fit(X[["liveness"]]).transform(X[["liveness"]])
    X['valence']= minmax.fit(X[["valence"]]).transform(X[["valence"]])
    X['tempo']= minmax.fit(X[["tempo"]]).transform(X[["tempo"]])
    X['loudness']= minmax.fit(X[["loudness"]]).transform(X[["loudness"]])
    X['key']= minmax.fit(X[["key"]]).transform(X[["key"]])

    # Instanciate and train audio feature model
    knn_tempo = KNeighborsRegressor().fit(X,y_tempo)

    # Use the model's kneighbors method to pass in a song and grat the 2 nearest to it / drop non-numerial data / returns tuple
    knn_recommended_tempo = knn_tempo.kneighbors(X, n_neighbors=5)

    # Grab the indexes of the recommended songs from knn
    suggested_album_indexes_tempo = knn_recommended_tempo[1][:, 1:]

    # Turn the KNN results into values in a dictionary with keys matching indexes
    suggested_album_dict = dict(enumerate(suggested_album_indexes_tempo))

    # Turn the KNN dictionary results into a dataframe
    suggested_album_index_df = pd.DataFrame(suggested_album_dict.values(), index=suggested_album_dict.keys())

    # Concatanate to the main dataframe & rename columns
    recommender_dataset_with_X = pd.concat([X, suggested_album_index_df], axis=1)
    recommender_dataset_with_X.rename(columns={0: 'rec_album_1', 1: 'rec_album_2', 2: 'rec_album_3', 3: 'rec_album_4'}, inplace=True)

    # Turn album_id column into a index/id matching dictionary
    album_image_dictionary = dict(recommender_dataset["album_cover"])
    album_id_dictionary = dict(recommender_dataset['album_id'])
    album_artist_dictionary = dict(recommender_dataset['artists'])
    album_name_dictionary = dict(recommender_dataset['album_name'])

    # Create new columns for the suggested album cover image (urls)
    recommender_dataset_with_X["rec_album_image_1"] = recommender_dataset_with_X.rec_album_1.map(album_image_dictionary)
    recommender_dataset_with_X["rec_album_image_2"] = recommender_dataset_with_X.rec_album_2.map(album_image_dictionary)
    recommender_dataset_with_X["rec_album_image_3"] = recommender_dataset_with_X.rec_album_3.map(album_image_dictionary)
    recommender_dataset_with_X["rec_album_image_4"] = recommender_dataset_with_X.rec_album_4.map(album_image_dictionary)

    # Create new columns for the suggested album artist
    recommender_dataset_with_X["rec_album_artist_1"] = recommender_dataset_with_X.rec_album_1.map(album_artist_dictionary)
    recommender_dataset_with_X["rec_album_artist_2"] = recommender_dataset_with_X.rec_album_2.map(album_artist_dictionary)
    recommender_dataset_with_X["rec_album_artist_3"] = recommender_dataset_with_X.rec_album_3.map(album_artist_dictionary)
    recommender_dataset_with_X["rec_album_artist_4"] = recommender_dataset_with_X.rec_album_4.map(album_artist_dictionary)

    # Create new columns for the suggested album name
    recommender_dataset_with_X["rec_album_name_1"] = recommender_dataset_with_X.rec_album_1.map(album_name_dictionary)
    recommender_dataset_with_X["rec_album_name_2"] = recommender_dataset_with_X.rec_album_2.map(album_name_dictionary)
    recommender_dataset_with_X["rec_album_name_3"] = recommender_dataset_with_X.rec_album_3.map(album_name_dictionary)
    recommender_dataset_with_X["rec_album_name_4"] = recommender_dataset_with_X.rec_album_4.map(album_name_dictionary)

    # Assign the respective album_id in each column
    recommender_dataset_with_X.rec_album_1 = recommender_dataset_with_X.rec_album_1.map(album_id_dictionary)
    recommender_dataset_with_X.rec_album_2 = recommender_dataset_with_X.rec_album_2.map(album_id_dictionary)
    recommender_dataset_with_X.rec_album_3 = recommender_dataset_with_X.rec_album_3.map(album_id_dictionary)
    recommender_dataset_with_X.rec_album_4 = recommender_dataset_with_X.rec_album_4.map(album_id_dictionary)
    # Concatanate the suggested album dataframe to the main dataset
    # recommender_dataset_with_X = pd.concat([recommender_dataset_with_X, suggested_album_id_df], axis=1)
    # recommender_dataset_with_X.rename(columns={0:'suggested_album_id'}, inplace=True)

    # Concatanate the original dataset with the suggested albums dataset
    recommender_dataset = pd.concat([recommender_dataset, recommender_dataset_with_X], axis=1)
    # Write result as csv to a file path

    recommender_dataset.to_csv(recommender_output_path, index=False)
