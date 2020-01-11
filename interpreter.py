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
# Last updated on 11.01.20
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

scopes = [{}]
Routine = namedtuple("Routine", ["params", "blockNode"])
routines = {}

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
    """
    Checks if the dimensions have been set during the initialization.
    """
    if globals["width"] * globals["height"] == 0:
        logger.error("Semantic error", "0", "Missing dimension initialization")
        sys.exit(-1)


def to_hex_color(color):
    """
    Formats the given color (integer between 0 and 0xFFFFFF) into TKinter compliant string
    """
    try:
        return "#" + hex(int(color))[2:].ljust(6, '0')
    except:
        return color


def method_width(arr):
    """
    Init function that sets the width of the window
    """
    width = arr[0]
    if width <= 0:
        logger.error("Semantic error", "0 (init block)", f"Cannot set width to non-positive value {width}")
        sys.exit(-1)

    globals["width"] = width


def method_height(arr):
    """
    Init function that sets the height of the window
    """
    height = arr[0]
    if height <= 0:
        logger.error("Semantic error", "0 (init block)", f"Cannot set height to non-positive value {height}")
        sys.exit(-1)

    globals["height"] = height


def method_background(arr):
    """
    Init function that sets the background color of the window
    """
    color = arr[0]
    if 0 <= color <= 0xFFFFFF:
        globals["background"] = arr[0]
    else:
        logger.error("Semantic error", "0 (init block)", f"Could not set color to 0x{color:06x} because it is out of bounds. Exiting.")
        sys.exit(-1)


def method_draw(arr):
    """
    Draws a line between the current position along the current vector (but does not move the current point)
    """
    x, y = globals["position"]
    dx, dy = globals["vector"]
    lw = globals["lineWidth"]
    color = to_hex_color(globals["color"])
    globals["canvas"].create_line(x, y, x+dx, y+dy, fill=color, width=lw)

    # Draw circles at endpoints to avoid disjointed segments
    if lw > 3:
        globals["canvas"].create_oval(
            x - lw / 2, y - lw / 2, x + lw / 2, y + lw / 2, fill=color, width=0)
        globals["canvas"].create_oval(
            x + dx - lw / 2, y + dy - lw / 2, x + dx + lw / 2, y + dy + lw / 2, fill=color, width=0)

    globals["line_count"] += 1
    globals["canvas"].pack()


def method_move(arr):
    """
    Move the current point along the current vector
    """
    globals["position"] = tuple(
        [globals["position"][i] + globals["vector"][i] for i in [0, 1]])


def method_rotate(arr):
    """
    Rotate the current vector
    """
    angle = arr[0]
    x, y = globals["vector"]

    globals["vector"] = (cos(angle) * x + sin(angle) * y,
                         - sin(angle) * x + cos(angle) * y)


def method_scale(arr):
    """
    Scale the current vector
    """
    globals["vector"] = tuple(map(lambda x: arr[0] * x, globals["vector"]))
    if not method_scale.already_warned_length_zero and globals["vector"][0] == 0 and globals["vector"][1] == 0:
        logger.warning("Runtime warning", f"The vector has reached length 0 after drawing {globals['line_count']} lines.")
        method_scale.already_warned_length_zero = True

method_scale.already_warned_length_zero = False


def method_set_color(arr):
    """
    Set the color of the lines
    """
    color = arr[0]
    if 0 <= color <= 0xFFFFFF:
        globals["color"] = color
    else:
        logger.warning("Runtime warning", f"Cannot set color to 0x{color:06x}. Color is unchanged.")


def method_log(arr):
    """
    Log the given variables
    """
    logger.debug(arr)


def method_sin(arr):
    """
    Sinus, accepts radians
    """
    return sin(arr[0])


def method_set_line_width(arr):
    """
    Set the line's width in pixels
    """
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

    # Create tkinter instance, canvas et set width/height
    master = tk.Tk()

    w = globals["width"]
    h = globals["height"]

    globals["canvas"] = tk.Canvas(master, width=w, height=h)

    master.geometry(f"{w}x{h}")
    globals["canvas"].config(bg=to_hex_color(globals["background"]))

    # Starting point is at the center of the screen
    globals["position"] = (w / 2, h / 2)


