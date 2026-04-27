grammar PLC_Project;

/*
 * Parser Rules
 */

program : (statement)* EOF ;

statement
    : ';'                                                               # emptyStatement
    | type idList ';'                                                   # declarationStatement
    | expression ';'                                                    # expressionStatement
    | 'read' idList ';'                                                 # readStatement
    | 'write' exprList ';'                                              # writeStatement
    | '{' statement* '}'                                                # blockStatement
    | 'if' '(' expression ')' statement ('else' statement)?             # ifStatement
    | 'while' '(' expression ')' statement                              # whileStatement
    | 'for' '(' expression ';' expression ';' expression ')' statement  # forStatement
    | 'fopen' expression ',' expression ';'                             # fopenStatement
    | 'fappend' expression ',' exprList ';'                             # fappendStatement
    | 'fread' expression ',' ID ';'                                     # freadStatement
    | expression '<<' inputList ';'                                     # arrowsStatement
    ;

type
    : INT_KW
    | FLOAT_KW
    | BOOL_KW
    | STRING_KW
    | FILE_KW
    ;

idList : ID (',' ID)* ;

exprList : expression (',' expression)* ;

inputList : expression ('<<' expression)* ;

expression
    : '!' expression                                    # logicalNotExpr
    | '-' expression                                    # unaryMinusExpr
    | expression op=('*' | '/' | '%') expression        # multiplicativeExpr
    | expression op=('+' | '-' | '.') expression        # additiveExpr
    | expression op=('<' | '>') expression              # relationalExpr
    | expression op=('==' | '!=') expression            # equalityExpr
    | expression '&&' expression                        # logicalAndExpr
    | expression '||' expression                        # logicalOrExpr
    | expression '?' expression TER_ELSE expression     # ternaryExpr
    | expression '[' expression ']'                     # indexingExpr
    | <assoc=right> ID '=' expression                   # assignmentExpr
    | '(' expression ')'                                # parenthesisExpr
    | literal                                           # literalExpr
    | ID                                                # identifierExpr
    ;

literal
    : INT
    | FLOAT
    | BOOL
    | STRING
    ;

/*
 * Lexer Rules
 */

// Keywords
READ    : 'read' ;
WRITE   : 'write' ;
IF      : 'if' ;
ELSE    : 'else' ;
TER_ELSE: ':' ;
WHILE   : 'while' ;
FOR     : 'for' ;
INT_KW  : 'int' ;
FLOAT_KW: 'float' ;
BOOL_KW : 'bool' ;
STRING_KW: 'string' ;
FILE_KW : 'FILE' ;
FOPEN   : 'fopen' ;
FAPPEND : 'fappend' ;
FREAD   : 'fread' ;

// Literals
BOOL    : 'true' | 'false' ;
INT     : [0-9]+ ;
FLOAT   : [0-9]+ '.' [0-9]* | '.' [0-9]+ ;
STRING  : '"' (~["\r\n])* '"' ; 

ID      : [a-zA-Z] [a-zA-Z0-9]* ;

// Whitespace and comments
WS      : [ \t\r\n]+ -> skip ;
COMMENT : '//' ~[\r\n]* -> skip ;
