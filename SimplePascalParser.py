from ply.yacc import yacc
import SimplePascalLexer
from SimplePascalLexer import tokens
from SimplePascalLexer import lex

import ast

import sys
import logging

precedence = (
    ('left', 'DOT'),
    ('left', 'RBRACK'),
    ('left', 'LBRACK'),
    ('left', 'RPAREN'),
    ('left', 'LPAREN'),
    ('right', 'NOTOP'),
    ('left', 'MULDIVANDOP'),
    ('left', 'ADDOP', 'OROP')
)

def p_program(p):
	'''
	program : header declarations subprograms comp_statement DOT 
	'''
	pass

def p_header(p):
	'''
	header : PROGRAM ID SEMI 
	'''
	pass

def p_declarations(p):
	'''
	declarations : constdefs typedefs vardefs 
	'''
	pass

def p_constdefs(p):
	'''
	constdefs : CONST constant_defs SEMI 
	'''
	pass

def p_constdefs_1(p):
	'''
	constdefs :   
	'''
	pass

def p_constant_defs(p):
	'''
	constant_defs : constant_defs SEMI ID EQU expression 
	'''
	pass

def p_constant_defs_1(p):
	'''
	constant_defs : ID EQU expression 
	'''
	pass

def p_expression(p):
	'''
	expression : expression RELOP expression 
	'''
	pass

def p_expression_1(p):
	'''
	expression : expression EQU expression 
	'''
	pass

def p_expression_2(p):
	'''
	expression : expression INOP expression 
	'''
	pass

def p_expression_3(p):
	'''
	expression : expression OROP expression 
	'''
	pass

def p_expression_4(p):
	'''
	expression : expression ADDOP expression 
	'''
	pass

def p_expression_5(p):
	'''
	expression : expression MULDIVANDOP expression 
	'''
	pass

def p_expression_6(p):
	'''
	expression : ADDOP expression 
	'''
	pass

def p_expression_7(p):
	'''
	expression : NOTOP expression 
	'''
	pass

def p_expression_8(p):
	'''
	expression : variable 
	'''
	pass

def p_expression_9(p):
	'''
	expression : ID LPAREN expressions RPAREN 
	'''
	pass

def p_expression_10(p):
	'''
	expression : constant 
	'''
	pass

def p_expression_11(p):
	'''
	expression : LPAREN expression RPAREN 
	'''
	pass

def p_expression_12(p):
	'''
	expression : setexpression 
	'''
	pass

def p_variable(p):
	'''
	variable : ID 
	'''
	pass

def p_variable_1(p):
	'''
	variable : variable DOT ID 
	'''
	pass

def p_variable_2(p):
	'''
	variable : variable LBRACK expressions RBRACK 
	'''
	pass

def p_expressions(p):
	'''
	expressions : expressions COMMA expression 
	'''
	pass

def p_expressions_1(p):
	'''
	expressions : expression 
	'''
	pass

def p_constant(p):
	'''
	constant : ICONST 
	'''
	pass

def p_constant_1(p):
	'''
	constant : RCONST 
	'''
	pass

def p_constant_2(p):
	'''
	constant : BCONST 
	'''
	pass

def p_constant_3(p):
	'''
	constant : CCONST 
	'''
	pass

def p_setexpression(p):
	'''
	setexpression : LBRACK elexpressions RBRACK 
	'''
	pass

def p_setexpression_1(p):
	'''
	setexpression : LBRACK RBRACK 
	'''
	pass

def p_elexpressions(p):
	'''
	elexpressions : elexpressions COMMA elexpression 
	'''
	pass

def p_elexpressions_1(p):
	'''
	elexpressions : elexpression 
	'''
	pass

def p_elexpression(p):
	'''
	elexpression : expression DOTDOT expression 
	'''
	pass

def p_elexpression_1(p):
	'''
	elexpression : expression 
	'''
	pass

def p_typedefs(p):
	'''
	typedefs : TYPE type_defs SEMI 
	'''
	pass

def p_typedefs_1(p):
	'''
	typedefs :   
	'''
	pass

def p_type_defs(p):
	'''
	type_defs : type_defs SEMI ID EQU type_def 
	'''
	pass

