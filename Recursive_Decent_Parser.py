'''
Recursive Decent Parser
'''
from pythonds.basic.stack import Stack
from graphviz import Source
from graphviz import Source

tStack = Stack()
index = 0
Tokens = open("Tokens.txt")
TokensList = Tokens.readlines()
TokensList.reverse()
for item in TokensList:
    item = item[:-1]
    tStack.push(item)


def type_check(t: str):
    if (t == 'main' or t == 'if' or t == 'then' or t == 'else' or t == 'while' or t == 'do' or t == 'begin' or \
                    t == 'end' or t == 'var' or t == 'integer' or t == 'real' or t == 'for' or t == 'function' or t == 'array' or \
                    t == 'procedure' or t == 'result' or t == 'program' or t == 'of'):
        return "KEYWORD"
    elif (t == '=' or t == '<>' or t == '<=' or t == '>=' or t == '>' or t == '<'):
        return "RELOP"
    elif (t == '+' or t == '-' or t == 'or'):
        return "ADDOP"
    elif (t == '*' or t == '/' or t == 'div' or t == 'mod' or t == 'and'):
        return "MULOP"
    elif t == ':=':
        return "ASSIGNOP"
    elif (t == '(' or t == ')' or t == ':' or t == ';' or t == ',' or t == ']' or t == '['):
        return "SYMBOLOP"
    else:
        return "IDENTIFIER"


def getNextToken():
    return tStack.pop()


class Node:
    def __init__(self, n: str, t: str, num: int):
        self.name = n
        self.type = t
        self.number = num
        self.point = []

node_generator = 0
node_list = {}

def types(ng :int):
    node_list[str(ng)] = Node("root1", "root", ng)
    root1 = node_list[str(ng)]
    ng += 1
    token = getNextToken()
    if token == "integer":
        node_list[str(ng)] = Node("integer", "KEYWORD", ng)
        root1.point.append(node_list[str(ng)])
        ng += 1
    elif token == "real":
        node_list[str(ng)] = Node("real", "KEYWORD", ng)
        root1.point.append(node_list[str(ng)])
        ng += 1
    elif token == "array":
        node_list[str(ng)] = Node("array", "KEYWORD", ng)
        root1.point.append(node_list[str(ng)])
        ng += 1
        token = getNextToken()
        if token == '[':
            node_list[str(ng)] = Node("[", "SYMBOLOP", ng)
            root1.point.append(node_list[str(ng)])
            ng += 1
            token = getNextToken()
            if type_check(token) == "CONSTANT":
                node_list[str(ng)] = Node(token, "CONSTANT", ng)
                root1.point.append(node_list[str(ng)])
                ng += 1
                token = getNextToken()
                if token == ']':
                    node_list[str(ng)] = Node(token, "SYMBOLOP", ng)
                    root1.point.append(node_list[str(ng)])
                    ng += 1
                    token = getNextToken()
                    if token == 'of':
                        node_list[str(ng)] = Node("of", "KEYWORD", ng)
                        root1.point.append(node_list[str(ng)])
                        ng += 1
                        token = getNextToken()
                        if token == 'integer':
                            node_list[str(ng)] = Node("integer", "KEYWORD", ng)
                            root1.point.append(node_list[str(ng)])
                            ng += 1
                        elif token == 'real':
                            node_list[str(ng)] = Node("real", "KEYWORD", ng)
                            root1.point.append(node_list[str(ng)])
                            ng += 1
                        else:
                            tStack.push(token)
                    else:
                        tStack.push(token)
                else:
                    tStack.push(token)
            else:
                tStack.push(token)
        else:
            tStack.push(token)
    return root1


def parameter_list(ng :int):
    node_list[str(ng)] = Node("root2", "root2", ng)
    root2 = node_list[str(ng)]
    ng += 1
    root2.point.append(identifier_list(ng))
    token = getNextToken()
    if token == ':':
        node_list[str(ng)] = Node(':', "SYMBOLOP", ng)
        root2.point.append(node_list[str(ng)])
        ng += 1
        root2.point.append(types(ng))
        token = getNextToken()
        if token == ';':
            node_list[str(ng)] = Node(';', "SYMBOLOP", ng)
            root2.point.append(node_list[str(ng)])
            ng += 1
            root2.point.append(parameter_list(ng))
        else:
            tStack.push(token)
    else:
        tStack.push(token)
    return root2


