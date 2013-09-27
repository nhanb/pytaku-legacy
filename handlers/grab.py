import webapp2
import cgi
from google.appengine.api import urlfetch, files, users
from dropbox import upload
from auth import Otaku
from sites import factory
import re


class Grab(webapp2.RequestHandler):

    def imgToBlob(self, content):
        # Create the file
        fname = files.blobstore.create(mime_type='image/png')

        # Open the file and write to it
        with files.open(fname, 'a') as f:
            f.write(content)

        # Finalize the file. Do this before attempting to read it.
        files.finalize(fname)

        # Get the file's blob key
        blob_key = files.blobstore.get_blob_key(fname)
        return blob_key

    def post(self):
        link = cgi.escape(self.request.get('content'))
        siteOb = factory(link)
        self.async_download(siteOb)

    def async_download(self, site_obj):
        # Fetch user
        user = users.get_current_user()
        otaku = Otaku.query(Otaku.userid == user.user_id()).get()

        # Upload to dropbox
        for page in site_obj.pages:

            #rpc = urlfetch.create_rpc()
            #rpc.callback = create_callback(rpc)
            #urlfetch.make_fetch_call(rpc, url)
            #rpcs.append(rpc)

            # Image binary
            img = urlfetch.fetch(page[1]).content

            # Full file path on dropbox
            path = site_obj.chapter_name + '/' + page[0]
            self.response.write(path + '<br />')

            resp = upload(img, path, otaku)
            self.response.write(str(resp) + '<br />')


def get_pages_from_chapter(chapter_link):
    chapter_html = urlfetch.fetch(chapter_link).content
    #lstImages.push("http://2.bp.blogspot.com/-dDoTjVP9jIk/UZNi2wUDSdI/
    #AAAAAAAAKh0/IbV0Pi2WZiQ/001.png?imgmax=2000");

    # Create regex to match page link
    pat = re.compile('lstImages\.push\("(.+?)"\);')
    matches = pat.findall(chapter_html)

    return matches
