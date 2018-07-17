<img src="https://geniuslounge.github.io/share2/images/gllogo.png" width=150px> </img>
# MetaLink

A prettier way to share your YouTube videos on Facebook, Twitter, and other social media.

### Sometimes social media sites don't treat your YouTube videos with enough respect
MetaLink provides the whole thumbnail to the social service, rather than a cropped square (Facebook) or text link (Twitter).

Currently designed to be deployed via [heroku](http://heroku.com), it should be fairly easy to update to your deployment system of choice.


## Before and After (Facebook)
![](https://geniuslounge.github.io/share2/images/facebook.png)


## Before and After (Twitter)
![](https://geniuslounge.github.io/share2/images/twitter.png)

All you need to do is set the following environment variables

* `channel_domain` - in the form of `geniuslounge.com`
* `DISABLE_COLLECTSTATIC = 1` - For heroku config, this was required, as it doesn't even have a DB, or defined static files!
* `django_secret_key` - because making your secret key public in GitHub is bad luck.
* `yt_api_key` - Your [YouTube API key](https://console.cloud.google.com/apis/library/youtube.googleapis.com?q=youtube)
