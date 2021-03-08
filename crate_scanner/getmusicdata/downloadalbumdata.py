 #!/usr/bin/python3


import pandas as pd
from sklearn.neighbors import KNeighborsRegressor
from crate_scanner.getmusicdata.dataprocessing import *
from crate_scanner.getmusicdata.getmetadata import *


def get_album_metadata(input_file, input_file_2, nrows, skiprows, album_output_file):

    # Reads and ammends files from "https://www.besteveralbums.com/"
    # Read data file into dataframe
    input_df = pd.read_csv(input_file, skiprows = skiprows, nrows = nrows, header=None)
    input_df['artists'] = input_df[1]
    input_df = input_df['artists']
    input_df = pd.DataFrame(input_df)

    # Clean data in the artist column
    input_df['artists'] = input_df['artists'].map(clean_artists_col)

    # Retreive album data from Spotify API
    input_df['album'] = input_df['artists'].map(get_album)

    # Extract from the album column
    input_df['album_cover'] = input_df['album'].map(get_album_image)
    input_df['album_name'] = input_df['album'].map(get_album_name)
    input_df['album_id'] = input_df['album'].map(get_album_id)

    # Read Best album dataset file into dataframe
    input_df_2 = pd.read_csv(input_file_2, skiprows = range(1,skiprows), nrows = nrows)
    input_df_2['artists'] = input_df_2['Band']
    input_df_2['album_name'] = input_df_2['Title']
    input_df_2 = input_df_2.drop(['DecadeRank', 'Compilation',\
                                  'OverallRank', 'RankScore',\
                                  "AvgRating", "NumRatings", "AlbumID",\
                                  "Notes", "Buy", "Rank", "Live", \
                                  "YearRank", "Title", "Band", \
                                  "Country", "Year"], axis=1)
    input_df_2["album_artist"] = input_df_2["artists"] + " " + input_df_2["album_name"]

    # # Retreive album data from Spotify API and creat album column
    input_df_2["album"] = input_df_2['album_artist'].map(get_album)

    # Extract details from the album column and set to respective attributes
    input_df_2["album_name"] = input_df_2["album"].map(get_album_name)
    input_df_2["album_cover"] = input_df_2["album"].map(get_album_image)
    input_df_2["album_id"] = input_df_2["album"].map(get_album_id)
    del input_df_2["album_artist"]

    #Re-order the columns to match column order of input_df
    input_df_2 = input_df_2[['artists', 'album', 'album_cover', 'album_name', 'album_id']]

    # #Concatenate the two dataframes into one
    album_dataset = pd.concat([input_df, input_df_2], ignore_index=True)

    # Add a column with the first track based on album_id
    album_dataset["first_track_id"]=album_dataset["album_id"].map(get_track_from_album)

    # Create a series with audio features (as dicts{}) for each song
    music_features = album_dataset["first_track_id"].map(get_track_audio_features)
    # Create a dataframe with audio features
    music_features_df = pd.DataFrame(list(music_features), columns=["danceability", "energy", "key", "loudness", "mode", "speechiness", "acousticness", "instrumentalness", "liveness", "valence", "tempo"])

    # Horizontally concatenate the album_id_df with the music features df
    album_dataset = pd.concat([album_dataset, music_features_df], axis=1)

    # # Drop duplicates and rows with none values in the album_id column
    album_dataset = album_dataset.dropna(axis=0, subset=['album_id'])
    album_dataset.drop_duplicates(subset=['album_id'], inplace=True)
    album_dataset.reset_index(drop=True, inplace=True)

    # ['artists', 'album', 'album_cover', 'album_name', 'album_id',
       #'first_track_id', 'danceability', 'energy', 'key', 'loudness', 'mode',
      # 'speechiness', 'acousticness', 'instrumentalness', 'liveness',
       #'valence', 'tempo']

    # ALBUM RECOMMENDER
    # Define X / Remove non-numerical columns
    non_numerical_cols = ['artists','album_cover', 'album_name', 'album_id', 'first_track_id', 'album']
    X = album_dataset.drop(columns=non_numerical_cols).copy()

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
    album_dataset_with_X = pd.concat([X, suggested_album_df], axis=1)
    album_dataset_with_X.rename(columns={0: 'suggested_album_index'}, inplace=True)

    # Convert the index/index matching dictionary into to an index/album_id matching dictionary
    for key, value in suggested_album_dict.items():
        suggested_album_dict[key] = album_dataset["album_id"][value]

    # Convert this new dictionary of albums into a dataframe
    suggested_album_id_df = pd.DataFrame(list(suggested_album_dict.values()), index=suggested_album_dict.keys())

    # Concatanate the suggested album dataframe to the main dataset
    album_dataset_with_X = pd.concat([album_dataset_with_X, suggested_album_id_df], axis=1)
    album_dataset_with_X.rename(columns={0:'suggested_album_id'}, inplace=True)



    # Concatanate the original dataset with the suggested albums dataset
    album_dataset = pd.concat([album_dataset, album_dataset_with_X], axis=1)
    # Write result as csv to a file path

    album_dataset.to_csv(album_output_file, index=False)


def get_song_metadata(input_file, nrows, skiprows, song_output_file):

    # Read Kaggle "Spotify Dataset 1921-2020, 160k+ Tracks" metadata into a dataframe
    input_df = pd.read_csv(input_file, skiprows = range(1,skiprows), nrows = nrows)

    # Call the Spotify API to extract the correct albumn_id based on track_id and make it in a new column
    input_df["album_id"] = input_df["id"].map(get_album_by_track_id)

    # Save file as csv
    input_df.to_csv(song_output_file, index=False)


if __name__ == "__main__":
    # execute only if run as a script
    album_output_path = "/Users/wesleyhouse/code/WesH0use/crate_scanner/crate_scanner/data/full_albums.csv"
    local_path = "/Users/wesleyhouse/code/WesH0use/crate_scanner/notebooks/data/data.csv"
    local_path_2 = "/Users/wesleyhouse/code/WesH0use/crate_scanner/notebooks/data/best_albums.csv"
    get_album_metadata(local_path, local_path_2, nrows=15000, skiprows=1000, album_output_file = album_output_path)
    # Returns dataframe with 5 rows
    #return input_df




