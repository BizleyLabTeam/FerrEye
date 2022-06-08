""" Module for interacting with, and recording video via Raspberry Pi

options:
  -h, --help            show this help message and exit
  -m MODE, --mode MODE  Choose whether to preview or record
  -t TIME, --time TIME  Choose how long to record (preview is unlimited)
  -w WIDTH, --width WIDTH
                        Video frame width
  -v HEIGHT, --height HEIGHT
                        Video frame height
  -l LEDS [LEDS ...], --LEDs LEDS [LEDS ...]
                        GPIO pins of IR LEDs to use

Examples:
    # Default (record for 10 seconds)
    python -m datacap                
    
    # Streams preview to image window
    python -m datacap -m preview           
    
    # Records for 20 seconds
    python -m datacap -m record -t 20      
    
    # Preview with a smaller image (640 x 480)
    python -m datacap -m preview -w 640 -v 480
    
    # Record for 12 seconds with three LED active
    python -m datacap -m record -t 12 --LEDs 17 18 22


Information:
    LEDs: Connected to GPIO 17, 18, 22 and 27 (though this may change in future)
    Resolution: Typically 1920 x 1080 pixels but could be lower
"""

import argparse
from datetime import datetime
from time import sleep
from typing import List, Tuple

# import RPi.GPIO as GPIO
# import picamera


def configure_GPIO() -> None:
    """ Set channel mapping and disable warnings """
    
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)


def turn_LEDs_ON(LEDs:List[int]=[17, 27],) -> None:
    """ Set GPIO pin to send output and make signal high"""

    for pin_num in LEDs:
    
        GPIO.setup(pin_num, GPIO.OUT)
        GPIO.output(pin_num, GPIO.HIGH)
    

def turn_LEDs_OFF(LEDs:List[int]=[17, 27]) -> None:
    """ Set GPIO pin to send output and make signal high"""

    for pin_num in LEDs:    
        GPIO.output(pin_num, GPIO.LOW)


def make_output_name(t:datetime) -> str:
    """ Generate file name for video using current datetime"""

    return t.strftime('%Y-%m-%d_SpyVid_%H-%M-%S.h264')


def preview_camera() -> None:
    """ Open-ended streaming of data from camera to image window"""

    camera = picamera.PiCamera()
    camera.resolution = resolution

    try:
        camera.start_preview()
    finally:
        camera.stop_preview()
        camera.close()


def timed_recording(resolution:Tuple[int, int]=(1920, 1080), duration:int=30) -> None:
    """ Sample frames for a fixed length period of time """
    
    camera = picamera.PiCamera()
    camera.resolution = resolution
    camera.start_recording(make_output_name(datetime.now()))
    camera.wait_recording(duration)
    camera.stop_recording()


def get_timelapse():

    camera = picamera.PiCamera()
    camera.start_preview()
    sleep(2)
    for filename in camera.capture_continuous('imgX.jpg'):
        print('Captured %s' % filename)
        sleep(0.1) # wait 1 second



def main():

    # Parse inputs
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--mode", help="Choose whether to preview or record", type=str, default='record')
    parser.add_argument("-t", "--time", help="Choose how long to record (preview is unlimited)", type=float, default=10.0)
    parser.add_argument("-w", "--width", help="Video frame width", type=int, default=1920)
    parser.add_argument("-v", "--height", help="Video frame height", type=int, default=1080)
    parser.add_argument("-l", '--LEDs', help='GPIO pins of IR LEDs to use ', nargs='+', type=int, default=[17,27])

    args = parser.parse_args()       
    print(f"Mode = {args.mode}, duration = {args.time}, size = {args.width} x {args.height}")

    # Capture data
    configure_GPIO()
    turn_LEDs_ON(args.LEDs)    

    if args.mode == 'record':
        timed_recording(resolution=(args.width, args.height), duration=args.time)
    
    elif args.mode == 'preview':
        preview_camera(resolution=(args.width, args.height))
    
    turn_LEDs_OFF(args.LEDs)


if __name__ == "__main__":
    main()
