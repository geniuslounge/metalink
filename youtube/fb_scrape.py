import requests
import os


def fb_scrape(url_to_scrape):
    payload = {
        'scrape':'true',
        'id': url_to_scrape,
        'access_token': os.environ['fb_access_token']
    }
    r = requests.post('https://graph.facebook.com/v4.0/', payload)
    return r.status_code
