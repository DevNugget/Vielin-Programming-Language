from compileall import compile_file
import os
import compiler
import sys

cls_com = "clear"
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

for i in splitstack:
    bel = ""
    rem = i.split("\n")
    stack.extend(rem)
        
    counti += 1

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
    "callproc"
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
        output += "proc " + stack[counter+1]
        
    # Function arguements        
    elif i == "args":
        output += stack[counter+1] + ")"

    # Function body declaration   
    elif i == "in":
        output += " = \n"

    # Function return type declaration
    elif i == "--":
        output += ": " + stack[counter+1]

    # Function opening    
    elif i == "def":
        output += "("

    # Tab notation
    elif i == ".":
        output += "    "

    # Function calling
    elif i == "callproc":
        output += stack[counter+1] + "(" + stack[counter+2] + ")"

    # For loops
    elif i == "for":
        if stack[counter+1] != "op" or stack[counter+1] != "hop": 
            ins = convertstr(stack[counter+1])
            ins.pop(0)
            ins.pop(-1)
            reg = ""
            for i in ins:
                reg += i
            output += "for " + reg
        elif stack[counter+1] == "op" or stack[counter+1] != "hop":
            output += "for " 

    # If statements
    elif i == "if":
        if stack[counter+1] != "op" or stack[counter+1] != "hop" or stack[counter+1] != "chop": 
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
        if stack[counter+1] != "op" or stack[counter+1] != "hop": 
            ins = convertstr(stack[counter+1])
            ins.pop(0)
            ins.pop(-1)
            reg = ""
            for i in ins:
                reg += i
            output += "elif " + reg
        elif stack[counter+1] == "op" or stack[counter+1] != "hop":
            output += "elif " 

    # Else cases
    elif i == "else":
        output += "else"

    # Prepocated body declaration
    elif i == "do":
        output += ":\n"

    # If statement matched
    elif i == "then":
        output += ":\n"

    # While loops
    elif i == "during":
        if stack[counter+1] != "op" or stack[counter+1] != "hop": 
            ins = convertstr(stack[counter+1])
            ins.pop(0)
            ins.pop(-1)
            reg = ""
            for i in ins:
                reg += i
            output += "while " + reg
        elif stack[counter+1] == "op" or stack[counter+1] != "hop":
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
        if stack[counter+2] != "$" and stack[counter+2] != "callproc" and stack[counter+1] != "as":
            output += "let " + stack[counter+1] + " = " + stack[counter+2]
        elif stack[counter+1] == "as":
            output += "let " + stack[counter+3] + ": " + stack[counter+2] + " = " + stack[counter+4]
        else:
            output += "let " + stack[counter+1] + " = "

    # Standard variables        
    elif i == "obj":
        if stack[counter+2] != "$" and stack[counter+2] != "callproc" and stack[counter+1] != "as":
            output += "var " + stack[counter+1] + " = " + stack[counter+2]
        elif stack[counter+1] == "as":
            output += "var " + stack[counter+3] + ": " + stack[counter+2] + " = " + stack[counter+4]
        else:
            output += "var " + stack[counter+1] + " = "

    # Constant containers        
    elif i == "const":
        if stack[counter+2] != "$" and stack[counter+2] != "callproc" and stack[counter+1] != "as":
            output += "const " + stack[counter+1] + " = " + stack[counter+2]
        elif stack[counter+1] == "as":
            output += "const " + stack[counter+3] + ": " + stack[counter+2] + " = " + stack[counter+4]
        else:
            output += "const " + stack[counter+1] + " = "

    # Setting references        
    elif i == "ref":
        if stack[counter+2] != "$" and stack[counter+2] != "callproc":
            output += stack[counter+1] + " = " + stack[counter+2]   
        elif stack[counter+2] == "callproc":
            output += stack[counter+1] + " = "

    # Super pop char
    elif i == "chop":
        output -= " "    
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
