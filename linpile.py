import os
import sys

cls_com = "clears"
os.system(cls_com)

compile_commands = []
compile_options = []

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
	if c == "'" or c == '"' or c == "|":
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

print(splitstack)
counti = 0

stack = []
tabstack = []
finalstack = []

for i in splitstack:
	rem = i.split("\n")
	tabstack.extend(rem)

	counti += 1

for i in range(len(tabstack)):
	if tabstack[i].startswith("\t"):
		for c in range(len(tabstack[i])):
			if tabstack[i][c] == "\t": finalstack.append("\t")
		finalstack.append(tabstack[i].replace("\t", ""))
	else: finalstack.append(tabstack[i])

print(finalstack)
stack = finalstack

output = ""
counter = 0

ignores = [
	"op",
	"hop",
	"chop",
	"callproc",
	"ncallproc",
        "if",
	"#",
	"as",
        "+",
        "+=",
        "-=",
        "-",
        "*",
        "*=",
        "/",
        "/=",
]

print(stack)

for i in stack:

	# Push printing
	if i == "push":
		if stack[counter+1] not in ignores:
			output += "echo " + stack[counter+1]
		else:
			output += "echo "

	if i == "pull":
		if stack[counter+1] not in ignores:
			output += "var " + stack[counter+1] + " = readLine(" + stack[counter+2] + ")"

	elif i == "#param{":
		for j in stack[counter+1:]:
			if j == "}#endparam":
				break
			elif j.startswith("--") or j.startswith("-"):
				if len(compile_options) != 1:
					compile_options.append(j)
				else:
					compile_options.append(" ")
					compile_options.append(j)
			else:
				if len(compile_commands) != 1:
					compile_commands.append(j)
				else:
					compile_commands.append(" ")
					compile_commands.append(j)

	elif i == "#dec{":
		for j in stack[counter+1:]:
			if j == "}#enddec":
				break
			else:
				if j != '' and j != 'endl':
					decimal_value = int(j)
					ascii_value = chr(decimal_value)
					output += ascii_value
				elif j == 'endl':
					output += "\n"

	elif i == "#hex{":
		for j in stack[counter+1:]:
			if j == "}#endhex":
				break
			else:
				if j != '' and j != 'endl':
					hex_value = j[2:]
					bytes_object = bytes.fromhex(hex_value)
					ascii_value = bytes_object.decode("ASCII")
					output += ascii_value
				elif j == 'endl':
					output += "\n"

	# End line and Create new line
	elif i == "end":
		output += "\n"

	elif i == "when":
                output += "when "

	elif i == "group":
		if stack[counter+1] == "VAR":
			output += "var"
		elif stack[counter+1] == "TYPE":
			output += "type"
		elif stack[counter+1] == "CONST":
			output += "const"
		elif stack[counter+1] == "PER":
			output += "let"

	elif i == "include":
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

	elif i == "+=":
				output += stack[counter+1] + " += " + stack[counter+2]

	elif i == "+":
			output += stack[counter+1] + " + " + stack[counter+2]

	elif i == "-=":
			output += stack[counter+1] + " -= " + stack[counter+2]

	elif i == "-":
			output += stack[counter+1] + " - " + stack[counter+2]

	elif i == "*=":
			output += stack[counter+1] + " *= " + stack[counter+2]

	elif i == "*":
			output += stack[counter+1] + " * " + stack[counter+2]

	elif i == "/=":
			output += stack[counter+1] + " /= " + stack[counter+2]

	elif i == "/":
			output += stack[counter+1] + " / " + stack[counter+2]
				
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
		if stack[counter+2] not in ignores and stack[counter+1] != "as":
			output += "let " + stack[counter+1] + " = " + stack[counter+2]
		elif stack[counter+1] == "as":
			output += "let " + stack[counter+3] + ": " + stack[counter+2] + " = " + stack[counter+4]
		else:
			output += "let " + stack[counter+1] + " = "

	# Standard variables
	elif i == "obj":
		if stack[counter+2] not in ignores and stack[counter+1] != "as":
			output += "var " + stack[counter+1] + " = " + stack[counter+2]
		elif stack[counter+1] == "as":
			output += "var " + stack[counter+3] + ": " + stack[counter+2] + " = " + stack[counter+4]
		else:
			output += "var " + stack[counter+1] + " = "

	# Constant containers
	elif i == "const":
		if stack[counter+2] not in ignores and stack[counter+1] != "as":
			output += "const " + stack[counter+1] + " = " + stack[counter+2]
		elif stack[counter+1] == "as":
			output += "const " + stack[counter+3] + ": " + stack[counter+2] + " = " + stack[counter+4]
		else:
			output += "const " + stack[counter+1] + " = "

	# Setting references
	elif i == "ref":
		if stack[counter+2] not in ignores:
			output += stack[counter+1] + " = " + stack[counter+2]
		else:
			output += stack[counter+1] + " = "
	elif i == "make":
		if stack[counter+1] == "err":
        		output += "error " + stack[counter+2]

	# Super pop char
	elif i == "chop":
		output -= " "

	elif i == "use":
		if stack[counter+1] not in ignores:
			output += "import " + stack[counter+1]
		else:
			output += "import "

	elif i == ".":
		if stack[counter+1] not in ignores and stack[counter+2] not in ignores and stack[counter+1] != "stdout" and stack[counter+2] != "write":
			output += stack[counter+1] + "." + stack[counter+2]
		elif stack[counter+1] == "stdout" and stack[counter+2] == "write":
								output += stack[counter+1] + "." + stack[counter+2] + " " + stack[counter+3]
		else:
			output += stack[counter+1] + "."

	elif i == "nap":
		output += "sleep " + stack[counter+1]
	counter += 1

fw = open(sys.argv[2] + ".nim", "w")
fw.write(output)
fw.close()

com_commands = ""
com_options = ""

for command in compile_commands:
	com_commands += command

for option in compile_options:
	com_options += option

os.system(cls_com)
print("nim " + com_commands + " " + com_options + " " + sys.argv[2] + ".nim")
os.system("nim " + com_commands + " " + com_options + " " + sys.argv[2] + ".nim")
