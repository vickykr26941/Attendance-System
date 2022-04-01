from email.mime import image
import cv2
import face_recognition
import os
from datetime import datetime 

# face_recognition module works with dlib and generate 128 unique points

path = 'images'
images = []
personName = []

myList = os.listdir(path)
print(myList)

for cu_img in myList:
    current_image = cv2.imread(f'{path}/{cu_img}')
    images.append(current_image)
    personName.append(os.path.splitext(cu_img)[0])

print(personName)

# incode all the images present in our directory
def face_encodings(images):

    encodeList = []
    for img in images:

        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB) # we have to convert images BGR to RGB format
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    
    return encodeList

encode_list_of_images = face_encodings(images)
# print(encode_list_of_images) # we can see the values of encoding of images

cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    faces = cv2.resize(frame,(0,0),None,0.25)
    