# Genate LR table from text file
def generate_table(file_dir):
    
    # action / goto 테이블의 공통 구조:
    # - 'header': 컬럼 이름 (터미널 / 비터미널)
    # - 'elements': 상태별 row 값 리스트들의 리스트
    action_table = {
        'header': [],
        'elements': []
    }

    goto_table = {
        'header': [],
        'elements': []
    }

    with open(file_dir) as file:
        # 첫 줄: 헤더 라인 (탭 구분)
        headers = file.readline().rstrip().split('\t')

        # '$' 컬럼(EOF)의 바로 다음부터가 GOTO(비터미널) 영역이라는 가정
        goto_idx = headers.index('$') + 1

        # 액션 헤더: '$'까지 포함한 터미널 헤더
        action_table['header'] = headers[:goto_idx]
        # GOTO 헤더: '$' 다음부터 끝까지 (비터미널 헤더)
        goto_table['header'] = headers[goto_idx:]

        # 이후 각 줄 == 한 상태(state)의 row
        for line in file.readlines():
            # 각 row의 맨 앞 셀은 라벨이니까 버림
            row = line.rstrip().split('\t')[1:]

            # row의 길이가 헤더보다 짧으면 빈 칸으로 채워서 길이를 맞춰줌
            row.extend([' '] * (len(headers) - len(row)))

            # 액션 / GOTO 영역으로 슬라이스해서 각각 추가
            action_table['elements'].append(row[:goto_idx])
            goto_table['elements'].append(row[goto_idx:])

    return action_table, goto_table



def generate_grammar_table(file_dir):
    grammar_table = []
    with open(file_dir) as file:
        for line in file.readlines():
            # 한 줄을 공백 기준으로 토큰화함
            # 기대 형식: LHS -> RHS1 RHS2 ...
            row = line.rstrip().split()
            grammar_table.append({
                'left': row[0], # LHS
                'right': None if row[2] == "''" else row[2:] # RHS 토큰 리스트, ε는 None
            })

    return grammar_table