import json
class Attribute_handler:
	"""docstring for Attribute_handler"""
	'''
	def __init__(self, arg):
		super(Attribute_handler, self).__init__()
		self.arg = arg
	'''

	def __init__(self, point):
		self.point = point

	def get_x(self):
		return self.point.x

	def get_y(self):
		return self.point.y

	def get_attr_value(self, attribute):
		if self.point.name == None:
			return ""

		point_name = '{' + self.point.name.replace("'", '"') + '}'
		decoded = json.loads(point_name)

		if attribute in decoded:
			return decoded[attribute]
		else:
			return None

		# index = self.point.name.find(attr_name)
		# return self.point.name[index + 3]
		# self.point.name.find()


	def get_serif(self):
		attr_value = self.get_attr_value("serif")
		return attr_value

	def get_dependX(self):
		attr_value = self.get_attr_value("dependX")
		return attr_value

	def get_dependY(self):
		attr_value = self.get_attr_value("dependY")
		return attr_value

	def get_penPair(self):
		attr_value = self.get_attr_value("penPair")
		return attr_value

	def get_round(self):
		attr_value = self.get_attr_value("round")
		return attr_value

	def set_attr_value(self, attribute, new_value):
		if self.point.name == None:
			self.point.name = ''
		point_name = '{' + self.point.name.replace("'", '"') + '}'
		decoded = json.loads(point_name)
		decoded[attribute] = new_value
		encoded = json.dumps(decoded)
		self.point.name = encoded.replace('"', "'")[1:-1]

	def set_serif(self, new_value):
		if new_value == 'False':
			self.set_attr_value("serif", '')
		else:
			self.set_attr_value("serif", new_value)

	def set_dependX(self, new_value):
		if new_value == 'False':
			self.set_attr_value("dependX", '')
		else:
			self.set_attr_value("dependX", new_value)

	def set_dependY(self, new_value):
		if new_value == 'False':
			self.set_attr_value("dependY", '')
		else:
			self.set_attr_value("dependY", new_value)

	def set_penPair(self, new_value):
		if new_value == 'False':
			self.set_attr_value("penPair", '')
		else:
			self.set_attr_value("penPair", new_value)

	def set_round(self, new_value):
		if new_value == 'False':
			self.set_attr_value("round", '')
		else:
			self.set_attr_value("round", new_value)
