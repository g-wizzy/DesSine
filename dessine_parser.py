import ply.yacc as yacc
import AST
from lex import tokens
import logger
import sys

###########################################
# DesSine parser
# Made by Pierre Bürki and Loïck Jeanneret
# Last updated on 10.01.20
###########################################

# Program must always start with an init block
def p_program(p):
    '''program : init_block newline body'''
    p[0] = AST.ProgramNode(p.lineno(1), [p[1], p[3]])


# Init block must contain at least one instruction
def p_init_block(p):
    '''init_block : init 
        | init_block newline init'''
    try:
        children = p[1].children + [p[3]]
    except:
        children = [p[1]]
    p[0] = AST.InitBlockNode(p.lineno(1), children)


# An init instruction consists of an init function call (e.g. #width(100))
def p_init(p):
    '''init : INIT_PREFIX INIT_FUNCTION PARENTHESIS_OPEN parameters PARENTHESIS_CLOSE'''
    p[0] = AST.InitNode(p.lineno(2), p[2], p[4])


def p_routine_definition(p):
    '''routine_definition : FUNCTION IDENTIFIER PARENTHESIS_OPEN parameters PARENTHESIS_CLOSE block'''
    p[0] = AST.RoutineDefinitionNode(p.lineno(2), p[2], p[4], p[6])


def p_routine_call(p):
    '''routine_call : IDENTIFIER PARENTHESIS_OPEN parameters PARENTHESIS_CLOSE'''
    p[0] = AST.RoutineCallNode(p.lineno(1), p[1], p[3])


def p_body(p):
    '''body : statement
        | body newline statement'''
    try:
        p[0] = AST.BodyNode(p.lineno(1), p[1].children + [p[3]])
    except:
        p[0] = AST.BodyNode(p.lineno(1), p[1])

# The next two rules are used to "absorb" new lines surrounding the body
def p_reduce_left_body(p):
    '''body : newline body'''
    p[0] = p[2]


def p_reduce_right_body(p):
    '''body : body newline'''
    p[0] = p[1]

# Changes scope
def p_block(p):
    '''block : BRACKET_OPEN body BRACKET_CLOSE'''
    p[0] = AST.BlockNode(p.lineno(2), [p[2]])

# We do not want syntaxic errors on empty blocks, even though they have no reason to exist
def p_empty_block(p):
    '''block : BRACKET_OPEN empty BRACKET_CLOSE'''
    p[0] = AST.BlockNode(p.lineno(1), [])

# Syntaxic sugar allowing us to use "empty" instead of not writing anything
def p_empty(p):
    'empty :'
    pass

# Parameters can be empty, contain one expression, or a list of expression separated by commas
def p_parameters(p):
    '''parameters : expression
        | expression COMMA parameters'''
    try:
        p[0] = [p[1]] + p[3]
    except:
        p[0] = [p[1]]

# For lisibility's sake
def p_empty_parameters(p):
    'parameters : empty'
    p[0] = []


def p_statement(p):
    '''statement : assignment
        | structure
        | action
        | routine_definition
        | routine_call'''
    p[0] = p[1]


def p_comparison(p):
    'comparison : expression COMPARATOR expression'
    p[0] = AST.ComparisonNode(p.lineno(2), p[2], [p[1], p[3]])


def p_structure(p):
    '''structure : if
        | while
        | for'''
    p[0] = p[1]

# if and if...else blocks
# Note that the condition must be a comparison (e.g. if(a == 1) works, but if(a) does not)
# Note that brackets must be on the same line
def p_if(p):
    '''if : IF PARENTHESIS_OPEN comparison PARENTHESIS_CLOSE block
        | IF PARENTHESIS_OPEN comparison PARENTHESIS_CLOSE block ELSE block'''
    try:
        p[0] = AST.IfNode(p.lineno(1), [p[3], p[5], p[7]])
    except:
        p[0] = AST.IfNode(p.lineno(1), [p[3], p[5]])

# Note that the condition must be a comparison (e.g. while(a == 1) works, but while(a) does not)
def p_while(p):
    '''while : WHILE PARENTHESIS_OPEN comparison PARENTHESIS_CLOSE block'''
    p[0] = AST.WhileNode(p.lineno(1), [p[3], p[5]])

# Note that the condition must be a comparison
def p_for(p):
    'for : FOR PARENTHESIS_OPEN assignment SEMICOLON comparison SEMICOLON assignment PARENTHESIS_CLOSE block'
    p[0] = AST.ForNode(p.lineno(1), [p[3], p[5], p[7], p[9]])

# An action returns nothing
def p_action(p):
    'action : BUILTIN_ACTION PARENTHESIS_OPEN parameters PARENTHESIS_CLOSE'
    p[0] = AST.FunctionNode(p.lineno(1), p[1], p[3])


def p_assignment(p):
    'assignment : IDENTIFIER EQUAL expression'
    p[0] = AST.AssignNode(p.lineno(1), [AST.TokenNode(p.lineno(1), p[1]), p[3]])

# Starting here, all the different expression types
def p_expression_num(p):
    '''expression : NUMBER
        | HEX_NUMBER'''
    p[0] = AST.TokenNode(p.lineno(1), p[1])


def p_expression_constant(p):
    'expression : BUILTIN_READONLY'
    p[0] = AST.TokenNode(p.lineno(1), p[1])


def p_expression_var(p):
    'expression : IDENTIFIER'
    p[0] = AST.TokenNode(p.lineno(1), p[1])


def p_expression_function(p):
    'expression : BUILTIN_FUNCTION PARENTHESIS_OPEN parameters PARENTHESIS_CLOSE'
    p[0] = AST.FunctionNode(p.lineno(1), p[1], p[3])


precedence = (
    ('left', 'ADD_OP'),
    ('left', 'MUL_OP'),
    ('right', 'UN_OP')
)


def p_expression_op(p):
    '''expression : expression ADD_OP expression
    | expression MUL_OP expression
    | expression MOD_OP expression'''
    p[0] = AST.OpNode(p.lineno(1), p[2], [p[1], p[3]])


def p_unary_op(p):
    ''' expression : ADD_OP expression %prec UN_OP'''
    p[0] = AST.OpNode(p.lineno(1), p[1], [p[2]])


def p_expression_paren(p):
    'expression : PARENTHESIS_OPEN expression PARENTHESIS_CLOSE'
    p[0] = p[2]

# The parser exits whenever it encounters an error
def p_error(p):
    try:
        logger.error("Syntax error", p.lineno, f"Unexpected token '{p.value}'")
    except:
        # p is None => end of file reached
        logger.error("Syntax error", "EOF", "Couldn't parse program, check for missing bracket / parenthesis")
    
    sys.exit(-1)


yacc.yacc(outputdir='')


def parse(program):
    return yacc.parse(program)


if __name__ == "__main__":
    import os

    with open(sys.argv[1]) as prog:
        result = yacc.parse(prog.read(), debug=True)
        print(result)
        graph = result.makegraphicaltree()
        name = os.path.splitext(sys.argv[1])[0] + '-ast.pdf'
        graph.write_pdf(name)
        print("wrote ast to ", name)
        