from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import FaceEnroll,FaceDetection

# Required Modules
import numpy as np
from tensorflow.keras.applications.vgg16 import VGG16
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg16 import preprocess_input
from tensorflow.keras.models import Model

import ast

import base64


# Load pre-trained VGG16 model
vgg_model = VGG16(weights='imagenet')
model = Model(inputs=vgg_model.input, outputs=vgg_model.get_layer('fc1').output)



# get current directory path 
import os
c_path = os.path.abspath(os.getcwd())



# Function to extract features from the face image
def extract_features(img_path):
    img = image.load_img(img_path, target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    features = model.predict(x)
    return features.flatten()




# View
@api_view(['POST'])
def face_enroll(request):
    if request.method=='POST':
        img = request.data['img']
        name = request.data['name']
        if img and name :

            fe = FaceEnroll(name=name,img=img)
            fe.save()

            #path of image
            path_of_image = img.name

            # full path
            obj = FaceEnroll.objects.latest('id')
            full_path = c_path + obj.img.url

            features = extract_features(full_path)
            features_bytes = features.tostring()
            features_str = base64.b64encode(features_bytes).decode('utf-8') 

            FaceEnroll.objects.filter(pk=obj.id).update(feature=features_str)



            return Response({'result':'Face enrolled successfully!'},status=status.HTTP_201_CREATED)
        else:
            return Response({'msg':"All Fields are required."},status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def face_detection(request):
    if request.method=='POST':
        img = request.data['img']
        if img :

            fd = FaceDetection(img=img)
            fd.save()

            #path of image
            path_of_image = img.name

            # full path
            obj = FaceDetection.objects.latest('id')
            full_path = c_path + obj.img.url


            #face recognition
            features = extract_features(full_path)

            # Store attendance in a file
            # with open("attendance.txt", "a") as file:
            #     file.write(identity + "\n")

            # Function to recognize faces from the database
            min_dist = float('inf')
            identity = None

            pre_faces = FaceEnroll.objects.all()
            for object in pre_faces:
            # for (name, db_features) in database.items():
                features_bytes = base64.b64decode(object.feature)
                db_features = np.frombuffer(features_bytes, dtype=np.float32)
                dist = np.linalg.norm(features - db_features)
                if dist < min_dist:
                    min_dist = dist
                    identity = object.name
                    FaceDetection.objects.filter(pk=obj.id).update(face_enroll=object)
                    break

            if min_dist > 0.7:  # Set your own threshold value for face recognition
                identity = 'Unknown'
                FaceDetection.objects.filter(pk=obj.id).update(face_enroll='')





            return Response({'result':f'Recognized as: {identity}'},status=status.HTTP_201_CREATED)
        else:
            return Response({'msg':"Please Choose img first"},status=status.HTTP_400_BAD_REQUEST)