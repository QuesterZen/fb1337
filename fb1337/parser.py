# FBl337
# Programming Code Golf Language
# Created: 21 February 2024
# Version: 21 February 2024 12:00PM
# Copyright: James Leibert 2024
# Licence: Available for use under the GPL3 Licence https://www.gnu.org/licenses/gpl-3.0.txt

# parser.py
# Abstract Syntax Tree builder for fb1337 interpreter


from fb1337.lexer import tokenize

# Complete list of all functions available and their signatures. These need to match the commands
# given in the FBLCommands module
command_dictionary = dict()


def add_command_signature(symbol, signature, alias):
	global command_dictionary
	command_dictionary[symbol] = (signature, alias,)


class SyntaxToken:
	"""Syntax Tokens are nodes in the Syntax Tree. Each node consists of a single token
	(similar to a parse token with extra information on its location in the tree) as well
	as the parameters and blocks for function tokens required to run the token, which
	constitute the next level in the tree."""

	def __init__(self, lexical_token,
	             token_type=None, value=None,
	             stack_values=None, code_tokens=None, fn_tokens=None, sub_tree=None):

		self.token_type = lexical_token[0] if token_type is None else token_type
		self.value = lexical_token[1] if value is None else value

		self.comments = lexical_token[2]['comments']
		self.code_location = lexical_token[2]['code location']
		self.code_text = lexical_token[2]['token_code']
		self.parse_token_type = lexical_token[0]
		self.parse_token = lexical_token

		self.stack_values = 0 if stack_values is None else stack_values
		self.code_tokens = [] if code_tokens is None else code_tokens
		self.fn_tokens = [] if fn_tokens is None else fn_tokens
		self.sub_tree = None if sub_tree is None else sub_tree

		self.location = None
		self.index = None

	def __repr__(self):
		params = []
		if self.stack_values > 0:
			params.append(str(self.stack_values))
		else:
			params.append('-')
		if len(self.code_tokens) > 0:
			params.append(str([x.value for x in self.code_tokens]))
		else:
			params.append('-')
		if len(self.fn_tokens) > 0:
			params.append(str([x.value for x in self.fn_tokens]))
		else:
			params.append('-')
		if self.sub_tree is not None and len(self.sub_tree) > 0:
			params.append("block")
		else:
			params.append('-')

		s = ''
		s += "<"
		s += str(self.index)
		s += ' ' + str(self.token_type)
		s += ' ' + (str(self.value) if self.value != '' else 'Ø')
		s += ' '
		s += ' '.join(params)
		s += ">"
		return s


