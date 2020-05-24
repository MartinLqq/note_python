"""
Clean markdown file content copyed from the url:
    https://www.cnblogs.com/panwenbin-logs/p/5731265.html  (SQLAlchemy模型使用)
"""


def _can_del(line):
    delete_items = ['copycode.gif', '.gif']
    for item in delete_items:
        if item in line:
            return True
    return False

def _del_num_before_code(line):
    # delete num and space before code line
    line = line.lstrip()
    if line.split(' ') and line.split(' ')[0].isdigit():
        num = int(line.split(' ')[0])
        line = line.replace(str(num) + ' ', '')
    return line

def _is_empty_line(line):
    if not line.lstrip('-').strip():
        return True
    return False


def clean_md_copyed_from_html(src_path, dst_path):
    result = []
    with open(src_path, 'r', encoding='utf8') as file:
        lines = file.readlines()
    in_code = False
    code_start = 0
    for line in lines:
        if _can_del(line):
            continue

        if '```' in line:
            code_start += 1
            if code_start % 2 == 1:
                line = line.strip() + 'python\n'

        if code_start % 2 == 1:
            in_code = True

        if in_code:
            line = _del_num_before_code(line)

        if not in_code and _is_empty_line(line):
            continue

        if 'coding:' in line:
            continue
        if '/usr/bin/env' in line:
            continue

        result.append(line)

    with open(dst_path, 'w', encoding='utf8') as f:
        f.write(''.join(result))


if __name__ == '__main__':
    clean_md_copyed_from_html(
        src_path='tmp_sqlalchemy.md',
        dst_path='tmp.md'
    )