def arguments(ng :int):
    node_list[str(ng)] = Node("root3", "root3", ng)
    root3 = node_list[str(ng)]
    ng += 1
    token = getNextToken()
    if token == '(':
        node_list[str(ng)] = Node("(", "SYMBOLOP", ng)
        root3.point.append(node_list[str(ng)])
        ng += 1
        root3.point.append(parameter_list(ng))
        token = getNextToken()
        if token == ')':
            node_list[str(ng)] = Node(")", "SYMBOLOP", ng)
            root3.point.append(node_list[str(ng)])
        else:
            tStack.push(token)
    else:
        tStack.push(token)
    return root3


def identifier_list(ng: int):
    token = getNextToken()
    node_list[str(ng)] = Node("root4", "root4", ng)
    root4 = node_list[str(ng)]
    if type_check(token) == "IDENTIFIER":
        ng += 1
        node_list[str(ng)] = Node(token, "IDENTIFIER", ng)
        root4.point.append(node_list[str(ng)])
        ng += 1
        token = getNextToken()
        if token == ',':
            node_list[str(ng)] = Node(",", "SYMBOLOP", ng)
            root4.point.append(node_list[str(ng)])
            ng += 1
            root4.point.append(identifier_list(ng))
        else:
            tStack.push(token)
    else:
        tStack.push(token)
    return root4


def declaration_list(ng :int):
    node_list[str(ng)] = Node("root5", "root5", ng)
    root5 = node_list[str(ng)]
    ng += 1
    root5.point.append(identifier_list(ng))
    token = getNextToken()
    if token == ':':
        node_list[str(ng)] = Node(token, "SYMBOLOP", ng)
        root5.point.append(node_list[str(ng)])
        ng += 1
        root5.point.append(types(ng))
        token = getNextToken()
        if token == ';':
            node_list[str(ng)] = Node(token, "SYMBOLOP", ng)
            root5.point.append(node_list[str(ng)])
            ng += 1
            token = getNextToken()
            if token != 'function' and token != 'begin' and token != 'procedure' and token != 'var':
                root5.point.append(declaration_list(ng))
            else:
                tStack.push(token)
        else:
            tStack.push(token)
    else:
        tStack.push(token)
    return root5

def declarations(ng :int):
    token = getNextToken()
    node_list[str(ng)] = Node("root6", "root6", ng)
    root6 = node_list[str(ng)]
    ng += 1
    if token == "var":
        node_list[str(ng)] = Node(token, "KEYWORD", ng)
        root6.point.append(node_list[str(ng)])
        ng += 1
        root6.point.append(declaration_list(ng))
    else:
        tStack.push(token)
    return root6


def subprogram_head(ng :int):
    node_list[str(ng)] = Node("root30", "root30", ng)
    root30 = node_list[str(ng)]
    ng += 1
    token = getNextToken()
    if token == 'function':
        node_list[str(ng)] = Node("function", "KEYWORD", ng)
        root30.point.append(node_list[str(ng)])
        ng += 1
        token = getNextToken()
        if type_check(token) == "IDENTIFIER":
            node_list[str(ng)] = Node(token, "IDENTIFIER", ng)
            root30.point.append(node_list[str(ng)])
            ng += 1
            root30.point.append(arguments(ng))
            token = getNextToken()
            if token == ':':
                node_list[str(ng)] = Node(":", "SYMBOLOP", ng)
                root30.point.append(node_list[str(ng)] )
                ng += 1
                token = getNextToken()
                if token == 'result':
                    node_list[str(ng)] = Node("result", "KEYWORD", ng)
                    root30.point.append(node_list[str(ng)])
                    ng += 1
                    token = getNextToken()
                    if token == 'integer':
                        node_list[str(ng)] = Node("integer", "KEYWORD", ng)
                        root30.point.append(node_list[str(ng)])
                        ng += 1
                        token = getNextToken()
                        if token == ';':
                            node_list[str(ng)] = Node(":", "SYMBOLOP", ng)
                            root30.point.append(node_list[str(ng)])
                            ng += 1
                        else:
                            tStack.push(token)
                    elif token == 'real':
                        node_list[str(ng)] = Node("real", "KEYWORD", ng)
                        root30.point.append(node_list[str(ng)])
                        ng += 1
                        if token == ';':
                            node_list[str(ng)] = Node(":", "SYMBOLOP", ng)
                            root30.point.append(node_list[str(ng)])
                            ng += 1
                        else:
                            tStack.push(token)
                    else:
                        tStack.push(token)
                else:
                    tStack.push(token)
            else:
                tStack.push(token)
        else:
            tStack.push(token)
    elif token == 'procedure':
        node_list[str(ng)] = Node("procedure", "KEYWORD", ng)
        root30.point.append(node_list[str(ng)])
        ng += 1
        token = getNextToken()
        if type_check(token) == "IDENTIFIER":
            node_list[str(ng)] = Node(token, "IDENTIFIER", ng)
            root30.point.append(node_list[str(ng)])
            ng += 1
            root30.point.append(arguments(ng))
            token = getNextToken()
            if token == ';':
                node_list[str(ng)] = Node(":", "SYMBOLOP", ng)
                root30.point.append(node_list[str(ng)])
                ng += 1
    else:
        tStack.push(token)
    return root30


