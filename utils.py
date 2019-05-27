from socket import socket, AF_INET, SOCK_STREAM
import json, time
import RPi.GPIO as GPIO
import oled

chan_list = [5, 6]
GPIO.setmode(GPIO.BCM)
GPIO.setup(chan_list, GPIO.OUT)

def welcome(user):
    led_green()
    oled.render([{'text': u'欢迎', 'size': 22}, {'text': user, 'size': 26}])
    time.sleep(5)
    led_red()
    oled.render()

def unlock_fail(message):
    led_red()
    oled.render([{'text': message, 'size': 22}])
    time.sleep(5)
    oled.render()

class Client:
    def __init__(self, hid):
        self.hid = hid

    def send_message(self, type, data):
        payload = {
            'type': type,
            'data': data
        }
        self.s.send(json.dumps(payload).encode('utf-8'))

    def connect(self, server='127.0.0.1', port=28591):
        self.s = socket(AF_INET, SOCK_STREAM)
        self.s.connect((server, port))
        self.send_message('handshake', self.hid)

    def message_handler(self, message):
        if message['type'] == 'unlock':
            print('Welcome, %s!' % message['data']['user'])
            self.s.send(json.dumps({
                'success': True,
                'message': 'ok'
            }).encode('utf-8'))
            welcome(message['data']['user'])
        else:
            self.s.send(json.dumps({
                'success': False,
                'message': 'Bad type'
            }).encode('utf-8'))

    def pool(self):
        while True:
            data = json.loads(self.s.recv(8192))
            self.message_handler(data)

def led_green():
    GPIO.output(chan_list, (GPIO.HIGH, GPIO.LOW))

def led_red():
    GPIO.output(chan_list, (GPIO.LOW, GPIO.HIGH))