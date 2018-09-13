'''
Compiler Project
Basic Pascal Recursive Decent Parser
& Lexical Analyzer & Parse Tree Construction & Syntax Error Detection

Powered By Ali Forghani in Sadjad University of Technology

Compiler Design Course
'''


from subprocess import Popen
from pythonds.basic.stack import Stack

import os
initial = None
accept = None

sigma = "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890-=_+/*-+.()"
REfile = open("re_0.txt")
class NFA:
    def __init__(self, state_name):
        self.name = state_name
        self.epoint1 = None
        self.epoint2 = None
        self.spoint = None
        self.sname = None
        self.accept = None
        self.initial = None
        self.file = open("nfa_0.txt", 'r+')

def infix_to_postfix(infixexpr: str):
    prec = {}
    prec["."] = 2
    prec["|"] = 1
    prec["*"] = 3
    # prec["+"] = 2
    prec["(."] = 0
    opStack = Stack()
    postfixList = []
    tokenList = infixexpr.split()

    for token in tokenList:
        if token in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890()":
            postfixList.append(token)
        elif token == '(.':
            opStack.push(token)
        elif token == ').':
            topToken = opStack.pop()
            while topToken != '(.':
                postfixList.append(topToken)
                topToken = opStack.pop()
        else:
            while (not opStack.isEmpty()) and \
                    (prec[opStack.peek()] >= prec[token]):
                  postfixList.append(opStack.pop())
            opStack.push(token)

    while not opStack.isEmpty():
        postfixList.append(opStack.pop())
    return " ".join(postfixList)


def NFA_creator(postfixexpr: str):
    postfix_list = postfixexpr.split(' ')
    ptStack = Stack()
    aptStack = Stack()
    index_generate = 0
    accept1 = None
    initial1 = None

    for i in postfix_list:
        if i == '.':
            m2 = ptStack.pop()
            m1 = ptStack.pop()
            apt2 = aptStack.pop()
            apt1 = aptStack.pop()
            apt1.accept = False
            m2.initial = False
            apt1.spoint = m2.spoint
            apt1.sname = m2.sname
            apt1.epoint1 = m2.epoint1
            apt1.epoint2 = m2.epoint2
            m2.sname = None
            m2.epoint1 = None
            m2.epoint2 = None
            ptStack.push(m1)
            aptStack.push(apt2)

        elif i == '|':
            index_generate += 1
            ti = NFA(index_generate)
            index_generate += 1
            ta = NFA(index_generate)

            ti.initial = True
            ti.accept = False
            ta.initial = False
            ta.accept = True
            accept1 = str(ta.name)
            m2 = ptStack.pop()
            m1 = ptStack.pop()
            apt2 = aptStack.pop()
            apt1 = aptStack.pop()
            ti.epoint1 = m1
            ti.epoint2 = m2
            apt1.epoint1 = ta
            apt2.epoint1 = ta
            ptStack.push(ti)
            aptStack.push(ta)

        elif i == '*':
            index_generate += 1
            ti2 = NFA(index_generate)
            index_generate += 1
            ta2 = NFA(index_generate)
            ti2.initial = True
            ti2.accept = False
            ta2.initial = False
            ta2.accept = True
            accept1 = str(ta2.name)
            m1 = ptStack.pop()
            apt1 = aptStack.pop()
            ti2.epoint1 = m1
            ti2.epoint2 = ta2
            apt1.epoint1 = m1
            apt1.epoint2 = ta2
            ptStack.push(ti2)
            aptStack.push(ta2)

        else:
            index_generate += 1
            t1 = NFA(index_generate)
            t1.sname = i
            t1.initial = True
            t1.accept = False
            index_generate += 1
            t2 = NFA(index_generate)
            t2.initial = False
            t2.accept = True
            accept1 = str(t2.name)
            t1.spoint = t2
            ptStack.push(t1)
            aptStack.push(t2)
    initial1 = ptStack.peek().name
    return ptStack.peek(),initial1,accept1


checklist = []
file = open("nfa_0.txt", 'w')

def saving_NFA(st: NFA):
    if st.name == None:
        return
    if not st.name in checklist:
        checklist.append(st.name)
        if st.epoint1 != None:
            file.write(str(st.name) + " " + str(st.epoint1.name) + " " + "@" + '\n')
            saving_NFA(st.epoint1)
        if st.epoint2 != None:
            file.write(str(st.name) + " " + str(st.epoint2.name) + " " + "@" + '\n')
            saving_NFA(st.epoint2)
        if st.spoint != None:
            file.write(str(st.name) + " " + str(st.spoint.name) + " " + str(st.sname) + '\n')
            saving_NFA(st.spoint)



Re = REfile.readlines()
print(str(Re[0]))
temptest,initial,accept = NFA_creator(infix_to_postfix(str(Re[0])))
file.write("x" + " " + str(initial) + " " + "@" + '\n')
saving_NFA(temptest)
file.write(str(accept) + " " + "y" + " " + "@" + '\n')



print("")

