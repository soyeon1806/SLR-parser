import sys
import syntax_analyzer
import table_generator

if __name__ == '__main__':
    input_file = open(sys.argv[1])

    action_table, goto_table = table_generator.generate_lr_table('lr_table.txt')
    grammar_table = table_generator.generate_grammar_table('grammar.txt')

    syntax_analyzer.slr_parse(input_file.readlines(), action_table, goto_table, grammar_table)
    