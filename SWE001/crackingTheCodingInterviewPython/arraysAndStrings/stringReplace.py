# write a method to replace all spaces in a string with '%20'
def replace20(string):
	out = ''
	for char in string:
		if char == ' ':
			out += '%20'
		else:
			out += char
	return out

print replace20('Mr. John Smith')