def subprogram_declarations(ng :int):
    node_list[str(ng)] = Node("root8", "root8", ng)
    root8 = node_list[str(ng)]
    ng += 1
    root8.point.append(subprogram_declaration(ng))
    # root8.point.append(subprogram_declarations(ng))
    return root8


def subprogram_declaration(ng :int):
    node_list[str(ng)] = Node("root9", "root9", ng)
    root9 = node_list[str(ng)]
    ng += 1
    root9.point.append(subprogram_head(ng))
    root9.point.append(declarations(ng))
    root9.point.append(compound_statement(ng))
    return root9


def function_reference(ng :int):
    procedure_statement(ng)


def factor(ng :int):
    node_list[str(ng)] = Node("root10", "root10", ng)
    root10 = node_list[str(ng)]
    ng += 1
    token1 = getNextToken()
    token2 = getNextToken()
    tStack.push(token2)
    tStack.push(token1)
    if token2 == '(':
        root10.point.append(function_reference(ng))
    else:
        token = getNextToken()
        if type_check(token) == "CONSTANT":
            node_list[str(ng)] = Node(token, "CONSTANT", ng)
            root10.point.append(node_list[str(ng)])
            ng += 1
        elif token == '(':
            node_list[str(ng)] = Node("(", "SYMBOLOP", ng)
            root10.point.append(node_list[str(ng)])
            ng += 1
            root10.point.append(expression(ng))
            token = getNextToken()
            if token == ')':
                node_list[str(ng)] = Node(")", "SYMBOLOP", ng)
                root10.point.append(node_list[str(ng)])
                ng += 1
            else:
                tStack.push(token)
        elif token == 'not':
            node_list[str(ng)] = Node("not", "KEYWORD", ng)
            root10.point.append(node_list[str(ng)])
            ng += 1
            root10.point.append(factor(ng))
        else:
            tStack.push(token)
            root10.point.append(variable(ng))
    return root10


def term(ng :int):
    node_list[str(ng)] = Node("root11", "root11", ng)
    root11 = node_list[str(ng)]
    ng += 1
    root11.point.append(factor(ng))
    root11.point.append(term_prime(ng))
    return root11

def term_prime(ng :int):
    node_list[str(ng)] = Node("root31", "root31", ng)
    root31 = node_list[str(ng)]
    token = getNextToken()
    if type_check(token) == "MULOP":
        node_list[str(ng)] = Node(token, "MULOP", ng)
        root31.point.append(node_list[str(ng)])
        ng += 1
        root31.point.append(factor(ng))
        root31.point.append(term_prime(ng))
    else:
        tStack.push(token)
    return root31

def simple_expression(ng :int):
    node_list[str(ng)] = Node("root12", "root12", ng)
    root12 = node_list[str(ng)]
    ng += 1
    token = getNextToken()
    if token == '+':
        node_list[str(ng)] = Node("+", "plus", ng)
        root12.point.append(node_list[str(ng)])
        ng += 1
    elif token == '-':
        node_list[str(ng)] = Node("-", "minus", ng)
        root12.point.append(node_list[str(ng)])
        ng += 1
    else:
        tStack.push(token)
    root12.point.append(term(ng))
    root12.point.append(simple_expression_prime(ng))
    return root12

def simple_expression_prime(ng :int):
    node_list[str(ng)] = Node("root40", "root40", ng)
    root40 = node_list[str(ng)]
    ng += 1
    token = getNextToken()
    if type_check(token) == "ADDOP":
        node_list[str(ng)] = Node(token, "ADDOP", ng)
        root40.point.append(node_list[str(ng)])
        ng += 1
        root40.point.append(simple_expression(ng))
        root40.point.append(simple_expression_prime(ng))
    else:
        tStack.push(token)
    return root40


