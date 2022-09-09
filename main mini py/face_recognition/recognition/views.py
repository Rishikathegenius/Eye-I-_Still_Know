from django.shortcuts import render
from django.http.response import StreamingHttpResponse
from recognition.camera import FaceDetect,VideoCamera,t2s
from recognition.webcam_detection import ObjectDetect
import sys
sys.path.append('model')
sys.path.insert(1, 'model/research/object_detection/webcam_detection.py')
from django.http import HttpResponse
import pyttsx3
import datetime
import os

from django.shortcuts import redirect
import cv2
import threading
import os
import time
import speech_recognition as sr
r = sr.Recognizer() 
# Create your views here.


def wish():
    hour=int(datetime.datetime.now().hour)

    if hour>=0 and hour<=12:
        t2s("Good Morning User")
    elif hour>12 and hour<18:
        t2s("Good Afternoon User")
    else:
        t2s("Good Evening User")


def index(request):
    wish()
    t2s("Click Anywhere On the screen")
    return render(request, 'recognition/index.html')
def saystart(request):
    t2s("Welcome! Just say start ,to start the process")
    while (1):
        try:
            with sr.Microphone() as source2:
                r.adjust_for_ambient_noise(source2, duration=0.2)
                # listens for the user's input
                audio4 = r.listen(source2)
                # Using ggogle to recognize audio
                inpcmd = r.recognize_google(audio4)
                inpcmd = inpcmd.lower()
                print("Said" + inpcmd)
                if inpcmd == "start":
                    t2s("Nice so we are ready to go")
                    return redirect('/start')
                else:
                    t2s("you said " + inpcmd + " say again")
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
        except sr.UnknownValueError:
            t2s("sorry did not hear you say again")
            print("unknown error occured")
            # return redirect('/start')
def start(request):
    # text = "give your command"
    # engine = pyttsx3.init()
    # rate = engine.getProperty('rate')
    # engine.setProperty('rate', rate-70)
    # # pyttsx3.engine.Engine.setPropertyValue(age,'F')
    # engine.say(text)
    t2s("Please give your command, the commands are; new ,for new person ;face to detect face, and object to detect object")
    while (1):
        try:
            with sr.Microphone() as source2:
                r.adjust_for_ambient_noise(source2, duration=0.2)

                # listens for the user's input
                audio4 = r.listen(source2)
                # Using ggogle to recognize audio
                inpcmd = r.recognize_google(audio4)
                inpcmd = inpcmd.lower()
                print("Said" + inpcmd)
                if inpcmd == "new":
                    t2s("processing to add new person")
                    return redirect('/new')
                if inpcmd == "face":
                    t2s("processing to detect face, please wait")
                    return redirect('/face')
                if inpcmd == "object":
                    t2s("processing to detect objects please wait")
                    return redirect('/object')
                else:
                    t2s("you said " + inpcmd + " say again")
                    # return redirect('/start')
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
        except sr.UnknownValueError:
            t2s("sorry did not hear you say again")
            print("unknown error occured")
            # return redirect('/start')

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/png\r\n\r\n' + frame + b'\r\n\r\n')
def facecam_feed(request):
    return StreamingHttpResponse(gen(FaceDetect()),
                                 content_type='multipart/x-mixed-replace; boundary=frame')
def ogen(webcam_detection):
    while True:
        frame = webcam_detection.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/png\r\n\r\n' + frame + b'\r\n\r\n')

def objcam_feed(request):
    return StreamingHttpResponse(ogen(ObjectDetect()),
                                 content_type='multipart/x-mixed-replace; boundary=frame')


# class VideoCamera(object):
#     def __init__(self):
#         self.video = cv2.VideoCapture(0)
#         (self.grabbed, self.frame) = self.video.read()
#         threading.Thread(target=self.update, args=()).start()

#     def __del__(self):
#         self.video.release()

#     def get_frame(self):
#         image = self.frame
#         ret, jpeg = cv2.imencode('.jpg', image)
#         return jpeg.tobytes()

#     def update(self):
#         while True:
#             (self.grabbed, self.frame) = self.video.read()

def new(request):
    # cam.release()
    text = "This will Add a new person"
    print(text)
    engine = pyttsx3.init()
    t2s(text)
    # time.sleep(10)
    return StreamingHttpResponse(gen(VideoCamera()),
                                 content_type="multipart/x-mixed-replace;boundary=frame")
def face(request):
    # cam.release()
    text = "This will detect the person in front of you"
    engine = pyttsx3.init()
    t2s(text)
    print(text)
    # time.sleep(10)
    return render(request, 'recognition/home.html')
def object(request):
    # cam.release()
    # VideoCapture(0)
    text = "This will detect the objects in front of you"
    engine = pyttsx3.init()
    t2s(text)
    print(text)
    # time.sleep(10)
    #response = redirect('https://affectionate-kirch-815a13.netlify.app/')
    return render(request, 'recognition/obj.html')


    #return HttpResponse("https://affectionate-kirch-815a13.netlify.app/")
