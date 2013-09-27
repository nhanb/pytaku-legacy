#!/usr/bin/env python
from __future__ import with_statement

import sys
sys.path.insert(0, 'lib')
sys.path.insert(0, 'helpers')
sys.path.insert(0, 'sites')

import webapp2


app = webapp2.WSGIApplication([('/', 'handlers.index.MainPage'),
                               ('/grab', 'handlers.grab.Grab'),
                               ('/oauth', 'handlers.auth.Step1'),
                               ('/oauth/1', 'handlers.auth.Step1'),
                               ('/oauth/2', 'handlers.auth.Step2'),
                               ('/serve/([^/]+)?',
                                'handlers.serve.ServeHandler')
                               ],
                              debug=True)
