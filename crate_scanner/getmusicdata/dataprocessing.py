#MOVE TO METADATA FOLDER

# GET AND CLEAN DATAF FROM SPOTIFY AND PUT INTO DATAFRAME
def clean_artists_col(artists):
    cleaned_text = artists.replace('[','').replace(']','')
    return cleaned_text


def get_album_image(album):
    # Extract the relevant album image url (64x64) from the API json
    if album and len(album['images'])>0:
        return album['images'][0]['url']
    else:
        return None


def get_album_name(album):
    # Extract the relevant album name from the API json
    if album:
        return album['name']
    else:
        return None


def get_album_id(album):
    # Extract the relevant album_id from the API json
    if album:
        return album['id']
    else:
        return None