def p_type_defs_1(p):
	'''
	type_defs : ID EQU type_def 
	'''
	pass

def p_type_def(p):
	'''
	type_def : ARRAY LBRACK dims RBRACK OF typename 
	'''
	pass

def p_type_def_1(p):
	'''
	type_def : SET OF typename 
	'''
	pass

def p_type_def_2(p):
	'''
	type_def : RECORD fields END 
	'''
	pass

def p_type_def_3(p):
	'''
	type_def : LPAREN identifiers RPAREN 
	'''
	pass

def p_type_def_4(p):
	'''
	type_def : limit DOTDOT limit 
	'''
	pass

def p_dims(p):
	'''
	dims : dims COMMA limits 
	'''
	pass

def p_dims_1(p):
	'''
	dims : limits 
	'''
	pass

def p_limits(p):
	'''
	limits : limit DOTDOT limit 
	'''
	pass

def p_limits_1(p):
	'''
	limits : ID 
	'''
	pass

def p_limit(p):
	'''
	limit : ADDOP ICONST 
	'''
	pass

def p_limit_1(p):
	'''
	limit : ADDOP ID 
	'''
	pass

def p_limit_2(p):
	'''
	limit : ICONST 
	'''
	pass

def p_limit_3(p):
	'''
	limit : CCONST 
	'''
	pass

def p_limit_4(p):
	'''
	limit : BCONST 
	'''
	pass

def p_limit_5(p):
	'''
	limit : ID 
	'''
	pass

def p_typename(p):
	'''
	typename : standard_type 
	'''
	pass

def p_typename_1(p):
	'''
	typename : ID 
	'''
	pass

def p_standard_type(p):
	'''
	standard_type : INTEGER 
	'''
	pass

def p_standard_type_1(p):
	'''
	standard_type : REAL 
	'''
	pass

def p_standard_type_2(p):
	'''
	standard_type : BOOLEAN 
	'''
	pass

def p_standard_type_3(p):
	'''
	standard_type : CHAR 
	'''
	pass

def p_fields(p):
	'''
	fields : fields SEMI field 
	'''
	pass

def p_fields_1(p):
	'''
	fields : field 
	'''
	pass

def p_field(p):
	'''
	field : identifiers COLON typename 
	'''
	pass

def p_identifiers(p):
	'''
	identifiers : identifiers COMMA ID 
	'''
	pass

def p_identifiers_1(p):
	'''
	identifiers : ID 
	'''
	pass

def p_vardefs(p):
	'''
	vardefs : VAR variable_defs SEMI 
	'''
	pass

def p_vardefs_1(p):
	'''
	vardefs :   
	'''
	pass

def p_variable_defs(p):
	'''
	variable_defs : variable_defs SEMI identifiers COLON typename 
	'''
	pass

def p_variable_defs_1(p):
	'''
	variable_defs : identifiers COLON typename 
	'''
	pass

def p_subprograms(p):
	'''
	subprograms : subprograms subprogram SEMI 
	'''
	pass

def p_subprograms_1(p):
	'''
	subprograms :   
	'''
	pass

def p_subprogram(p):
	'''
	subprogram : sub_header SEMI FORWARD 
	'''
	pass

def p_subprogram_1(p):
	'''
	subprogram : sub_header SEMI declarations subprograms comp_statement 
	'''
	pass

def p_sub_header(p):
	'''
	sub_header : FUNCTION ID formal_parameters COLON standard_type 
	'''
	pass

def p_sub_header_1(p):
	'''
	sub_header : PROCEDURE ID formal_parameters 
	'''
	pass

def p_sub_header_2(p):
	'''
	sub_header : FUNCTION ID 
	'''
	pass

def p_formal_parameters(p):
	'''
	formal_parameters : LPAREN parameter_list RPAREN 
	'''
	pass

def p_formal_parameters_1(p):
	'''
	formal_parameters :   
	'''
	pass

def p_parameter_list(p):
	'''
	parameter_list : parameter_list SEMI pass identifiers COLON typename 
	'''
	pass

def p_parameter_list_1(p):
	'''
	parameter_list : pass identifiers COLON typename 
	'''
	pass

def p_pass(p):
	'''
	pass : VAR 
	'''
	pass

