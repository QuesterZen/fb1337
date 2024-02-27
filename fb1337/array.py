# FBl337
# Programming Code Golf Language
# Created: 21 February 2024
# Version: 21 February 2024 12:00PM
# Copyright: James Leibert 2024
# Licence: Available for use under the GPL3 Licence https://www.gnu.org/licenses/gpl-3.0.txt

# array.py
# Array types: (flat) List, StructuredArray, Matrix and Coordinates


from functools import reduce
from itertools import accumulate
from math import sqrt
from operator import add, mul

import numpy as np


class Array:

	def __init__(self):
		self.values = None
		self.default = None

	# Must be implemented by sub-classes

	def get_shape(self):
		# Return a tuple with length of each axis
		raise NotImplementedError

	def can_reshape(self):
		# Return True if rectangular array that can be reshaped
		raise NotImplementedError

	def structured_values(self):
		# Return a structured array, does not need to have identical length components
		raise NotImplementedError

	def flat_list(self):
		# Create a list of the elements that will be used for sets, filtering, outer and inner products etc.
		# Should return a hashable type if used with set functions
		raise NotImplementedError

	def all_values(self):
		raise NotImplementedError

	def mutate(self, structured_list):
		# Update the values in the current list
		raise NotImplementedError

	def build(self, structured_list):
		# Create a new list of this type
		raise NotImplementedError

	# Class functions relating to types

	@staticmethod
	def truthy(x):
		if x is None: return False
		if type(x) is bool: return x
		if type(x) is int: return x != 0
		if type(x) is str: return x != ''
		if type(x) is float or type(x) is np.float_: return x != 0.
		return True

	@staticmethod
	def container(x):
		return type(x) in [list, np.ndarray]

	@staticmethod
	def number(x):
		return type(x) in [int, float, bool, np.float_]

	# Type Conversions

	@staticmethod
	def coordinate(array):
		if all([Array.number(x) for x in array.all_values() if x != '']):
			return Coordinate([int(x) for x in array.all_values() if x != ''])
		else:
			return ''

	@staticmethod
	def promote(array):
		if isinstance(array, FlatList) and all(
				[type(x) is list and len(x) == len(array.flat_list()[0]) for x in array.flat_list()]):
			return StructuredArray([x for x in array.flat_list() if x != ''])
		elif isinstance(array, FlatList):
			return StructuredArray(
				[x.flat_list() if isinstance(x, Array) else x for x in array.all_values() if x != ''])
		elif isinstance(array, Coordinate):
			return StructuredArray([x for x in array.flat_list()])
		else:
			return array

	@staticmethod
	def demote(array):
		if isinstance(array, MatrixArray):
			return FlatList(array.flat_list().tolist())
		elif isinstance(array, Coordinate):
			if len(array.values) == 0:
				return ''
			elif len(array.values) == 1:
				return array.values[0]
			else:
				return FlatList(array.flat_list())
		elif isinstance(array, StructuredArray):
			return FlatList(array.flat_list())
		elif isinstance(array, Coordinate):
			return FlatList(array.flat_list())

	# Class functions relating to structured arrays - utilities

	@staticmethod
	def flatten_structured(obj):
		if Array.container(obj):
			return sum([Array.flatten_structured(x) for x in obj], start=[])
		else:
			return [obj]

	@staticmethod
	def shape_of_structured(obj):
		if Array.container(obj) and len(obj) > 0:
			sub_shapes = sorted(tuple([Array.shape_of_structured(x) for x in obj]))
			return tuple([len(sub_shapes)] + list(sub_shapes[0]))
		else:
			return ()

	@staticmethod
	def all_indices(shape):
		if len(shape) == 1:
			for i in range(shape[0]):
				yield (i,)
		else:
			for i in range(shape[0]):
				for x in Array.all_indices(shape[1:]):
					yield tuple([i] + list(x))

	@staticmethod
	def shape_structured(values, shape, default=0):
		total_size = reduce(mul, shape, 1)
		if len(values) < total_size:
			values = values + [default] * (total_size - len(values))
		else:
			values = values

		def shape_rec(items, rec_shape):
			if len(rec_shape) == 1:
				return items
			chunk_shape = rec_shape[1:]
			chunk_size = reduce(mul, chunk_shape, 1)
			return [shape_rec(items[(i * chunk_size):((i + 1) * chunk_size)], rec_shape[1:]) for i in
			        range(rec_shape[0])]

		return shape_rec(values, shape)

	@staticmethod
	def index_value(index):
		if type(index) is int:
			return index,
		elif type(index) in (float, np.float_):
			return int(index),
		elif isinstance(index, Coordinate):
			return index.values
		elif Array.container(index):
			return tuple(index)
		elif isinstance(index, Array):
			return tuple([int(x) for x in index.all_values()])
		elif type(index) is tuple:
			return index
		else:
			raise ValueError("Index type not usable", type(index))

	@staticmethod
	def flat_index_for_coordinate(coordinate, shape):
		used = (list(Array.index_value(coordinate)) + [0] * len(shape))[:len(shape)]
		offsets = list(accumulate((list(shape)[1:] + [1])[::-1], func=mul))[::-1]
		return sum([x * y for x, y in zip(used, offsets)])

	@staticmethod
	def coordinates_for_flat_index(index, shape):
		offsets = list(accumulate((list(shape)[1:] + [1])[::-1], func=mul))[::-1]

		def coord_rec(ix, sh):
			if len(sh) == 1:
				return [ix]
			else:
				chunk_number = ix // sh[0]
				chunk_index = ix % sh[0]
				remaining = coord_rec(chunk_index, sh[1:])
				return [chunk_number] + remaining

		return coord_rec(index, offsets)

	@staticmethod
	def indices_to_bool(indices_list, shape):
		size = reduce(mul, shape, 1)
		bool_array_flat = [0] * size
		for c in indices_list:
			i = Array.flat_index_for_coordinate(c, shape)
			bool_array_flat[int(i)] = 1
		bool_array = Array.shape_structured(bool_array_flat, shape, 0)
		return bool_array

	@staticmethod
	def bool_to_indices(bool_array):
		shape = Array.shape_of_structured(bool_array)
		indices = []
		for i, b in enumerate(Array.flatten_structured(bool_array)):
			if Array.truthy(b):
				index = Array.coordinates_for_flat_index(i, shape)
				if len(index) == 1:
					index = index[0]
				indices.append(index)
		return indices

	@staticmethod
	def first_index(bool_array):
		indices = Array.bool_to_indices(bool_array)
		if len(indices) == 0:
			return ''
		else:
			return indices[0]

	@staticmethod
	def permute_axes(struc, permutation=None):
		shape = Array.shape_of_structured(struc)
		size = reduce(mul, shape, 1)
		dimensions = len(shape)
		if permutation is None or len(permutation) != dimensions or sorted(permutation) != list(range(dimensions)):
			permutation = list(range(dimensions))[::-1]
		permuted_shape = [shape[i] for i in permutation]
		new_flat = [0] * size
		old_flat = Array.flatten_structured(struc)
		for i, x in enumerate(old_flat):
			old_coord = Array.coordinates_for_flat_index(i, shape)
			new_coord = [old_coord[i] for i in permutation]
			new_flat[Array.flat_index_for_coordinate(new_coord, permuted_shape)] = x
		new_struc = Array.shape_structured(new_flat, permuted_shape)
		return new_struc

	@staticmethod
	def promote_axis(struc, axis):
		if axis == 0:
			return struc
		shape = Array.shape_of_structured(struc)
		dim = len(shape)
		permutation = list(range(dim))
		permutation = [permutation[axis]] + permutation[:axis] + permutation[axis + 1:]
		return Array.permute_axes(struc, permutation)

	@staticmethod
	def map_struc(a, fn):
		def map_rec(a_struc):
			if Array.container(a_struc):
				return [map_rec(x) for x in a_struc]
			else:
				return fn(a_struc)

		return map_rec(a)

	@staticmethod
	def bi_map_struc(a, b, fn):
		def bi_rec(a_struc, b_struc):
			if Array.container(a_struc) and Array.container(b_struc):
				return [bi_rec(x, y) for x, y in zip(a_struc, b_struc)]
			elif not Array.container(a_struc) and not Array.container(b_struc):
				return fn(a_struc, b_struc)
			else:
				raise ValueError("Incompatible shapes", Array.shape_of_structured(a_struc),
				                 Array.shape_of_structured(b_struc))

		return bi_rec(a, b)

	@staticmethod
	def reduce_struc(a, fn):
		if len(a) < 2: return a
		accumulated = []
		acc = a[0]
		accumulated.append(acc)
		for v in a[1:]:
			acc = Array.bi_map_struc(acc, v, fn)
			accumulated.append(acc)
		return accumulated

	@staticmethod
	def reduce_struc_r(a, fn):
		if not Array.container(a): return [a]
		if len(a) == 0: return a
		if len(a) == 1: return [a[0]]
		next_struc = Array.reduce_struc_r(a[1:], fn)
		return [Array.bi_map_struc(a[0], next_struc[0], fn)] + next_struc

	@staticmethod
	def select_ranges(obj, ranges):
		if isinstance(obj, Array):
			target = obj.all_values()
		elif Array.container(obj):
			target = obj
		elif isinstance(obj, str):
			target = obj
		else:
			raise ValueError("Incompatible type", type(obj))
		new_values = [target[b: e] for b, e in ranges]
		return new_values

	@staticmethod
	def make_ranges(values):
		range_list = []
		last = 0
		start = None
		for i, v in enumerate(values + [0]):
			if v > last or v == 0:
				if start is not None:
					range_list.append((start, i))
					start = None if v == 0 else i
				elif v != 0:
					start = i
				last = v
		return range_list

	@staticmethod
	def find_sequence_bool(sequence, sub_sequence):
		target = tuple(sub_sequence)
		target_length = len(target)
		return [tuple(sequence[i:i + target_length]) == target for i, _ in enumerate(sequence)]

	def unique_values(self):
		return list(set(self.flat_list()))

	# Default Implementation of List Functions

	# Methods that do not alter the array

	def count(self, axis=-1):
		shape = self.get_shape()
		if -len(shape) <= axis < len(shape):
			return shape[axis]
		else:
			return 0

	def equivalent(self, other):
		if not isinstance(other, Array):
			return False
		elif self.get_shape() != other.get_shape():
			return False
		elif not all([x == y for x, y in zip(self.all_values(), other.all_values())]):
			return False
		else:
			return True

	def grade(self, reverse=False):
		grades = [i for _, i in sorted([(v, i) for i, v in enumerate(self.all_values())], reverse=reverse)]
		if self.can_reshape():
			structured = Array.shape_structured(grades, self.get_shape())
			return self.build(structured)
		else:
			return self.build(grades)

	def shape(self):
		return Coordinate(self.get_shape())

	# Methods that mutate the existing array

	def reshape(self, shape):
		all_values = self.all_values()
		new_shape = [x for x in shape if x != 0]
		if len(new_shape) == 0 and len(all_values) == 0:
			return self.mutate([self.default])
		elif len(new_shape) == 0:
			return self.mutate([all_values[0]])
		elif len(new_shape) == 1 and new_shape[0] <= len(all_values):
			return self.mutate(all_values[:new_shape[0]])
		elif len(new_shape) == 1:
			return self.mutate(all_values + [self.default] * (new_shape[0] - len(all_values)))
		else:
			new_struc = Array.shape_structured(self.all_values(), shape, self.default)
			return Array.promote(self.mutate(new_struc))

	def flatten(self):
		new_struc = self.all_values()
		return self.mutate(new_struc)

	def set_bool(self, bool_array, new_value):
		s_flat = self.all_values()
		b_flat = bool_array.all_values()
		new_values = [new_value if Array.truthy(b) else s for s, b in zip(s_flat, b_flat)]
		new_struc = Array.shape_structured(new_values, self.get_shape())
		return self.mutate(new_struc)

	def set_index(self, index, new_value):
		shape = self.get_shape()
		flat_index = Array.flat_index_for_coordinate(index, shape)
		values = self.all_values()
		values[flat_index] = new_value
		struc = Array.shape_structured(values, shape)
		return self.mutate(struc)

	def set_indices(self, indices, new_value):
		shape = self.get_shape()
		flat_indices = [Array.flat_index_for_coordinate(i, shape) for i in indices]
		values = self.all_values()
		for fi in flat_indices:
			values[fi] = new_value
		struc = Array.shape_structured(values, shape)
		return self.mutate(struc)

	def set_flat_index(self, flat_index, new_value):
		values = self.flat_list()
		if 0 <= flat_index < len(values):
			values[int(flat_index)] = new_value
		return self.mutate(values)

	def extend(self, obj, start=False):
		if self.can_reshape() and isinstance(obj, Array) and obj.can_reshape() and self.get_shape() == obj.get_shape():
			if start:
				return StructuredArray([obj.structured_values(), self.structured_values()])
			else:
				return StructuredArray([self.structured_values(), obj.structured_values()])
		elif self.can_reshape() and len(self.structured_values()) > 0 and isinstance(obj, Array) and len(
				obj.flat_list()) == len(self.structured_values()[0]):
			if start:
				self.mutate([obj.structured_values()] + self.structured_values())
				return self
			else:
				self.mutate(self.structured_values() + [obj.structured_values()])
				return self
		elif isinstance(obj, Array) and len(self.flat_list()) == len(obj.flat_list()):
			if start:
				return StructuredArray([obj.flat_list(), self.flat_list()])
			else:
				return StructuredArray([self.flat_list(), obj.flat_list()])
		elif not self.can_reshape() and isinstance(obj, Array) and not obj.can_reshape():
			if start:
				return self.mutate([obj] + self.flat_list())
			else:
				return self.mutate(self.flat_list() + [obj])
		elif not self.can_reshape() and isinstance(obj, Array):
			if start:
				return StructuredArray(obj.flat_list() + self.flat_list())
			else:
				return StructuredArray(self.flat_list() + obj.flat_list())
		else:
			return self.insert(obj, 0 if start else -1)

	def insert(self, obj, loc=-1):
		values = self.flat_list()
		if loc < 0: loc = len(values) + loc + 1
		values = values[:loc] + [obj] + values[loc:]
		return self.mutate(values)

	def at_least_2_dim(self):
		if len(self.get_shape()) == 1:
			return self.mutate([self.structured_values()])

	# Methods that create new arrays by combining arrays

	def join_on_axis(self, other, axis=-1):
		s_struc = self.structured_values()
		o_struc = other.structured_values()
		u_axis = axis if axis >= 0 else len(self.get_shape()) + axis

		def join_rec(a1, a2, ax):
			if ax == 0:
				if type(a1) is not list: a1 = [a1]
				if type(a2) is not list: a2 = [a2]
				return a1 + a2
			else:
				return [join_rec(x, y, ax - 1) for x, y in zip(a1, a2)]

		return self.build(join_rec(s_struc, o_struc, u_axis))

	def add_first_axis(self, other):
		s_struc = self.structured_values()
		o_struc = other.structured_values()
		s_shape = self.get_shape()
		o_shape = other.get_shape()
		if len(s_shape) == len(o_shape):
			new_struc = [s_struc, o_struc]
		elif len(s_shape) == len(o_shape) + 1:
			new_struc = s_struc + [o_struc]
		elif len(o_shape) == len(s_shape) + 1:
			new_struc = [s_struc] + o_struc
		else:
			raise ValueError("Incompatible array shapes", s_shape, o_shape)
		return self.build(new_struc)

	# Methods that return a new array, composed largely from the current array

	def take(self, n):
		struc = self.structured_values()
		new_struc = struc[:n]
		return self.build(new_struc)

	def drop(self, n):
		struc = self.structured_values()
		new_struc = struc[n:]
		return self.build(new_struc)

	def sort(self, reverse):
		return self.build(sorted(self.flat_list(), reverse=reverse))

	def transpose(self):
		return self.build(Array.permute_axes(self.structured_values()))

	def reverse_on_axis(self, axis):
		if axis < 0: axis = len(self.get_shape()) + axis

		def rev_rec(struc, u_axis):
			if not Array.container(struc):
				return struc
			elif u_axis == 0:
				return struc[::-1]
			else:
				return [rev_rec(s, u_axis - 1) for s in struc]

		new_struc = rev_rec(self.structured_values(), axis)
		return self.build(new_struc)

	def rotate_on_axis(self, axis, n):
		shape = self.get_shape()
		if axis < 0:
			used_axis = len(shape) + axis
		else:
			used_axis = axis
		original = list(range(len(shape)))
		permutation = [original[used_axis]] + original[:used_axis] + original[used_axis + 1:]
		inverse = original[1:used_axis + 1] + [original[0]] + original[used_axis + 1:]
		permuted = Array.permute_axes(self.structured_values(), permutation)
		permuted = permuted[-n:] + permuted[:-n]
		returned = Array.permute_axes(permuted, inverse)
		return self.build(returned).reshape(shape)

	def shift_on_axis(self, axis, n):
		shape = self.get_shape()
		if axis < 0:
			used_axis = len(shape) + axis
		else:
			used_axis = axis
		original = list(range(len(shape)))
		permutation = [original[used_axis]] + original[:used_axis] + original[used_axis + 1:]
		inverse = original[1:used_axis + 1] + [original[0]] + original[used_axis + 1:]
		permuted = Array.permute_axes(self.structured_values(), permutation)
		default = Array.map_struc(permuted[0], lambda x: self.default)
		if n > 0:
			shifted = [(default * n)] + permuted[:-n]
		else:
			shifted = permuted[-n:] + [(default * -n)]
		returned = Array.permute_axes(shifted, inverse)
		return self.build(returned).reshape(shape)

	def select_bool(self, array_bool):
		boolean_values = array_bool.all_values()
		target = self.all_values()
		result = [t for t, b in zip(target, boolean_values) if Array.truthy(b)]
		return FlatList(result)

	def select_index(self, index):
		s_flat = self.all_values()
		flat_index = self.flat_index_for_coordinate(index, self.get_shape())
		return s_flat[flat_index] if 0 <= flat_index < len(s_flat) else ''

	def select_indices(self, indices):
		return self.build([self.select_index(i) for i in indices.all_values()])

	def select_string(self, string):
		indices = self.all_values()
		return ''.join([string[i] for i in indices if 0 <= i < len(string)])

	def classify(self):
		shape = self.get_shape()
		classification = []
		for u in self.unique_values():
			group_indices = []
			for i, v in enumerate(self.all_values()):
				if v == u:
					if len(shape) == 1:
						group_indices.append(i)
					else:
						group_indices.append(Array.coordinates_for_flat_index(i, shape))
			classification.append(group_indices)
		return self.build(classification)

	def member(self, from_array, method='all'):
		if not isinstance(from_array, Array) and not Array.container(from_array):
			target = [from_array]
			return_type = 'value'
		elif Array.container(from_array):
			target = from_array
			return_type = 'value' if len(from_array) > 1 else 'array'
		else:
			target = from_array.unique_values()
			return_type = 'array'
		values = self.all_values()
		if method == 'all':
			result = all([v in target for v in values])
		elif method == 'bool':
			return_type = 'array'
			bool_array = [v in target for v in values]
			result = Array.shape_structured(bool_array, self.get_shape())
		elif method == 'indices':
			flat_indices = [i for i, v in enumerate(values) if v in target]
			shape = self.get_shape()
			result = []
			for i in flat_indices:
				coordinate = self.coordinates_for_flat_index(i, self.get_shape())
				if len(coordinate) == 1 or len(shape) == 1:
					result.append(coordinate[0])
				else:
					result.append(coordinate)
		else:
			raise ValueError("method " + method + " not valid")
		if return_type == 'array':
			return self.build(result)
		else:
			result = Array.flatten_structured(result)
			if len(result) > 0:
				return result[0]
			else:
				return None

	def window(self, window_size, reduce_fn, edges=False):
		shape = self.get_shape()

		window_shape = [window_size for _ in shape]
		window_relative = [win_rel_coord for win_rel_coord in Array.all_indices(window_shape)]
		valid_coordinates = [array_coord for array_coord in Array.all_indices(shape)]

		all_values = self.all_values()

		new_values = []
		for index in valid_coordinates:
			window_corner = [c - (w - 1) // 2 for c, w in zip(index, window_shape)]
			window_coordinates = [tuple([c + w for c, w in zip(window_corner, window_relative_coord)]) for
			                      window_relative_coord in window_relative]
			if not edges and all([w in valid_coordinates for w in window_coordinates]):
				values = [all_values[Array.flat_index_for_coordinate(c, shape)] for c in window_coordinates]
				new_values.append(Array.reduce_struc(values, reduce_fn)[-1])
			elif edges:
				valid_window_coordinates = [w for w in window_coordinates if w in valid_coordinates]
				values = [all_values[Array.flat_index_for_coordinate(c, shape)] for c in valid_window_coordinates]
				if len(values) == 0:
					new_values.append(self.default)
				else:
					new_values.append(Array.reduce_struc(values, reduce_fn)[-1])
			else:
				pass
		if not edges:
			new_shape = [s - w + 1 for w, s in zip(window_shape, shape) if s - w + 1 > 0]
		else:
			new_shape = shape

		return self.build(new_values).reshape(new_shape)

	def choose_slice_on_axis(self, n, axis):
		if axis < 0: axis = len(self.get_shape()) + axis
		if axis == 0:
			return self.build(self.structured_values()[n])
		else:
			return self.build(Array.promote_axis(self.structured_values(), axis)[n])

	# Selection indices / boolean mask conversions

	def bool_mask_from_indices(self, template):
		mask_template = []
		if type(template) is int:
			mask_template = [0] * template
		elif type(template) is list:
			mask_template = Array.map_struc(template, lambda x: 0)
		elif isinstance(template, Array):
			mask_template = Array.map_struc(template.structured_values(), lambda x: 0)
		else:
			ValueError("Boolean mask template type not usable", type(template))
		template_shape = Array.shape_of_structured(mask_template)
		bool_mask = Array.indices_to_bool([Array.index_value(i) for i in self.structured_values()], template_shape)
		if isinstance(template, Array):
			return template.build(bool_mask).reshape(template_shape)
		elif Array.number(template):
			return FlatList((bool_mask + [self.default] * int(template))[:template])
		else:
			return StructuredArray(bool_mask).reshape(template_shape)

	def indices_from_bool_mask(self):
		indices = Array.bool_to_indices(self.structured_values())
		return FlatList([Coordinate(i) for i in indices])

	def first_index_from_bool_mask(self):
		index = Array.first_index(self.structured_values())
		return Coordinate(index)

	# Higher level functions - return a new array or structure

	def filter(self, fn):
		new_values = [x for x in self.flat_list() if (fn(FlatList(x)) if Array.container(x) else fn(x))]
		return self.build(new_values)

	def reduce(self, fn, axis, reverse=False, partial_sums=False):
		shape = self.get_shape()
		if axis < 0: axis = len(shape) + axis
		if self.can_reshape():
			s_struc = Array.promote_axis(self.structured_values(), axis)
		else:
			s_struc = self.flat_list()
		if len(shape) > 1 and self.can_reshape():
			s_struc = [self.build(s) for s in s_struc]
		if reverse:
			new_array = Array.reduce_struc_r(s_struc, fn)
		else:
			new_array = Array.reduce_struc(s_struc, fn)
		if not Array.container(new_array):
			return new_array
		elif partial_sums:
			return self.build(new_array)
		elif not reverse and not Array.container(new_array[-1]):
			return new_array[-1]
		elif reverse and not Array.container(new_array[0]):
			return new_array[0]
		elif not reverse:
			return self.build(new_array[-1])
		else:
			return self.build(new_array[0])

	def reduce_all(self, fn, reverse=False, partial_sums=False):
		flat = self.build(self.all_values())
		return flat.reduce(fn, reverse, partial_sums)

	def map(self, fn):
		if self.can_reshape():
			return self.build(Array.map_struc(self.structured_values(), fn))
		else:
			return self.build(Array.map_struc(self.flat_list(), fn))

	def map_on_axis(self, fn, axis=-1):
		if axis < 0: axis = len(self.get_shape()) + axis
		if axis != 0:
			s_struc = Array.promote_axis(self.structured_values(), axis)
		else:
			s_struc = self.structured_values()
		result_struc = []
		for x in s_struc:
			row_val = fn(self.build(x))
			if isinstance(row_val, Array):
				row_val = row_val.structured_values()
			result_struc.append(row_val)
		return self.build(result_struc)

	# Array as a set methods

	def set_exclude(self, other):
		self_flat = self.flat_list()
		other_flat = other.all_values()
		self_values = [(tuple(x) if Array.container(x) else x) for x in self_flat]
		other_values = [(tuple(x) if Array.container(x) else x) for x in other_flat]
		values = [x for x in self_values if x not in other_values]
		unique = sorted(list(set(values)))
		return FlatList(unique)

	def set_intersection(self, other):
		self_values = [tuple(x) if Array.container(x) else x for x in self.flat_list()]
		other_values = [tuple(x) if Array.container(x) else x for x in other.flat_list()]
		values = [x for x in self_values if x in other_values]
		unique = list(set(values))
		return FlatList(unique)

	def set_union(self, other):
		self_values = [tuple(x) if Array.container(x) else x for x in self.flat_list()]
		other_values = [tuple(x) if Array.container(x) else x for x in other.flat_list()]
		values = [x for x in self_values + other_values]
		unique = list(set(values))
		return FlatList(unique)

	def set_unique(self):
		self_values = [tuple(x) if Array.container(x) else x for x in self.flat_list()]
		values = [x for x in self_values]
		unique = list(set(values))
		return FlatList(unique)

	def pop(self):
		self_values = [tuple(x) if Array.container(x) else x for x in self.flat_list()]
		unique = list(set(self_values))
		if len(unique) > 0:
			first, rest = unique[0], unique[1:]
			self.mutate(rest)
			return first
		else:
			return ''

	def add_value(self, obj):
		self_values = [tuple(x) if Array.container(x) else x for x in self.flat_list()]
		self_values.append(obj)
		unique = list(set(self_values))
		return self.mutate(unique)

	# Binary array product methods

	def bi_map(self, other, fn):
		if self.can_reshape():
			return self.build(Array.bi_map_struc(self.structured_values(), other.structured_values(), fn))
		else:
			return self.build(Array.bi_map_struc(self.flat_list(), other.flat_list(), fn))

	def inner_product(self, other, reduce_fn, combine_fn):
		result = []
		s_struc = self.structured_values()
		o_struc = other.structured_values()
		s_shape = self.get_shape()
		o_shape = other.get_shape()
		if len(s_shape) == 1 and len(o_shape) == 1:
			combined = [combine_fn(x, y) for x, y in zip(s_struc, o_struc)]
			if len(combined) > 1:
				reduced = reduce(reduce_fn, combined[1:], combined[0])
			else:
				reduced = combined
			return reduced
		else:
			for s in self.promote_axis(s_struc, 0):
				row = []
				for o in self.promote_axis(o_struc, -1):
					combined = Array.bi_map_struc(s, o, combine_fn)
					reduced = Array.reduce_struc(combined, reduce_fn)[-1]
					row.append(reduced)
				result.append(row)
			return self.build(result)

	def outer_product(self, other, combine_fn):
		result = []
		for x1 in self.flat_list():
			if Array.container(x1):
				x1_used = self.build(x1)
			else:
				x1_used = x1
			current_row = []
			for x2 in other.flat_list():
				if Array.container(x2):
					x2_used = self.build(x2)
				else:
					x2_used = x2
				current_row.append(combine_fn(x1_used, x2_used))
			result.append(current_row)
		return StructuredArray.build(self, result)

	# String Functions

	def stringify(self, code_points=False):
		if code_points and all([type(i) is int for i in self.all_values()]):
			return ''.join([chr(int(i)) for i in self.all_values() if i not in ('', None, 0)])
		else:
			return ''.join([str(x) for x in self.all_values()])


class FlatList(Array):
	def __init__(self, values, default=''):

		super(FlatList, self).__init__()

		self.values = values
		self.default = default

	# Required implementations

	def get_shape(self):
		return len(self.values),

	def can_reshape(self):
		return False

	def flat_list(self):
		return self.values

	def structured_values(self):
		return self.values

	def all_values(self):
		return self.flatten_structured(self.values)

	def mutate(self, structured_values):
		self.values = structured_values
		return self

	def build(self, structured_values):
		return FlatList(Array.flatten_structured(structured_values))

	# Specific to this sub-class

	def partition(self, obj):
		ranges = Array.make_ranges(self.all_values())
		return self.build(Array.select_ranges(obj, ranges))

	def split(self, obj):
		values = self.all_values()
		if isinstance(obj, Array):
			ranges = Array.make_ranges([not x for x in Array.find_sequence_bool(values, obj.all_values())])
		else:
			ranges = Array.make_ranges([x != obj for x in values])
		return self.build(Array.select_ranges(values, ranges))

	def group(self, obj):
		if isinstance(obj, Array):
			target = obj.all_values()
		elif type(obj) is str:
			target = obj
		else:
			raise ValueError("Incompatible type for group", type(obj))
		groups = self.unique_values()
		if type(obj) is str:
			group_struc = [''.join([v for s, v in zip(self.all_values(), target) if s == g]) for g in groups]
		else:
			group_struc = [[v for s, v in zip(self.all_values(), target) if s == g] for g in groups]
		return self.build(group_struc)

	# Method overrides

	def sort(self, reverse):
		values = [x for x in self.all_values() if x != '']
		return self.build(sorted(values, reverse=reverse))

	def __repr__(self):
		return '<FlatList ' + ' || '.join([str(s) for s in self.values]) + '>'


class StructuredArray(Array):
	def __init__(self, structured_values, default=0):
		super(StructuredArray, self).__init__()

		self.values = structured_values
		self.shape = Array.shape_of_structured(structured_values)
		self.default = default

	# Required implementations

	def get_shape(self):
		return self.shape

	def can_reshape(self):
		return True

	def structured_values(self):
		return self.values

	def flat_list(self):
		return self.values

	def all_values(self):
		return Array.flatten_structured(self.values)

	def mutate(self, structured_values):
		self.values = structured_values
		self.shape = Array.shape_of_structured(structured_values)
		return self

	def build(self, structured_values):
		return StructuredArray(structured_values, self.default)

	# Overrides of default implementation

	def reshape(self, shape):
		new_struc = Array.shape_structured([x for x in self.all_values() if x != ''], shape=shape, default=0)
		self.values = new_struc
		self.shape = shape
		self.default = 0
		return self

	def matrix_multiply(self, other):
		return self.inner_product(other, add, mul)

	def __repr__(self):
		return "<Structured Array " + str(self.structured_values()) + '>'


class MatrixArray(Array):
	data_type = np.float64

	def __init__(self, structured_values, shape=None):

		super(MatrixArray, self).__init__()

		self.values = np.array(structured_values, dtype=MatrixArray.data_type)
		if shape is not None:
			self.values = self.values.reshape(shape)
		self.default = 0.

	# Required implementations

	def get_shape(self):
		return self.values.shape

	def can_reshape(self):
		return True

	def structured_values(self):
		return self.values

	def flat_list(self):
		return Array.flatten_structured(self.values)

	def all_values(self):
		return Array.flatten_structured(self.values)

	def mutate(self, struc):
		self.values = np.array(struc, dtype=MatrixArray.data_type)
		return self

	def build(self, structured_values):
		return MatrixArray(structured_values, None)

	# Overrides of default implementations

	def reshape(self, shape):
		all_values = self.all_values()
		used_shape = [s for s in shape if s != 0]
		if len(used_shape) == 0 and len(all_values) > 0:
			values = self.all_values()[0]
		elif len(used_shape) == 0:
			values = [self.default]
		else:
			current_size = len(all_values)
			new_size = reduce(mul, used_shape, 1)
			if new_size > current_size:
				values = all_values + [self.default] * (max(0, new_size - current_size))
			else:
				values = all_values[:new_size]
		values = np.array(values, dtype=self.data_type)
		self.values = values.reshape(used_shape)
		return self

	def join_on_axis(self, other, axis=-1):
		return self.build(np.concatenate((self.values, other.values), axis))

	def select_index(self, coordinate):
		if isinstance(coordinate, Coordinate):
			flat_index = Array.flat_index_for_coordinate(coordinate.values, self.get_shape())
		else:
			flat_index = coordinate
		return self.all_values()[flat_index]

	def select_indices(self, indices):
		return self.build([self.values[i] for i in indices.values])

	def transpose(self):
		new_matrix = MatrixArray(self.all_values(), self.get_shape())
		new_matrix.values.transpose()
		return MatrixArray(self.structured_values().transpose())

	@classmethod
	def promote_axis(cls, struc, axis):
		return np.moveaxis(struc, axis, 0)

	def return_mutated(self, new_struc):
		self.values = np.array(new_struc)
		return self

	def matrix_multiply(self, other):
		return self.build(np.matmul(self.structured_values(), other.structured_values()))

	# Specific to this subclass

	def matrix_binary(self, other, fn):
		s_struc = self.structured_values()
		o_struc = other.structured_values()
		s_flat = s_struc.flatten()
		o_flat = o_struc.flatten()
		r_flat = np.array([fn(s, o) for s, o in zip(s_flat, o_flat)], dtype=self.data_type)
		structured = r_flat.reshape(s_struc.shape)
		return self.build(structured)

	def __repr__(self):
		return "<Matrix Array " + str(self.structured_values()).replace('\n', '') + ">"


# Coordinates are used for indexing into structured arrays
# When 1-dimensional, they generally produce integers when used

class Coordinate(Array):

	def __init__(self, coordinates):

		super(Coordinate, self).__init__()

		if type(coordinates) in (int, float, np.float_):
			self.values = (int(coordinates),)
		else:
			self.values = tuple([int(c) for c in coordinates])

	def get_shape(self):
		return len(self.values),

	def can_reshape(self):
		return False

	def structured_values(self):
		return self.values

	def flat_list(self):
		return list(self.values)

	def all_values(self):
		return list(self.values)

	def mutate(self, structured_list):
		self.values = Array.flatten_structured(structured_list)
		return self

	def build(self, structured_list):
		return Coordinate(Array.flatten_structured(structured_list))

	# Specific to this subclass

	def add_dimension(self, i, start=True):
		if start:
			self.values = tuple([int(i)] + list(self.values))
		else:
			self.values = tuple(list(self.values) + [int(i)])
		return self

	def __eq__(self, other):
		if isinstance(other, Coordinate):
			return self.values == other.values
		elif Array.container(other):
			return self.values == tuple(other)
		else:
			return self.values == other

	def __add__(self, other):
		return Coordinate([x + y for x, y in zip(self.values, other.values)])

	def __sub__(self, other):
		return Coordinate([x - y for x, y in zip(self.values, other.values)])

	def __mul__(self, other):
		return Coordinate([x * other for x in self.values])

	def __lt__(self, other):
		for i, j in zip(self.values, other.values):
			if i < j: return True
			if i > j: return False
		return False

	def grid_len(self):
		return sum([abs(x) for x in self.values])

	def vector_len(self):
		return sqrt(sum([x * x for x in self.values]))

	def __len__(self):
		return len(self.values)

	def __hash__(self):
		return self.values.__hash__()

	def __repr__(self):
		return '<Coordinate ' + str(self.values) + '>'
