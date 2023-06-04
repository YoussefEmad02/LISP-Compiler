#!/usr/bin/env python
# coding: utf-8
import os
# In[49]:


import tkinter as tk
from tkinter import *
from tkinter import ttk
from enum import Enum
import re
from PIL import Image

import customtkinter
import pandas
import pandastable as pt
from nltk.tree import *
from customtkinter import CTk


class Token_type(Enum):  # listing all tokens type

    Error = 1
    Constant = 2
    Identifier = 3
    NIL = 4
    T = 5
    open_bracket = 6
    close_bracket = 7
    apostrophe = 8
    String = 9
    print = 10
    write = 11
    writeLine = 12
    read = 13
    mod = 14
    PlusOp = 15
    MinusOp = 16
    MultiplyOp = 17
    DivideOp = 18
    incf = 19
    decf = 20
    LessThanOp = 21
    GreaterThanOp = 22
    LessThanequalOp = 23
    GreaterThanequalOp = 24
    EqualityOp = 25
    NOT = 26
    AND = 27
    OR = 28
    IF = 29
    when = 30
    dotimes = 31
    setq = 32
    rem = 33
    function = 34
    defun = 35
    int = 36
    Semicolon = 37
    defconstant = 38


# class token to hold string and token type
class token:
    def __init__(self, lex, token_type):
        self.lex = lex
        self.token_type = token_type

    def to_dict(self):
        return {
            'Lex': self.lex,
            'token_type': self.token_type
        }


# Reserved word Dictionary

NeedsSpace = {
    "(": Token_type.open_bracket,
    ")": Token_type.close_bracket,
    ";": Token_type.Semicolon,
    "+": Token_type.PlusOp,
    "*": Token_type.MultiplyOp,
    "/": Token_type.DivideOp,
    "incf": Token_type.incf,
    "decf": Token_type.decf,
    "defun": Token_type.defun,
    "setq": Token_type.setq
}

ReservedWords = {"dotimes": Token_type.dotimes,
                 "setq": Token_type.setq,
                 "print": Token_type.print,
                 "write": Token_type.write,
                 "if": Token_type.IF,
                 "write-line": Token_type.writeLine,
                 "when": Token_type.when,
                 "read": Token_type.read,
                 "T": Token_type.T,
                 "defun": Token_type.function,
                 "nil": Token_type.NIL,
                 "defconstant": Token_type.defconstant
                 }

Symbols = {"(": Token_type.open_bracket,
           ")": Token_type.close_bracket,
           "'": Token_type.apostrophe
           }

Operators = {"+": Token_type.PlusOp,
             "-": Token_type.MinusOp,
             "*": Token_type.MultiplyOp,
             "/": Token_type.DivideOp,
             "mod": Token_type.mod,
             "rem": Token_type.rem
             }

RelOperators = {">": Token_type.GreaterThanOp,
                "<": Token_type.LessThanOp,
                "=": Token_type.EqualityOp,
                ">=": Token_type.GreaterThanequalOp,
                "<=": Token_type.LessThanequalOp
                }

LogicalOperators = {"and": Token_type.AND,
                    "or": Token_type.OR,
                    "not": Token_type.NOT
                    }

IncOperators = {"decf": Token_type.decf,
                "incf": Token_type.incf
                }

Tokens = []  # to add tokens to list
errors = []  # to add errors to list


