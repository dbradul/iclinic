import base64

import json
import requests
import os
import hashlib


ID = os.getenv('ID')
SECRET = os.getenv('SECRET')
URL = 'https://my.iclinic.ua/rest/api/v1/lead'


def bytes_to_hexstring(b):
    return b.hex()


def bytes_to_base64(b):
    return  base64.b64encode(b).decode('utf-8')


def hash_sha256(secret, msg):
    return hashlib.sha256((secret + msg).encode('utf-8')).digest()


def create_headers(seller_id, secret, msg):
    signature = hash_sha256(secret, msg)
    signature_base64 = bytes_to_base64(signature)
    return {
        'Content-Type': 'application/json; charset=utf-8',
        'Id': seller_id,
        'Sign': signature_base64,
    }


def create_payload(name, phone, date=None, time=None, comments='', clinic=None):
    payload = {
        "name": name,
        "phone": phone
    }

    if date:
        payload["date"] = date
    if time:
        payload["time"] = time
    if comments:
        payload["comments"] = comments
    if clinic:
        payload["clinic"] = clinic

    return payload


def send_request(url, payload, headers):
    response = requests.post(url, data=payload, headers=headers)
    return response


def test_signature():
    sig = hash_sha256('SECRET', 'Test message')
    assert bytes_to_base64(sig) == 'tyhcy7FwbKwXK254kuKlS9/8gqWFFZEM+Vb1w8U39HM='
    assert bytes_to_hexstring(sig) == 'b7285ccbb1706cac172b6e7892e2a54bdffc82a58515910cf956f5c3c537f473'


def test_send_request():
    payload = create_payload(
        name='Test',
        phone='+380979797979',
        date='2022-09-30',
    )
    json_payload = json.dumps(payload)
    headers = create_headers(ID, SECRET, json_payload)
    resp = send_request(URL, json_payload, headers)
    assert resp.status_code == 201


def main():
    # test_signature()
    test_send_request()


if __name__ == '__main__':
    main()