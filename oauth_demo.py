from google.appengine.ext import ndb
import logging
import webapp2
import json

class OauthHandler(webapp2.RequestHandler):
	def get(self):
		logging.debug('The contents of the GET request are:' + repr(self.request.GET))


class MainPage(webapp2.RequestHandler):
	def get(self):
		self.response.write("hello")

app = webapp2.WSGIApplication([
	('/', MainPage),
	('/oauth', OauthHandler)
], debug=True)