def find_token(text):
    # To separate between characters such as ( ) ; during scanning if the user hadn't seperated them

    for needSpace in NeedsSpace:
        text = text.replace(needSpace, ' ' + needSpace + ' ')

    pattern = r'([><]=|[<>=])'
    re.sub(pattern, r' \1 ', text)

    # Removing spaces between strings
    pattern = r'"[^"]*"'
    match_list = re.findall(pattern, text)

    # Adding spaces between write-line and write
    pattern = r'(\bwrite(-line)?\b)'
    replacement_str = r' \1 '
    text = re.sub(pattern, replacement_str, text)

    # Adding spaces between - if there are numbers on the left or right position
    pattern = r'([0-9]*\.?[0-9]+)-([0-9]*\.?[0-9]+)'
    replacement_str = r' \1 - \2 '

    text = re.sub(pattern, replacement_str, text)

    # Remove spaces from within each matched string
    for match in match_list:
        new_match = match.replace(" ", "")
        text = text.replace(match, new_match)

    S = text.split()

    for idx, w in enumerate(S):

        if w in ReservedWords:
            t = token(w, ReservedWords[w])
            Tokens.append(t)




        elif re.match(r'^\".*\"$', w):
            t = token(w, token_type=Token_type.String)
            Tokens.append(t)


        # Detecting Relational Operators
        elif w in RelOperators:
            t = token(w, RelOperators[w])
            Tokens.append(t)

        elif w in IncOperators:
            t = token(w, IncOperators[w])
            Tokens.append(t)

        elif w in LogicalOperators:
            t = token(w, LogicalOperators[w])
            Tokens.append(t)



        # Detecting Operations
        elif w in Operators:
            t = token(w, Operators[w])
            Tokens.append(t)



        # Detecting Constants ( Integers and Floats )
        elif re.match(r'^[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?$', w):
            t = token(w, token_type=Token_type.Constant)
            Tokens.append(t)

        elif re.match("^[a-zA-Z][a-zA-Z0-9]*$", w):
            t = token(w, token_type=Token_type.Identifier)
            Tokens.append(t)

        elif w in Symbols:
            t = token(w, Symbols[w])
            Tokens.append(t)

        # None Detected --> Error!
        else:
            t = token(w, token_type=Token_type.Error)
            errors.append("Lexical error  " + w)


def Parse():
    j = 0
    Children = []
    Tokens_Dict = Tokens[j].to_dict()

    if (j < len(Tokens)) and re.match("^\".*\"$", Tokens_Dict['Lex']):
        String_dict = Match(Token_type.String, j)
        Children.append(String_dict["node"])

    elif (j < len(Tokens)) and Tokens_Dict['Lex'] == '(':
        Statements_dict = Statements(j)
        Children.append(Statements_dict["node"])

    else:
        errors.append("Syntax error: empty program")
        Children.append(errors[len(errors) - 1])

    Node = Tree('Program', Children)

    return Node


def Statements(j):
    Children = []
    output = dict()
    if (j < len(Tokens)):
        Tokens_Dict = Tokens[j].to_dict()

    if (j < len(Tokens)) and Tokens_Dict['Lex'] == '(':  # for recursion
        List_Dict = List(j)
        Children.append(List_Dict["node"])
        out1 = Statements(List_Dict["index"])
        if out1:
            Children.append(out1["node"])
            output["index"] = out1["index"]
        else:
            output["index"] = List_Dict["index"]

    else:
        return

    node = Tree('Statements', Children)
    output["node"] = node

    return output


def List(j):
    Children = []
    output = dict()

    out1 = Match(Token_type.open_bracket, j)
    Children.append(out1["node"])

    ListItem_Dict = ListItem(out1["index"])
    if ListItem_Dict:
        Children.append(ListItem_Dict["node"])

    index = ListItem_Dict["index"] if ListItem_Dict else out1["index"]  # check for epsillum

    out2 = Match(Token_type.close_bracket, index)
    Children.append(out2["node"])

    node = Tree('List', Children)
    output["node"] = node
    output["index"] = out2["index"]
    return output


def ListItem(j):
    Children = []
    output = dict()

    if (j < len(Tokens)):
        Tokens_Dict = Tokens[j].to_dict()

    if (j < len(Tokens)) and (
            re.match("^\".*\"$", Tokens_Dict['Lex']) or re.match("^[0-9]\.?[0-9]*?$", Tokens_Dict['Lex'])):
        Atom_Dict = Atom(j)
        Children.append(Atom_Dict["node"])
        output["index"] = Atom_Dict["index"]

    elif (j < len(Tokens)) and (
            Tokens_Dict['Lex'] == 'setq' or
            Tokens_Dict['Lex'] == 'write-line' or
            Tokens_Dict['Lex'] == 'write' or
            Tokens_Dict['Lex'] == 'print' or
            Tokens_Dict['Lex'] == 'when' or
            Tokens_Dict['Lex'] == 'dotimes' or
            re.match("^[a-zA-Z][a-zA-Z0-9]*$", Tokens_Dict['Lex']) or
            Tokens_Dict['Lex'] in Operators or
            Tokens_Dict['Lex'] in RelOperators or
            Tokens_Dict['Lex'] in LogicalOperators or
            Tokens_Dict['Lex'] in IncOperators
    ):
        Statement_Dict = Statement(j)
        Children.append(Statement_Dict["node"])
        output["index"] = Statement_Dict["index"]

    else:
        return

    node = Tree('ListItem', Children)
    output["node"] = node

    return output