@addToClass(AST.BlockNode)
def execute(self):
    # Scope is a list, with push/pop it when we change scope
    scopes.append({})
    for c in self.children:
        c.execute()
    scopes.pop()


@addToClass(AST.RoutineDefinitionNode)
def execute(self):
    # Defining routines
    routines[self.name] = Routine(self.params, self.block)


@addToClass(AST.RoutineCallNode)
def execute(self):
    # Check routine validity before callling them
    # Name
    if self.name not in routines.keys():
        logger.error("Semantic error", self.lineno, f"No function with name '{self.name}' exists.")
        sys.exit(-1)
    
    routine = routines[self.name]
    
    # Args length
    if len(routine.params) != len(self.children):
        logger.error("Semantic error", self.lineno, f"Bad number of arguments in '{self.name}' call.")
        sys.exit(-1)

    # Execute parameters
    args = [c.execute() for c in self.children]

    # New scope for the function
    scopes.append({})

    # Set parameters values in the function scope (parameters are converted to "variables")
    for param, value in zip(routine.params, args):
        scopes[-1][param] = value
    
    routine.blockNode.execute()

    # Exit function scope
    scopes.pop()


@addToClass(AST.TokenNode)
def execute(self):
    if isinstance(self.tok, str):
        # Is the token a constant?
        if self.tok in constants:
            return constants[self.tok]

        # We can access variables from parent scopes so we have to check each scope to find
        # if a variable is defined or not
        for scope in scopes[-1::-1]:
            if self.tok in scope.keys():
                return scope[self.tok]
        logger.error("Semantic error", self.lineno, f"Variable '{self.tok}' is not defined.")
        sys.exit(-1)

    return self.tok


@addToClass(AST.OpNode)
def execute(self):
    args = [c.execute() for c in self.children]

    # Handle unary operator
    if len(args) == 1:
        args.insert(0, 0)

    # Prevent dividing by 0
    if self.op == '/' and args[1] == 0:
        logger.error("Semantic error", self.lineno, "Division by zero.")
        sys.exit(-1)

    return reduce(operators[self.op], args)


@addToClass(AST.ComparisonNode)
def execute(self):
    args = [c.execute() for c in self.children]
    return comparators[self.operator](args[0], args[1])


@addToClass(AST.AssignNode)
def execute(self):
    identifier = self.children[0].tok
    value = self.children[1].execute()

    # When assigning a variable, we need to check if it does not exists in a parent scope
    # If it does, we change it in the parent scope
    for scope in scopes[-1::-1]:
        if identifier in scope.keys():
            scope[identifier] = value
            return

    # If it does not exists, we declare it in the current scope
    scopes[-1][identifier] = value


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
    func = built_ins[self.action]

    # Check valid number of args
    if len(args) == func.arity or func.arity == -1:
        return func.method(args)

    logger.error("Semantic error", self.lineno, f"Bad number of arguments in {self.action} call.")
    sys.exit(-1)


@addToClass(AST.IfNode)
def execute(self):
    # if "or" if ... else
    if self.children[0].execute():
        self.children[1].execute()
    elif len(self.children) > 2:
        self.children[2].execute()


@addToClass(AST.ForNode)
def execute(self):
    # Init
    self.children[0].execute()
    # Condition
    while self.children[1].execute():
        # Body
        self.children[3].execute()
        # Increment
        self.children[2].execute()


@addToClass(AST.FunctionNode)
def execute(self):
    args = [c.execute() for c in self.children]
    func = built_ins[self.action]

    # Check valid number of args
    if len(args) == func.arity or func.arity == -1:
        return func.method(args)
    logger.error("Semantic error", self.lineno, f"Bad number of arguments in '{self.action}' call.")
    sys.exit(-1)


if __name__ == "__main__":
    from dessine_parser import parse
    prog = open(sys.argv[1]).read()
    ast = parse(prog)

    ast.init()
    check_init_block()
    ast.execute()

    # Display the result
    logger.info("DesSine", f"Starting render of {globals['line_count']} lines.")

    tk.mainloop()
