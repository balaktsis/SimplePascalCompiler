''' 
Programming Languages & Compilers Project
Author: Christos Balaktsis
AEM:    3865

File:   Parser
'''

import ply.yacc as yacc
import SPLexer
from SPASTBuilder import build_tree 
from SPLexer import tokens
from SPLexer import lex

import sys
import logging

precedence = (
	('nonassoc', 'INOP', 'RELOP', 'EQU'),
  	('left', 'ADDOP', 'OROP'),
    ('left', 'MULDIVANDOP'),
    ('right', 'NOTOP'),  
	('left', 'DOT','RBRACK','LBRACK','LPAREN','RPAREN'),
	('right', 'ELSE')
)


def p_program(p):
	'''
	program : header declarations subprograms comp_statement DOT 
	'''
	p[0] = (p[1], p[2], p[3], p[4], p[5])

def p_header(p):
	'''
	header : PROGRAM ID SEMI 
	'''
	p[0] = (p[1], p[2], p[3])

def p_declarations(p):
	'''
	declarations : constdefs typedefs vardefs 
	'''
	p[0] = (p[1], p[2], p[3])

def p_constdefs(p):
	'''
	constdefs : CONST constant_defs SEMI 
	'''
	p[0] = (p[1], p[2], p[3])

def p_constdefs_1(p):
	'''
	constdefs :   
	'''
	p[0] = None

def p_constant_defs(p):
	'''
	constant_defs : constant_defs SEMI ID EQU expression 
	'''
	p[0] = (p[1], p[2], p[3], p[4], p[5])

def p_constant_defs_1(p):
	'''
	constant_defs : ID EQU expression 
	'''
	p[0] = (p[1], p[2], p[3])

def p_expression(p):
	'''
	expression : expression RELOP expression 
	'''
	p[0] = (p[2], p[1], p[3])

def p_expression_1(p):
	'''
	expression : expression EQU expression 
	'''
	p[0] = (p[2], p[1], p[3])

def p_expression_2(p):
	'''
	expression : expression INOP expression 
	'''
	p[0] = (p[2], p[1], p[3])

def p_expression_3(p):
	'''
	expression : expression OROP expression 
	'''
	p[0] = (p[2], p[1], p[3])

def p_expression_4(p):
	'''
	expression : expression ADDOP expression 
	'''
	p[0] = (p[2], p[1], p[3])

def p_expression_5(p):
	'''
	expression : expression MULDIVANDOP expression 
	'''
	p[0] = (p[2], p[1], p[3])

def p_expression_6(p):
	'''
	expression : ADDOP expression 
	'''
	p[0] = (p[1], p[2])

def p_expression_7(p):
	'''
	expression : NOTOP expression 
	'''
	p[0] = (p[1], p[2])

def p_expression_8(p):
	'''
	expression : variable 
	'''
	p[0] = (p[1])

def p_expression_9(p):
	'''
	expression : ID LPAREN expressions RPAREN 
	'''
	p[0] = (p[1], p[2], p[3], p[4])

def p_expression_10(p):
	'''
	expression : constant 
	'''
	p[0] = (p[1])

def p_expression_11(p):
	'''
	expression : LPAREN expression RPAREN 
	'''
	p[0] = (p[1], p[2], p[3])

def p_expression_12(p):
	'''
	expression : setexpression 
	'''
	p[0] = (p[1])

def p_variable(p):
	'''
	variable : ID 
	'''
	p[0] = (p[1])

def p_variable_1(p):
	'''
	variable : variable DOT ID 
	'''
	p[0] = (p[1], p[2], p[3])

def p_variable_2(p):
	'''
	variable : variable LBRACK expressions RBRACK 
	'''
	p[0] = (p[1], p[2], p[3], p[4])

def p_expressions(p):
	'''
	expressions : expressions COMMA expression 
	'''
	p[0] = (p[2], p[1], p[3])

def p_expressions_1(p):
	'''
	expressions : expression 
	'''
	p[0] = (p[1])

def p_constant(p):
	'''
	constant : ICONST 
	'''
	p[0] = (p[1])