def Atom(j):
    Children = []
    output = dict()

    if (j < len(Tokens)):
        Tokens_Dict = Tokens[j].to_dict()

    if (j < len(Tokens)) and re.match("^\".*\"$", Tokens_Dict['Lex']):
        String_dict = Match(Token_type.String, j)
        Children.append(String_dict["node"])
        output["index"] = String_dict["index"]

    elif (j < len(Tokens)) and (re.match("^[0-9]\.?[0-9]*?$", Tokens_Dict['Lex'])):
        const_Dict = Match(Token_type.Constant, j)
        Children.append(const_Dict["node"])
        output["index"] = const_Dict["index"]

    else:
        return

    node = Tree('ListItem', Children)
    output["node"] = node

    return output


def Statement(j):
    Children = []
    output = dict()

    if (j < len(Tokens)):
        Tokens_Dict = Tokens[j].to_dict()

    if (j < len(Tokens)) and Tokens_Dict['Lex'] == 'setq':
        out1 = Match(Token_type.setq, j)
        Children.append(out1["node"])
        out2 = Match(Token_type.Identifier, out1["index"])
        Children.append(out2["node"])
        Terms_Dict = Terms(out2["index"])
        Children.append(Terms_Dict["node"])
        output["index"] = Terms_Dict["index"]

    elif (j < len(Tokens)) and Tokens_Dict['Lex'] == 'defconstant':
        out1 = Match(Token_type.defconstant, j)
        Children.append(out1["node"])
        out2 = Match(Token_type.Identifier, out1["index"])
        Children.append(out2["node"])
        Terms_Dict = Terms(out2["index"])
        Children.append(Terms_Dict["node"])
        output["index"] = Terms_Dict["index"]


    elif (j < len(Tokens)) and Tokens_Dict['Lex'] == 'write-line':
        out1 = Match(Token_type.writeLine, j)
        Children.append(out1["node"])
        out2 = Match(Token_type.String, out1["index"])
        Children.append(out2["node"])
        output["index"] = out2["index"]

    elif (j < len(Tokens)) and Tokens_Dict['Lex'] == 'print':
        out1 = Match(Token_type.print, j)
        Children.append(out1["node"])
        temp = Tokens[j + 1].to_dict()

        if (j + 1 < len(Tokens)) and temp['Lex'][0] == '"':
            # The next token is a string literal
            out2 = Match(Token_type.String, j + 1)
            Children.append(out2["node"])
            output["index"] = out2["index"]
        else:
            # The next token is a term
            Term_Dict = Term(out1["index"])
            Children.append(Term_Dict["node"])
            output["index"] = Term_Dict["index"]

    elif (j < len(Tokens)) and Tokens_Dict['Lex'] == 'write':
        out1 = Match(Token_type.write, j)
        Children.append(out1["node"])
        temp = Tokens[j + 1].to_dict()

        if (j + 1 < len(Tokens)) and temp['Lex'][0] == '"':
            # The next token is a string literal
            out2 = Match(Token_type.String, j + 1)
            Children.append(out2["node"])
            output["index"] = out2["index"]
        else:
            # The next token is a term
            Term_Dict = Term(out1["index"])
            Children.append(Term_Dict["node"])
            output["index"] = Term_Dict["index"]

    elif (j < len(Tokens)) and Tokens_Dict['Lex'] == 'when':
        out1 = Match(Token_type.when, j)
        Children.append(out1["node"])
        out2 = Match(Token_type.open_bracket, out1["index"])
        Children.append(out2["node"])
        WhenTerm_Dict = WhenTerm(out2["index"])
        Children.append(WhenTerm_Dict["node"])
        out3 = Match(Token_type.close_bracket, WhenTerm_Dict["index"])
        Children.append(out3["node"])
        Stmts_Dict = Statements(out3["index"])
        if Stmts_Dict:
            Children.append(Stmts_Dict["node"])

        output["index"] = Stmts_Dict["index"] if Stmts_Dict else out3["index"]

    elif (j < len(Tokens)) and Tokens_Dict['Lex'] == 'dotimes':
        out1 = Match(Token_type.dotimes, j)
        Children.append(out1["node"])
        out2 = Match(Token_type.open_bracket, out1["index"])
        Children.append(out2["node"])
        out3 = Match(Token_type.Identifier, out2["index"])
        Children.append(out3["node"])
        Factor_Dict = Factor(out3["index"])
        Children.append(Factor_Dict["node"])
        out3 = Match(Token_type.close_bracket, Factor_Dict["index"])
        Children.append(out3["node"])
        Stmts_Dict = Statements(out3["index"])
        if Stmts_Dict:
            Children.append(Stmts_Dict["node"])

        output["index"] = Stmts_Dict["index"] if Stmts_Dict else out3["index"]


    elif (j < len(Tokens)) and (Tokens_Dict['Lex'] in IncOperators):
        Inc_Dict = Incrementation(j)
        Children.append(Inc_Dict["node"])
        out1 = Match(Token_type.Identifier, Inc_Dict["index"])
        Children.append(out1["node"])
        IncVar_Dict = IncrementVar(out1["index"])

        if IncVar_Dict:
            Children.append(IncVar_Dict["node"])

        index = IncVar_Dict["index"] if IncVar_Dict else out1["index"]
        output["index"] = index

    elif (j < len(Tokens)) and (Tokens_Dict['Lex'] in Operators):
        Exp_Dict = Expression(j)
        Children.append(Exp_Dict["node"])
        output["index"] = Exp_Dict["index"]

    elif (j < len(Tokens)) and (Tokens_Dict['Lex'] in RelOperators):
        Cond_Dict = Condition(j)
        Children.append(Cond_Dict["node"])
        output["index"] = Cond_Dict["index"]

    elif (j < len(Tokens)) and (Tokens_Dict['Lex'] in LogicalOperators):
        Bool_Dict = BoolExp(j)
        Children.append(Bool_Dict["node"])
        output["index"] = Bool_Dict["index"]

    elif (j < len(Tokens)) and re.match("^[a-zA-Z][a-zA-Z0-9]*$", Tokens_Dict['Lex']):
        out1 = Match(Token_type.Identifier, j)
        Children.append(out1["node"])
        Factors_Dict = Factors(out1["index"])
        Children.append(Factors_Dict["node"])
        output["index"] = Factors_Dict["index"]


    else:
        errors.append("Syntax error: Expected Statement")
        Children.append(errors[len(errors) - 1])
        output["index"] = j

    node = Tree('Statement', Children)
    output["node"] = node

    return output


