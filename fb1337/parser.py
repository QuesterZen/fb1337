# FBl337
# Programming Code Golf Language
# Created: 21 February 2024
# Version: 21 February 2024 12:00PM
# Copyright: James Leibert 2024
# Licence: Available for use under the GPL3 Licence https://www.gnu.org/licenses/gpl-3.0.txt

# parser.py
# fb1337 code parser - regex based parsing


import re

number_aliases = {'ḣ': 100, 'ḳ': 1000, 'Ḳ': 1024, 'ṁ': 1_000_000, 'ḃ': 1_000_000_000, 'ṫ': 10, 'Ḷ': 50, 'ḟ': 15, 'Ḟ': 255}
number_names = {'ḣ': 'hundred', 'ḳ': 'thousand', 'Ḳ': 'binary k', 'ṁ': 'million', 'ḃ': 'billion', 'ṫ': 'ten', 'Ḷ': 'fifty', 'ḟ': 'fifteen', 'Ḟ': 'byte max'}

class Reader:
	"""The following methods are exposed:
	    tokenize - converts a program into a list of tokens with comments embedded
    Tokens are returned as tuples (token_type, token_value, token_info)
    token_info is a dictionary containing
        comments - comments in the annotated code immediately after than token
        token_code - actual original code string used to generate the token
        code_location - the start and end points in the original program where the token was found
	"""

	# The following regex expressions are used to identify tokens in the language
	# from left to right. They are greedy.
	# noinspection SpellCheckingInspection,SpellCheckingInspection
	token_patterns = [
		('[\ ,]', 'noop'),

		('Ø', 'null'),

		("0", 'number'),
		("[123456789]\d*", 'number'),
		("~[123456789]\d*", 'number'),
		("[\ḣ\ḳ\Ḳ\ṁ\ḃ\ṫ\Ḷ\ḟ\Ḟ](?![a-zA-Z])", 'number'),

		("`nl", 'newline'),
		("([a-zA-Z]|`.)+", 'literal'),

		("(\)|\;)", 'block end'),

		('.', 'symbol')
	]

	comment_pattern = "\A[\t ]*([^\t⍝]*)[\t⍝]([^\n\r]*)(?:[\n\r]*)"

	number_alias_lookup = number_aliases
	
	def __init__(self, patterns=token_patterns):
		self.patterns = [(re.compile(pattern), name) for pattern, name in patterns]

	def match(self, code_string, offset):
		"""takes a code string and finds the first matching token after offset"""

		code = code_string[offset:]

		if len(code) == 0:
			return '', "return", len(code_string)
		
		for p, token_type in self.patterns:
			m = p.match(code)
				
			if m:
				return m.group(), token_type, offset + m.end()
		
		print("Could not find a match for code", code)
		raise SyntaxError


	@staticmethod
	def tokenize(program):
		"""convert an annotated program into a list of tokens (containing comments)"""

		# Extract comments from the code, to be added to the tokens later
		lines = program.split('\n')
		p = re.compile(Reader.comment_pattern)
		code = ""
		location = 0
		comments = dict()
		for line in lines:
			m = p.match(line)
			if m:
				new_code, new_comment = m.group(1), m.group(2).strip(' \t\n\r')
				code += new_code
				location += len(new_code)
				if len(new_comment) > 0:
					if location in comments:
						comments[location] = comments[location] + '; ' + new_comment
					else:
						comments[location] = new_comment
			else:
				new_code = line.strip(' \t\n\r')
				code += new_code
				location += len(new_code)


		# Parse the code (with comments removed) into tokens
		reader = Reader()
		location = 0
		tokens = []
		lost_comments = []
		while len(code) > 0:

			# Read the next token
			token, token_type, consumed = reader.match(code, 0)
			
			token_comments = []
			if len(lost_comments) > 0:
				token_comments += lost_comments
				lost_comments = []
			for i in range(location + 1, location + consumed + 1):
				if i in comments:
					token_comments += [comments[i]]
			token_comments = '; '.join(token_comments)
			
			token_start = location
			location += consumed
			token_code, code = code[:consumed], code[consumed:]
			
			value = token
			if token_type == 'noop':
				lost_comments.append(token_comments)
				continue

			elif token_type == 'null':
				token_type = 'value'
				value = ''

			elif token_type == 'newline':
				token_type = 'value'
				value = '\n'

			elif token_type == 'number':
				token_type = 'value'
				if value[0] == '~':
					value = -int(value[1:])
				elif value in Reader.number_alias_lookup:
					value = Reader.number_alias_lookup[value]
				else:
					value = int(value)

			elif token_type == 'literal':
				token_type = 'value'
				value = token.replace('`', '')
				
			tokens.append( (token_type, value,
				{'comments': token_comments, 'token_code': token_code, 'code location': (token_start, location)}) )
			
		return tokens
