# FBl337
# Programming Code Golf Language
# Created: 25 January 2024
# Version: 25 January 2024 11:00PM
# Copyright: James Leibert 2023
# Licence: Available for use under the GPL3 Licence https://www.gnu.org/licenses/gpl-3.0.txt

# command_assistant.py
# Lookup commands quickly


from fb1337.commands import FBLeet_language, print_commands, print_symbols
from fb1337.parser import number_aliases, number_names


help_text = """
fb1337 Command Assistant

'command' - see details of the command
'text?'   - search command documentation
'group!'  - list all group commands
q - quit, ? - lists all commands, ?? - symbol table

"""

print(help_text)
while True:

    print()
    c = input("Command: ")

    if c in ['q', 'Q', 'x', 'X', 'exit', 'quit']:
        break
    elif c in ['h', 'H', 'help', 'Help', '?']:
        print(help_text)
        print("----- parser -----")
        for k in number_aliases:
            print(k, '\t', number_names[k], number_aliases[k])
        print('⍝', '\t', "Comment")
        print('Ø', '\t', "Null")
        print_commands()
        continue
    elif c in ['symbols', '??', 'all??', 'all symbols', 'all ??', 'sym']:
        print('parser')
        print('\t', ' '.join([k for k in number_aliases] + ['Ø', '⍝']))
        print_symbols(grouped=('all' not in c))
        continue
    found = False

    # Parser symbols
    for k, v in number_names.items():
        if c in v:
            print(number_names[k], '\t', "'"+str(k)+"'", number_aliases[k])
            found = True
    if all([ch in '01234567890' for ch in c]):
        i = int(c)
        for k, v in number_aliases.items():
            if v == i:
                print(number_names[k], '\t', "'"+str(k)+"'", number_aliases[k])
                found = True
                break
    for command in ['Ø', 'null', 'none', "Null", "NULL", "''", 'None']:
        if c == command or c in command:
            print('null', '\t', "'Ø'\t", "'Null value'")
            found = True
    for command in ['⍝', 'finger', 'comment', '#']:
        if c == command or c in command:
            print('comment', '\t', "'⍝'\t", "'Start of comment. Continues until new line'")
            found = True

    # Command symbols
    for command in FBLeet_language:
        if len(c) > 1 and c[-1] == '?':
            for pattern in command['patterns']:
                if c[:-1] in pattern['description']:
                    print(command['alias'], '\t', "'"+command['symbol']+"'\t", command['signature'], pattern['signature'], '"'+pattern['description']+'"')
                    found = True
        elif c in command['alias'] or c == command['symbol'] or (len(c) > 1 and c[-1] == '!' and c[:-1] in command['group']):
            print(command['alias'], '\t', "'"+command['symbol']+"'\t", command['signature'])
            for pattern in command['patterns']:
                print('\t\t', pattern['signature'], '"'+pattern['description']+'"')
            found = True
    if not found:
        print("not found", c)