def Terms(j):
    Children = []
    output = dict()

    if (j < len(Tokens)):
        Tokens_Dict = Tokens[j].to_dict()

    if (j < len(Tokens)) and re.match("^\".*\"$", Tokens_Dict['Lex']):
        out1 = Match(Token_type.String, j)
        Children.append(out1["node"])
        output["index"] = out1["index"]

    elif (j < len(Tokens)) and (re.match("^[a-zA-Z][a-zA-Z0-9]*$", Tokens_Dict['Lex'])
                                or re.match("^[0-9]\.?[0-9]*?$", Tokens_Dict['Lex'])
                                or Tokens_Dict['Lex'] == '('):
        Term_Dict = Term(j)
        Children.append(Term_Dict["node"])
        output["index"] = Term_Dict["index"]

    else:
        errors.append("Syntax error: Expected string or term")
        Children.append(errors[len(errors) - 1])
        output["index"] = j

    node = Tree('Terms', Children)
    output["node"] = node

    return output


def Term(j):
    Children = []
    output = dict()

    if (j < len(Tokens)):
        Tokens_Dict = Tokens[j].to_dict()

    if (j < len(Tokens)) and (re.match("^[a-zA-Z][a-zA-Z0-9]*$", Tokens_Dict['Lex']) or re.match("^[0-9]\.?[0-9]*?$",
                                                                                                 Tokens_Dict[
                                                                                                     'Lex']) or re.match(
        r'^\".*\"$', Tokens_Dict['Lex'])):
        Factor_Dict = Factor(j)
        Children.append(Factor_Dict["node"])
        output["index"] = Factor_Dict["index"]

    elif (j < len(Tokens)) and Tokens_Dict['Lex'] == '(':
        out = Match(Token_type.open_bracket, j)
        Children.append(out["node"])
        BoolItem_Dict = BoolItem(out["index"])
        Children.append(BoolItem_Dict["node"])
        out1 = Match(Token_type.close_bracket, BoolItem_Dict["index"])
        Children.append(out1["node"])
        output["index"] = out1["index"]


    else:
        errors.append("Syntax error: Expected id or constant or (boolExp)")
        Children.append(errors[len(errors) - 1])
        output["index"] = j

    node = Tree('Term', Children)
    output["node"] = node

    return output


