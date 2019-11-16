import cs2py
import regex
import re
import math

sourceText = """
using System;

if (0==1){
    int a = 0;
    bool d = true; int asd = 5; string asd1 = "hello world";
    if (1){
        Console.WriteLine("lol");
        Console.Write("ban");
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
            float b = Math.Cos(25) * Math.PI;
            int c = new Random().Next(0, 1000);
            double t = new Random().NextDouble();
            if (!(true || false && 1)) { }
        }
        for (int i = 0; i < 5; i+=1){
            Console.WriteLine(i);
            foreach (var lol in customArray){
                var l = 0;
                if (true){ }
            }
        }
    }
    interface ITest{
        /* test interface.*/
        void test();
    }
    int[] a = {1, 2, 3, 4};
}
"""
translator = cs2py.CSharpToPython(useRegex=1)
print(translator.compile(sourceText))
# sourceText = regex.sub(r"\n(?P<blockIndent>[ ]*)if[ ]*\((?P<condition>[\S ]*)\){[\r\n]+(?P<body>(?P<indent>[ ]*)[^\r\n]+[\r\n]+((?P=indent)[^\r\n]+[\r\n]+)*)(?P=blockIndent)}",
#     r"\n\g<blockIndent>if \g<condition>:\n\g<body>", sourceText)
# print(sourceText)
# print(round(math.e))