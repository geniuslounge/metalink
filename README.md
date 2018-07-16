# MetaLink

A prettier way to share your YouTube videos on Facebook, Twitter, and other social media.
It provides the whole thumbnail to the social service, rather than a cropped square (Facebook) or text link (Twitter)

## Before
![](https://geniuslounge.github.io/share2/images/before.jpg)

## After
![](https://geniuslounge.github.io/share2/images/after.jpg)

All you need to do is set the following environment variables

* `channel_domain` - in the form of `geniuslounge.com`
* `DISABLE_COLLECTSTATIC` - For heroku config, this was required, as it doesn't even have a DB, or defined static files!
* `django_secret_key` - because making your secret key in GitHub is bad luck.
* `yt_api_key` - Your YouTube API key.
(Get one here: https://console.cloud.google.com/apis/library/youtube.googleapis.com?q=youtube)
