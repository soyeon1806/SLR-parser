from pathlib import Path
from contextlib import redirect_stdout
import sys
import syntax_analyzer
import table_generator

if __name__ == '__main__':
    src_path = Path(sys.argv[1])           # inputs/01.txt
    out_dir = Path('outputs')
    out_dir.mkdir(exist_ok=True)
    out_file = out_dir / (src_path.stem + '_tree.txt')

    # LR 테입르 로드
    action_table, goto_table = table_generator.generate_table('lr_table.txt')

    # 문법 로드
    grammar_table = table_generator.generate_grammar_table('grammar.txt')

    # 파일 읽기
    lines = src_path.read_text(encoding="utf-8").splitlines()

    # 파싱 실행
    with out_file.open('w', encoding='utf-8') as f, redirect_stdout(f):
        syntax_analyzer.slr_parse(lines, action_table, goto_table, grammar_table)

    print(f"Result has been saved to {out_file}")