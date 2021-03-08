import numpy as np
import pandas as pd
from sklearn.neighbors import KNeighborsRegressor
from crate_scanner.getmusicdata.dataprocessing import *
from crate_scanner.getmusicdata.getmetadata import *



def album_recommender(album_dataset, recommender_output_path):

    recommender_dataset = album_dataset

    non_numerical_cols = ['artists','album_cover', 'album_name', 'album_id', 'first_track_id', 'album', 'loudness']
    X = recommender_dataset.drop(columns=non_numerical_cols).copy()

    # Define y's through specific features
    y_tempo = X['tempo']

    # Instanciate and train audio feature model
    knn_tempo = KNeighborsRegressor().fit(X,y_tempo)

    # Use the model's kneighbors method to pass in a song and grat the 2 nearest to it / drop non-numerial data / returns tuple
    knn_recommended_tempo = knn_tempo.kneighbors(X, n_neighbors=2)

    # Grab the indexes of the recommended songs from knn
    suggested_album_indexes_tempo = knn_recommended_tempo[1][:, 1]

    # Turn the KNN results into values in a dictionary with keys matching indexes
    suggested_album_dict = dict(enumerate(suggested_album_indexes_tempo .flatten(), 0))

    # Turn the KNN dictionary results into a dataframe
    suggested_album_df = pd.DataFrame(suggested_album_indexes_tempo, index=suggested_album_dict.keys())

    # Concatanate to the main dataframe
    recommender_dataset_with_X = pd.concat([X, suggested_album_df], axis=1)
    recommender_dataset_with_X.rename(columns={0: 'suggested_album_index'}, inplace=True)

    # Convert the index/index matching dictionary into to an index/album_id matching dictionary
    for key, value in suggested_album_dict.items():
        suggested_album_dict[key] = recommender_dataset["album_id"][value]

    # Convert this new dictionary of albums into a dataframe
    suggested_album_id_df = pd.DataFrame(list(suggested_album_dict.values()), index=suggested_album_dict.keys())

    # Concatanate the suggested album dataframe to the main dataset
    recommender_dataset_with_X = pd.concat([recommender_dataset_with_X, suggested_album_id_df], axis=1)
    recommender_dataset_with_X.rename(columns={0:'suggested_album_id'}, inplace=True)

    # Concatanate the original dataset with the suggested albums dataset
    recommender_dataset = pd.concat([recommender_dataset, recommender_dataset_with_X], axis=1)
    # Write result as csv to a file path

    recommender_dataset.to_csv(recommender_output_path, index=False)
