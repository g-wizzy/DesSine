import ply.yacc as yacc
import AST
from lex import tokens


def p_program(p):
    '''program: init_block newline body'''
    p[0] = AST.ProgramNode({
        "init": p[1],
        "body": p[3]
    })


def p_init_block(p):
    '''init_block: init | init newline init'''
    try:
        children = [p[1]] + p[3].children
    except:
        children = [p[1]]
    p[0] = AST.InitBlockNode(children)


def p_init(p):
    '''init: INIT_PREFIX INIT_FUNCTION PARENTHESIS_OPEN parameters PARENTHESIS_CLOSE'''
    p[0] = AST.InitNode(p[2], p[4])


def p_body(p):
    '''body : statement
        | statement newline body'''
    try:
        children = [p[1]] + p[3].children
    except:
        children = [p[1]]
    p[0] = AST.Node(children)

 def p_empty(p):
     'empty :'
     pass

# If empty does not work, copy rule without parameters or make something between
def p_parameters(p):
    '''parameters : expression
        | expression COMMA parameters
        | empty'''
    try:
        p[0] = [p[1]] + p[3]
    except:
        try:
            p[0] = [p[0]]
        except:
            p[0] = []


def p_statement(p):
    '''statement : assignment
        | structure
        | action'''
    p[0] = p[1]


def p_comparison(p):
    'comparison : expression COMPARATOR expression'
    p[0] = AST.ComparisonNode(p[2], [p[1], p[3]])


def p_structure(p):
    '''structure : if
        | while
        | for'''
    p[0] = p[1]


def p_if(p):
    '''if : IF comparison BRACKET_OPEN body BRACKET_CLOSE
        | IF comparison BRACKET_OPEN body BRACKET_CLOSE ELSE BRACKET_OPEN body BRACKET_CLOSE'''
    try:
        p[0] = AST.IfNode([p[2], p[4], p[8]])
    except:
        p[0] = AST.IfNode([p[2], p[4]])


def p_while(p):
    '''while : WHILE comparison BRACKET_OPEN body BRACKET_CLOSE'''
    p[0] = AST.WhileNode([p[2], p[4]])


def p_for(p):
    'for : FOR PARENTHESIS_OPEN assignment SEMICOLON comparison SEMICOLON assignment PARENTHESIS_CLOSE BRACKET_OPEN block BRACKET_CLOSE'
    p[0] = AST.ForNode([p[3], p[5], p[7], p[10]])


def p_action(p):
    'action : BUILTIN_ACTION PARENTHESIS_OPEN parameters PARENTHESIS_CLOSE'
    p[0] = AST.FunctionNode(p[1], p[2])


def p_assignment(p):
    'assignment : IDENTIFIER EQUAL expression'
    p[0] = AST.AssignNode([AST.TokenNode(p[1]), p[3]])


def p_expression_num(p):
    'expression : NUMBER'
    p[0] = AST.TokenNode(p[1])


def p_expression_constant(p):
    'expression : BUILTIN_READONLY'
    p[0] = AST.TokenNode(p[1])


def p_expression_var(p):
    'expression : IDENTIFIER'
    p[0] = AST.TokenNode(p[1])


def p_expression_function(p):
    'expression : BUILTIN_FUNCTION PARENTHESIS_OPEN parameters PARENTHESIS_CLOSE'
    p[0] = AST.FunctionNode(p[1], p[3])


operations = {
    '+': lambda x, y: x + y,
    '-': lambda x, y: x - y,
    '*': lambda x, y: x * y,
    '/': lambda x, y: x / y
}


precedence = (
    ('left', 'ADD_OP'),
    ('left', 'MUL_OP'),
    ('right', 'UN_OP')
)


def p_expression_op(p):
    '''expression : expression ADD_OP expression
    | expression MUL_OP expression'''
    p[0] = AST.OpNode(p[2], [p[1], p[3]])


def p_unary_op(p):
    ''' expression : ADD_OP expression %prec UN_OP'''
    p[0] = AST.OpNode(p[1], [p[2]])


def p_expression_paren(p):
    'expression : PARENTHESIS_OPEN expression PARENTHESIS_CLOSE'
    p[0] = p[2]


def p_error(p):
    print(f"Syntax error in line {p.lineno}")
    yacc.errok()
