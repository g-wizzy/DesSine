import pydot


class Node:
    count = 0
    type = 'Node (unspecified)'
    shape = 'ellipse'

    def __init__(self, children=None):
        self.ID = str(Node.count)

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
    type = 'Program'

    def __init__(self, initNode, children):
        Node.__init__(self, children)
        self.initNode = initNode


class BodyNode(Node):
    type = 'Body'


class InitBlockNode(Node):
    type = 'InitBlock'


class ComparisonNode(Node):
    type = 'Comparison'

    def __init__(self, operator, children):
        Node.__init__(self, children)
        self.operator = operator

    def __repr__(self):
        return self.operator


class InitNode(Node):
    type = "Init"

    def __init__(self, action, children):
        Node.__init__(self, children)
        self.action = action


class TokenNode(Node):
    type = 'token'

    def __init__(self, tok):
        Node.__init__(self)
        self.tok = tok
        self.assign = False

    def __repr__(self):
        return repr(self.tok)


class OpNode(Node):
    def __init__(self, op, children):
        Node.__init__(self, children)
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
    type = 'For'


class FunctionNode(Node):
    type = 'Action'

    def __init__(self, action, arguments):
        Node.__init__(self, arguments)
        self.action = action
    
    def __repr__(self):
        return self.action


class EntryNode(Node):
    type = 'ENTRY'

    def __init__(self):
        Node.__init__(self, None)


def addToClass(cls):
    ''' Add decorated function to class. Dirty POO polyfill for python. Decorated method is still saved in the initial namespace'''
    def decorator(func):
        setattr(cls, func.__name__, func)
        return func
    return decorator
