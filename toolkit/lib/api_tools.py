import requests
import json
from flask import current_app

def generate_answer(data={}, success=True):
    data["success"] = success
    return data

def post_request_api(url, params):
    domain = current_app.config['URL_APP']
    try: 
        x = requests.post(domain + url, data = params).json()
        return x
    except:
        return False


def get_request_api(url):
    domain = current_app.config['URL_APP']
    try:
        x = requests.get(domain + url).json()
        return x
    except:
        return False
