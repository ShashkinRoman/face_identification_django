#todo сделать добавление картинок из бд а не вручную
import json
import face_recognition
import cv2
import numpy as np
from time import sleep
from datetime import datetime, date, time
import websocket
import json
from base64 import b64encode
import copy
from faceidentification.models import Access_status, Info_about_face


ws = websocket.WebSocket()
ws.connect("ws://192.168.88.23:9000", max_size=1000000000000)



class Base64Encoder(json.JSONEncoder):
    # pylint: disable=method-hidden
    def default(self, o):
        if isinstance(o, bytes):
            return b64encode(o).decode()
        return json.JSONEncoder.default(self, o)

# This is a demo of running face recognition on live video from your webcam. It's a little more complicated than the
# other example, but it includes some basic performance tweaks to make things run a lot faster:
#   1. Process each video frame at 1/4 resolution (though still display it at full resolution)
#   2. Only detect faces in every other frame of video.

# PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
# OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
# specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.

# Get a reference to webcam #0 (the default one)
# video_capture = cv2.VideoCapture('rtsp://admin:12345@192.168.1.100:554/stream1')
video_capture = cv2.VideoCapture(0)



# # Load a sample picture and learn how to recognize it.
# roman_image = face_recognition.load_image_file("faceidentification/static/img/media/roman.jpg")
# roman_face_encoding = face_recognition.face_encodings(roman_image)[0]
#
# roman_in_glasses_image = face_recognition.load_image_file("faceidentification/static/img/media/roman_in_glasses.jpg")
# roman_in_glasses_face_encoding = face_recognition.face_encodings(roman_in_glasses_image)[0]
#
# alexandr_image = face_recognition.load_image_file("faceidentification/static/img/media/alexandr.jpg")
# alexandr_face_encoding = face_recognition.face_encodings(alexandr_image)[0]

known_face_encodings = []
known_face_names = []
def formed_model_encoding():
    query_access_users = Access_status.objects.all()
    for user in query_access_users:
        if user.name != "Unknown":
            name_ = user.name
            known_face_names.append(name_)
            path_in_db = user.path_download
            path_for_encoding = '/home/roman/PycharmProjects/face_identification_django/faceidentification/static/img/media/' + str(path_in_db)
            image = face_recognition.load_image_file(path_for_encoding)
            image_face_encoding = face_recognition.face_encodings(image)[0]
            known_face_encodings.append(image_face_encoding)
formed_model_encoding()

# formed_model_encoding()
#
# known_face_names = [
#     "Roman",
#     "Alexander"
# ]

# Create arrays of known face encodings and their names
# known_face_encodings = [
#     roman_face_encoding,
#     alexandr_face_encoding

# ]
# white_face_names = [
#     "Roman",
#     'Roman_in_glasses',
# ]
# black_known_face_names = [
#     "Alexandr"
# ]
#
# path_image_dict = {
#     "Roman": "static/img/media/roman.jpg",
#     "Alexandr": "static/img/media/alexandr.jpg",
#     "Unknown": "static/img/media/Unknown.jpg"
#
# }
# def face_detect(face_names):
#     if face_names in white_face_names:
#         status = 'Access is open'
#     elif face_names in black_known_face_names:
#         status = 'Warning'
#     else:
#         status = 'Access closet'
#     return name, status



white_face_names = []
black_known_face_names = []

def access_statuses():
    query = Access_status.objects.all()
    for i in query:
        if i.status == "Warning":
            black_known_face_names.append(i.name)
        if i.status == "Access is open":
            white_face_names.append(i.name)


access_statuses()

path_image_dict = {}

def path_image_func():
    query = Access_status.objects.all()
    for i in query:
        path_image_dict[i.name] = 'faceidentification/static/img/' + str(i.path_download)

path_image_func()

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True


def face_detect(face_names):
    status = Access_status.objects.get(name=face_names).status
    return status


def ws_json(name, answer, path_screen, path_image, date_for_path):
    ws.send(json.dumps({'name': name,
                        'status': answer,
                        'image': path_image,
                        'screen_image': path_screen,
                        'date': date_for_path}, cls=Base64Encoder))
    print({'name': name,
                        'status': answer,
                        'image': path_image,
                        'screen_image': path_screen,
                        'date': date_for_path})


def show_frame(face_locations, name_, frame_):
    face_names = [name_]
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
    cv2.imshow('Video', frame_)
    date_ = datetime.now()
    date_for_path = date_.strftime("%d/%m/%y %H:%M:%S")
    path = r'/static/img/media/screenshots/{}_{}.png'.format(name_, date_for_path)
    cv2.imwrite('static/img/media/screenshots/{}_{}.png'.format(face_names, date_for_path), frame_)
    return path, date_, date_for_path

count_white = 0
count_unknown = 0
count_black = 0
list_check = []

#
# check_state = False

# def bla():
#     check_state=True
#     websocket_object.onmessage(bla())


frame_counter = 0
while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()
    # frame_counter += 1
    # if frame_counter % 25 != 0:
    #     continue
    # frame = cv2.resize(frame, (512, 5212))
    # if check_state is not True:
    #     continue
    # check_state = False
    face_in_frame = copy.copy(frame)

    # Resize frame of video to 1/4 size for faster face recognition processing
    # small_frame = frame
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            # # If a match was found in known_face_encodings, just use the first one.
            # if True in matches:
            #     first_match_index = matches.index(True)
            #     name = known_face_names[first_match_index]

            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                try:
                    name = known_face_names[best_match_index]
                    count_white += 2
                except:
                    pass

            if name == "Unknown":
                count_unknown += 2

            if name in black_known_face_names:
                count_black += 2

            if count_black == 50:
                answer = face_detect(name)
                count_black == 0
                path_screen, date_, date_for_path = show_frame(face_locations, name, frame)
                path_image = path_image_dict.get(name)
                ws_json(name, answer, path_screen, path_image, date_for_path)
                Info_about_face.objects.create(name=name, status=answer, path_screen=path_screen,
                                               date=date_, path_image=path_image)


            if count_unknown == 50:
                frame_ = b64encode(frame)
                answer = face_detect(name)
                path_screen, date_, date_for_path = show_frame(face_locations, name, frame)
                path_image = path_image_dict.get(name)
                ws_json(name, answer, path_screen, path_image, date_for_path)
                Info_about_face.objects.create(name=name, status=answer, path_screen=path_screen,
                                               date=date_, path_image=path_image)
                count_unknown = 0

            if count_white == 50:
                frame_ = b64encode(frame)
                answer = face_detect(name)
                # path = screen_save(name, face_in_frame)
                path_screen, date_, date_for_path = show_frame(face_locations, name, frame)
                path_image = path_image_dict.get(name)
                ws_json(name, answer, path_screen, path_image, date_for_path)
                Info_about_face.objects.create(name=name, status=answer, path_screen=path_screen,
                                               date=date_, path_image=path_image)
                count_white = 0

            face_names.append(name)

    process_this_frame = not process_this_frame

    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
