from os import listdir
from os.path import isfile, join
import pandas as pd

def get_testing_dataframe(directory_path):
    '''directory_path: Your directory path where you have stored all the testing images'''
    digits = ['0','1','2','3','4','5','6','7','8','9']

    # Create list of all filenames
    filenames = [f for f in listdir(directory_path) if isfile(join(directory_path, f))]
    filenames.sort()
    # Omit .DOS file
    filenames = filenames[1:]

    # Create Dataframe
    df = pd.DataFrame(columns=["picture_path","filename", "label"])

    # Creating labeled dataframe with picture filepath, filename and the respective label
    for i in range(len(filenames)):
        # Clear string of spaces, the numbers from the jpeg (not possible album names with numbers) and the underscores

        # remove .jpg and lowercase
        cleaned_string = filenames[i][:-4].lower()
        # Delete the numbers from the scraping naming convention, do this twice as there are can be two digit numbers
        if cleaned_string[-1] in digits:
            cleaned_string = cleaned_string[:-1]

        if cleaned_string[-1] in digits:
            cleaned_string = cleaned_string[:-1]

        # remove whitespace and underscores
        cleaned_string = cleaned_string.replace(" ", "").replace('_','')

        # Appending each row with image filepath,filename and its label
        df = df.append({
             "picture_path": f'{directory_path}{filenames[i]}',
             "filename": filenames[i],
             # Clear the remaining 'jpg' string at the end of every cleaned string
             "label": cleaned_string
              }, ignore_index=True)
    return df