def p_constant_1(p):
	'''
	constant : RCONST 
	'''
	p[0] = (p[1])

def p_constant_2(p):
	'''
	constant : BCONST 
	'''
	p[0] = (p[1])

def p_constant_3(p):
	'''
	constant : CCONST 
	'''
	p[0] = (p[1])

def p_setexpression(p):
	'''
	setexpression : LBRACK elexpressions RBRACK 
	'''
	p[0] = (p[1], p[2], p[3])

def p_setexpression_1(p):
	'''
	setexpression : LBRACK RBRACK 
	'''
	p[0] = (p[1], p[2])

def p_elexpressions(p):
	'''
	elexpressions : elexpressions COMMA elexpression 
	'''
	p[0] = (p[2], p[1], p[3])

def p_elexpressions_1(p):
	'''
	elexpressions : elexpression 
	'''
	p[0] = (p[1])

def p_elexpression(p):
	'''
	elexpression : expression DOTDOT expression 
	'''
	p[0] = (p[2], p[1], p[3])

def p_elexpression_1(p):
	'''
	elexpression : expression 
	'''
	p[0] = (p[1])

def p_typedefs(p):
	'''
	typedefs : TYPE type_defs SEMI 
	'''
	p[0] = (p[1], p[2], p[3])

def p_typedefs_1(p):
	'''
	typedefs :   
	'''
	p[0] = None

def p_type_defs(p):
	'''
	type_defs : type_defs SEMI ID EQU type_def 
	'''
	p[0] = (p[1], p[2], p[3], p[4], p[5])

def p_type_defs_1(p):
	'''
	type_defs : ID EQU type_def 
	'''
	p[0] = (p[1], p[2], p[3])

def p_type_def(p):
	'''
	type_def : ARRAY LBRACK dims RBRACK OF typename 
	'''
	p[0] = (p[1], p[2], p[3], p[4], p[5], p[6])

def p_type_def_1(p):
	'''
	type_def : SET OF typename 
	'''
	p[0] = (p[1], p[2], p[3])

def p_type_def_2(p):
	'''
	type_def : RECORD fields END 
	'''
	p[0] = (p[1], p[2], p[3])

def p_type_def_3(p):
	'''
	type_def : LPAREN identifiers RPAREN 
	'''
	p[0] = (p[1], p[2], p[3])

def p_type_def_4(p):
	'''
	type_def : limit DOTDOT limit 
	'''
	p[0] = (p[2], p[1], p[3])

def p_dims(p):
	'''
	dims : dims COMMA limits 
	'''
	p[0] = (p[2], p[1], p[3])

def p_dims_1(p):
	'''
	dims : limits 
	'''
	p[0] = (p[1])

def p_limits(p):
	'''
	limits : limit DOTDOT limit 
	'''
	p[0] = (p[2], p[1], p[3])

def p_limits_1(p):
	'''
	limits : ID 
	'''
	p[0] = (p[1])

def p_limit(p):
	'''
	limit : ADDOP ICONST 
	'''
	p[0] = (p[1], p[2])

def p_limit_1(p):
	'''
	limit : ADDOP ID 
	'''
	p[0] = (p[1], p[2])

def p_limit_2(p):
	'''
	limit : ICONST 
	'''
	p[0] = (p[1])

def p_limit_3(p):
	'''
	limit : CCONST 
	'''
	p[0] = (p[1])

def p_limit_4(p):
	'''
	limit : BCONST 
	'''
	p[0] = (p[1])

def p_limit_5(p):
	'''
	limit : ID 
	'''
	p[0] = (p[1])

def p_typename(p):
	'''
	typename : standard_type 
	'''
	p[0] = (p[1])

def p_typename_1(p):
	'''
	typename : ID 
	'''
	p[0] = (p[1])

def p_standard_type(p):
	'''
	standard_type : INTEGER 
	'''
	p[0] = (p[1])

def p_standard_type_1(p):
	'''
	standard_type : REAL 
	'''
	p[0] = (p[1])

def p_standard_type_2(p):
	'''
	standard_type : BOOLEAN 
	'''
	p[0] = (p[1])