def p_pass_1(p):
	'''
	pass :   
	'''
	pass

def p_comp_statement(p):
	'''
	comp_statement : BEGIN statements END 
	'''
	pass

def p_statements(p):
	'''
	statements : statements SEMI statement 
	'''
	pass

def p_statements_1(p):
	'''
	statements : statement 
	'''
	pass

def p_statement(p):
	'''
	statement : assignment 
	'''
	pass

def p_statement_1(p):
	'''
	statement : if_statement 
	'''
	pass

def p_statement_2(p):
	'''
	statement : while_statement 
	'''
	pass

def p_statement_3(p):
	'''
	statement : for_statement 
	'''
	pass

def p_statement_4(p):
	'''
	statement : with_statement 
	'''
	pass

def p_statement_5(p):
	'''
	statement : subprogram_call 
	'''
	pass

def p_statement_6(p):
	'''
	statement : io_statement 
	'''
	pass

def p_statement_7(p):
	'''
	statement : comp_statement 
	'''
	pass

def p_statement_8(p):
	'''
	statement :   
	'''
	pass

def p_assignment(p):
	'''
	assignment : variable ASSIGN expression 
	'''
	pass

def p_assignment_1(p):
	'''
	assignment : variable ASSIGN STRING 
	'''
	pass

def p_if_statement(p):
	'''
	if_statement : IF expression THEN statement if_tail 
	'''
	pass

def p_if_tail(p):
	'''
	if_tail : ELSE statement 
	'''
	pass

def p_if_tail_1(p):
	'''
	if_tail :   
	'''
	pass

def p_while_statement(p):
	'''
	while_statement : WHILE expression DO statement 
	'''
	pass

def p_for_statement(p):
	'''
	for_statement : FOR ID ASSIGN iter_space DO statement 
	'''
	pass

def p_iter_space(p):
	'''
	iter_space : expression TO expression 
	'''
	pass

def p_iter_space_1(p):
	'''
	iter_space : expression DOWNTO expression 
	'''
	pass

def p_with_statement(p):
	'''
	with_statement : WITH variable DO statement 
	'''
	pass

def p_subprogram_call(p):
	'''
	subprogram_call : ID 
	'''
	pass

def p_subprogram_call_1(p):
	'''
	subprogram_call : ID LPAREN expressions RPAREN 
	'''
	pass

def p_io_statement(p):
	'''
	io_statement : READ LPAREN read_list RPAREN 
	'''
	pass

def p_io_statement_1(p):
	'''
	io_statement : WRITE LPAREN write_list RPAREN 
	'''
	pass

def p_read_list(p):
	'''
	read_list : read_list COMMA read_item 
	'''
	pass

def p_read_list_1(p):
	'''
	read_list : read_item 
	'''
	pass

def p_read_item(p):
	'''
	read_item : variable 
	'''
	pass

def p_write_list(p):
	'''
	write_list : write_list COMMA write_item 
	'''
	pass

def p_write_list_1(p):
	'''
	write_list : write_item 
	'''
	pass

def p_write_item(p):
	'''
	write_item : expression 
	'''
	pass

def p_write_item_1(p):
	'''
	write_item : 
	'''
	pass




def p_error(p):
    if p is None:
        signal_error("Unexpected end-of-file", 'end')
    else:
        signal_error("Unexpected token '{0}'".format(p.value), p.lineno)

parser = yacc()

def signal_error(string, lineno):
    print(string, str(lineno))
    SimplePascalLexer.errorflag = True

#def from_file(filename):
#    try:
#        with open(filename, "rU") as f:
#            init()
#            parser.parse(f.read(), lexer=lex.lex(module=decaflexer), debug=None)
#        return not SimplePascalLexer.errorflag
#    except IOError as e:
#        print("I/O error: %s: %s" % (filename, e.strerror))


if __name__ == "__main__" :
    f = open(sys.argv[1], "r")
    logging.basicConfig(
            level=logging.CRITICAL,
    )
    log = logging.getLogger()
    res = parser.parse(f.read(), lexer=lex(module=SimplePascalLexer), debug=log)

    if parser.errorok :
        print("Parsing succeeded")
    else:
        print("Parsing failed")