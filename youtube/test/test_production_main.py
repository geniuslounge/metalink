import youtube.test.library as test_lib
import os
import youtube.yt_fetch as yt
import pytest

"""This grouping of test checks to make sure things under the /channel umbrella work as expected"""

#List of popular channels to check with
base_url = 'https://geniuslounge.com'

@pytest.mark.prod
def test_homepage():
    r = test_lib.get_URL(''.join((base_url)))
    assert r.status_code == 200
@pytest.mark.prod
def test_latest():
    r = test_lib.get_URL(''.join((base_url, '/latest')))
    assert r.status_code == 200

@pytest.mark.prod
def test_latest_image():
    r = test_lib.get_URL(''.join((base_url,'/latest/image')))
    assert r.status_code == 200

@pytest.mark.prod
def test_subscribe():
    r = test_lib.get_URL(''.join((base_url,'/subscribe')))
    assert r.status_code == 200

@pytest.mark.prod
def test_feed():
    r = test_lib.get_URL(''.join((base_url, '/feed')))
    assert r.status_code == 200

@pytest.mark.prod
def test_sitemap():
    r = test_lib.get_URL(''.join((base_url,'/sitemap.xml')))
    assert r.status_code == 200

@pytest.mark.prod
def test_mobile_banner():
    r = test_lib.get_URL(''.join((base_url,'/mobile_banner')))
    assert r.status_code == 200

### This grabs the lastest 25 videos and then trys to resolve the URLs

# def test_latest_25_vids():
#     vid_list = yt.channel_feed(channel_id=os.environ['channel_id'])
#     for x in vid_list['items']:
#         r=test_lib.get_URL(''.join((base_url,'/',x['vid_id'])))
#         print('testing video_id: ', x['vid_id'], ' • Status: ', str(r.status_code))
#         assert r.status_code == 200