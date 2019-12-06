import ply.lex as lex

# TODO: For report, tell why we set <= as 1 lexem and not 
reserved_words = (
    'while',
    'for',
    'if',
    'else',
    'draw',
    'move',
    'setColor',
    'rotate',
    'scale',
    'sin',
    'PI'
)

tokens = (
    'ADD_OP',
    'MUL_OP',
    'MOD_OP',
    'PARENTHESIS_OPEN',
    'PARENTHESIS_CLOSE',
    'BRACKET_OPEN',
    'BRACKET_CLOSE',
    'NUMBER',
    'HEXNUMBER',
    'SEMICOLON',
    'IDENTIFIER',
    'EQUAL',
    'COMPARATOR',
    'INIT_PREFIX'
) + tuple(map(lambda s: s.upper(), reserved_words))

t_ADD_OP = r"[+-]"
t_MUL_OP = r"[*/]"
t_MOD_OP = r"%"

t_PARENTHESIS_OPEN = r"("
t_PARENTHESIS_CLOSE = r")"

t_BRACKET_OPEN = r"{"
t_BRACKET_CLOSE = r"}"

t_SEMICOLON = r";"

t_EQUAL = r"="
t_COMPARATOR = r"[!=]=|[><]=?"

t_INIT_PREFIX = r"#"

def t_IDENTIFIER(t):
    r"[A-Za-z_][\w_]*"
    if t.value in reserved_words:
        t.type = t.value.upper()
    return t


def t_NUMBER(t):
    r"\d+(?:\.\d*)?"
    if '.' in t.value:
        t.value = float(t.value)
    else:
        t.value = int(t.value)
    return t

def t_HEXNUMBER(t):
    r"0x[0-9A-Fa-f]{6}"
    t.value = int(t.value)

def t_newline(t):
    r"\n+"
    t.lexer.lineno += len(t.value)

t_ignore = " \t"

def t_error(t):
    print(f"Illegal character {t.value[0]}")
    t.lexer.skip(1)

lex.lex()

if __name__ == "__main__":
    import sys
    with open(sys.argv[1]) as file:
        lex.input(file.read())

        while True:
            tok = lex.token()
            if not tok: break
            print(f"line {tok.lineno}: {tok.type}({tok.value})")