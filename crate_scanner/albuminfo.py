
import cv2
# from scipy.spatial import distance
import numpy as np
import urllib
import requests
from numpy.linalg import norm


def get_feature_vector(img, basemodel):
    img1 = cv2.resize(img, (224, 224))
    feature_vector = basemodel.predict(img1.reshape(1, 224, 224, 3))
    return feature_vector

def calculate_similarity(vector1, vector2):
    # return dot(vector1, vector2.T)/(norm(vector1)*norm(vector2))
    return 1-(np.dot(vector1,vector2.T))/(norm(vector1)*norm(vector2))


def find_match(image,database):
    similarity = []
    for index, row in enumerate(database):
        # similarity = np.append(similarity,calculate_similarity(feature_vector_test, row[0][1]))
        similarity.append(calculate_similarity(image, row[1]))

    similarity = np.array(similarity)
    index = np.argmin(similarity)
    return database[index][0]

def make_prediction(model,image,database):
    # tmp_crop = draw_frame(image)
    # cropped = tmp_crop[1]
    cropped = url_to_image(image)
    
    feature_vector_test = get_feature_vector(cropped,model)
    feature_vector_test_reduced = feature_vector_test
    # feature_vector_test_reduced = np.mean(feature_vector_test.reshape(-1, 32), axis=1)
    match = find_match(feature_vector_test_reduced,database)
    return match




def matched_album(input_image, basemodel, full_vectors):
    img1 = url_to_image(input_image)

    f1 = get_feature_vector(img1, basemodel)
    comparison = []
    for vector in full_vectors:
        for i in vector[1]:
            comparison.append(calculate_similarity(f1, i))
    index = comparison.index(min(comparison))
    album = full_vectors[index]
    return album[0]

def url_to_image(url):
    # download the image, convert it to a NumPy array, and then read
    # it into OpenCV format
    resp = requests.get(url)
    image = np.asarray(bytearray(resp.content), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    # return the image
    return image
