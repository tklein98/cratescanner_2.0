from tensorflow.keras.layers import Flatten, Dense, Input,concatenate
from tensorflow.keras.layers import Conv2D, MaxPooling2D
from tensorflow.keras.layers import Activation, Dropout
from tensorflow.keras.models import Model, Sequential
from scipy.spatial import distance
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import cv2
import os
from os import listdir
from os.path import isfile, join



LOCAL_PATH = '/home/beres/code/tklein98/crate_scanner/notebooks/test_images'


def get_model():
    vgg16 = tf.keras.applications.VGG16(weights='imagenet', include_top=True,\
        pooling='max', input_shape=(224, 224, 3))
    basemodel = Model(inputs=vgg16.input, outputs=vgg16.get_layer('fc2').output)
    return basemodel



def get_feature_vector(img):
    img1 = cv2.resize(img, (224, 224))
    feature_vector = basemodel.predict(img1.reshape(1, 224, 224, 3))
    return feature_vector



def calculate_similarity(vector1, vector2):
    '''introduce score to calculate the accuracy'''
    return distance.cosine(vector1, vector2)




def compare_testing():
    '''compares test images with album cover database and finds the best match'''
    comparisons = []
    for filename in os.listdir(directory):
        img = cv2.imread(f'test_images/{filename}')
        img1 = get_feature_vector(img)
        comparison = {}
        counter = 0
        for vector in vectors:
            for j in vector[1]:
                if len(comparison) == 0:
                    comparison[filename] = (counter, calculate_similarity(img1, j))
                elif comparison[filename][1] > calculate_similarity(img1, j):
                    comparison[filename] = (counter, calculate_similarity(img1, j))
                counter += 1
        comparisons.append(comparison)
    return comparisons




def get_testing_dataframe(directory_path):
    '''directory_path: Your directory path where you have stored all the testing images'''
    digits = ['0','1','2','3','4','5','6','7','8','9']

    # Create list of all filenames and dataframe
    filenames = [f for f in listdir(directory_path) if isfile(join(directory_path, f))]
    df = pd.DataFrame(columns=["picture_path","filename", "label"])

    # Creating labeled dataframe with picture filepath, filename and the respective label
    for i in range(len(filenames)):
        # remove .jpg and lowercase
        cleaned_string = filenames[i][:-4].lower()
        # Delete the numbers - twice as can be two digit numbers
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
             # Clear the remaining 'jpg' string
             "label": cleaned_string
              }, ignore_index=True)
    return df





def accuracy_model(testing_dataframe):
    '''introduce score to calculate the accuracy'''
    score = 0 
    for i in range(len(testing_dataframe)):
        # Look in comparisons to get index of image
        index_matched_image = list(comparisons[i].values())[0][0]
        # Get the predicted album from all the vectors with the defined index
        predicted_album = full_vectors[index_matched_image][0][3]
        
        # Clean the album string
        predicted_album_cleaned = predicted_album.lower().replace(' ','')
        # If the predicted label matches the test image, increase score by one
        if testing_dataframe['label'][i] == predicted_album_cleaned:
            score += 1
        print(index_matched_image, predicted_album_cleaned, testing_dataframe['label'][i])
    return score/len(testing_dataframe)
    