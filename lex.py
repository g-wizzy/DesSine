import ply.lex as lex
import sys
import logger

###########################################
# DesSine lexer
# Made by Pierre Bürki and Loïck Jeanneret
# Last updated on 10.01.20
###########################################

reserved_words = (
    'while',
    'for',
    'if',
    'else',
    'function',
)

tokens = (
    # Operators
    'ADD_OP',
    'MUL_OP',
    'MOD_OP',
    'EQUAL',
    'COMPARATOR',
    # Delimiters
    'INIT_PREFIX',
    'COMMENT',
    'SEMICOLON',
    'COMMA',
    'PARENTHESIS_OPEN',
    'PARENTHESIS_CLOSE',
    'BRACKET_OPEN',
    'BRACKET_CLOSE',
    'newline',
    # Terms
    'NUMBER',
    'HEX_NUMBER',
    'IDENTIFIER',
    # Builtins
    'INIT_FUNCTION',
    'BUILTIN_ACTION',
    'BUILTIN_FUNCTION',
    'BUILTIN_READONLY',
) + tuple(map(lambda s: s.upper(), reserved_words))  # Appends reserved words

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
t_COMPARATOR = r"[!=]=|[><]=?"  # Matches ==, !=, <=, >=, <, >

t_INIT_PREFIX = r"\#"

# Functions that can only be called at the start using #
init_functions = ("width", "height", "background")

# builtin methods returning nothing
builtin_actions = ("draw",
                   "move",
                   "rotate",
                   "scale",
                   "setColor",
                   "setLineWidth",
                   "log",)

# builting methods returning something
builtin_functions = ("sin",)

# constants (called readonlys because it may support position in the future)
builtin_readonlys = ("PI",)

# Identifiers may identify the following things:
# - reserved words (for, if, else, while, ...)
# - init functions (width, height, ...)
# - built-in functions, actions, readonlys (sin, draw, pi, ...)
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

# Hex numbers are used to encode colors
def t_HEX_NUMBER(t):
    r"0x[0-9A-Fa-f]+"
    t.value = int(t.value, 16)
    return t

# Support integer and float numbers
def t_NUMBER(t):
    r"\d+(?:\.\d*)?"
    if '.' in t.value:
        t.value = float(t.value)
    else:
        t.value = int(t.value)
    return t

# We use new lines as instruction separator
def t_newline(t):
    r"\n+"
    t.lexer.lineno += len(t.value)
    return t

# No multiline comment support as of yet
def t_COMMENT(t):
    r"//.*\n*"
    t.lexer.lineno += t.value.count("\n")
    pass


t_ignore = " \t"


def t_error(t):
    logger.error("Lexical error", t.lineno, f"illegal character '{t.value[0]}'")
    t.lexer.skip(1)
    sys.exit()


lex.lex()

if __name__ == "__main__":
    with open(sys.argv[1]) as file:
        lex.input(file.read())

        while True:
            tok = lex.token()
            if not tok:
                break
            print(f"line {tok.lineno}: {tok.type}({tok.value})")
