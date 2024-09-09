# Generate LR Table from text file
def generate_lr_table(file_dir):
    action_table = {
        'header': [],
        'elements': []
    }

    goto_table = {
    'header': [],
    'elements': []
    }

    with open(file_dir) as file:
        headers = file.readline().rstrip().split('\t')
        goto_idx = headers.index('$') + 1 # goto table's start index

        action_table['header'] = headers[:goto_idx]
        goto_table['header'] = headers[goto_idx:]

        for line in file.readlines():
            row = line.rstrip().split('\t')[1:] # remove row header
            row.extend([' '] * (len(headers) - len(row)))

            action_table['elements'].append(row[:goto_idx])
            goto_table['elements'].append(row[goto_idx:])

    return action_table, goto_table


def generate_grammar_table(file_dir):
    grammar_table = []
    with open(file_dir) as file:
        for line in file.readlines():
            row = line.rstrip().split()
            grammar_table.append({
                'left': row[0], # LHS
                'right': None if row[2] == "''" else row[2:] # RHS
            })

    return grammar_table