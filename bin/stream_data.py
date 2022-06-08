"""
Module for streaming data across network

For more details on connections to Pi from PC, see:
https://picamera.readthedocs.io/en/release-1.10/recipes1.html#recording-to-a-network-stream


"""



import argparse
from email.policy import default
import socket
from time import sleep





def echo_client(HOST, PORT, Msg:bytes=b'Hello World'):
    """ Test connection by sending a string across a socket"""

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(Msg)
        data = s.recv(1024)

    print('Received', repr(data))


def echo_server(HOST, PORT):
    """ Test server for checking connection"""

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        
        s.bind((HOST, PORT))
        s.listen(1)
        
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                conn.sendall(data)



def picam_client(HOST, PORT):
    """ Create client to send data from camera to server """
    
    client_socket = socket.socket()
    client_socket.connect((HOST, PORT))

    # Make a file-like object out of the connection
    connection = client_socket.makefile('wb')
    try:
        with picamera.PiCamera() as camera:
            
            # Force low settings to reduce demands on connection
            camera.resolution = (640, 480)
            camera.framerate = 24
            
            # Start a preview and let the camera warm up for 2 seconds
            camera.start_preview()
            sleep(2)
            
            # Start recording, sending the output to the connection for 60
            # seconds, then stop
            camera.start_recording(connection, format='h264')
            camera.wait_recording(60)
            camera.stop_recording()
    finally:
        connection.close()
        client_socket.close()


def picam_server(HOST, PORT):
    """Listen for images from client and display results"""
        
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


def main():

    # Parse inputs
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--mode", help="Client or server mode", type=str, default='client')
    parser.add_argument("-i", "--host", help="Host IP Address (127.0.0.1 for testing on local host)", type=str)
    parser.add_argument("-p", "--port", help="Video frame width", type=int, default=65432)
    
    args = parser.parse_args()       

    if args.mode == 'client':
        echo_client(HOST=args.host, PORT=args.port)

    elif args.mode == 'server':
        echo_server(HOST=args.host, PORT=args.port)
    

if __name__ == "__main__":
    main()