def WhenTerm(j):
    Children = []
    output = dict()

    if (j < len(Tokens)):
        Tokens_Dict = Tokens[j].to_dict()

    if (j < len(Tokens)) and (Tokens_Dict['Lex'] in RelOperators):
        Cond_Dict = Condition(j)
        Children.append(Cond_Dict["node"])
        output["index"] = Cond_Dict["index"]

    elif (j < len(Tokens)) and (Tokens_Dict['Lex'] in LogicalOperators):
        Bool_Dict = BoolExp(j)
        Children.append(Bool_Dict["node"])
        output["index"] = Bool_Dict["index"]

    else:
        errors.append("Syntax error: Expected WhenTerm")
        Children.append(errors[len(errors) - 1])
        output["index"] = j

    node = Tree('WhenTerm', Children)
    output["node"] = node

    return output


def Incrementation(j):
    Children = []
    output = dict()

    if (j < len(Tokens)):
        Tokens_Dict = Tokens[j].to_dict()

    if (j < len(Tokens)) and Tokens_Dict['Lex'] == 'incf':
        out = Match(Token_type.incf, j)
        Children.append(out["node"])
        output["index"] = out["index"]

    elif (j < len(Tokens)) and Tokens_Dict['Lex'] == 'decf':
        out = Match(Token_type.decf, j)
        Children.append(out["node"])
        output["index"] = out["index"]

    else:
        errors.append("Syntax error: Expected Incrementation")
        Children.append(errors[len(errors) - 1])
        output["index"] = j

    node = Tree('Incrementation', Children)
    output["node"] = node

    return output


def Condition(j):
    Children = []
    output = dict()

    RelOp_Dict = RelOp(j)
    Children.append(RelOp_Dict["node"])

    ExpDash_Dict1 = ExpDash(RelOp_Dict["index"])
    Children.append(ExpDash_Dict1["node"])

    ExpDash_Dict2 = ExpDash(ExpDash_Dict1["index"])
    Children.append(ExpDash_Dict2["node"])

    node = Tree('Condition', Children)
    output["node"] = node
    output["index"] = ExpDash_Dict2["index"]
    return output


def Factor(j):
    Children = []
    output = dict()

    if (j < len(Tokens)):
        Tokens_Dict = Tokens[j].to_dict()

    if (j < len(Tokens)) and re.match("^[0-9]\.?[0-9]*?$", Tokens_Dict['Lex']):
        out1 = Match(Token_type.Constant, j)
        Children.append(out1["node"])
        output["index"] = out1["index"]

    elif (j < len(Tokens)) and re.match("^[a-zA-Z][a-zA-Z0-9]*$", Tokens_Dict['Lex']):
        out2 = Match(Token_type.Identifier, j)
        Children.append(out2["node"])
        output["index"] = out2["index"]
    # elif (j < len(Tokens)) and re.match(r'^\".*\"$', Tokens_Dict['Lex']):
    #     out3 = Match(Token_type.String, j)
    #     Children.append(out3["node"])
    #     output["index"] = out3["index"]

    else:
        errors.append("Syntax error: Expected identifier or constant")
        Children.append(errors[len(errors) - 1])
        output["index"] = j

    node = Tree('Factor', Children)
    output["node"] = node

    return output


def Factors(j):
    Children = []
    output = dict()

    if (j < len(Tokens)):
        Tokens_Dict = Tokens[j].to_dict()

    if (j < len(Tokens)) and (re.match("^[a-zA-Z][a-zA-Z0-9]*$", Tokens_Dict['Lex']) or re.match("^[0-9]\.?[0-9]*?$",
                                                                                                 Tokens_Dict['Lex'])):
        Factor_Dict = Factor(j)
        Children.append(Factor_Dict["node"])
        Facsss_Dict = Factors(Factor_Dict["index"])
        if Facsss_Dict:
            Children.append(Facsss_Dict["node"])
        output["index"] = Facsss_Dict["index"] if Facsss_Dict else Factor_Dict["index"]

    else:
        return

    node = Tree('Factors', Children)
    output["node"] = node

    return output


