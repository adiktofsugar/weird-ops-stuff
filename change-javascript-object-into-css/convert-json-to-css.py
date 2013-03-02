import json;
import sys;
import os;
import re;
import glob;

#Set JSON_DIR and CSS_DIR based on arguments
try:
	JSON_DIR=sys.argv[1]
	CSS_DIR=sys.argv[2]
except IndexError:
	print 'Usage: %s JSON_DIR CSS_DIR' % sys.argv[0]
	sys.exit(1)
	


SELECTOR_TEMPLATE = '.%(name)s_id_'

# This changes each hash key from a camelCased name to a hypphen-delimted one, recursively
# and also makes the key that contains a dictionary a selector type
def convert_dict(d):
	new_d={}
	for key in d:

		converted_key = key

		#change the original value
		if isinstance(d[key], dict):
			d[key] = convert_dict(d[key])
			converted_key = SELECTOR_TEMPLATE % {
				"name": key
			}

		capital_letters = re.finditer(r'([A-Z])', converted_key)
		if capital_letters:

			for m in capital_letters:
				index = m.start()
				
				converted_key = "%s-%s%s" % (\
					converted_key[0:index],\
					converted_key[index].lower(),\
					converted_key[index+1:]\
				)
		new_d[converted_key] = d[key]
	return new_d

def css_string (obj, depth=0):
	tabs = ""
	single_tab = "    "
	for i in range(0, depth):
		tabs += single_tab

	string = "{\n"
	for key in obj:
		value = obj[key]
		template = '%s%s: %s;'

		if isinstance(value, dict):
			value = css_string(obj[key], depth+1)
			template = '%s%s %s'
		
		string += single_tab + template % (tabs, key, value)
		string += "%s\n" % (tabs)

	string += "\n%s}" % tabs
	return string

def parse (filename, out_filename):
	file = open(filename)
	json_string = file.read()
	file.close()

	obj = json.loads( json_string )
	obj = convert_dict(obj)


	# now actually write the css file
	print css_string(obj)
	#print 'Writing ' + out_filename
	#css_file = open( out_filename, 'w')
	#css_file.write( css_string(obj) )	
	#css_file.close()


for file_path in glob.glob( JSON_DIR+'/*' ):
	filename = os.path.basename(file_path)
	print 'Parsing %s' % file_path
	parse(os.path.join(JSON_DIR, filename), os.path.join(CSS_DIR, filename + '.css'))


