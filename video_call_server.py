import cv2
import socket
import pickle
import numpy as np
import sys
from threading import Thread
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
soc.bind(('0.0.0.0',8080))
soc.listen(5)
conn,addr=soc.accept()
print("[*] Connected \n\n")

print("[*] Creating open socket server at 5050 port for audio")
## connecting to audio socket at 5050
audioSocket.bind(("0.0.0.0",5050))
audioSocket.listen(5)
cAudio, addr_ = audioSocket.accept()
print("[*] Connected \n")

print("[*] ..  .. ... Inititalizing completed ")
print("[*] ..  .. ... Starting threads ")


def connection():
    global conn
    while 1:
        try:
            data=b""
            length=0
            while length<921764:
                pac=conn.recv(9999999)
                length+=len(pac)
                data+=pac
            if data[0:1]==b'a':
	            frame1=pickle.loads(data[1::])
	            cv2.imshow("frame1",frame1)
	            key=cv2.waitKey(1)
	            if key == 27:
	                break
        except KeyboardInterrupt:
            sys.exit()
            

def send_img():
    global conn,video
    while 1:
        try:
            _,frame=video.read()
            img_data=np.array(frame)
            data=pickle.dumps(img_data)
            conn.send(b"b"+data)
        except KeyboardInterrupt:
            video.release()
            sys.exit()


def recordAudio():
    time.sleep(5)
    while True:
        data = stream.read(chunk)
        if data:
            cAudio.sendall(data)
def rcvAudio():
     while True:
          audioData = audioSocket.recv(chunk)
          audioData = pickle.loads(audioData)
          stream.write(audioData)


sending=Thread(target=connection)
recving=Thread(target=send_img)
audioRCV =Thread(target = rcvAudio)
#audioREC = Thread(target = recordAudio)

audioRCV.start()
sending.start()
recving.start()
#audioRCV.start()

cv2.destroyAllWindows()



