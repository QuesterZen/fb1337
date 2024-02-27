# FBl337
# Programming Code Golf Language
# Created: 21 February 2024
# Version: 21 February 2024 12:00PM
# Copyright: James Leibert 2024
# Licence: Available for use under the GPL3 Licence https://www.gnu.org/licenses/gpl-3.0.txt

# environment.py
# The global and local environment, including the stack and namespace


import os


class Environment:

	def __init__(self, parent=None, path=None):
		# Local environment
		self.namespace = dict()
		self.implicit_object = None

		# Environment hierarchy
		self.parent = parent
		self.base_env = self if parent is None else parent.base_env

		# Base environment only: whole of program environment
		if parent is None:
			self.program_parameters = []
			self.stack = [] if parent is None else None
			if path is not None:
				self.path = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(path)))
			else:
				self.path = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
			self.writing = False
			self.reading = None

	# Stack Methods
	def get_stack(self):
		"""Return the entire stack without removing values"""
		return self.base_env.stack

	def push(self, value):
		"""Push a value to the stack"""
		if value is not None:
			self.base_env.stack.append(value)

	def pop(self):
		"""Pop a value from the stack and return it. Return None if the stack is empty"""
		if len(self.base_env.stack) > 0:
			value, self.base_env.stack = self.base_env.stack[-1], self.base_env.stack[:-1]
			return value
		else:
			return None

	def peek(self):
		"""Return the top value on the stack without removing it. Return None if the stack is empty"""
		if len(self.base_env.stack) > 0:
			return self.base_env.stack[-1]
		else:
			return None

	def dup(self, x):
		"""Push the same value twice onto the stack
		(usually this is taken from the stack, thus duplicating the top stack value)"""
		self.push(x)
		self.push(x)

	def dup2(self, x, y):
		"""Push a pair of values onto the stack twice
		(usually these are taken from the stack, thus duplicating the top two stack values)"""
		self.push(x)
		self.push(y)
		self.push(x)
		self.push(y)

	def under(self, x, y):
		"""Push two values onto the stack, then repeat the first value
		(usually these are taken from the stack, thus copying the lower value to the top of the stack"""
		self.push(x)
		self.push(y)
		self.push(x)

	def dup_under(self, x, y):
		"""Push the first value onto the stack twice, then the second value
		(usually these are taken from the stack, thus copying the lower value under the top of the stack"""
		self.push(x)
		self.push(x)
		self.push(y)

	def deep(self, n):
		"""Copy the value n-deep and put it on the top of the stack"""
		if len(self.base_env.stack) > n >= 1:
			index = len(self.base_env.stack) - n - 1
			self.base_env.stack += [self.base_env.stack[index]]

	def swap(self, x, y):
		"""Pushes two values to the stack in reverse order
		(usually these are taken from the stack, thus reversing the top two stack values)"""
		self.push(y)
		self.push(x)

	def rotate(self, x, y, z):
		"""Pushes three values onto the stack in rotated order
		(usually these are taken from the stack, thus rotating the top three stack values abc->bca"""
		self.push(y)
		self.push(z)
		self.push(x)

	# Implicit Methods

	def implicit(self, back_ref=0, previous=False):
		"""Returns the current loop implicit value, or one from an earlier loop"""

		if back_ref == 0 and self.implicit_object is not None:
			if previous:
				return self.implicit_object.previous
			else:
				return self.implicit_object.implicit

		elif self.implicit_object is None and self.parent is not None and self.parent != self:
			return self.parent.implicit(back_ref, previous)

		elif back_ref > 0 and self.implicit_object is not None and self.parent is not None and self.parent != self:
			return self.parent.implicit(back_ref - 1, previous)

		else:
			return None

	# Variable lookup and assignment

	def assign(self, name, value):
		self.namespace[name] = value

	def lookup(self, name):
		# Implicit references
		if type(name) is int:
			name = str(name)
		if name == '_':
			return self.implicit()

		elif name in ['⓪', '①', '②', '③', '④', '⑤']:
			back_ref = ['⓪', '①', '②', '③', '④', '⑤'].index(name)
			return self.implicit(back_ref)


		# Program Parameter references
		elif name[0] in '0123456789':
			index = int(name)
			if index < len(self.base_env.program_parameters):
				return self.base_env.program_parameters[index]
			else:
				return None

		elif name in ['➊', '➋', '➌', '➍', '➎']:
			index = ['➊', '➋', '➌', '➍', '➎'].index(name) + 1
			if index < len(self.base_env.program_parameters):
				return self.base_env.program_parameters[index]
			else:
				return None

		# Local named variable references
		elif name[0] in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz':
			if name in self.namespace:
				return self.namespace[name]
			elif self.parent is not None and self.parent != self:
				return self.parent.lookup(name)

		print('lookup failed', name)
		raise KeyError

	def pin(self, n_values):
		# Collects n values from the stack and keeps them in the local environment
		values = [self.pop() for _ in range(n_values)][::-1]
		values = [x for x in values if x is not None]
		for i, v in enumerate(values):
			self.namespace['local_' + str(i + 1)] = v
		for i in range(n_values - len(values)):
			self.namespace['local_' + str(i + 1 + len(values))] = ''

	def local_lookup(self, i):
		name = 'local_' + str(i)
		try:
			result = self.lookup(name)
		except KeyError:
			return ''
		return result

	# Iterator Related

	def exit_iteration(self):
		if self.implicit_object is not None:
			self.implicit_object.exit_iteration()

	# File related

	def load_value(self):
		path_in = os.path.join(self.base_env.path, self.base_env.program_parameters[0] + '.in')
		path_out = os.path.join(self.base_env.path, self.base_env.program_parameters[0] + '.out')
		if os.path.exists(path_in):
			path = path_in
		elif os.path.exists(path_out):
			path = path_out
		else:
			return None
		if self.base_env.reading is None:
			self.base_env.reading = open(path, 'r')
		line = self.base_env.reading.readline()
		return line.strip('\n\r\t ')

	def save_value(self, x):
		path_out = os.path.join(self.base_env.path, self.base_env.program_parameters[0] + '.out')
		if self.base_env.writing:
			flag = 'a'
		else:
			self.base_env.writing = True
			flag = 'w'
		with open(path_out, flag) as f:
			f.write(str(x) + '\n')
		return None

	def file_in(self, ints=False, cols=False):
		path_in = os.path.join(self.base_env.path, self.base_env.program_parameters[0] + '.in')
		path_out = os.path.join(self.base_env.path, self.base_env.program_parameters[0] + '.out')
		if os.path.exists(path_in):
			path = path_in
		elif os.path.exists(path_out):
			path = path_out
		else:
			return None
		with open(path, 'r') as f:
			values = f.readlines()
		values = [v.strip('\n\t\r ') for v in values]
		if cols:
			values = [line.split(' ') for line in values]
			if ints:
				values = [[int(x) for x in line] for line in values]
			return values
		else:
			if ints:
				values = [int(str(v)) for v in values]
			return values
