import webapp2
import cgi
import jinja2
import os
from google.appengine.api import taskqueue, users
from handlers.auth import Otaku

JINJA_ENV = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__) +
                                   '/../templates/'),
    extensions=['jinja2.ext.autoescape'])

SUCCESS_PAGE_HTML = """
Your request has been fired off. Check your dropbox.<br />
<a href="/">Click here</a> to submit another link.
"""

alert_messages = {
    'approved': ("Dropbox account connected!", "success"),
    'not_approved': ("Failed to connect Dropbox account. Why did you cancel?",
                     "danger"),
    'please_setup': ("You haven't linked your Dropbox account. Click\
                     'Authenticate with Dropbox' first.", "danger"),
}


class MainPage(webapp2.RequestHandler):

    def get(self):
        user = users.get_current_user()
        template = JINJA_ENV.get_template('index.html')
        template_values = {
            'username': user.email(),
            'logout_link': users.create_logout_url('/'),
        }

        msg = self.request.get('msg')

        if msg in alert_messages:
            alert_values = {
                'alert_display': 'block',
                'alert_type': alert_messages[msg][1],
                'alert_msg': alert_messages[msg][0],
            }
            template_values = dict(template_values.items() +
                                   alert_values.items())

        else:
            # Show warning if not authenticated with dropbox yet
            otaku = Otaku.query(Otaku.userid == user.user_id()).get()
            if not (otaku and otaku.access_token):
                msg = 'please_setup'
                alert_values = {
                    'alert_display': 'block',
                    'alert_type': alert_messages[msg][1],
                    'alert_msg': alert_messages[msg][0],
                }
                template_values = dict(template_values.items() +
                                       alert_values.items())

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
