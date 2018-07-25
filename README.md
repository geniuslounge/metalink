<img src="https://geniuslounge.github.io/metalink/images/gllogo.png" width=150px> </img>

# MetaLink

Generate beautiful social links for you YouTube videos, as well as YouTube RSS feeds.

### Sometimes social media sites don't treat your YouTube videos with enough respect
MetaLink provides the whole thumbnail to the social service, rather than a cropped square (Facebook) or text link (Twitter).

Currently designed to be deployed via [heroku](http://heroku.com), it should be fairly easy to update to your deployment system of choice.

# Pretty links for your YouTube Videos
## Before and After (Facebook)
![](https://geniuslounge.github.io/metalink/images/facebook.png)


## Before and After (Twitter)
![](https://geniuslounge.github.io/metalink/images/twitter.png)



# YouTube RSS Feeds!
### (And RFC822 compatible)
![](https://geniuslounge.github.io/metalink/images/rss.png)


## Try it!
* Post this to Facebook: `http://geniuslounge.com/WaFMDe5cE8w`
or try your own video: `http://geniuslounge.com/{YouTube Video ID}`

* For a RSS feed: `http://geniuslounge.com/feed/UCU261fOCKtUwxigoCcZuVHQ`
or your own channel: `http://geniuslounge.com/feed/{YouTube Channel ID}`


### Other nifty things to try

* `/latest`  - Allows you to have a static link that always points to your latest video. [Our Latest video](http://geniuslounge.com/latest)
* `/contribute` - Provides a pretty link to let your YouTube Community help with translations & transcriptions. [Help us caption](http://geniuslounge.com/contribute) 



All you need is `Python 3`, a heroku account (free works, too),  and to set the following environment variables:

* `channel_domain` - in the form of `geniuslounge.com`
* `DISABLE_COLLECTSTATIC = 1` - For heroku config, this was required, as it doesn't even have a DB, or defined static files!
* `django_secret_key` - because making your secret key public in GitHub is bad luck.
* `yt_api_key` - Your [YouTube API key](https://console.cloud.google.com/apis/library/youtube.googleapis.com?q=youtube)
* `channel_id` - Your YouTube channel id, for `/latest/` lookups, etc...
