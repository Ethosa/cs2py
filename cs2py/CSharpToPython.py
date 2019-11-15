# -*- coding: utf-8 -*-
# author: Ethosa
from retranslator import Translator

class CSharpToPython(Translator):
    def __init__(self, codeString="", extra=[], useRegex=False):
        """initialize class
        
        Keyword Arguments:
            codeString {str} -- source code on C# (default: {""})
            extra {list} -- include your own rules (default: {[]})
            useRegex {bool} -- this parameter tells you to use regex (default: {False})
        """
        self.codeString = codeString
        self.extra = extra
        self.Transform = self.compile = self.translate # callable objects

        # create little magic ...
        self.rules = CSharpToPython.RULES[:]
        self.rules.extend(self.extra)
        self.rules.extend(CSharpToPython.LAST_RULES)
        Translator.__init__(self, codeString, self.rules, useRegex)

    RULES = [
        # true
        # True
        (r"(?P<left>[\r\n]+(([^\"\r\n]*\"[^\"\r\n]+\"[^\"\r\n]*)+|[^\"\r\n]+))true", r"\g<left>True", None, 0),
        # false
        # False
        (r"(?P<left>[\r\n]+(([^\"\r\n]*\"[^\"\r\n]+\"[^\"\r\n]*)+|[^\"\r\n]+))false", r"\g<left>False", None, 0),
        # // ...
        # # ...
        (r"//([^\r\n]+)", r"#\1",None, 0),
        # for (...){
        #     ....
        # }
        # for ... in ...:
        #     ....
        (r"(?P<blockIndent>[ ]*)for[ ]*\((?P<varType>[\S]+)[ ]*(?P<varName>[\S]+)[ ]*=[ ]*(?P<variable>[\S]+)[ ]*;[ ]*(?P=varName)[ ]*[\S]+[ ]*(?P<number>[\S]+)[ ]*;[ ]*(?P=varName)[ ]*(\+=|\-=|\+\+|\-\-)[ ]*(?P<number2>[\S]+)[ ]*\){[\r\n]+(?P<body>(?P<indent>[ ]*)[^\r\n]+[\r\n]+((?P=indent)[^\r\n]+[\r\n]+)*)(?P=blockIndent)}", r'\g<blockIndent>for \g<varName> in range(\g<variable>, \g<number>, \g<number2>):\n\g<body>', None, 70),
        # ;\n
        # \n
        (r"(?P<indent>[ ]*)(?P<line>[\S \t]*);\n", r"\g<indent>\g<line>\n",None, 0),
        # ;
        # \n
        (r"(?P<indent>[ ]*)(?P<line>[\S \t]*);[^\r\n]*;", r"\g<indent>\g<line>\n\g<indent>",None, 10),
        # ;
        # \n
        (r"(?P<indent>[ ]*)(?P<line>[\S \t]*);[^\r\n]*#", r"\g<indent>\g<line> #",None, 10),
        # /* ... */
        # """ ... """
        (r"/\*(?P<comment>[\S\s]+)\*/", r'"""\g<comment>"""',None, 0),
        # else if (...){
        #     ....
        # }
        # elif ...:
        #     ....
        (r"(?P<blockIndent>[ ]*)else if[ ]*\((?P<condition>[\S ]*)\){[\r\n]+(?P<body>(?P<indent>[ ]*)[^\r\n]+[\r\n]+((?P=indent)[^\r\n]+[\r\n]+)*)(?P=blockIndent)}", r'\g<blockIndent>elif \g<condition>:\n\g<body>', None, 70),
        # if (...){
        #     ....
        # }
        # if ...:
        #     ....
        (r"(?P<blockIndent>[ ]*)if[ ]*\((?P<condition>[\S ]*)\){[\r\n]+(?P<body>(?P<indent>[ ]*)[^\r\n]+[\r\n]+((?P=indent)[^\r\n]+[\r\n]+)*)(?P=blockIndent)}", r'\g<blockIndent>if \g<condition>:\n\g<body>', None, 70),
        # else{
        #     ....
        # }
        # else:
        #     ....
        (r"(?P<blockIndent>[ ]*)else[ ]*{[\r\n]+(?P<body>(?P<indent>[ ]*)[^\r\n]+[\r\n]+((?P=indent)[^\r\n]+[\r\n]+)*)(?P=blockIndent)}", r'\g<blockIndent>else:\n\g<body>', None, 70),
        # while (...){
        #     ....
        # }
        # while ...:
        #     ....
        (r"(?P<blockIndent>[ ]*)while[ ]*\((?P<condition>[\S ]*)\){[\r\n]+(?P<body>(?P<indent>[ ]*)[^\r\n]+[\r\n]+((?P=indent)[^\r\n]+[\r\n]+)*)(?P=blockIndent)}", r'\g<blockIndent>while \g<condition>:\n\g<body>', None, 70),
        # garbage delete
        (r"\n\n", r"\n", None, 0)
    ]

    LAST_RULES = []
