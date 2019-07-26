import requests

def get_URL(url):
    r=requests.get(url)
    return r
