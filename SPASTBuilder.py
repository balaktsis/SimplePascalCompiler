''' 
Programming Languages & Compilers Project
Author: Christos Balaktsis
AEM:    3865

File:   Abstract Systax Tree (AST) Builder
'''

# The following code belongs to user Peilonrayz [CC BY-SA 4.0]
# (https://codereview.stackexchange.com/users/42401/peilonrayz)
# and was found on https://codereview.stackexchange.com/a/238106.
# It is used to format the AST output of ply.yacc as a tree.

def build_tree(root):
    return '\n'.join(_build_tree(root))


def _build_tree(node):
    if not isinstance(node, tuple):
        yield str(node)
        return

    values = [_build_tree(n) for n in node]
    if len(values) == 1:
        yield from build_lines('──', '  ', values[0])
        return

    start, *mid, end = values
    yield from build_lines('┬─', '│ ', start)
    for value in mid:
        yield from build_lines('├─', '│ ', value)
    yield from build_lines('└─', '  ', end)


def build_lines(first, other, values):
    yield first + next(values)
    for value in values:
        yield other + value