def Op(j):
    Children = []
    output = dict()

    if (j < len(Tokens)):
        Tokens_Dict = Tokens[j].to_dict()

    if (j < len(Tokens)) and Tokens_Dict['Lex'] == "+":
        out1 = Match(Token_type.PlusOp, j)
        Children.append(out1["node"])
        output["index"] = out1["index"]

    elif (j < len(Tokens)) and Tokens_Dict['Lex'] == "-":
        out2 = Match(Token_type.MinusOp, j)
        Children.append(out2["node"])
        output["index"] = out2["index"]

    elif (j < len(Tokens)) and Tokens_Dict['Lex'] == "*":
        out3 = Match(Token_type.MultiplyOp, j)
        Children.append(out3["node"])
        output["index"] = out3["index"]

    elif (j < len(Tokens)) and Tokens_Dict['Lex'] == "/":
        out4 = Match(Token_type.DivideOp, j)
        Children.append(out4["node"])
        output["index"] = out4["index"]

    elif (j < len(Tokens)) and Tokens_Dict['Lex'] == "mod":
        out5 = Match(Token_type.mod, j)
        Children.append(out5["node"])
        output["index"] = out5["index"]

    elif (j < len(Tokens)) and Tokens_Dict['Lex'] == "rem":
        out6 = Match(Token_type.rem, j)
        Children.append(out6["node"])
        output["index"] = out6["index"]

    else:
        errors.append("Syntax error: Expected operator")
        Children.append(errors[len(errors) - 1])
        output["index"] = j

    node = Tree('Op', Children)
    output["node"] = node
    return output


def RelOp(j):
    Children = []
    output = dict()

    if (j < len(Tokens)):
        Tokens_Dict = Tokens[j].to_dict()

    if (j < len(Tokens)) and Tokens_Dict['Lex'] == "=":
        out1 = Match(Token_type.EqualityOp, j)
        Children.append(out1["node"])
        output["index"] = out1["index"]

    elif (j < len(Tokens)) and Tokens_Dict['Lex'] == ">":
        out2 = Match(Token_type.GreaterThanOp, j)
        Children.append(out2["node"])
        output["index"] = out2["index"]

    elif (j < len(Tokens)) and Tokens_Dict['Lex'] == "<":
        out3 = Match(Token_type.LessThanOp, j)
        Children.append(out3["node"])
        output["index"] = out3["index"]

    elif (j < len(Tokens)) and Tokens_Dict['Lex'] == "<=":
        out4 = Match(Token_type.LessThanequalOp, j)
        Children.append(out4["node"])
        output["index"] = out4["index"]

    elif (j < len(Tokens)) and Tokens_Dict['Lex'] == ">=":
        out5 = Match(Token_type.GreaterThanequalOp, j)
        Children.append(out5["node"])
        output["index"] = out5["index"]

    else:
        errors.append("Syntax error: Expected Reloperator")
        Children.append(errors[len(errors) - 1])
        output["index"] = j

    node = Tree('RelOp', Children)
    output["node"] = node

    return output


def Incrementation(j):
    Children = []
    output = dict()

    if (j < len(Tokens)):
        Tokens_Dict = Tokens[j].to_dict()

    if (j < len(Tokens)) and Tokens_Dict['Lex'] == "incf":
        out1 = Match(Token_type.incf, j)
        Children.append(out1["node"])
        output["index"] = out1["index"]

    elif (j < len(Tokens)) and Tokens_Dict['Lex'] == "decf":
        out2 = Match(Token_type.decf, j)
        Children.append(out2["node"])
        output["index"] = out2["index"]

    else:
        errors.append("Syntax error: Expected Incoperator")
        Children.append(errors[len(errors) - 1])
        output["index"] = j

    node = Tree('Incrementation', Children)
    output["node"] = node

    return output


def IncrementVar(j):
    Children = []
    output = dict()

    if (j < len(Tokens)):
        Tokens_Dict = Tokens[j].to_dict()

    if (j < len(Tokens)) and (re.match("^[a-zA-Z][a-zA-Z0-9]*$", Tokens_Dict['Lex']) or re.match("^[0-9]\.?[0-9]*?$",
                                                                                                 Tokens_Dict['Lex'])):
        Factor_dict = Factor(j)
        Children.append(Factor_dict["node"])

    else:
        return

    node = Tree('IncrementVar', Children)
    output["node"] = node
    output["index"] = Factor_dict["index"]
    return output


