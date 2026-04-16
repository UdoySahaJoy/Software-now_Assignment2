import os


def evaluate_file(input_path):
    dir_path = os.path.dirname(input_path)
    output_path = os.path.join(dir_path, 'output.txt')
    results = []

    with open(input_path, 'r') as f:
        lines = f.readlines()

    out_file = open(output_path, 'w')

    for line in lines:
        expr = line.strip()
        if not expr:
            continue

        result = process(expr)
        results.append(result)

        out_file.write("Input: " + result['input'] + "\n")
        out_file.write("Tree: " + result['tree'] + "\n")
        out_file.write("Tokens: " + result['tokens'] + "\n")

        res_val = result['result']
        if res_val == 'ERROR':
            out_file.write("Result: ERROR\n")
        else:
            if res_val == int(res_val):
                out_file.write("Result: " + str(int(res_val)) + "\n")
            else:
                out_file.write("Result: " + f"{res_val:.4f}" + "\n")

        out_file.write("\n")

    out_file.close()
    return results

def process(expr):
    try:
        i = 0
        tokens = []

        while i < len(expr):
            if expr[i] == ' ':
                i = i + 1
            elif expr[i].isdigit() or expr[i] == '.':
                j = i
                while j < len(expr) and (expr[j].isdigit() or expr[j] == '.'):
                    j = j + 1
                tokens.append(('NUM', float(expr[i:j])))
                i = j
            elif expr[i] in '+-*/':
                tokens.append(('OP', expr[i]))
                i = i + 1
            elif expr[i] == '(':
                tokens.append(('LPAREN', '('))
                i = i + 1
            elif expr[i] == ')':
                tokens.append(('RPAREN', ')'))
                i = i + 1
            else:
                raise Exception("bad")

        tokens.append(('END', None))

        new_tokens = []
        for k in range(len(tokens)):
            new_tokens.append(tokens[k])
            if k < len(tokens) - 1:
                curr = tokens[k][0]
                nxt = tokens[k + 1][0]
                if (curr == 'NUM' and nxt == 'LPAREN') or (curr == 'RPAREN' and nxt == 'LPAREN') or (curr == 'RPAREN' and nxt == 'NUM'):
                    new_tokens.append(('OP', '*'))
        tokens = new_tokens

        token_str = ""
        for tok in tokens:
            if tok[0] == 'NUM':
                if tok[1] == int(tok[1]):
                    token_str = token_str + "[NUM:" + str(int(tok[1])) + "] "
                else:
                    token_str = token_str + "[NUM:" + str(tok[1]) + "] "
            elif tok[0] == 'OP':
                token_str = token_str + "[OP:" + tok[1] + "] "
            elif tok[0] == 'LPAREN':
                token_str = token_str + "[LPAREN:(] "
            elif tok[0] == 'RPAREN':
                token_str = token_str + "[RPAREN:)] "
            elif tok[0] == 'END':
                token_str = token_str + "[END]"

        tree, pos = parse_add(tokens, 0)

        tree_str = tree_to_str(tree)

        try:
            value = calc(tree)
            result_val = value
        except:
            result_val = 'ERROR'

        return {
            'input': expr,
            'tree': tree_str,
            'tokens': token_str,
            'result': result_val
        }
    except:
        return {
            'input': expr,
            'tree': 'ERROR',
            'tokens': 'ERROR',
            'result': 'ERROR'
        }
    
def parse_add(tokens, pos):
    left, pos = parse_mul(tokens, pos)

    while pos < len(tokens) and tokens[pos][0] == 'OP' and (tokens[pos][1] == '+' or tokens[pos][1] == '-'):
        op = tokens[pos][1]
        pos = pos + 1
        right, pos = parse_mul(tokens, pos)
        left = (op, left, right)

    return left, pos


def parse_mul(tokens, pos):
    left, pos = parse_neg(tokens, pos)

    while pos < len(tokens) and tokens[pos][0] == 'OP' and (tokens[pos][1] == '*' or tokens[pos][1] == '/'):
        op = tokens[pos][1]
        pos = pos + 1
        right, pos = parse_neg(tokens, pos)
        left = (op, left, right)

    return left, pos

def parse_neg(tokens, pos):
    if pos < len(tokens) and tokens[pos][0] == 'OP' and tokens[pos][1] == '-':
        pos = pos + 1
        val, pos = parse_neg(tokens, pos)
        return ('neg', val), pos

    return parse_atom(tokens, pos)


def parse_atom(tokens, pos):
    if pos >= len(tokens):
        raise Exception("end")

    tok = tokens[pos]

    if tok[0] == 'NUM':
        return tok[1], pos + 1
    elif tok[0] == 'LPAREN':
        pos = pos + 1
        val, pos = parse_add(tokens, pos)
        if pos >= len(tokens) or tokens[pos][0] != 'RPAREN':
            raise Exception("no close")
        return val, pos + 1
    else:
        raise Exception("bad")


def calc(tree):
    if isinstance(tree, (int, float)):
        return float(tree)

    if tree[0] == 'neg':
        return -calc(tree[1])

    op = tree[0]
    left = calc(tree[1])
    right = calc(tree[2])

    if op == '+':
        return left + right
    elif op == '-':
        return left - right
    elif op == '*':
        return left * right
    elif op == '/':
        if right == 0:
            raise Exception("div")
        return left / right


def tree_to_str(tree):
    if isinstance(tree, (int, float)):
        if tree == int(tree):
            return str(int(tree))
        return str(tree)

    if tree[0] == 'neg':
        return "(neg " + tree_to_str(tree[1]) + ")"

    op = tree[0]
    left = tree_to_str(tree[1])
    right = tree_to_str(tree[2])
    return "(" + op + " " + left + " " + right + ")"
