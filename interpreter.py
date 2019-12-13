import AST
from AST import addToClass
from functools import reduce

from math import pi, sin, cos

import tkinter as tk

operations = {
    '+': lambda x, y: x + y,
    '-': lambda x, y: x - y,
    '*': lambda x, y: x * y,
    '/': lambda x, y: x / y,
    '%': lambda x, y: x % y,
}

comparators = {
    '>': lambda x, y: x > y,
    '<': lambda x, y: x < y,
    '>=': lambda x, y: x >= y,
    '<=': lambda x, y: x <= y,
    '==': lambda x, y: x == y,
    '!=': lambda x, y: x != y
}

vars = {}
globals = {
    "width": None,
    "height": None,
    "color": "black",
    "lineWidth": 1,
    "position": (0, 0),
    "vector": (1, 0),
    "canvas": None
}


def current_color():
    try:
        return hex(globals["color"])
    except:
        return globals["color"]


def method_width(arr):
    globals["width"] = arr[0]


def method_height(arr):
    globals["height"] = arr[0]


def method_draw(arr):
    x, y = globals["position"]
    dx, dy = globals["vector"]
    # TODO: draw circles at endpoints to avoid jagged angles
    globals["canvas"].create_line(x, y, x+dx, y+dy, fill=current_color(), width=globals["lineWidth"])
    globals["canvas"].pack()


def method_move(arr):
    globals["position"] = tuple([globals["position"][i] + globals["vector"][i] for i in [0,1]])


def method_rotate(arr):
    angle = arr[0]
    x, y = globals["vector"]

    globals["vector"] = (cos(angle) * x - sin(angle) * y,
                         sin(angle) * x + cos(angle) * y)


def method_scale(arr):
    globals["vector"] = tuple(map(lambda x: arr[0] * x, globals["vector"]))


def method_set_color(arr):
    globals["colors"] = arr[0]


def method_log(arr):
    print("[DesSine Debug] ", *arr)


def method_sin(arr):
    return sin(arr[0])


methods = {
    'width': method_width,
    'height': method_height,
    'draw': method_draw,
    'move': method_move,
    'rotate': method_rotate,
    'scale': method_scale,
    'setColor': method_set_color,
    'log': method_log,
    'sin': method_sin,
}

constants = {
    "PI": pi,
}


@addToClass(AST.ProgramNode)
def init(self):
    # Init block
    self.children[0].execute()


@addToClass(AST.ProgramNode)
def execute(self):
    # Body block
    self.children[1].execute()


@addToClass(AST.InitBlockNode)
def execute(self):
    for c in self.children:
        c.execute()

    master = tk.Tk()
    
    globals["canvas"] = tk.Canvas(
        master, width=globals["width"], height=globals["height"])
    master.geometry(f"{globals['width']}x{globals['height']}")
    globals["position"] = (globals["width"] / 2, globals["height"] / 2)



@addToClass(AST.TokenNode)
def execute(self):
    if isinstance(self.tok, str):
        try:
            return vars[self.tok]
        except KeyError:
            try:
                return constants[self.tok]
            except KeyError:
                print(f"*** Error: variable {self.tok} undefined !")
    return self.tok


@addToClass(AST.OpNode)
def execute(self):
    args = [c.execute() for c in self.children]
    if len(args) == 1:
        args.insert(0, 0)
    return reduce(operations[self.op], args)


@addToClass(AST.ComparisonNode)
def execute(self):
    args = [c.execute() for c in self.children]
    return comparators[self.operator](args[0], args[1])


@addToClass(AST.AssignNode)
def execute(self):
    vars[self.children[0].tok] = self.children[1].execute()


@addToClass(AST.WhileNode)
def execute(self):
    while self.children[0].execute():
        self.children[1].execute()


@addToClass(AST.BodyNode)
def execute(self):
    for c in self.children:
        c.execute()


@addToClass(AST.InitNode)
def execute(self):
    args = [c.execute() for c in self.children]
    methods[self.action](args)


@addToClass(AST.IfNode)
def execute(self):
    if self.children[0].execute():
        self.children[1].execute()
    else:
        if self.children[2]:
            self.children[2].execute()


@addToClass(AST.ForNode)
def execute(self):
    # init
    self.children[0].execute()
    # condition
    while self.children[1].execute():
        # body
        self.children[3].execute()
        # increment
        self.children[2].execute()


@addToClass(AST.FunctionNode)
def execute(self):
    args = [c.execute() for c in self.children]
    methods[self.action](args)


if __name__ == "__main__":
    from parser import parse
    import sys
    prog = open(sys.argv[1]).read()
    ast = parse(prog)

    # program instruction example
    # globals["canvas"].create_rectangle(50, 25, 150, 75, fill="blue")

    # Call init block & body block
    ast.init()
    ast.execute()

    # Display the result
    tk.mainloop()