def expression_list(ng :int):
    node_list[str(ng)] = Node("root25", "root25", ng)
    root25 = node_list[str(ng)]
    ng += 1
    root25.point.append(expression(ng))
    token = getNextToken()
    if token == ',':
        node_list[str(ng)] = Node(",", "SYMBOLOP", ng)
        root25.point.append(node_list[str(ng)])
        ng += 1
        root25.point.append(expression_list(ng))
    else:
        tStack.push(token)
    return root25

def expression(ng :int):
    node_list[str(ng)] = Node("root13", "root13", ng)
    root13 = node_list[str(ng)]
    ng += 1
    token1 = getNextToken()
    token2 = getNextToken()
    tStack.push(token2)
    tStack.push(token1)
    if type_check(token2) == "RELOP":
        root13.point.append(simple_expression(ng))
        token = getNextToken()
        if type_check(token) == "RELOP":
            node_list[str(ng)] = Node(token, "RELOP", ng)
            root13.point.append(node_list[str(ng)])
            ng += 1
            root13.point.append(simple_expression(ng))
        else:
            tStack.push(token)
    else:
        root13.point.append(simple_expression(ng))
    return root13


def procedure_statement(ng :int):
    node_list[str(ng)] = Node("root14", "root14", ng)
    root14 = node_list[str(ng)]
    ng += 1
    token1 = getNextToken()
    token2 = getNextToken()
    tStack.push(token2)
    tStack.push(token1)
    token = getNextToken()
    if token2 == '(':
        if type_check(token) == "IDENTIFIER":
            node_list[str(ng)] = Node(token, "IDENTIFIER", ng)
            root14.point.append(node_list[str(ng)])
            ng += 1
            token = getNextToken()
            if token == '(':
                node_list[str(ng)] = Node("(", "SYMBOLOP", ng)
                root14.point.append(node_list[str(ng)])
                ng += 1
                root14.point.append(expression_list(ng))
                token = getNextToken()
                if token == ')':
                    node_list[str(ng)] = Node(")", "SYMBOLOP", ng)
                    root14.point.append(node_list[str(ng)])
                    ng += 1
                else:
                    tStack.push(token)
            else:
                tStack.push(token)
        else:
            tStack.push(token)
    else:
        if type_check(token) == "IDENTIFIER":
            node_list[str(ng)] = Node(token, "IDENTIFIER", ng)
            root14.point.append(node_list[str(ng)])
    return root14


def variable(ng :int):
    node_list[str(ng)] = Node("root15", "root15", ng)
    root15 = node_list[str(ng)]
    ng += 1
    token1 = getNextToken()
    token2 = getNextToken()
    tStack.push(token2)
    tStack.push(token1)
    token = getNextToken()
    if token2 == '[':
        if type_check(token) == "IDENTIFIER":
            node_list[str(ng)] = Node(token, "IDENTIFIER", ng)
            root15.point.append(node_list[str(ng)])
            ng += 1
            token = getNextToken()
            if token == '[':
                node_list[str(ng)] = Node("[", "SYMBOLOP", ng)
                root15.point.append(node_list[str(ng)])
                ng += 1
                root15.point.append(expression(ng))
                token = getNextToken()
                if token == ']':
                    node_list[str(ng)] = Node("]", "SYMBOLOP", ng)
                    root15.point.append(node_list[str(ng)])
                else:
                    tStack.push(token)
            else:
                tStack.push(token)
    else:
        if type_check(token) == "IDENTIFIER":
            node_list[str(ng)] = Node(token, "IDENTIFIER", ng)
            root15.point.append(node_list[str(ng)])
    return root15


def elementary_statement(ng :int):
    node_list[str(ng)] = Node("root16", "root16", ng)
    root16 = node_list[str(ng)]
    ng += 1
    token1 = getNextToken()
    token2 = getNextToken()
    tStack.push(token2)
    tStack.push(token1)
    if type_check(token2) == "ASSIGNOP":
        root16.point.append(variable(ng))
        token = getNextToken()
        if type_check(token) == "ASSIGNOP":
            node_list[str(ng)] = Node(token, "ASSIGNOP", ng)
            root16.point.append(node_list[str(ng)])
            ng += 1
            root16.point.append(expression(ng))
        else:
            tStack.push(token)
    else:
        token = getNextToken()
        tStack.push(token)
        if type_check(token) == "IDENTIFIER":
            root16.point.append(procedure_statement(ng))
        else:
            tStack.push(token)
            root16.point.append(compound_statement(ng))
    return root16


