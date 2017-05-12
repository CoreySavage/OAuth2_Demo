# oauth_demo.py
#
# Corey Savage
# CS 496
#
# OAuth 2.0 Web Client Demo  
# Demonstrates a basic website with OAuth 2.0 authentication
#

import jinja2
import urllib2
import urllib
import os
import logging
import webapp2
import json
from google.appengine.ext import ndb
from webapp2_extras import sessions
from google.appengine.api import urlfetch

import string
import random
chars = string.letters + string.digits
chars = string.letters + string.digits + string.punctuation
pwdSize = 32
key = ''.join((random.choice(chars)) for x in range(pwdSize))

secret_key = key

config = {}
config['webapp2_extras.sessions'] = {'secret_key': key,}




jinja_environment = jinja2.Environment(
   loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__),'templates')),
   autoescape = True)


class BaseRequestHandler(webapp2.RequestHandler):
    def dispatch(self):
        self.session_store = sessions.get_store(request=self.request)

        try:
            # Dispatch the request.
            webapp2.RequestHandler.dispatch(self)
        finally:
            # Save all sessions.
            self.session_store.save_sessions(self.response)

    @webapp2.cached_property
    def session(self):
        # Returns a session using the default cookie key.
        return self.session_store.get_session()



class OauthHandler(BaseRequestHandler):
    def get(self):
        code = self.request.get('code')
        url = 'https://www.googleapis.com/oauth2/v4/token'
        self.response.write(code)
        data_to_post = {
            'code': code,
            'client_id':'838080691485-jf0lut0oq1tdirerhoa9tc7lf3roard3.apps.googleusercontent.com',
            'redirect_uri':'https://oauth2demo-167110.appspot.com/oauth',
            'client_secret':'kXaXyMr8ssNNZkzpRWdzUw3-',
            'grant_type': 'authorization_code' }
        encoded_data = urllib.urlencode(data_to_post)
        # Send encoded data to application-2
        result = urlfetch.fetch(url, encoded_data, method='POST')
        self.response.write(self.request.get('access_token'))


    def post(self):
        self.response.write("PPPPOOOOOO")
        authorizeString = 'Bearer ' + json_result['access_token']
        req = urllib2.Request('https://www.googleapis.com/plus/v1/people/me')
        req.add_header('Authorization', authorizeString)
        resp = urllib2.urlopen(req)
        content = resp.read()
        self.response.write(content)


class MainPage(BaseRequestHandler):
    def get(self):
        template_values = {
            'a_variable':'Welcome to the web page',
            'title':"Main",
            'url':"https://oauth2demo-167110.appspot.com"
        }
        self.response.write("hello")
        template = jinja_environment.get_template('index.html')
        self.response.write(template.render(template_values))

    def post(self):
        url = 'https://accounts.google.com/o/oauth2/v2/auth'
        data = urllib.urlencode({'response_type':'code',
                                'client_id':'838080691485-jf0lut0oq1tdirerhoa9tc7lf3roard3.apps.googleusercontent.com',
                                'redirect_uri':'https://oauth2demo-167110.appspot.com/oauth',
                                'scope':'email',
                                'state': secret_key})
        try:
            address = url + '?' + data
            self.redirect(address)
        except urllib2.URLError:
            logging.exception('Caught exception fetching url')




app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/oauth', OauthHandler)
], debug=True, config=config)