import ConfigParser

config = ConfigParser.ConfigParser()
config.read("conf.ini")

consumer_key = config.get("Dropbox", "ConsumerKey")
consumer_secret = config.get("Dropbox", "ConsumerSecret")
request_token_url = config.get("Dropbox", "RequestTokenURL")
authorize_url = config.get("Dropbox", "AuthorizeURL")