def p_standard_type_3(p):
	'''
	standard_type : CHAR 
	'''
	p[0] = (p[1])

def p_fields(p):
	'''
	fields : fields SEMI field 
	'''
	p[0] = (p[1], p[2], p[3])

def p_fields_1(p):
	'''
	fields : field 
	'''
	p[0] = (p[1])

def p_field(p):
	'''
	field : identifiers COLON typename 
	'''
	p[0] = (p[1], p[2], p[3])

def p_identifiers(p):
	'''
	identifiers : identifiers COMMA ID 
	'''
	p[0] = (p[1], p[2], p[3])

def p_identifiers_1(p):
	'''
	identifiers : ID 
	'''
	p[0] = (p[1])

def p_vardefs(p):
	'''
	vardefs : VAR variable_defs SEMI 
	'''
	p[0] = (p[1], p[2], p[3])

def p_vardefs_1(p):
	'''
	vardefs :   
	'''
	p[0] = None

def p_variable_defs(p):
	'''
	variable_defs : variable_defs SEMI identifiers COLON typename 
	'''
	p[0] = (p[1], p[2], p[3], p[4], p[5])

def p_variable_defs_1(p):
	'''
	variable_defs : identifiers COLON typename 
	'''
	p[0] = (p[1], p[2], p[3])

def p_subprograms(p):
	'''
	subprograms : subprograms subprogram SEMI 
	'''
	p[0] = (p[1], p[2], p[3])

def p_subprograms_1(p):
	'''
	subprograms :   
	'''
	p[0] = None

def p_subprogram(p):
	'''
	subprogram : sub_header SEMI FORWARD 
	'''
	p[0] = (p[1], p[2], p[3])

def p_subprogram_1(p):
	'''
	subprogram : sub_header SEMI declarations subprograms comp_statement 
	'''
	p[0] = (p[1], p[2], p[3], p[4], p[5])

def p_sub_header(p):
	'''
	sub_header : FUNCTION ID formal_parameters COLON standard_type 
	'''
	p[0] = (p[1], p[2], p[3], p[4], p[5])

def p_sub_header_1(p):
	'''
	sub_header : PROCEDURE ID formal_parameters 
	'''
	p[0] = (p[1], p[2], p[3])

def p_sub_header_2(p):
	'''
	sub_header : FUNCTION ID 
	'''
	p[0] = (p[1], p[2])

def p_formal_parameters(p):
	'''
	formal_parameters : LPAREN parameter_list RPAREN 
	'''
	p[0] = (p[1], p[2], p[3])

def p_formal_parameters_1(p):
	'''
	formal_parameters :   
	'''
	p[0] = None

def p_parameter_list(p):
	'''
	parameter_list : parameter_list SEMI pass identifiers COLON typename 
	'''
	p[0] = (p[1], p[2], p[3], p[4], p[5], p[6])

def p_parameter_list_1(p):
	'''
	parameter_list : pass identifiers COLON typename 
	'''
	p[0] = (p[1], p[2], p[3], p[4])

def p_pass(p):
	'''
	pass : VAR 
	'''
	p[0] = (p[1])

def p_pass_1(p):
	'''
	pass :   
	'''
	p[0] = None

def p_comp_statement(p):
	'''
	comp_statement : BEGIN statements END 
	'''
	p[0] = (p[1], p[2], p[3])

def p_statements(p):
	'''
	statements : statements SEMI statement 
	'''
	p[0] = (p[1], p[2], p[3])

def p_statements_1(p):
	'''
	statements : statement 
	'''
	p[0] = (p[1])

def p_statement(p):
	'''
	statement : assignment 
	'''
	p[0] = (p[1])

def p_statement_1(p):
	'''
	statement : if_statement 
	'''
	p[0] = (p[1])

def p_statement_2(p):
	'''
	statement : while_statement 
	'''
	p[0] = (p[1])

def p_statement_3(p):
	'''
	statement : for_statement 
	'''
	p[0] = (p[1])

def p_statement_4(p):
	'''
	statement : with_statement 
	'''
	p[0] = (p[1])

