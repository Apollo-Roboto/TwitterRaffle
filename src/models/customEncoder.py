import json

class CustomEncoder(json.JSONEncoder):
	def default(self, obj):
		return obj.__dict__