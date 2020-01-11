import pydot

###########################################
# DesSine AST
# Made by Pierre Bürki and Loïck Jeanneret
# Last updated on 11.01.20
###########################################


class Node:
    """
    Same as the file used in all the course's exercises,
    with the added field of the line number
    """
    count = 0
    type = 'Node (unspecified)'
    shape = 'ellipse'

    def __init__(self, lineno, children=None):
        self.ID = str(Node.count)
        self.lineno = lineno

        Node.count += 1

        if not children:
            self.children = []
        elif hasattr(children, '__len__'):
            self.children = children
        else:
            self.children = [children]

        self.next = []

    def addNext(self, next):
        self.next.append(next)

    def asciitree(self, prefix=''):
        result = "%s%s\n" % (prefix, repr(self))
        prefix += '|  '

        for c in self.children:
            if not isinstance(c, Node):
                result += "%s*** Error: Child of type %r: %r\n" % (
                    prefix, type(c), c)
                continue
            result += c.asciitree(prefix)
        return result

    def __str__(self):
        return self.asciitree()

    def __repr__(self):
        return self.type

    def makegraphicaltree(self, dot=None, edgeLabels=True):
        if not dot:
            dot = pydot.Dot()

        dot.add_node(pydot.Node(self.ID, label=repr(self), shape=self.shape))
        label = edgeLabels and len(self.children)-1

        for i, c in enumerate(self.children):
            c.makegraphicaltree(dot, edgeLabels)
            edge = pydot.Edge(self.ID, c.ID)
            if label:
                edge.set_label(str(i))
            dot.add_edge(edge)
            # Workaround for a bug in pydot 1.0.2 on Windows:
            #dot.set_graphviz_executables({'dot': r'C:\Program Files\Graphviz2.38\bin\dot.exe'})
        return dot


class ProgramNode(Node):
    """
    Root of the syntaxic tree.
    Has two children : the init block and the body
    """
    type = 'Program'


class BodyNode(Node):
    """
    Node whose children are a succession of statements
    """
    type = 'Body'

class BlockNode(Node):
    """
    Node representing a body surrounded by brackets, changes scope
    """
    type = 'Block'

class InitBlockNode(Node):
    """
    Block whose children are a succession of InitNode, it must exist once at the start of the program
    """
    type = 'InitBlock'


class InitNode(Node):
    """
    Child of the InitBlockNode. Each one comprises of a call to an init function.
    """
    type = "Init"

    def __init__(self, lineno, action, children):
        Node.__init__(self, lineno, children)
        self.action = action

    def __repr__(self):
        return self.action


class RoutineDefinitionNode(Node):
    type = 'Routine Definition'

    def __init__(self, lineno, name, params, block):
        Node.__init__(self, lineno)
        self.name = name
        self.params = list(map(lambda tokenNode: tokenNode.tok, params))
        self.block = block
    
    def __repr__(self):
        return f"{self.name}({self.params})"


class RoutineCallNode(Node):
    type = 'Routine Call'

    def __init__(self, lineno, name, params):
        Node.__init__(self, lineno, params)
        self.name = name


class ComparisonNode(Node):
    """
    Node that will yields true / false when evaluated
    """
    type = 'Comparison'

    def __init__(self, lineno, operator, children):
        Node.__init__(self, lineno, children)
        self.operator = operator

    def __repr__(self):
        return self.operator


class TokenNode(Node):
    type = 'token'

    def __init__(self, lineno, tok):
        Node.__init__(self, lineno)
        self.tok = tok
        self.assign = False

    def __repr__(self):
        return repr(self.tok)


class OpNode(Node):
    def __init__(self, lineno, op, children):
        Node.__init__(self, lineno, children)
        self.op = op
        try:
            self.nbargs = len(children)
        except AttributeError:
            self.nbargs = 1

    def __repr__(self):
        return "%s (%s)" % (self.op, self.nbargs)


class AssignNode(Node):
    type = '='


class IfNode(Node):
    type = 'if'


class WhileNode(Node):
    type = 'while'


class ForNode(Node):
    type = 'for'


class FunctionNode(Node):
    type = 'Function'

    def __init__(self, lineno, action, arguments):
        Node.__init__(self, lineno, arguments)
        self.action = action

    def __repr__(self):
        return self.action


class EntryNode(Node):
    type = 'ENTRY'

    def __init__(self, lineno):
        Node.__init__(self, lineno, None)


def addToClass(cls):
    '''
    Copied from the decorator used in the course's exercises

    Add decorated function to class.
    Dirty POO polyfill for python.
    Decorated method is still saved in the initial namespace
    '''
    def decorator(func):
        setattr(cls, func.__name__, func)
        return func
    return decorator
