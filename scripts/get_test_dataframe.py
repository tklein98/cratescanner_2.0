from os import listdir
from os.path import isfile, join
import matplotlib.pyplot as plt
import pandas as pd
from imageio import imread

def get_test_dataframe(directory_path):
    '''directory_path: Your directory path where you have stored all the testing images'''

    # Create list of all filenames
    filenames = [f for f in listdir(directory_path) if isfile(join(directory_path, f))]
    filenames.sort()
    # Omit .DOS file
    filenames = filenames[1:]

    # Create Dataframe
    df = pd.DataFrame(columns=["picture_path","filename", "label"])

    # Whitelist for creating cleaned string
    whitelist = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')

    # Creating labeled dataframe with picture filepath, filename and the respective label
    # Syntax for label: all lowercase no label
    for i in range(len(filenames)):
        # Clear string of all numbers and special characters and spaces
        cleaned_string = ''.join(filter(whitelist.__contains__, filenames[i]))

        #Appending each row with image filepath,filename and its label
        df = df.append({
             "picture_path": f'{directory_path}{filenames[i]}',
             "filename": filenames[i],
             # Clear the remaining 'jpg' string at the end of every cleaned string
             "label":  cleaned_string[:-3].lower()
              }, ignore_index=True)
    return df
