from importlib import import_module

JSON = 'json'
RAPIDJSON = 'rapidjson'

json_libs = (RAPIDJSON, ) 

# can chose faster json module if it installed
mode = JSON

for module in json_libs:
	try:
		json = import_module(module)
	except ImportError:
		continue

	mode = module
	break

if mode == RAPIDJSON:
	def dumps(data):
		return json.dumps(data, ensure_ascii=False)

	def loads(data):
		return json.loads(data, number_mode=json.NM_NATIVE)

else:
	import json

	def dumps(data):
		return json.dumps(data, ensure_ascii=False)

	def loads(data):
		return json.loads(data)
