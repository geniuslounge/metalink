import youtube.test.library as test_lib
import os

"""This grouping of test checks to make sure things under the /channel umbrella work as expected"""

#List of popular channels to check with
base_url = ''.join(('http://',os.environ['channel_domain']))

def test_homepage():
    r = test_lib.get_URL(''.join((base_url)))
    assert r.status_code == 200

def test_latest():
    r = test_lib.get_URL(''.join((base_url, '/latest')))
    assert r.status_code == 200

def test_latest_image():
    r = test_lib.get_URL(''.join((base_url,'/latest/image')))
    assert r.status_code == 200

def test_subscribe():
    r = test_lib.get_URL(''.join((base_url,'/subscribe')))
    assert r.status_code == 200

def test_feed():
    r = test_lib.get_URL(''.join((base_url, '/feed')))
    assert r.status_code == 200

def test_sitemap():
    r = test_lib.get_URL(''.join((base_url,'/sitemap.xml')))
    assert r.status_code == 200

def test_mobile_banner():
    r = test_lib.get_URL(''.join((base_url,'/mobile_banner')))
    assert r.status_code == 200