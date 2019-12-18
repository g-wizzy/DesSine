import ply.lex as lex

# TODO: For report, tell why we set <= as 1 lexem and not
reserved_words = (
    'while',
    'for',
    'if',
    'else'
)

tokens = (
    'INIT_PREFIX',
    'SEMICOLON',
    'COMMA',
    'ADD_OP',
    'MUL_OP',
    'MOD_OP',
    'EQUAL',
    'PARENTHESIS_OPEN',
    'PARENTHESIS_CLOSE',
    'BRACKET_OPEN',
    'BRACKET_CLOSE',
    'NUMBER',
    'HEX_NUMBER',
    'IDENTIFIER',
    'COMPARATOR',
    'COMMENT',
    'INIT_FUNCTION',
    'BUILTIN_ACTION',
    'BUILTIN_FUNCTION',
    'BUILTIN_READONLY',
    'newline'
) + tuple(map(lambda s: s.upper(), reserved_words))

t_ADD_OP = r"[+-]"
t_MUL_OP = r"[*/]"
t_MOD_OP = r"%"

t_PARENTHESIS_OPEN = r"\("
t_PARENTHESIS_CLOSE = r"\)"

t_BRACKET_OPEN = r"\{"
t_BRACKET_CLOSE = r"\}"

t_SEMICOLON = r";"
t_COMMA = r","

t_EQUAL = r"="
t_COMPARATOR = r"[!=]=|[><]=?"

t_INIT_PREFIX = r"\#"

init_functions = ("width", "height", "background")

builtin_actions = ("draw",
                   "move",
                   "rotate",
                   "scale",
                   "setColor",
                   "setLineWidth",
                   "log")

builtin_functions = ("sin",)

builtin_readonlys = ("PI", "x", "y")


def t_IDENTIFIER(t):
    r"[A-Za-z_][\w_]*"
    if t.value in reserved_words:
        t.type = t.value.upper()
    elif t.value in init_functions:
        t.type = "INIT_FUNCTION"
    elif t.value in builtin_actions:
        t.type = "BUILTIN_ACTION"
    elif t.value in builtin_functions:
        t.type = "BUILTIN_FUNCTION"
    elif t.type in builtin_readonlys:
        t.type = "BUILTIN_READONLY"
    return t


def t_HEX_NUMBER(t):
    r"0x[0-9A-Fa-f]+"
    t.value = int(t.value, 16)
    return t


def t_NUMBER(t):
    r"\d+(?:\.\d*)?"
    if '.' in t.value:
        t.value = float(t.value)
    else:
        t.value = int(t.value)
    return t


def t_newline(t):
    r"\n+"
    t.lexer.lineno += len(t.value)
    return t


def t_COMMENT(t):
    r"//.*\n+"
    t.lexer.lineno += 1
    pass


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
            if not tok:
                break
            print(f"line {tok.lineno}: {tok.type}({tok.value})")
