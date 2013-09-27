import webapp2

MAIN_PAGE_HTML = """\
<html>
  <body>

    <form action="/grab" method="post">
      <div><textarea name="content" rows="3" cols="60"></textarea></div>
      <div><input type="submit" value="Get pic"></div>
    </form>

  </body>
</html>
"""


class MainPage(webapp2.RequestHandler):

    def get(self):
        self.response.write(MAIN_PAGE_HTML)
