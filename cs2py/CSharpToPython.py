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
        # this
        # self
        (r"(?P<left>[\r\n]+(([^\"\r\n]*\"[^\"\r\n]+\"[^\"\r\n]*)+|[^\"\r\n]+))this", r"\g<left>self", None, 0),
        # ||
        # or
        (r"\|\|", r"or", None, 0),
        # a.length
        # len(a)
        (r"([a-zA-Z0-9_]+)[ ]*\.[ ]*length", r"len(\1)", None, 0),
        # &&
        # and
        (r"&&", r"and", None, 0),
        # !(...)
        # not (...)
        (r"(?P<left>[\r\n]+(([^\"\r\n]*\"[^\"\r\n]+\"[^\"\r\n]*)+|[^\"\r\n]+))!\((?P<condition>[\S ]+)\)", r"\g<left>not (\g<condition>)", None, 0),
        # // ...
        # # ...
        (r"//([^\r\n]+)", r"#\1",None, 0),
        # i++
        # i+=1
        (r"\+\+", r"+=1",None, 0),
        # i--
        # i-=1
        (r"\-\-", r"-=1",None, 0),
        # for (int i = 0; i < 5; i++){
        #     ....
        # }
        # for i in range(0, 5, 1):
        #     ....
        (r"(?P<blockIndent>[ ]*)for[ ]*\((?P<varType>[\S]+)[ ]*(?P<varName>[\S]+)[ ]*=[ ]*(?P<variable>[\S]+)[ ]*;[ ]*(?P=varName)[ ]*[\S]+[ ]*(?P<number>[\S ]+)[ ]*;[ ]*(?P=varName)[ ]*(\+=|\-=)[ ]*(?P<number2>[\S ]*)[ ]*\){[\r\n]+(?P<body>(?P<indent>[ ]*)[^\r\n]+[\r\n]+((?P=indent)[^\r\n]+[\r\n]+)*)(?P=blockIndent)}", r'\g<blockIndent>for \g<varName> in range(\g<variable>, \g<number>, \g<number2>):\n\g<body>', None, 70),
        # foreach (var i in array){
        #     ....
        # }
        # for i in array:
        #     ....
        (r"(?P<blockIndent>[ ]*)foreach[ ]*\((?P<varType>[\S]+)[ ]*(?P<varName>[\S]+)[ ]*in[ ]*(?P<array>[\S]+)\){[\r\n]+(?P<body>(?P<indent>[ ]*)[^\r\n]+[\r\n]+((?P=indent)[^\r\n]+[\r\n]+)*)(?P=blockIndent)}", r'\g<blockIndent>for \g<varName> in \g<array>:\n\g<body>', None, 70),
        # ;\n
        # \n
        (r"(?P<indent>[ ]*)(?P<line>[\S \t]*);\n", r"\g<indent>\g<line>\n",None, 0),
        # ;
        # \n
        (r"(?P<indent>[ ]*)(?P<line>[\S \t]*);[^\r\n]*;", r"\g<indent>\g<line>\n\g<indent>",None, 0),
        # ;
        # \n
        (r"(?P<indent>[ ]*)(?P<line>[\S \t]*);[^\r\n]*#", r"\g<indent>\g<line> #",None, 0),
        # int i = 0;
        # i = 0;
        (r"(?P<blockIndent>[ ]*)(?P<varType>[\w\[\]]+)[ ]*(?P<varName>\w+)[ ]*=", r'\g<blockIndent>\g<varName> =',None, 0),
        # int[] i = {1, 2, 3};
        # i = [1, 2, 3];
        (r"(?P<blockIndent>[ ]*)(?P<varName>[a-zA-Z0-9_]+)[ ]*=[ ]*{(?P<list>[\S ]+)}", r'\g<blockIndent>\g<varName> = [\g<list>]',None, 0),
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
        (r"\n(?P<blockIndent>[ ]*)if[ ]*\((?P<condition>[\S ]*)\){[\r\n]+(?P<body>(?P<indent>[ ]*)[^\r\n]+[\r\n]+((?P=indent)[^\r\n]+[\r\n]+)*)(?P=blockIndent)}", r'\n\g<blockIndent>if \g<condition>:\n\g<body>', None, 70),
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
        # interface IInterface{
        #     ....
        # }
        # class IInterface:
        #     ....
        (r"(?P<blockIndent>[ ]*)interface[ ]*(?P<interfaceName>[a-zA-Z0-9_]+)[ ]*{[\r\n]+(?P<body>(?P<indent>[ ]*)[^\r\n]+[\r\n]+((?P=indent)[^\r\n]+[\r\n]+)*)(?P=blockIndent)}", r'\g<blockIndent>class \g<interfaceName>:\n\g<body>', None, 70),
        # void test();
        # def test():
        #     pass
        (r"(?P<start>[\r\n]+)(?P<blockIndent>[ ]*)(?P<returnType>\w+)[ ]+(?P<methodName>\w+)[ ]*\((?P<args>[\S ]*)\)", r'\g<start>\g<blockIndent>def \g<methodName>(\g<args>):\n\g<blockIndent>    pass', None, 0),
        # garbage delete
        (r"\n\n", r"\n", None, 0),
        (r"(?P<blockIndent>[ ]*)(?P<blockName>[a-z]+)[ ]*\([ ]*(?P<other>[\S ]*)[ ]*\)[ ]*{[\s]*}", r"\g<blockIndent>\g<blockName> \g<other>:\n\g<blockIndent>    pass", None, 0),
        # better view
        # b==a
        # b == a
        (r"(\S)(==|!=|<=|<|>|>=|=)(\S)", r"\1 \2 \3", None, 0),
        #(r"not \(([\S ]+)(?!and|or)([\S ]+)\)", r"not \1\2", None, 0)
    ]

    LAST_RULES = [
        # python methods:
        (r"Console\.WriteLine\((?P<args>[^\)]+)\)", r"print(\g<args>)", None, 0),
        (r"Console\.Write\((?P<args>[^\)]+)\)", r"sys.stdout.write(\g<args>)", None, 0),
        (r"using[ ]+\w+", r"", None, 0),
        (r"\A", r"import random\nimport math\nimport sys", None, 0),
        (r"([a-zA-Z0-9_]+)\.contains\(([\S ]+)\)", r"\2 in \1", None, 0),
        (r"([a-zA-Z0-9_]+)\.equals\(([\S ]+)\)", r"\1 == \2", None, 0),
        # math module:
        (r"Math\.Abs", r"abs", None, 0),
        (r"Math\.Round", r"round", None, 0),
        (r"Math\.PI", r"math.pi", None, 0),
        (r"Math\.E", r"math.e", None, 0),
        (r"Math\.A(?P<name>[a-z]+)", r"math.a\g<name>", None, 0),
        (r"Math\.B(?P<name>[a-z]+)", r"math.b\g<name>", None, 0),
        (r"Math\.C(?P<name>[a-z]+)", r"math.c\g<name>", None, 0),
        (r"Math\.D(?P<name>[a-z]+)", r"math.d\g<name>", None, 0),
        (r"Math\.E(?P<name>[a-z]+)", r"math.e\g<name>", None, 0),
        (r"Math\.F(?P<name>[a-z]+)", r"math.f\g<name>", None, 0),
        (r"Math\.M(?P<name>[a-z]+)", r"math.m\g<name>", None, 0),
        (r"Math\.R(?P<name>[a-z]+)", r"math.r\g<name>", None, 0),
        (r"Math\.P(?P<name>[a-z]+)", r"math.p\g<name>", None, 0),
        (r"Math\.S(?P<name>[a-z]+)", r"math.s\g<name>", None, 0),
        (r"Math\.T(?P<name>[a-z]+)", r"math.t\g<name>", None, 0),
        # random module:
        (r"new[ ]+Random\(\)\.Next\((?P<first>\d+)[ ]*,[ ]*(?P<second>\d+)\)", r"random.randint(\g<first>, \g<second>+1)", None, 0),
        (r"new[ ]+Random\(\)\.NextDouble\(\)", r"random.uniform(0, 1)", None, 0)
    ]
