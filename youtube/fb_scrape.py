import requests
import os
import asyncio

async def fb_scrape(url_to_scrape):
    payload = {
        'id': url_to_scrape,
        'scrape':'true',
        'access_token': os.environ['fb_access_token']
    }
    r = requests.post('https://graph.facebook.com/v4.0/', payload)
    return r.status_code
