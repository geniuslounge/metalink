import youtube.test.library as test_lib
import os

"""This grouping of test checks to make sure things under the /channel umbrella work as expected"""

#List of popular channels to check with
channel_id_list = ['UCU261fOCKtUwxigoCcZuVHQ','UCBJycsmduvYEL83R_U4JriQ', 'UCAkM_UgVD8EK4oJePdv36fQ','UCsi7f6y5dH5uuye3MeCfojA','UCY1kMZp36IQSyNx_9h4mpCg']
base_url = 'https://geniuslounge.com/channel/'

def test_channel_home():
    for x in channel_id_list:
        r = test_lib.get_URL(''.join((base_url,x)))
        assert r.status_code == 200

def test_channel_latest_video():
    for x in channel_id_list:
        r = test_lib.get_URL(''.join((base_url,x,'/latest')))
        assert r.status_code == 200


def test_channel_latest_video_image():
    for x in channel_id_list:
        r = test_lib.get_URL(''.join((base_url, x, '/latest/image')))
        assert r.status_code == 200

def test_channel_feed():
    for x in channel_id_list:
        r = test_lib.get_URL(''.join((base_url, x, '/feed')))
        assert r.status_code == 200

def test_channel_mobile_banner():
    for x in channel_id_list:
        r = test_lib.get_URL(''.join((base_url, x, '/mobile_banner')))
        assert r.status_code == 200