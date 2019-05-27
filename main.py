import oled, time
import RPi.GPIO as GPIO
from PIL import ImageFont
from utils import Client
import time
from dotenv import find_dotenv, load_dotenv
import os
import card
import threading
import face

load_dotenv(find_dotenv())

def start_socket_client():
    client = Client(os.environ.get('HID'))
    client.connect(server='lock.dy.tongqu.me')
    client.pool()

socket_thread = threading.Thread(target=start_socket_client)
socket_thread.start()
card_thread = threading.Thread(target=card.polling_nfc)
card_thread.start()
face_thread = threading.Thread(target=face.poll)
face_thread.start()


# oled.render([{'text': u'欢迎', 'size': 22}, {'text': u'何炳昌', 'size': 26}])
# time.sleep(5)
# oled.render()
# GPIO.cleanup()