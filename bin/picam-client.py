'''
stream_2_net.py

Taken from https://picamera.readthedocs.io/en/release-1.10/recipes1.html#recording-to-a-network-stream

Stephen Town, 11th Dec 2019

'''

import socket
import time
import picamera

# Connect a client socket 
HOST = '192.168.0.110'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

client_socket = socket.socket()
client_socket.connect((HOST, PORT))

# Make a file-like object out of the connection
connection = client_socket.makefile('wb')
try:
    with picamera.PiCamera() as camera:
        camera.resolution = (640, 480)
        camera.framerate = 24
        # Start a preview and let the camera warm up for 2 seconds
        camera.start_preview()
        time.sleep(2)
        # Start recording, sending the output to the connection for 60
        # seconds, then stop
        camera.start_recording(connection, format='h264')
        camera.wait_recording(60)
        camera.stop_recording()
finally:
    connection.close()
    client_socket.close()