def LogicalOp(j):
    Children = []
    output = dict()

    if (j < len(Tokens)):
        Tokens_Dict = Tokens[j].to_dict()

    if (j < len(Tokens)) and Tokens_Dict['Lex'] == "not":
        out1 = Match(Token_type.NOT, j)
        Children.append(out1["node"])
        output["index"] = out1["index"]

    elif (j < len(Tokens)) and Tokens_Dict['Lex'] == "and":
        out2 = Match(Token_type.AND, j)
        Children.append(out2["node"])
        output["index"] = out2["index"]

    elif (j < len(Tokens)) and Tokens_Dict['Lex'] == "or":
        out3 = Match(Token_type.OR, j)
        Children.append(out3["node"])
        output["index"] = out3["index"]

    else:
        errors.append("Syntax error: Expected Logicaloperator")
        Children.append(errors[len(errors) - 1])
        output["index"] = j

    node = Tree('LogicalOp', Children)
    output["node"] = node

    return output


def BoolExp(j):
    Children = []
    output = dict()

    Logic_Dict = LogicalOp(j)
    Children.append(Logic_Dict["node"])

    BoolDash_Dict1 = BoolExpDash(Logic_Dict["index"])
    if BoolDash_Dict1:
        Children.append(BoolDash_Dict1["node"])
    index = BoolDash_Dict1["index"] if BoolDash_Dict1 else Logic_Dict["index"]

    BoolDash_Dict2 = BoolExpDash(index)
    if BoolDash_Dict2:
        Children.append(BoolDash_Dict2["node"])
    index2 = BoolDash_Dict2["index"] if BoolDash_Dict2 else index

    node = Tree('BoolExp', Children)
    output["node"] = node
    output["index"] = index2

    return output


def BoolExpDash(j):
    Children = []
    output = dict()

    if (j < len(Tokens)):
        Tokens_Dict = Tokens[j].to_dict()

    if (j < len(Tokens)) and Tokens_Dict['Lex'] == '(':
        out1 = Match(Token_type.open_bracket, j)
        Children.append(out1["node"])
        BoolItem_Dict = BoolItem(out1["index"])
        Children.append(BoolItem_Dict["node"])
        out2 = Match(Token_type.close_bracket, BoolItem_Dict["index"])
        Children.append(out2["node"])
        output["index"] = out2["index"]

    elif (j < len(Tokens)) and (re.match("^[a-zA-Z][a-zA-Z0-9]*$", Tokens_Dict['Lex']) or re.match("^[0-9]\.?[0-9]*?$",
                                                                                                   Tokens_Dict['Lex'])):
        Factor_dict = Factor(j)
        Children.append(Factor_dict["node"])
        output["index"] = Factor_dict["index"]

    elif (j < len(Tokens)) and Tokens_Dict['Lex'] == 'nil':
        out = Match(Token_type.NIL, j)
        Children.append(out["node"])
        output["index"] = out["index"]

    elif (j < len(Tokens)) and Tokens_Dict['Lex'] == 't':
        out = Match(Token_type.T, j)
        Children.append(out["node"])
        output["index"] = out["index"]

    else:
        return

    node = Tree('BoolExpDash', Children)
    output["node"] = node

    return output


def BoolItem(j):
    Children = []
    output = dict()

    if (j < len(Tokens)):
        Tokens_Dict = Tokens[j].to_dict()

    if (j < len(Tokens)) and ((Tokens_Dict['Lex'] in Operators) or (Tokens_Dict['Lex'] in RelOperators)):
        logExp_Dict = LogicExp(j)
        Children.append(logExp_Dict["node"])
        output["index"] = logExp_Dict["index"]

    elif (j < len(Tokens)) and Tokens_Dict['Lex'] in LogicalOperators:
        BoolExp_Dict = BoolExp(j)
        Children.append(BoolExp_Dict["node"])
        output["index"] = BoolExp_Dict["index"]

    else:
        errors.append("Syntax error: Expected Logical Expression or Boolean Expression")
        Children.append(errors[len(errors) - 1])
        output["index"] = j

    node = Tree('BoolItem', Children)
    output["node"] = node

    return output


