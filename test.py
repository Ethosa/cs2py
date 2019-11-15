import cs2py
import regex
import re
import math

sourceText = """
using System;
if (0==1){
    int a = 0;
    bool b = true; int asd = 5; string asd1 = "hello world";
    if (1){
        Console.WriteLine("lol");
    }
    while (true){
        if (1){
            a = 0;
        }
        else if (2){
            a = 0; // here is comment
        }
        else{
            a = 0;
        }
        for (int i = 0; i < 5; i+=1){
            Console.WriteLine(i);
        }
    }
}
"""
translator = cs2py.CSharpToPython(useRegex=1)
print(translator.compile(sourceText))
# sourceText = regex.sub(r"(?P<blockIndent>[ ]*)if[ ]*(?P<condition>[\S ]*){[\r\n]+(?P<body>(?P<indent>[ ]*)[^\r\n]+[\r\n]+((?P=indent)[^\r\n]+[\r\n]+)*)(?P=blockIndent)}",
#     r"\g<blockIndent>if \g<condition>:\n\g<body>", sourceText)
# print(sourceText)
# print(round(math.e))