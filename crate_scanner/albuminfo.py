import cv2
from scipy.spatial import distance


def get_feature_vector(img, basemodel):
    img1 = cv2.resize(img, (224, 224))
    feature_vector = basemodel.predict(img1.reshape(1, 224, 224, 3))
    return feature_vector

def calculate_similarity(vector1, vector2):
    return distance.cosine(vector1, vector2)

def matched_album(input_image, basemodel, full_vectors):
    img1 = cv2.imread(f"{input_image}")
    f1 = get_feature_vector(img1, basemodel)
    comparison = []
    for vector in full_vectors:
        for i in vector[1]:
            comparison.append(calculate_similarity(f1, i))
    index = comparison.index(min(comparison))
    album = full_vectors[index]
    return album[0]