def LogicExp(j):
    Children = []
    output = dict()

    if (j < len(Tokens)):
        Tokens_Dict = Tokens[j].to_dict()

    if (j < len(Tokens)) and (Tokens_Dict['Lex'] in Operators):
        Exp_Dict = Expression(j)
        Children.append(Exp_Dict["node"])
        output["index"] = Exp_Dict["index"]

    elif (j < len(Tokens)) and (Tokens_Dict['Lex'] in RelOperators):
        Cond_Dict = Condition(j)
        Children.append(Cond_Dict["node"])
        output["index"] = Cond_Dict["index"]

    else:
        errors.append("Syntax error: Expected Logical Expression")
        Children.append(errors[len(errors) - 1])
        output["index"] = j

    node = Tree('LogicExp', Children)
    output["node"] = node

    return output


global m2
m2 = 1


def Expression(j):
    global m2
    Children = []
    output = dict()
    m2 = j

    Op_Dict = Op(j)
    Children.append(Op_Dict["node"])

    ExpDash_Dict1 = ExpDash(Op_Dict["index"])
    Children.append(ExpDash_Dict1["node"])
    m2 = m2+1

    ExpDash_Dict2 = ExpDash(ExpDash_Dict1["index"])
    Children.append(ExpDash_Dict2["node"])
    m2 = m2+1


    Temp = Tokens[m2+1].to_dict()

    if re.match('^[a-zA-Z][a-zA-Z0-9]*$', Temp['Lex']) is not None:
        ExpDash_Dict3 = ExpDash(ExpDash_Dict2["index"])
        Children.append(ExpDash_Dict3["node"])
        node = Tree('Expression', Children)
        output["node"] = node
        output["index"] = ExpDash_Dict3["index"]
    else:
        node = Tree('Expression', Children)
        output["node"] = node
        output["index"] = ExpDash_Dict2["index"]

    return output


def ExpDash(j):
    Children = []
    output = dict()

    if (j < len(Tokens)):
        Tokens_Dict = Tokens[j].to_dict()

    if (j < len(Tokens)) and Tokens_Dict['Lex'] == '(':
        out1 = Match(Token_type.open_bracket, j)
        Children.append(out1["node"])
        Exp_Dict = Expression(out1["index"])
        Children.append(Exp_Dict["node"])
        out2 = Match(Token_type.close_bracket, Exp_Dict["index"])
        Children.append(out2["node"])
        output["index"] = out2["index"]

    elif (j < len(Tokens)) and (re.match("^[a-zA-Z][a-zA-Z0-9]*$", Tokens_Dict['Lex']) or re.match("^[0-9]\.?[0-9]*?$",
                                                                                                   Tokens_Dict['Lex'])):
        Factor_dict = Factor(j)
        Children.append(Factor_dict["node"])
        output["index"] = Factor_dict["index"]

    else:
        errors.append("Syntax error: Expected Expression or identifier or constant")
        Children.append(errors[len(errors) - 1])
        output["index"] = j

    node = Tree('ExpDash', Children)
    output["node"] = node

    return output


def Match(a, j):
    output = dict()
    if (j < len(Tokens)):
        Temp = Tokens[j].to_dict()
        if (Temp['token_type'] == a):
            j += 1
            output["node"] = [Temp['Lex']]
            output["index"] = j
            return output
        elif ((Temp['token_type'] != a) and (
                (Temp['Lex'] in ReservedWords) or (Temp['Lex'] in Operators) or (Temp['Lex'] in RelOperators) or (
                Temp['Lex'] in LogicalOperators) or (Temp['Lex'] in IncOperators))):
            output["node"] = ["Syntax error : " + " Expected " + str(a.name)]
            output["index"] = j + 1
            errors.append("Syntax error : " + " Expected " + str(a.name))
            return output
        else:
            output["node"] = ["Syntax error : " + " Expected " + str(a.name)]
            output["index"] = j
            errors.append("Syntax error : " + " Expected " + str(a.name))
            return output
    else:
        output["node"] = ["Syntax error: Close Bracket expected"]
        errors.append("Syntax error: Close Bracket expected")
        output["index"] = j + 1
        return output


# GUI


global ImageCounter
ImageCounter = 0
