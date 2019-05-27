from smartcard.scard import *
import time
import requests
import os, json
import utils

def polling_nfc():
    hresult, hcontext = SCardEstablishContext(SCARD_SCOPE_USER)
    assert hresult == SCARD_S_SUCCESS
    hresult, readers = SCardListReaders(hcontext, [])
    assert len(readers) > 0
    reader = readers[0]

    has_card = False
    while True:
        try:
            hresult, hcard, dwActiveProtocol = SCardConnect(
                hcontext,
                reader,
                SCARD_SHARE_SHARED,
                SCARD_PROTOCOL_T0 | SCARD_PROTOCOL_T1)

            hresult, response = SCardTransmit(hcard,dwActiveProtocol,[0xFF,0xCA,0x00,0x00,0x00])

            if not has_card:
                uid = ""
                for index in range(4):
                    uid += format(response[index], 'x')

                r = requests.post('https://lock.dy.tongqu.me/lock-terminal/unlock/card', {
                    'hid': os.environ.get('HID'),
                    'card_uid': uid
                })
                data = json.loads(r.content)
                if data['success']:
                    utils.welcome(data['data']['user']['name'])
                else:
                    utils.unlock_fail(data['message'])
                has_card = True

            time.sleep(0.5)
        except:
            has_card = False
            time.sleep(0.5)
            pass