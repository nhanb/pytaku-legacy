import webapp2
import cgi
from google.appengine.api import taskqueue, users


MAIN_PAGE_HTML = """\
<html>
  <body>

    <form action="/" method="post">
      <div><textarea name="content" rows="3" cols="60"></textarea></div>
      <div><input type="submit" value="Get pic"></div>
    </form>

  </body>
</html>
"""

SUCCESS_PAGE_HTML = """
Your request has been fired off. Check your dropbox.<br />
<a href="/">Click here</a> to submit another link.
"""


class MainPage(webapp2.RequestHandler):

    def get(self):
        self.response.write(MAIN_PAGE_HTML)

    # Handle grab request by firing off a task
    def post(self):
        links = self.request.get('content').split('\n')
        userid = users.get_current_user().user_id()
        for link in links:
            taskqueue.add(method="POST",
                          url="/grab",
                          params={'content': link,
                                  'userid': userid})
            self.response.write(cgi.escape(userid))
        self.response.write(SUCCESS_PAGE_HTML)
