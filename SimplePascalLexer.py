''' 
Programming Languages & Compilers Project
Author: Christos Balaktsis
AEM:    3865

File:   Lexer
'''

from ply.lex import lex
import sys

errorflag = False

reserved = {
    'program' : 'PROGRAM',
    'const' : 'CONST',
    'type' : 'TYPE',
    'array' : 'ARRAY',
    'set' : 'SET',
    'of' : 'OF',
    'record' : 'RECORD',
    'var' : 'VAR',
    'forward' : 'FORWARD',
    'function' : 'FUNCTION',
    'procedure' : 'PROCEDURE',
    'integer' : 'INTEGER',
    'real' : 'REAL',
    'boolean' : 'BOOLEAN',
    'char' : 'CHAR',
    'begin' : 'BEGIN',
    'end' : 'END',
    'if' : 'IF',
    'then' : 'THEN',
    'else' : 'ELSE',
    'while' : 'WHILE',
    'do' : 'DO',
    'for' : 'FOR',
    'downto' : 'DOWNTO',
    'to' : 'TO',
    'with' : 'WITH',
    'read' : 'READ',
    'write' : 'WRITE',
    'in' : 'INOP',
    'not' : 'NOTOP',
    'or' : 'OROP'
}

tokens = ['ID', 'ICONST', 'RCONST', 'BCONST', 'CCONST', 'RELOP',
        'ADDOP', 'STRING', 'LPAREN', 'RPAREN', 'SEMI', 'DOT', 'COMMA',
        'EQU', 'COLON', 'LBRACK', 'RBRACK', 'ASSIGN', 'DOTDOT',
        'EOF', 'LCURL', 'RCURL', 'MULDIVANDOP'] + list(reserved.values())


t_EOF = r'EOF'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_RELOP = r'>=|<=|<>|>|<'
t_ADDOP = r'\+|\-'
t_DOT = r'\.'
t_LCURL = r'{'
t_RCURL = r'}'
t_LBRACK = r'\['
t_RBRACK = r'\]'
t_SEMI = r';'
t_ASSIGN = r':='
t_DOTDOT = r'\.\.'
t_COMMA = r','
t_EQU = r'='
t_COLON = r':'

t_ignore = " \t"


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    pass

def t_ignore_COMMENT_MULTI(t):
    r'{[^}]*|\n*}'
    t.lexer.lineno += t.value.count('\n')
    pass

def t_MULDIVANDOP(t):
    r'and|div|mod|\*|\/'
    t.value = str(t.value)
    t.type = 'MULDIVANDOP'
    return t

def t_RCONST(t):
    r'([1-9][0-9]*|0)*\.(0|[0-9]*[1-9][0-9]*)((e|E)(\+|-)?[0-9]+)?|[0-9]+(e|E)(\+|-)?[0-9]+|0H([a-fA-F1-9]+[a-fA-F1-9]*)*\.[0-9]*[1-9a-fA-F][a-fA-F0-9]*|0B[1]+\.[0-1]*[1][0-1]*'
    t.value = float(t.value)
    t.type = 'RCONST'
    return t

def t_ICONST_2(t):
    r'0H[a-fA-F1-9][a-fA-F0-9]*'
    t.value = int(str(t.value)[2:], 16)
    t.type = 'ICONST'
    return t

def t_ICONST_3(t):
    r'0B1[0-1]*'
    t.value = int(str(t.value)[2:], 2)
    t.type = 'ICONST'
    return t

def t_ICONST_1(t):
    r'0|[1-9][0-9]*'
    t.value = int(t.value)
    t.type = 'ICONST'
    return t

def t_BCONST(t):
    r'TRUE|FALSE'
    t.value = bool(t.value)
    t.type = 'BCONST'
    return t

def t_CCONST(t):
    r'\'([ -~]|\\n|\\f|\\t|\\r|\\b|\\v)\''
    t.value = t.value
    t.type = 'CCONST'
    t.lexer.lineno += t.value.count('\n') 
    return t

def t_STRING(t):
    r'"([^"]|\\\\|\\"|\\n|\\t)*"'
    t.value = str(t.value[1:-1])
    t.type = 'STRING'
    t.lexer.lineno += t.value.count('\n')
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_error(t):
    global errorflag
    print("{1}: Illegal character '{0}'".format(t.value[0], t.lineno))
    t.lexer.skip(1)
    errorflag = True


errorflag = False

lexer = lex()

def g_token(lexer):
    while True :
        t = lexer.token()
        if not t:
            return
        yield t

if __name__ == '__main__':
    f = open(sys.argv[1], "r")
    lexer.input(f.read())
    for tok in g_token(lexer):
        print("(%s,%r,%d,%d)" % (tok.type, tok.value, tok.lineno, tok.lexpos))