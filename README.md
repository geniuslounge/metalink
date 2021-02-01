<img src="https://s.gravatar.com/avatar/b9d6859916139942340c91db0a503bfc.png?s=300" width=150px> </img>

# Meta Link

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
* Post this to Facebook: `http://video.geniuslounge.com/WaFMDe5cE8w`
or try your own video: `http://video.geniuslounge.com/{YouTube Video ID}`

* For our RSS feed: `http://video.geniuslounge.com/feed`
or another YouTube channel's RSS feed: `http://video.geniuslounge.com/channel/{YouTube Channel ID}/feed`


### Other nifty things to try

* `/` - Redirects users to your channel (and uses your vanity URL if you have one)
* `/latest`  - Allows you to have a static link that always points to your latest video. [Our Latest video](http://video.geniuslounge.com/latest)
* `/latest/image` - Provides the thumbnail to the latest video.
* `/<video_id>/image` - Provides the image for the video_id
* `/feed` - (mentioned above) Provides RSS feed of your YouTube Channel
* `/sitemap.xml` - Generates a sitemap of the last 50 videos from your feed
* `/subscribe` - takes users to your subscribe link, prompting them to subscribe if they haven't already

### Channel specific links
#### Test these for your own channel
*  `http://video.geniuslounge.com/channel/{YouTube Channel ID}`
* `http://video.geniuslounge.com/channel/{YouTube Channel ID}/latest`
* `http://video.geniuslounge.com/channel/{YouTube Channel ID}/latest/image`
* `http://video.geniuslounge.com/channel/{YouTube Channel ID}/feed`
* `http://video.geniuslounge.com/channel/{YouTube Channel ID}/mobile_banner`

All you need is `Python 3`, a heroku account (Free level is fine),  and to set the following environment variables:

* `channel_domain` - in the form of `geniuslounge.com`
* `DISABLE_COLLECTSTATIC = 1` - For heroku config, this was required, as it doesn't even have a DB, or defined static files!
* `django_secret_key` - because making your secret key public in GitHub is bad luck.
* `yt_api_key` - Your [YouTube API key](https://console.cloud.google.com/apis/library/youtube.googleapis.com?q=youtube)
* `channel_id` - Your YouTube channel id, for `/latest/` lookups, etc...
