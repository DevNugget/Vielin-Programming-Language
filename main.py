from compileall import compile_file
from curses import can_change_color
import os
import re
import sys

cls_com = "clea"
os.system(cls_com)

def convertstr(string):
    list1 = []
    list1[:0]=string
    return list1

f = open(sys.argv[1], "r")
source_content = f.read()
f.close()

splitstack = []

results = [[]]
quote = None
for c in source_content:
  if c == "'" or c == '"':
    if c == quote:
      quote = None
    elif quote == None:
      quote = c
  elif c == ' ':
    if quote == None:
      results.append([])
      continue
  results[-1].append(c)

splitstack = [''.join(x) for x in results]

counti = 0

stack = []
tabstack = []
finalstack = []

for i in splitstack:
    bel = ""
    rem = i.split("\n")
    tabstack.extend(rem)

    counti += 1

tabcounti = 0
charcount = 0

print(tabstack)

for i in range(len(tabstack)):
    if tabstack[i].startswith("\t"):
        for c in range(len(tabstack[i])):
            if tabstack[i][c] == "\t": finalstack.append("\t")
        finalstack.append(tabstack[i].replace("\t", ""))
    else: finalstack.append(tabstack[i])

stack = finalstack

countd = 0
remflit = 0

output = ""
counter = 0
comcounter = 0

for i in stack:
    if i == "com":
        #stack.pop(comcounter)
        stack.pop(comcounter+1)

    comcounter += 1

ignores = [
    "op",
    "hop",
    "chop",
    "callproc",
    "ncallproc",
    "#",
]

print(stack)

for i in stack:

    # Push printing
    if i == "push":
        if stack[counter+1] not in ignores:
            output += "echo " + stack[counter+1]
        else:
            output += "echo "

    # End line and Create new line
    elif i == "end":
        output += "\n"

    # Function declaring
    elif i == "proc":
        if stack[counter+1] not in ignores:
            output += "proc " + stack[counter+1]
        else:
            output += "proc "

    # Function arguements
    elif i == "args":
        output += stack[counter+1] + ")"

    elif i == "nargs":
        output += ")"

    elif i == "pragma":
        output += "{." + stack[counter+1] + ".}"

    # Function body declaration
    elif i == "in":
        if stack[counter-1] != "op":
            output += " = \n"

    # Function return type declaration
    elif i == "--":
        output += ": " + stack[counter+1]

    # Function opening
    elif i == "def":
        output += "("

    # Tab notation
    elif i == "\t":
        if stack[counter-1] == "then":
            output += "    "
        else:
            output += "    "

    # Function calling
    elif i == "callproc":
        if stack[counter+1] not in ignores:
            if stack[counter+2] not in ignores:
                output += stack[counter+1] + "(" + stack[counter+2] + ")"
            elif stack[counter+2] == "callproc":
                stack.pop(counter+2)
                output += stack[counter+1] + "(" + stack[counter+2] + "(" + stack[counter+3] + "))"

    elif i == "ncallproc":
        if stack[counter+1] not in ignores:
            if stack[counter+2] not in ignores:
                output += stack[counter+1] + "()"
            elif stack[counter+2] == "callproc":
                stack.pop(counter+2)
                output += stack[counter+1] + "(" + stack[counter+2] + "(" + stack[counter+3] + "))"
            elif stack[counter+2] == "ncallproc":
                stack.pop(counter+2)
                output += stack[counter+1] + "(" + stack[counter+2] + "())"

    # For loops
    elif i == "for":
        if stack[counter+1] not in ignores:
            ins = convertstr(stack[counter+1])
            ins.pop(0)
            ins.pop(-1)
            reg = ""
            for i in ins:
                reg += i
            output += "for " + reg
        else:
            output += "for "

    elif i == "case":
        output += "case " + stack[counter+1] + "\n"

    elif i == "of":
        output += "of " + stack[counter+1]

    # If statements
    elif i == "if":
        if stack[counter+1] not in ignores:
            ins = convertstr(stack[counter+1])
            ins.pop(0)
            ins.pop(-1)
            reg = ""
            for i in ins:
                reg += i
            output += "if " + reg
        else:
            output += "if "

    # Elif statements
    elif i == "elif":
        if stack[counter+1] not in ignores:
            ins = convertstr(stack[counter+1])
            ins.pop(0)
            ins.pop(-1)
            reg = ""
            for i in ins:
                reg += i
            output += "elif " + reg
        else:
            output += "elif "

    # Else cases
    elif i == "else":
        output += "else"

    # Prepocated body declaration
    elif i == "do":
        output += ":\n"

    # If statement matched
    elif i == "then":
        if stack[counter-2] == "of":
            output += ": "
        else:
            output += ":\n"

    elif i == "dump":
        output += "discard "

    # While loops
    elif i == "during":
        if stack[counter+1] not in ignores:
            ins = convertstr(stack[counter+1])
            ins.pop(0)
            ins.pop(-1)
            reg = ""
            for i in ins:
                reg += i
            output += "while " + reg
        else:
            output += "while "

    # Super push
    elif i == "op":
        output += stack[counter+1]

    # Super space
    elif i == "hop":
        output += " "

    # Returning values
    elif i == "throw":
        output += "return " + stack[counter+1]

    elif i == "per":
        if stack[counter+2] not in ignores:
            output += "let " + stack[counter+1] + " = " + stack[counter+2]
        elif stack[counter+1] == "as":
            output += "let " + stack[counter+3] + ": " + stack[counter+2] + " = " + stack[counter+4]
        else:
            output += "let " + stack[counter+1] + " = "

    # Standard variables
    elif i == "obj":
        if stack[counter+2] not in ignores:
            output += "var " + stack[counter+1] + " = " + stack[counter+2]
        elif stack[counter+1] == "as":
            output += "var " + stack[counter+3] + ": " + stack[counter+2] + " = " + stack[counter+4]
        else:
            output += "var " + stack[counter+1] + " = "

    # Constant containers
    elif i == "const":
        if stack[counter+2] not in ignores:
            output += "const " + stack[counter+1] + " = " + stack[counter+2]
        elif stack[counter+1] == "as":
            output += "const " + stack[counter+3] + ": " + stack[counter+2] + " = " + stack[counter+4]
        else:
            output += "const " + stack[counter+1] + " = "

    # Setting references
    elif i == "ref":
        if stack[counter+2] not in ignores:
            output += stack[counter+1] + " = " + stack[counter+2]
        elif stack[counter+2] == "callproc":
            output += stack[counter+1] + " = "

    # Super pop char
    elif i == "chop":
        output -= " "

    elif i == "use":
        if stack[counter+1] not in ignores:
            output += "import " + stack[counter+1]
        else:
            output += "import "

    elif i == "#":
        if stack[counter+1] not in ignores:
            output += stack[counter+1]
            for i in stack[counter+2:]:
                if i == "end":
                    break
                else:
                    output += "." + i
                
        
    counter += 1

fw = open(sys.argv[2] + ".nim", "w")
fw.write(output)
fw.close()


if sys.argv[3] == "com":
    #compiler.compile_intructions("output.py", "output")
    os.system(cls_com)
    os.system("nim c " + sys.argv[2] +".nim")
    os.system(cls_com)

elif sys.argv[3] == "comd":
    #compiler.compile_intructions("output.py", "output")
    os.system(cls_com)
    os.system("nim c " + sys.argv[2] +".nim")

elif sys.argv[3] == "comr":
    os.system(cls_com)
    #os.system("cd bin")
    os.system("nim c " + sys.argv[2] +".nim")
    os.system(cls_com)
    os.system("./output")
