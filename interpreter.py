import AST
from AST import addToClass
from functools import reduce
from collections import namedtuple

from math import pi, sin, cos

import tkinter as tk
import sys, logger

###########################################
# DesSine interpreter
# Made by Pierre Bürki and Loïck Jeanneret
# Last updated on 10.01.20
###########################################

operators = {
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
    '!=': lambda x, y: x != y,
}

vars = {}
default_width = 480
default_height = 360
globals = {
    "width": 0,
    "height": 0,
    "background": "white",
    "color": "black",
    "lineWidth": 1,
    "position": (0, 0),
    "vector": (1, 0),
    "canvas": None,
    "line_count": 0,
}

def check_init_block():
    if globals["width"] * globals["height"] == 0:
        logger.error("Semantic error", "0", "Missing dimension initialization")
        sys.exit(-1)

def to_hex_color(color):
    try:
        return "#" + hex(int(color))[2:].ljust(6, '0')
    except:
        return color


def method_width(arr):
    width = arr[0]
    if width <= 0:
        logger.error("Semantic error", "0 (init block)", f"Cannot set width to non-positive value {width}")
        sys.exit(-1)

    globals["width"] = width


def method_height(arr):
    height = arr[0]
    if height <= 0:
        logger.error("Semantic error", "0 (init block)", f"Cannot set height to non-positive value {height}")
        sys.exit(-1)

    globals["height"] = height


def method_background(arr):
    color = arr[0]
    if 0 <= color <= 0xFFFFFF:
        globals["background"] = arr[0]
    else:
        logger.error("Semantic error", "0 (init block)", f"Could not set color to 0x{color:06x} because it is out of bounds. Exiting.")
        sys.exit(-1)



def method_draw(arr):
    x, y = globals["position"]
    dx, dy = globals["vector"]
    lw = globals["lineWidth"]
    color = to_hex_color(globals["color"])
    globals["canvas"].create_line(x, y, x+dx, y+dy, fill=color, width=lw)

    # Draw circles at endpoints to avoid disjointed segments
    globals["canvas"].create_oval(
        x - lw / 2, y - lw / 2, x + lw / 2, y + lw / 2, fill=color, width=0)
    # globals["canvas"].create_oval(
    #     x + dx - lw / 2, y + dy - lw / 2, lw, lw, fill=color, width=0)

    globals["line_count"] += 1
    globals["canvas"].pack()


def method_move(arr):
    globals["position"] = tuple(
        [globals["position"][i] + globals["vector"][i] for i in [0, 1]])


def method_rotate(arr):
    angle = arr[0]
    x, y = globals["vector"]

    globals["vector"] = (cos(angle) * x - sin(angle) * y,
                         sin(angle) * x + cos(angle) * y)


def method_scale(arr):
    globals["vector"] = tuple(map(lambda x: arr[0] * x, globals["vector"]))
    if not method_scale.already_warned_length_zero and globals["vector"][0] == 0 and globals["vector"][1] == 0:
        logger.warning("Runtime warning", f"The vector has reached length 0 after drawing {globals['line_count']} lines.")
        method_scale.already_warned_length_zero = True

method_scale.already_warned_length_zero = False

def method_set_color(arr):
    color = arr[0]
    if 0 <= color <= 0xFFFFFF:
        globals["color"] = color
    else:
        logger.warning("Runtime warning", f"Cannot set color to 0x{color:06x}. Color is unchanged.")


def method_log(arr):
    logger.debug(arr)


def method_sin(arr):
    return sin(arr[0])


def method_set_line_width(arr):
    globals["lineWidth"] = arr[0]

Function = namedtuple("Function", ["method", "arity"])
built_ins = {
    'width': Function(method_width, 1),
    'height': Function(method_height, 1),
    'background': Function(method_background, 1),
    'draw': Function(method_draw, 0),
    'move': Function(method_move, 0),
    'rotate': Function(method_rotate, 1),
    'scale': Function(method_scale, 1),
    'setColor': Function(method_set_color, 1),
    'log': Function(method_log, -1),
    'sin': Function(method_sin, 1),
    'setLineWidth': Function(method_set_line_width, 1),
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

    w = globals["width"]
    h = globals["height"]

    globals["canvas"] = tk.Canvas(master, width=w, height=h)

    master.geometry(f"{w}x{h}")
    globals["canvas"].config(bg=to_hex_color(globals["background"]))

    globals["position"] = (w / 2, h / 2)


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
    return reduce(operators[self.op], args)


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
    elif len(self.children) > 2:
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
    func = built_ins[self.action]
    if len(args) == func.arity or func.arity == -1:
        return func.method(args)
    logger.error("Semantic error", self.lineno, f"Bad number of arguments in {self.action} call.")


if __name__ == "__main__":
    from dessine_parser import parse
    import logger
    prog = open(sys.argv[1]).read()
    ast = parse(prog)

    ast.init()
    check_init_block()
    ast.execute()

    # Display the result
    logger.info("DesSine", f"Starting render of {globals['line_count']} lines.")

    tk.mainloop()
