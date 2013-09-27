from sites import Site
from google.appengine.api import urlfetch
import re
import urlparse


class KSite(Site):

    def __init__(self, url):
        super(KSite, self).__init__(url)
        self.fetch_pages()

    def fetch_pages(self):

        # Create regex to match page link
        pat = re.compile('lstImages\.push\("(.+?)"\);')
        page_links = pat.findall(self.html)

        # Get chapter name
        parsed = urlparse.urlparse(self.url)
        self.chapter_name = parsed.path.split('/')[-1]

        # Regex to match page image file name
        ipat = re.compile('/([0-9]{3}\.(png|jpg))\?')
        self.pages = ((ipat.findall(x)[0][0], x) for x in page_links)


def get_site(url):
    return KSite(url)
