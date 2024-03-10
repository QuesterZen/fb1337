# FBl337
# Programming Code Golf Language
# Created: 21 February 2024
# Version: 21 February 2024 12:00PM
# Copyright: James Leibert 2024
# Licence: Available for use under the GPL3 Licence https://www.gnu.org/licenses/gpl-3.0.txt

# lexer.py
# fb1337 code reading - regex based lexer


import re
from typing import List

# Shortcut substitutions
shortcut_aliases = {'ḣ': 100, 'ḳ': 1000, 'Ḳ': 1024, 'ṁ': 1_000_000, 'ḃ': 1_000_000_000, 'ṫ': 10, 'Ḷ': 50,
                    'ḟ': 15, 'Ḟ': 255, 'ẓ': 0, 'ṅ': -1}
shortcut_names = {'ḣ': 'hundred', 'ḳ': 'thousand', 'Ḳ': 'binary k', 'ṁ': 'million', 'ḃ': 'billion',
                  'ṫ': 'ten', 'Ḷ': 'fifty', 'ḟ': 'fifteen', 'Ḟ': 'byte max',
                  'ẓ': 'zero', 'ṅ': 'negative 1'}


# The following regex expressions are used to identify tokens in the language
# from left to right. They are greedy.
# noinspection SpellCheckingInspection,SpellCheckingInspection
token_patterns = [
	(r'[\ ,]', 'noop'),

	(r'Ø', 'null'),

	(r"0", 'number'),
	(r"[123456789]\d*", 'number'),
	(r"~[123456789]\d*", 'number'),
	(r"[\ḣ\ḳ\Ḳ\ṁ\ḃ\ṫ\Ḷ\ḟ\Ḟ](?![a-zA-Z])", 'number'),

	(r"`nl", 'newline'),

	(r"([a-zA-Z]|`.)+", 'literal'),

	(r"(\)|\;)", 'block end'),

	(r'.', 'symbol')]

comment_pattern = r"\A[\t ]*([^\t⍝]*)[\t⍝]([^\n\r]*)(?:[\n\r]*)"


def match(re_patterns: list, code_string: str, offset: int) -> (str, str, int):
	"""Takes a code string and finds the first matching token after the offset"""
	code = code_string[offset:]
	if len(code) == 0:
		return '', "return", len(code_string)

	for p, token_type in re_patterns:
		m = p.match(code)
		if m:
			return m.group(), token_type, offset + m.end()
	else:
		raise SyntaxError("No matching tokens found", code)


def separate_comments(commented_code: str) -> (str, dict):
	"""Extract the comments from the code and return the cleaned code and comments"""
	# Extract comments from the code, to be added to the tokens later
	lines: List[str] = commented_code.split('\n')
	comment_re = re.compile(comment_pattern)

	code_fragments: List[str] = []
	location: int = 0
	comments: dict = dict()

	for line in lines:
		m = comment_re.match(line)
		if m:
			code_fragment, new_comment = m.group(1), m.group(2).strip(' \t\n\r')
		else:
			code_fragment, new_comment = line.strip(' \t\n\r'), ""

		code_fragments.append(code_fragment)
		location += len(code_fragment)

		if new_comment:
			comments[location] = comments.get(location, "") + '; ' + new_comment

	return "".join(code_fragments), comments


def get_comments_for_token(comments, lost_comments, location, consumed):
	"""Identify comments belonging to the code consumed in last match"""
	token_comments: List[str] = []
	token_comments += lost_comments
	for i in range(location + 1, location + consumed + 1):
		if i in comments:
			token_comments += [comments[i]]
	return '; '.join(token_comments)


def tokenize(commented_code: str) -> list:
	"""Break the code into lexical tokens, and separate out the comments"""
	# compile the regex patterns for token identification
	code_re = [(re.compile(pattern), name) for pattern, name in token_patterns]

	# Extract comments from the code
	code: str
	comments: dict
	code, comments = separate_comments(commented_code)

	# Break the code into lexical tokens
	location: int = 0
	tokens: List[tuple] = []
	lost_comments: List[str] = []
	while len(code) > 0:

		# Read the next token
		token: str
		token_type: str
		consumed: int
		token_comment_str: str
		token, token_type, consumed = match(code_re, code, offset=0)

		# Identify any comments related to this token
		token_comment_str = get_comments_for_token(comments, lost_comments, location, consumed)
		lost_comments = []

		# Extract the token code and move ahead
		token_start = location
		location += consumed
		token_code, code = code[:consumed], code[consumed:]

		# Turn the regex identification into a correct lexical token
		value = token
		if token_type == 'noop':
			lost_comments.append(token_comment_str)
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
			elif value in shortcut_aliases:
				value = shortcut_aliases[value]
			else:
				value = int(value)

		elif token_type == 'literal':
			token_type = 'value'
			value = token.replace('`', '')

		tokens.append(
			(token_type,
			 value,
			 {'comments': token_comment_str,
			  'token_code': token_code,
			  'code location': (token_start, location)}))

	return tokens
