import pandas as pd


def grab_rec(album_id, db):
    recommendation_full_dataframe = db
    rec1_row = recommendation_full_dataframe.loc[recommendation_full_dataframe ['album_id'] == album_id]
    rec_list_1 = [] #rec_album image, album artist, album_name
    rec_list_2 = []
    rec_list_3 = []
    try:
        rec_album_image = rec1_row["rec_album_image_1"].values[0]
        rec_album_artist = rec1_row["rec_album_artist_1"].values[0]
        rec_album_name = rec1_row["rec_album_name_1"].values[0]
        rec_list_1.append(rec_album_image)
        rec_list_1.append(rec_album_artist)
        rec_list_1.append(rec_album_name)
        rec_album_image = rec1_row["rec_album_image_2"].values[0]
        rec_album_artist = rec1_row["rec_album_artist_2"].values[0]
        rec_album_name = rec1_row["rec_album_name_2"].values[0]
        rec_list_2.append(rec_album_image)
        rec_list_2.append(rec_album_artist)
        rec_list_2.append(rec_album_name)
        rec_album_image = rec1_row["rec_album_image_3"].values[0]
        rec_album_artist = rec1_row["rec_album_artist_3"].values[0]
        rec_album_name = rec1_row["rec_album_name_3"].values[0]
        rec_list_3.append(rec_album_image)
        rec_list_3.append(rec_album_artist)
        rec_list_3.append(rec_album_name)
        return [rec_list_1, rec_list_2, rec_list_3]
    except:
        return None
