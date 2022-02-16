import socket
import pickle
import numpy as np
import sys
from threading import Thread
import random
import cv2
import pyaudio
import time


print("[*]Initializing socket for Video")
# video socket
soc=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

print("[*]Initializing webcam for Video")
#initilizing webcam for videosocket
video=cv2.VideoCapture(0)
print("[*]Initializtion of webcam access succed\n")

print("[*] .... .")
print("[*] ...")

print("[*]Accessing mircophone")
#audio socket
chunk = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
p = pyaudio.PyAudio()
#initializing microphone for audio socket
stream = p.open(format = FORMAT, channels = CHANNELS, rate = RATE, input = True, frames_per_buffer = chunk)
print("[*]Succesfully accessed\n")
print("[*]... ..")

print("[*]Initializing socket for Audio output\n\n")
audioSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

# connecting to video socket at 8080
print("[*] Creating open socket server at 8080 port for video")
host=input("enter target ip:")
soc.connect((host,8080))
print("[*] Connected \n\n")

print("[*] Creating open socket server at 5050 port for audio")
## connecting to audio socket at 5050
try:
	time.sleep(5)
	audioSocket.connect((host,5050))
except:
	audioSocket.connect((host,5050))
print("[*] Connected \n")


print("[*] ..  .. ... Inititalizing completed ")
print("[*] ..  .. ... Starting threads ")


def send_img():
    global soc
    while 1:
        try:
            _,frame=video.read()
            img_data=np.array(frame)
            data=pickle.dumps(img_data)
            soc.send(b'a'+data)
        except KeyboardInterrupt:
            video.release()
            sys.exit()


def recv_img():
    global soc
    while 1:
        try:
            data=b''
            length=0
            while length<921766:
                pac2=soc.recv(9999999)
                length+=len(pac2)
                data=data+pac2
            if data[0:1]==b'b':
	            frame2=pickle.loads(data[1::])
	            cv2.imshow("frame2",frame2)
	            key=cv2.waitKey(1)
	            if key==27:
	                break
        except KeyboardInterrupt:
            sys.exit()	
           
           
def recordAudio():
    time.sleep(5)
    while True:
        data = stream.read(chunk)
        data=pickle.dumps(data)
        if data:
            audioSocket.send(data)
def rcvAudio():
     while True:
          audioData = audioSocket.recv(size)
          stream.write(audioData)

recving=Thread(target=recv_img)
sending=Thread(target=send_img)
audioREC = Thread(target = recordAudio)
#audioRCV = Thread(target = rcvAudio)

recving.start()
sending.start()
audioREC.start()
#audioRCV.start()

cv2.destroyAllWindows()

