#!/usr/bin/env python

from __future__ import division, print_function, absolute_import

import requests
from . import constants
from . import lang
from . import config
import sys

class AI(object):
	"""
	Python class wrapper for Gurunudi AI methods - uses POST method, but GET is also supported by server for testing purposes or quick usage.
	"""


	def __init__(self,api_key=None,version=1):
		"""
		version (int): The API version to be used while querying Gurunudi Server
		api_key (string): The API key to access the Gurunudi platform

		"""
		self.version='v'+str(version)
		
		if api_key:
			config.HEADERS['gnapi']=api_key

	def chat(self,text,lang=lang.ENGLISH):
		"""
		text (string): The text to be responded to
		lang (string): ISO3 language code of the text
		returns: chat response to the text - ideal for chatbots
		"""
 
		return self.__call_api(constants.API_CHAT,{constants.FIELD_TEXT:text,constants.FIELD_LANG:lang})

 
	def __call_api(self,api,data):
		"""
		calls given Gurunudi api with given data and returns the result
		api (string): The name of the API to call
		data (dict): Data to be sent to the API
		"""
 

		try:
			if config.DEBUG:
				print("Call API",api)
				print("Request Data",data)

			#call the API
			url = config.API_URL.format(self.version,api)
			response = requests.post(url, json=data, headers=config.HEADERS)
			json=response.json()

			if config.DEBUG:
				print("Response Code",response.status_code)
				print("Response data",json)
				
			if response.status_code==200:#if response OK
				return json
			else:
				raise APIError("status_code_"+str(response.status_code))

		except requests.exceptions.ConnectionError as ex:
			print(ex,file=sys.stderr)
			raise APIError(constants.ERROR_SERVER_INACCESSIBLE)

class APIError(Exception):
	def __init__(self, message):
		super(APIError,self).__init__(message)


