from functools import reduce
from tree import Node

# ---------------------------------------------------------------------
# 오류 위치 및 메시지 예쁘게 출력
#    inputs: 소스코드 (문자열 리스트, 줄 단위)
#    line  : 현재 줄 인덱스 (0-based)
#    index : 현재 줄에서 토큰 인덱스 (0-based), -1은 줄의 마지막을 의미함
# ---------------------------------------------------------------------
def print_error(inputs, line, index, error_message):
    print(f'Error at line {line + 1}:')
    print('    ' + inputs[line].strip())

    # 커서(^^^^) 표시용 보조 계산: '토큰 앞까지의 공백 길이'
    if index == 0:
        # 줄의 맨 앞 토큰에서 오류가 난 경우: 바로 밑에 ^^^ 적기
        print('    ' + '^' * len(inputs[line].split()[index]))
    
    if index == -1:
        # 줄의 마지막에서 오류가 난 경우
        print('    ' + ' ' * reduce(
            lambda x, y: x + y + 1,
            map(len, inputs[line].split())
        ) + '^')
    
    else:
        # 해당 토큰 앞까지의 공백(토큰 길이 + 공백 1칸)을 누적해서 들여쓰기
        print(
            '    ' +
            ' ' * reduce(
                lambda x, y: x + y + 1,
                map(len, inputs[line].split()[:index])
            ),
            '^' * len(inputs[line].split()[index])
        )

    print(error_message)





#---------------------------------------------------------------------------------
# SLR  파서의 본체
#    inputs        : 소스코드 (줄 단위 문자열 리스트)
#    action_table  : { 'header': [터미널들], 'elements': [각 상태별 Row(list)] }
#    goto_table    : { 'header': [터미널들], 'elements': [각 상태별 Row(list)] }
#    grammar_table : 인덱스 접근 가능한 규칙 테이블
#                    ε 규칙은 right == None 로 표현
#---------------------------------------------------------------------------------
def slr_parse(inputs, action_table, goto_table, grammar_table):
    line, index = 0, 0 # 현재 읽는 위치 (줄 / 토큰)

    #--------------------------------------------------------------------
    # 토큰 생성기
    #    - 마지막 줄 끝에 EOF 기호인 '$'를 덧붙여서 StopIteration을 방지함
    #    - line / index는 nonlocal로 공유함
    #--------------------------------------------------------------------
    def token_generator(inputs):
        nonlocal line, index
        
        inputs[-1] += ' $' # EOF 토큰 추가

        tokens = list(map(lambda l: l.split(), inputs)) # 각 줄 -> 토큰 리스트
        while line < len(tokens):
            # 현재 줄의 토큰을 다 소비하면 다음 줄로 넘어감
            while index >= len(tokens[line]):
                line += 1
                index = 0
                if line >= len(tokens):
                    return # 모든 줄 소비
                
            # 다음 토큰 공금
            yield tokens[line][index]
            index += 1

    tokens = token_generator(inputs) # 토큰 제너레이터 초기화
    next_symbol = next(tokens) # lookahead(다음 토큰)

    stack = [0] # 상태 스택 (초기 상태 0)
    nodes = [] # 파스트리 구성용 노드 스택

    while 1:
        # step 1) 현재 lookahead가 Action 헤더에 없으면 'REJECTED'
        if next_symbol not in action_table['header']:
            print('REJECTED')
            print_error(inputs, line, index, f"TokenError: '{next_symbol}' is unknown")
            return -1
            
        # step 2) 현재 상태와 lookahed로 Action 결정
        column_idx = action_table['header'].index(next_symbol)
        next_decision = action_table['elements'][stack[-1]][column_idx]

        # step 3) Accept
        if next_decision == 'acc':
            assert(len(nodes) == 1) # 전체 파스트리는 1개 루트여야 됨
            print('ACCEPTED')
            nodes[0].visualize() # 트리 출력
            return 1
            
        # step 4) Error: Action 셀 공백
        if next_decision == ' ':
            print('REJECTED')
            # 직전 줄에 유효 토큰이 전혀 없으면 line-1 기준으로 표시
            if index == 0:
                print_error(inputs, line -1, -1, "SyntaxError: invalid syntax")
            else:
                print_error(inputs, line, index, "SyntaxError: invalid syntax")
            return -1
            
        # step 5) shift: "sN" 형태 (ex. s5)
        if next_decision[0] == 's':
            # 상태 스택에 다음 상태 푸시
            stack.append(int(next_decision[1:]))
            # 파스트리 노드 스택에는 '토큰' 노드 푸시
            nodes.append(Node(next_symbol))
            # lookahead를 다음 토큰으로 갱신
            next_symbol = next(tokens)

        # step 6) reduce: "rK" 형태 (ex. r12)
        else:
            grammar = grammar_table[int(next_decision[1:])] # 사용 규칙

            # 파스트리 하위 노드 수집
            childs = []
            if grammar['right'] is None:
                childs.append(Node('ε'))
            else:
                # RHS 길이만큼 상태 스택 팝 + 노드 스택 팝해서 서브트리 구성
                for _ in range(len(grammar['right'])):
                    stack.pop()
                    childs.append(nodes.pop())

            # LHS를 부모로 해서 파스트리 노드 생성 (자식 순서를 뒤집어서 복구)
            nodes.append(Node(grammar['left'], childs[::-1]))

            # step 6-1) goto 테이블에서 다음 상태를 계산함
            if grammar['left'] not in goto_table['header']:
                print("Grammar is not corresponding with LR-Table")
                return -1
            
            column_idx = goto_table['header'].index(grammar['left'])
            # 현재 상태에서 LHS로 GOTO해서 다음 상태 푸시
            stack.append(int(goto_table['elements'][stack[-1]][column_idx]))