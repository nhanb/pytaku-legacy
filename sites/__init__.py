import urlparse
from google.appengine.api import urlfetch

# Return appropriate site object for link
def factory(url):
    parsed = urlparse.urlparse(url)
    if parsed.netloc == 'kissmanga.com':
        import kissmanga
        return kissmanga.get_site(url)
    else:
        return 'NOT IMPLEMENTED'


# Parent class for all specific website classes
class Site(object):

    def __init__(self, url):
        self.url = url
        self.pages = None
        self.chapter_name = None
        
        # Attempt to fetch html:
        resp = urlfetch.fetch(url)
        if resp.status_code == 200:
            self.html = resp.content
        else:
            self.html = None
