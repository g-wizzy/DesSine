import ply.yacc as yacc
import AST

from lex4 import tokens

vars = {}


def p_program(p):
    '''program : init newline statement
        | program newline statement'''
    try:
        p[0] = AST.ProgramNode(p[1], p[3])
    except:
        p[0] = AST.ProgramNode(p[1].initNode, p1.children + [p[3]])


def p_statement(p):
    '''statement : assignment
        | structure
        | drawstatement
        | movestatement
        | rotatestatement
        | ...'''
    p[0] = p[1]

def p_structure(p):
    '''structure : if
        | while'''
    p[0] = p[1]


def p_while(p):
    '''while : WHILE expression BRACKET_OPEN program BRACKET_CLOSE'''
    p[0] = AST.WhileNode([p[2], p[4]])


def p_if(p):
    '''if : IF expression BRACKET_OPEN program BRACKET_CLOSE
        | IF expression BRACKET_OPEN program BRACKET_CLOSE ELSE BRACKET_OPEN program BRACKET_CLOSE'''
    try:
        p[0] = AST.IfNode([p[2], p[4], p[8]])
    except:
        p[0] = AST.IfNode([p[2], p[4]])


def p_printexpression(p):
    'printexpression : PRINT expression'
    p[0] = AST.PrintNode(p[2])


def p_assignment(p):
    '''assignment : IDENTIFIER EQUAL expression'''
    p[0] = AST.AssignNode([AST.TokenNode(p[1]), p[3]])


def p_expression_num(p):
    'expression : NUMBER'
    p[0] = AST.TokenNode(p[1])


def p_expression_var(p):
    'expression : IDENTIFIER'
    p[0] = AST.TokenNode(p[1])


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
    'expression : PAREN_OPEN expression PAREN_CLOSE'
    p[0] = p[2]


def p_error(p):
    print(f"Syntax error in line {p.lineno}")
    yacc.errok()


yacc.yacc(outputdir='')


def parse(program):
    return yacc.parse(program)


if __name__ == "__main__":
    import sys
    import os
    with open(sys.argv[1]) as prog:
        result = yacc.parse(prog.read(), debug=False)
        print(result)
        graph = result.makegraphicaltree()
        name = os.path.splitext(sys.argv[1])[0] + '-ast.pdf'
        graph.write_pdf(name)
        print("wrote ast to ", name)
