import webapp2
import oauth2 as oauth
import urlparse
from parseini import consumer_key, consumer_secret,\
    request_token_url, authorize_url
from google.appengine.ext import ndb
from google.appengine.api import users


class Otaku(ndb.Model):
    userid = ndb.StringProperty()
    request_token = ndb.StringProperty(indexed=False)
    request_secret = ndb.StringProperty(indexed=False)
    access_token = ndb.StringProperty(indexed=False)
    access_secret = ndb.StringProperty(indexed=False)


class Step1(webapp2.RequestHandler):
    def get(self):

        user = users.get_current_user()
        otaku = Otaku.query(Otaku.userid == user.user_id()).get()

        if otaku:
            self.redirect("/")
            return

        otaku = Otaku()
        otaku.userid = user.user_id()

        # Create your consumer with the proper key/secret.
        consumer = oauth.Consumer(key=consumer_key,
                                  secret=consumer_secret)

        # Create our client.
        client = oauth.Client(consumer)

        # The OAuth Client request works just like httplib2 for the most part.
        resp, content = client.request(request_token_url, "GET")

        if resp['status'] != '200':
            raise Exception("Invalid response %s." % resp['status'])

        content_dict = dict(urlparse.parse_qsl(content))

        # Save for step2
        otaku.request_token = content_dict['oauth_token']
        otaku.request_secret = content_dict['oauth_token_secret']
        otaku.put()

        full_url = (authorize_url +
                    '?oauth_token=' + content_dict['oauth_token'] +
                    '&oauth_callback=' + self.request.host_url + '/oauth/2')

        self.response.write('<a href="' + full_url + '">Click</a><br />')
        self.response.write('<br />otaku.request_token:' + otaku.request_token)
        self.response.write('<br />Real token: ' + content_dict['oauth_token'])


class Step2(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        otaku = Otaku.query(Otaku.userid == user.user_id()).get()

        oauth_verifier = self.request.get('oauth_token')
        self.response.write("Received token = " + oauth_verifier + "<br />")

        otaku = Otaku.query(Otaku.userid == user.user_id()).get()
        self.response.write("Stored token = " + otaku.request_token + "<br />")

        token = oauth.Token(otaku.request_token,
                            otaku.request_secret)

        token.set_verifier(oauth_verifier)

        consumer = oauth.Consumer(key=consumer_key,
                                  secret=consumer_secret)

        client = oauth.Client(consumer, token)
        resp, content = client.request(
            "https://api.dropbox.com/1/oauth/access_token", "POST")

        access_token = dict(urlparse.parse_qsl(content))

        otaku.access_token = access_token['oauth_token']
        otaku.access_secret = access_token['oauth_token_secret']
        otaku.put()

        self.response.write(str(access_token))
        self.response.write("<br />")
        self.response.write(str(content))
        self.response.write("<br />")
        self.response.write(str(otaku))
        self.response.write("Access secret saved: " + otaku.access_secret)
