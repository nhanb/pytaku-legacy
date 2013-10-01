import webapp2
import cgi
import jinja2
import os
from google.appengine.api import taskqueue, users

JINJA_ENV = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__) +
                                   '/../templates/'),
    extensions=['jinja2.ext.autoescape'])

SUCCESS_PAGE_HTML = """
Your request has been fired off. Check your dropbox.<br />
<a href="/">Click here</a> to submit another link.
"""


class MainPage(webapp2.RequestHandler):

    def get(self):
        user = users.get_current_user()
        template = JINJA_ENV.get_template('index.html')
        template_values = {
            'username': user.email()
        }
        self.response.write(template.render(template_values))

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
