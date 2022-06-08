'''
receive_stream.py

The server collects frames from the client and displays them

Adapted from https://picamera.readthedocs.io/en/release-1.10/recipes1.html#recording-to-a-network-stream

Stephen Town, 11th Dec 2019

'''

import socket
import subprocess

# Start a socket listening for connections on 0.0.0.0:8000 (0.0.0.0 means
# all interfaces)

HOST = '192.168.0.105'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

server_socket = socket.socket()
server_socket.bind((HOST, PORT))
server_socket.listen(1)

# Accept a single connection and make a file-like object out of it
connection = server_socket.accept()[0].makefile('rb')
try:
    # Run a viewer with an appropriate command line. Uncomment the mplayer
    # version if you would prefer to use mplayer instead of VLC
    cmdline = [r'C:\Program Files\VideoLAN\VLC\vlc.exe', '--demux', 'h264', '-']
    #cmdline = ['mplayer', '-fps', '25', '-cache', '1024', '-']
    player = subprocess.Popen(cmdline, stdin=subprocess.PIPE)
    while True:
        # Repeatedly read 1k of data from the connection and write it to
        # the media pla.yer's stdin
        data = connection.read(1024)
        if not data:
            break
        player.stdin.write(data)
finally:
    connection.close()
    server_socket.close()
    player.terminate()