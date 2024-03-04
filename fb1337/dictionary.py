# FBl337
# Programming Code Golf Language
# Created: 21 February 2024
# Version: 21 February 2024 12:00PM
# Copyright: James Leibert 2024
# Licence: Available for use under the GPL3 Licence https://www.gnu.org/licenses/gpl-3.0.txt

# dictionary.py
# Dictionary Type


from fb1337.array import FlatList


class Dictionary:
	"""Dictionary class implements a simple key-value store"""

	def __init__(self):
		self.dictionary = dict()

	def fetch(self, key):
		if key is not None and type(key).__hash__ and key in self.dictionary:
			return self.dictionary[key]
		else:
			return ''

	def set(self, key, value):
		if key is not None and type(key).__hash__:
			self.dictionary[key] = value
			return self

	def keys(self):
		return FlatList(list(self.dictionary.keys()))

	def values(self):
		return FlatList(list(self.dictionary.values()))

	def items(self):
		return FlatList([[k, v] for k, v in self.dictionary.items()])

	def __repr__(self):
		return '<Dict ' + str(self.dictionary) + ">"
