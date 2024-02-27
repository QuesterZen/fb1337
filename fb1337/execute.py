# FBl337
# Programming Code Golf Language
# Created: 21 February 2024
# Version: 21 February 2024 12:00PM
# Copyright: James Leibert 2024
# Licence: Available for use under the GPL3 Licence https://www.gnu.org/licenses/gpl-3.0.txt

# execute.py
# FB1337 interpreter eval/apply loop


from fb1337.commands import Commands
from fb1337.environment import Environment
from fb1337.lambda_fn import run_object
from fb1337.syntax import SyntaxTree, SyntaxToken
from fb1337.type_utilities import parse_program_parameter, apply_type_transformations, return_value


class Program:

	def __init__(self, syntax_tree, parameters=None, debugger=None, logging=False):
		"""If parameters are provided, it is assumed the first parameter is the name of the program"""

		self.syntax_tree = syntax_tree
		self.parameters = [parse_program_parameter(parameter) for parameter in
		                   parameters] if parameters is not None else []
		self.debugger = debugger
		self.logging = logging
		self.commands = Commands()
		self.name = self.parameters[0] if len(self.parameters) > 0 and self.parameters[0] is not None else 'f'

	def _notify(self, env, info_dictionary):
		if self.debugger is not None:
			self.debugger.notify(env, info_dictionary)
		if self.logging:
			print("notification", 'stack:', env.get_stack(), 'implicit:', env.implicit(), 'info:', info_dictionary)

	def run(self, path=None):
		"""This function will run a program in syntax tree form.
		It is the only function fully exposed to other modules."""

		base_env = Environment(path=path)
		base_env.program_parameters = self.parameters

		self.eval_context(base_env, self.syntax_tree)

		return return_value(base_env.get_stack())

	def eval_context(self, env, tree):
		"""evaluate a single block of code"""

		if isinstance(tree, SyntaxToken):
			self.eval_token(env, tree)

		elif isinstance(tree, SyntaxTree):
			self.eval_context(env, tree.tree)

		elif type(tree) is list and len(tree) > 0:
			for token in tree:
				self.eval_context(env, token)

	def eval_token(self, env, token):
		"""evaluate a single token blocks are run with eval_context functions are run with apply"""

		token_type = token.token_type

		if token.value == ';' or token_type == 'end block':
			self._notify(env, {'token': token})

		elif token_type == 'fn':
			self.apply(env, token)

		elif token_type == "value":
			self._notify(env, {'token': token})
			env.push(token.value)

		else:
			print("Unknown token", token)
			raise SyntaxError

		return

	def apply(self, env, token):
		"""lookup a function token and run the associated code"""

		symbol = token.value
		stack_parameters = []
		code_parameters = []
		fn_parameters = []
		block_parameters = []

		for _ in range(token.stack_values):
			# Stack parameters are taken directly from the stack without evaluation
			stack_parameters.append(env.pop())
		stack_parameters = stack_parameters[::-1]

		for code_token in token.code_tokens:
			self.eval_context(env, code_token)
			code_parameters.append(env.pop())

		for fn_token in token.fn_tokens:
			# We want to use high-level functions with simple operators (eg. reduce (/+ in APL), combinators (/+÷# in APL) etc.)
			# So when we see a symbol as a fn parameter, we assume it is to be used this way,
			# The code below seems absurd, but seems to be necessary due to a weird Python 3 'bug'
			# just adding lambda e: self.eval_context(env, code_token) to the code_parameters doesn't work
			# python does not generate new lambdas each time through - it returns the same lambda every time, so this code forces
			# it to generate a brand new lambda each time. In particular the combinators wouldn't work without this change!
			# https://docs.python-guide.org/writing/gotchas/#late-binding-closures
			# So apparently this is a "feature" not a bug and due to python late binding / object reference assignment!
			if fn_token.token_type == 'fn' and fn_token.value in 'λµ(κ$':
				def wrapper(t):
					def f(e):
						self.eval_context(env, t)
						run_object(e, e.pop())

					return f

				new_lambda = wrapper(fn_token)
			else:
				new_lambda = (lambda t: (lambda e: self.eval_context(env, t)))(fn_token)
			fn_parameters.append(new_lambda)

		if token.sub_tree is not None:
			# There is only ever one code block controlled by a single token, it is passed with delayed execution
			# so the owner can control its environment and timing
			block_parameters.append(lambda e: self.eval_context(e, token.sub_tree))

		match = self.commands.match_command(symbol, stack_parameters, code_parameters, fn_parameters, block_parameters)
		if match is None:
			print("No matching function found", symbol,
			      [type(t).__name__ for t in stack_parameters],
			      [type(t).__name__ for t in code_parameters],
			      [type(t).__name__ for t in block_parameters])
			raise KeyError

		notification_info = {'token': token,
		                     'symbol': match['symbol'],
		                     'alias': match['alias'],
		                     'signature': match['signature'],
		                     'type signature': match['type signature'],
		                     'description': match['description'],
		                     's-params': stack_parameters,
		                     'c-params': code_parameters,
		                     'f-params': fn_parameters,
		                     'b-params': block_parameters,
		                     'value': None}
		self._notify(env, notification_info)

		all_parameters = stack_parameters + code_parameters + fn_parameters + block_parameters
		type_signature = match['type signature']
		used_fn = match['function']
		transformed_parameters, transformed_fn = apply_type_transformations(all_parameters, type_signature, used_fn)
		value = transformed_fn(env, *transformed_parameters)
		if value is not None:
			env.push(value)

		notification_info['value'] = value
		self._notify(env, notification_info)

		return
