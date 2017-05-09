# oauth_demo.py
#
# Corey Savage
# CS 496
#
# OAuth 2.0 Web Client Demo  
# Demonstrates a basic website with OAuth 2.0 authentication
#

from google.appengine.ext import ndb
import jinja2
import urllib2
import os

import logging
import webapp2
import json

SESSION_ATTRIBUTES = ['user_id', 'remember',
                      'token', 'token_ts', 'cache_ts']

env = Environment(
    loader = FileSystemLoader('/templates'),
    autoescape=select_autoescape(['html', 'xml'])
)


class OauthHandler(webapp2.RequestHandler):
    def get(self):
        logging.debug('The contents of the GET request are:' + repr(self.request.GET))


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.write("Hi")


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/oauth', OauthHandler)
], debug=True)