def p_statement_5(p):
	'''
	statement : subprogram_call 
	'''
	p[0] = (p[1])

def p_statement_6(p):
	'''
	statement : io_statement 
	'''
	p[0] = (p[1])

def p_statement_7(p):
	'''
	statement : comp_statement 
	'''
	p[0] = (p[1])

def p_statement_8(p):
	'''
	statement :   
	'''
	p[0] = None

def p_assignment(p):
	'''
	assignment : variable ASSIGN expression 
	'''
	p[0] = (p[2], p[1], p[3])

def p_assignment_1(p):
	'''
	assignment : variable ASSIGN STRING 
	'''
	p[0] = (p[2], p[1], p[3])

def p_if_statement(p):
	'''
	if_statement : IF expression THEN statement if_tail 
	'''
	p[0] = (p[1], p[2], p[3], p[4], p[5])

def p_if_tail(p):
	'''
	if_tail : ELSE statement 
	'''
	p[0] = (p[1], p[2])

def p_if_tail_1(p):
	'''
	if_tail : %prec ELSE
	'''
	p[0] = None

def p_while_statement(p):
	'''
	while_statement : WHILE expression DO statement 
	'''
	p[0] = (p[1], p[2], p[3], p[4])

def p_for_statement(p):
	'''
	for_statement : FOR ID ASSIGN iter_space DO statement 
	'''
	p[0] = (p[1], p[2], p[3], p[4], p[5], p[6])

def p_iter_space(p):
	'''
	iter_space : expression TO expression 
	'''
	p[0] = (p[2], p[1], p[3])

def p_iter_space_1(p):
	'''
	iter_space : expression DOWNTO expression 
	'''
	p[0] = (p[2], p[1], p[3])

def p_with_statement(p):
	'''
	with_statement : WITH variable DO statement 
	'''
	p[0] = (p[1], p[2], p[3], p[4])

def p_subprogram_call(p):
	'''
	subprogram_call : ID 
	'''
	p[0] = (p[1])

def p_subprogram_call_1(p):
	'''
	subprogram_call : ID LPAREN expressions RPAREN 
	'''
	p[0] = (p[1], p[2], p[3], p[4])

def p_io_statement(p):
	'''
	io_statement : READ LPAREN read_list RPAREN 
	'''
	p[0] = (p[1], p[2], p[3], p[4])

def p_io_statement_1(p):
	'''
	io_statement : WRITE LPAREN write_list RPAREN 
	'''
	p[0] = (p[1], p[2], p[3], p[4])

def p_read_list(p):
	'''
	read_list : read_list COMMA read_item 
	'''
	p[0] = (p[1], p[2], p[3])

def p_read_list_1(p):
	'''
	read_list : read_item 
	'''
	p[0] = (p[1])

def p_read_item(p):
	'''
	read_item : variable 
	'''
	p[0] = (p[1])

def p_write_list(p):
	'''
	write_list : write_list COMMA write_item 
	'''
	p[0] = (p[1], p[2], p[3])

def p_write_list_1(p):
	'''
	write_list : write_item 
	'''
	p[0] = (p[1])

def p_write_item(p):
	'''
	write_item : expression 
	'''
	p[0] = (p[1])

def p_write_item_1(p):
	'''
	write_item : STRING 
	'''
	p[0] = (p[1])


def p_error(p):
    if p is None:
        signal_error("Unexpected end-of-file", 'end')
    else:
        signal_error("Unexpected token '{0}'".format(p.value), p.lineno)


def signal_error(string, lineno):
    print(string + "found on line #" + str(lineno))
    SPLexer.errorFlag = True


parser = yacc.yacc()

inputFile = open(sys.argv[1], "r")
logging.basicConfig(level=logging.CRITICAL)
log = logging.getLogger()
ast = parser.parse(inputFile.read(), lexer=lex(module=SPLexer), debug=log)

if parser.errorok:
	print("AST (multi-line):")
	print(build_tree(ast))
	print("\nAST (single-line):")
	print(ast)
	print("\nParsing completed successfully!\n")
else:
	print("Parsing failed!")
