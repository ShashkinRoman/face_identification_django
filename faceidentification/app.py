from faceidentification.models import Info_about_face
from faceidentification.start_app import main
from datetime import datetime

face = main()
path = 'nado dopiplit screenshots'
def take_on_front():
    pass

def write_face_in_db(face, path):
    fase_obj = Info_about_face(name=face[0], status=face[1], path=path, date=datetime.now())
    fase_obj.save()