def restricted_statement(ng :int):
    node_list[str(ng)] = Node("root17", "root17", ng)
    root17 = node_list[str(ng)]
    ng += 1
    token = getNextToken()
    if token == 'if':
        node_list[str(ng)] = Node("if", "KEYWORD", ng)
        root17.point.append(node_list[str(ng)])
        ng += 1
        root17.point.append(expression(ng))
        token = getNextToken()
        if token == 'then':
            node_list[str(ng)] = Node("then", "KEYWORD", ng)
            root17.point.append(node_list[str(ng)])
            ng += 1
            root17.point.append(restricted_statement(ng))
            token = getNextToken()
            if token == 'else':
                node_list[str(ng)] = Node("else", "KEYWORD", ng)
                root17.point.append(node_list[str(ng)])
                ng += 1
                root17.point.append(restricted_statement(ng))
            else:
                tStack.push(token)
        else:
            tStack.push(token)
    elif token == 'while':
        node_list[str(ng)] = Node("while", "KEYWORD", ng)
        root17.point.append(node_list[str(ng)])
        ng += 1
        root17.point.append(expression(ng))
        token = getNextToken()
        if token == 'do':
            node_list[str(ng)] = Node("do", "KEYWORD", ng)
            root17.point.append(node_list[str(ng)])
            ng += 1
            root17.point.append(restricted_statement(ng))
        else:
            tStack.push(token)
    else:
        tStack.push(token)
        root17.point.append(elementary_statement(ng))
    return root17


def statement(ng :int):
    node_list[str(ng)] = Node("root18", "root18", ng)
    root18 = node_list[str(ng)]
    ng += 1
    token = getNextToken()
    if token == 'if':
        node_list[str(ng)] = Node("if", "KEYWORD", ng)
        root18.point.append(node_list[str(ng)])
        ng += 1
        root18.point.append(expression(ng))
        token = getNextToken()
        if token == 'then':
            node_list[str(ng)] = Node("then", "KEYWORD", ng)
            root18.point.append(node_list[str(ng)])
            ng += 1
            token = getNextToken()
            if type_check(token) == 'IDENTIFIER' or token == 'begin' or token == 'if' or token == 'while':
                tStack.push(token)
                root18.point.append(restricted_statement(ng))
                token = getNextToken()
                if token == 'else':
                    node_list[str(ng)] = Node("else", "KEYWORD", ng)
                    root18.point.append(node_list[str(ng)])
                    ng += 1
                    root18.point.append(statement(ng))
                else:
                    tStack.push(token)
            else:
                root18.point.append(statement(ng))
        else:
            tStack.push(token)
    elif token == 'while':
        node_list[str(ng)] = Node("while", "KEYWORD", ng)
        root18.point.append(node_list[str(ng)])
        ng += 1
        root18.point.append(expression(ng))
        token = getNextToken()
        if token == 'do':
            node_list[str(ng)] = Node("do", "KEYWORD", ng)
            root18.point.append(node_list[str(ng)])
            ng += 1
            root18.point.append(statement(ng))
        else:
            tStack.push(token)
    else:
        tStack.push(token)
        root18.point.append(elementary_statement(ng))
    return root18


def statement_list(ng :int):
    node_list[str(ng)] = Node("root19", "root19", ng)
    root19 = node_list[str(ng)]
    ng += 1
    root19.point.append(statement(ng))
    token = getNextToken()
    if token == ';':
        node_list[str(ng)] = Node(";", "SYMBOLOP", ng)
        root19.point.append(node_list[str(ng)])
        ng += 1
        root19.point.append(statement_list(ng))
    else:
        tStack.push(token)
    return root19


def compound_statement(ng :int):
    node_list[str(ng)] = Node("root20", "root20", ng)
    root20 = node_list[str(ng)]
    ng += 1
    token = getNextToken()
    if token == 'begin':
        node_list[str(ng)] = Node("begin", "KEYWORD", ng)
        root20.point.append(node_list[str(ng)])
        ng += 1
        root20.point.append(statement_list(ng))
        token = getNextToken()
        if token == 'end':
            node_list[str(ng)] = Node("end", "KEYWORD", ng)
            root20.point.append(node_list[str(ng)])
            ng += 1
        else:
            tStack.push(token)
    else:
        tStack.push(token)
    return root20


