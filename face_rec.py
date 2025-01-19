import cv2
import numpy as np
from facenet_pytorch import MTCNN, InceptionResnetV1
import torch
import os

mtcnn = MTCNN(keep_all=True, device='cuda' if torch.cuda.is_available() else 'cpu')
model = InceptionResnetV1(pretrained='vggface2').eval()

video_capture = cv2.VideoCapture

def get_embedding(path):
    path = cv2.imread(path)

    image_rgb = cv2.cvtColor(path, cv2.COLOR_BGR2RGB)
    boxes, _ = mtcnn.detect(image_rgb)

    if boxes is not None:
        face = mtcnn(image_rgb)

        if face is not None:
            embedding = model(face[0].unsqueeze(0))
            embedding = embedding.cpu().detach().numpy()
            return embedding
        else:
            return 1
    else:
        return 1

def identify_user(input_image):

    input_embeddings = get_embedding(input_image)

    def euclidean_distance(ref, inp):
        return np.linalg.norm(ref-inp)

    path = "faces"
    reference_database = os.listdir(path)
    reference_database.pop(reference_database.index(".DS_Store"))
    distances_compiled = []

    for reference_image in reference_database:
        reference_embeddings = get_embedding("faces/" + reference_image)
        distance = euclidean_distance(reference_embeddings, input_embeddings)
        distances_compiled.append(distance)

    min_val = min(distances_compiled)

    print(distances_compiled)


    if min_val < 0.75:
        user_id = reference_database[distances_compiled.index(min_val)]
        print("user", user_id)
        return user_id
    else:
        print("here")
        return 1