class SyntaxTree:
	"""The syntax tree is a semantic representation of the program. The top level of the
	tree is a sequence of tokens to be evaluated. Each function or block token also contains
	within it (at a lower level in the tree), the tokens that represent its parameters or
	block code.
	The Syntax Tree is used for both debugging the program and also for executing the code.
	Apart from its value as a structured data object to represent the code, it exposes
	the method 'traverse' which traverses the code tokens in order and allows the user to
	provide a function that will be run for each token."""

	def __init__(self, program):

		self.program = program
		self.tree = SyntaxTree._build_tree(program)  # A tree of tokens making up the program

		self.tokens = []  # All token objects, including those at lower levels in the syntax tree
		SyntaxTree._traverse(self.tree, lambda x: self.tokens.append(x))
		for i, token in enumerate(self.tokens):
			token.index = i

		SyntaxTree._add_token_locations(self.tree, [])
		self.locations = dict()  # reverse lookup to index of token at location
		for token in self.tokens:
			self.locations[token.location] = token.index

	@staticmethod
	def _build_tree(program):

		tree = []

		# Get a tree for each separate context block in the code
		parse_tokens = tokenize(program)
		while len(parse_tokens) > 0:
			syntax, parse_tokens = SyntaxTree._eval_syntax(parse_tokens)
			tree.append(syntax)

		# If there is only one context block, we don't need to wrap it
		while type(tree) is list and len(tree) == 1:
			tree = tree[0]

		return tree

	@staticmethod
	def _eval_syntax(parse_token_list):
		tree = []

		remaining = parse_token_list

		end_context = False
		while not end_context and len(remaining) > 0:
			end_context, syntax, remaining = SyntaxTree._eval_syntax_token(remaining)
			tree.append(syntax)

		return tree, remaining

	@staticmethod
	def _eval_syntax_token(parse_tokens):
		parse_token, remaining_parse_tokens = parse_tokens[0], parse_tokens[1:]
		token_type, value = parse_token[0], parse_token[1]

		if token_type == 'block end':
			return True, SyntaxToken(parse_token, token_type='end block'), remaining_parse_tokens

		elif token_type == 'value':
			return False, SyntaxToken(parse_token, token_type='value'), remaining_parse_tokens

		elif token_type == 'symbol':
			fn_syntax, remaining_parse_tokens = SyntaxTree._apply_syntax(parse_token, remaining_parse_tokens)
			return False, fn_syntax, remaining_parse_tokens

		else:
			print("Unexpected token", parse_token, remaining_parse_tokens)
			raise SyntaxError

	@staticmethod
	def _apply_syntax(token, remaining_parse_tokens):
		global command_dictionary

		symbol = token[1]
		signature, alias = command_dictionary[symbol] if symbol in command_dictionary else (None, None)

		if signature is None:
			print(symbol, 'not found')
			raise SyntaxError

		stack_values, code_values, function_values, blocks = signature
		code_value_syntax = []
		function_value_syntax = []

		for _ in range(code_values):
			end_context, syntax, remaining_parse_tokens = SyntaxTree._eval_syntax_token(remaining_parse_tokens)
			if end_context:
				print('unexpected end of program parsing command', symbol)
				raise SyntaxError
			code_value_syntax.append(syntax)

		for _ in range(function_values):
			end_context, syntax, remaining_parse_tokens = SyntaxTree._eval_syntax_token(remaining_parse_tokens)
			if end_context:
				print('unexpected end of program parsing command', symbol)
				raise SyntaxError
			function_value_syntax.append(syntax)

		if blocks:
			sub_tree_syntax = []
			while len(remaining_parse_tokens) > 0:
				end_context, new_token, remaining_parse_tokens = SyntaxTree._eval_syntax_token(remaining_parse_tokens)
				sub_tree_syntax.append(new_token)
				if end_context:
					break
		else:
			sub_tree_syntax = None

		return SyntaxToken(token,
		                   token_type='fn',
		                   value=symbol,
		                   stack_values=stack_values,
		                   code_tokens=code_value_syntax,
		                   fn_tokens=function_value_syntax,
		                   sub_tree=sub_tree_syntax), \
			remaining_parse_tokens

	@staticmethod
	def _add_token_locations(tree, depth_stack):
		if type(tree) is list:
			for i, t in enumerate(tree):
				SyntaxTree._add_token_locations(t, depth_stack + [i])

		elif isinstance(tree, SyntaxToken):
			node_type = tree.token_type
			if node_type == 'fn' or node_type == 'block':
				count = 0
				for t in tree.code_tokens:
					SyntaxTree._add_token_locations(t, depth_stack + [count * 2])
					count += 1
				for f in tree.fn_tokens:
					SyntaxTree._add_token_locations(f, depth_stack + [count * 2])
					count += 1
				if tree.sub_tree is not None:
					SyntaxTree._add_token_locations(tree.sub_tree, depth_stack)
					count += 1

			tree.location = tuple(depth_stack)

		else:
			print("Illegal syntax", tree)
			raise SyntaxError

	@staticmethod
	def _traverse(tree, call_fn):
		if type(tree) is list:
			for t in tree:
				SyntaxTree._traverse(t, call_fn)

		elif isinstance(tree, SyntaxToken):
			call_fn(tree)
			for t in tree.code_tokens + tree.fn_tokens:
				SyntaxTree._traverse(t, call_fn)
			if tree.sub_tree is not None:
				SyntaxTree._traverse(tree.sub_tree, call_fn)

		else:
			print("Illegal syntax", tree)
			raise SyntaxError

	def pretty_print(self):
		"""Print a listing of the program with indentations to indicate the tree structure"""

		def token_string(token, indent):
			s = ""
			s += ' ' * indent
			s += (str(token.value) if token.value != '' else 'Ø') + ' '
			if token.token_type == 'fn' and token.value in command_dictionary:
				s += "'" + command_dictionary[token.value][1] + "' "
				if command_dictionary[token.value][0][0] > 0:
					s += "(" + str(command_dictionary[token.value][0][0]) + ') '
				if len(token.code_tokens + token.fn_tokens) > 0:
					s += '['
				if token.sub_tree is not None:
					s += '{'
			if len(token.comments) > 0:
				s += '    # ' + token.comments + ' # '
			if token.token_type == 'fn' and token.value in command_dictionary:
				if len(token.code_tokens + token.fn_tokens) > 0:
					s += token_list_string(token.code_tokens + token.fn_tokens, indent + 2) + ']'
				if token.sub_tree is not None:
					s += token_list_string(token.sub_tree, indent + 2) + "}"
			return s

		def token_list_string(token_list, indent):
			return ''.join(['\n' + token_string(t, indent) for t in token_list])

		print(token_list_string(self.tree, 0))

	def __repr__(self):
		s = []
		SyntaxTree._traverse(self.tree, lambda x: s.append(x.value))
		return "<SyntaxTree " + ''.join([str(a) for a in s]) + ">"