def program(ng: int):
    token = getNextToken()
    if token == 'program':
        node_list[str(ng)] = Node("program_original", "root21", ng)
        root21 = node_list[str(ng)]
        node_list[str(ng)].point.append(Node("program", "TERM", ng))
        ng += 1
        token = getNextToken()
        if type_check(token) == "IDENTIFIER":
            node_list[str(ng)] = Node(token, "IDENTIFIER", ng)
            root21.point.append(node_list[str(ng)])
            ng += 1
            token = getNextToken()
            if token == '(':
                node_list[str(ng)] = Node("(", "SYMBOLOP", ng)
                root21.point.append(node_list[str(ng)])
                root21.point.append(identifier_list(ng))
                ng += 1
                token = getNextToken()
                if token == ')':
                    node_list[str(ng)] = Node(")", "SYMBOLOP", ng)
                    root21.point.append(node_list[str(ng)])
                    ng += 1
                    token = getNextToken()
                    if token == ';':
                        node_list[str(ng)] = Node(";", "SYMBOLOP", ng)
                        root21.point.append(node_list[str(ng)])
                        ng += 1
                        root21.point.append(declarations(ng))
                        root21.point.append(subprogram_declarations(ng))
                        root21.point.append(compound_statement(ng))
                    else:
                        tStack.push(token)
                else:
                    tStack.push(token)
            else:
                tStack.push(token)
        else:
            tStack.push(token)
    else:
        tStack.push(token)
    return root21

# def B():
#     t8 = Node("root", "ROOT")
#     t9 = Node("h", "TERM")
#     token = getNextToken()
#     if token == 'h':
#         t8.point.append(t9)
#         t8.point.append(B())
#     else:
#         tStack.push(token)
#     return t8
#
#
#
# def A():
#     t4 = Node("root", "ROOT")
#     t5 = Node("e", "TERM")
#     t6 = Node("f", "TERM")
#     t7 = Node("g", "TERM")
#     token = getNextToken()
#     if token == 'e':
#         t4.point.append(t5)
#         token = getNextToken()
#         if token == 'f':
#             t4.point.append(t6)
#             t4.point.append(B())
#             token = getNextToken()
#             if token == 'g':
#                 t4.point.append(t7)
#             else:
#                 tStack.push(token)
#         else:
#             tStack.push(token)
#     else:
#         tStack.push(token)
#     return t4
#
#
# def S():
#     t0 = Node("root", "ROOT")
#     t1 = Node("a", "TERM")
#     t2 = Node("b", "TERM")
#     t3 = Node("c", "TERM")
#     token = getNextToken()
#     if token == 'a':
#         t0.point.append(t1)
#         token = getNextToken()
#         if token == 'b':
#             t0.point.append(t2)
#             t0.point.append(A())
#             token = getNextToken()
#             if token == 'c':
#                 t0.point.append(t3)
#             else:
#                 tStack.push(token)
#         else:
#             tStack.push(token)
#     else:
#         tStack.push(token)
#     return t0

llist = []
gdp = ""
def tree_to_dot(root):
    if root.name == None:
        return
    gdp = ""
    if len(root.point) > 0:
        gdp += root.name + " -> {"
        for i in root.point:
            gdp += i.name() + " "
        gdp += "}" + '\n'
        llist.append(gdp)
        for j in root.point:
            tree_to_dot(j)






# def program:
#
mdp = ""
root = program(node_generator)
# lss = []
# flag = False
# while(root):
#     mdp += root.name
#     for i in root.point:
#         lss.append(i)
#     for j in lss:
#         mdp += j.name
#         mdp += ":"
#         for k in j.point:
#             mdp += i.name + ","
#             flag = True
#         if flag == False:
#             mdp = mdp[:-1]
#             mdp += ','
#         else:
#             if mdp[len(mdp)-1] == ',':
#                 mdp = mdp[:-1]
#                 mdp += ';'
#             elif mdp[len(mdp)-1] == ':':
#                 mdp = mdp[:-1]
#                 mdp += ','
#             else:
#                 mdp += ';'
#         root = j


temp = ""
temp += root.name + " -> {"
for i in root.point:
    temp += i.name + " "
temp += "}"
print(temp)
graph = open("graph_table.txt", 'w')
graph.write(temp)

print("Alliii")
