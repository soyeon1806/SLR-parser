from functools import reduce
from tree import Node

# print where the error occured and message
def print_error(inputs, line, index, error_message):
    print(f'Error at line {line + 1}:')
    print('    ' + inputs[line].strip())

    if index == 0:
        print('    ' + '^' * len(inputs[line].split()[index]))
    if index == -1: # error occured at last in line
        print('    ' + ' ' * reduce(lambda x, y : x + y + 1, map(len, inputs[line].split())) + '^')
    else:
        print('    ' + ' ' * reduce(lambda x, y : x + y + 1, map(len, inputs[line].split()[:index])), '^' * len(inputs[line].split()[index]))
    
    print(error_message)


def slr_parse(inputs, action_table, goto_table, grammar_table):
    line, index = 0, 0

    # Generate(Get) next token
    def token_generator(inputs):
        nonlocal line, index

        inputs[-1] += ' $' # Add EOF

        tokens = list(map(lambda l : l.split(), inputs))
        while line < len(tokens):
            while index >= len(tokens[line]): # if line has no token anymore -> Move to next line
                line += 1
                index = 0
            yield tokens[line][index] # yield next token
            index += 1


    tokens = token_generator(inputs) # initialize generator
    next_symbol = next(tokens)

    stack = [0] # initial State: 0
    nodes = [] # list for constructing Parse-Tree

    while 1:
        # Rejected (Unknown Token)
        if next_symbol not in action_table['header']:
            print('REJECTED')
            print_error(inputs, line, index, f"TokenError: '{next_symbol}' is unknown")
            return -1

        # Get decision from Action Table with current state and symbol
        column_idx = action_table['header'].index(next_symbol)
        next_decision = action_table['elements'][stack[-1]][column_idx]

        # Accepted
        if next_decision == 'acc':
            assert(len(nodes) == 1)

            print('ACCEPTED')
            nodes[0].visualize()
            return 1
        
        # Rejected (Invalid syntax)
        if next_decision == ' ':
            print('REJECTED')
            if index == 0: # if previous line has no valid token
                print_error(inputs, line - 1, -1, f"SyntaxError: invalid syntax")
            else:
                print_error(inputs, line, index, f"SyntaxError: invalid syntax")
            return -1

        # Shift
        if next_decision[0] == 's': 
            stack.append(int(next_decision[1:])) # Push next state
            nodes.append(Node(next_symbol))

            next_symbol = next(tokens) # Set indicator to next

        # Reduce
        else: 
            grammar = grammar_table[int(next_decision[1:])]
            
            childs = []
            if grammar['right'] == None: # LEFT -> '' (epsilon ε)
                childs.append(Node('ε'))
            else: # Construct Sub-Tree
                for _ in range(len(grammar['right'])): # Pop length of RHS from the stack
                    stack.pop()
                    childs.append(nodes.pop())     
            nodes.append(Node(grammar['left'], childs[::-1]))


            # Grammer Error
            if grammar['left'] not in goto_table['header']:
                print("Grammer is not corresponding with LR-Table")
                return -1

            # Push next state
            column_idx = goto_table['header'].index(grammar['left'])
            stack.append(int(goto_table['elements'][stack[-1]][column_idx]))