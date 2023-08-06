def clean(filename):
	new = []
	pout = False
	pin = False
	indents_fixed = 0
	p_i = False
	p_o = False
	p_c = False
	ops_spaced = 0
	commas_spaced = 0

	with open(filename, "r") as f:
		for line in f:
			if pin:
				print(line)
			new.append(line)

	indents = []
	for line in new:
		i = 0
		indent_end = None
		indent_depth = 0
	
		for ch in line:
			if indent_end == None:
				if ch == " ":
					indent_depth += 0.25
				elif ch == "	":
					indent_depth += 1
			
			if ch not in [" ", "	"]:
				if i == 0:
					indent_end = 0
					break
				indent_end = i
				break
			i += 1
		if p_i:
			print(indent_end, round(indent_depth))
		indent = "	" * round(indent_depth)
		indents.append((indent, indent_end, indent_depth))

	i = 0
	statements = []

	for indent in indents:
		if len(str(indent[2])) >= 3:
			if "." in str(indent[2]):
				indents_fixed += 1
			
		new[i] = indent[0] + new[i][indent[1]:]
		statements.append(new[i][round(indent[2]):len(new[i]) - 1])
		i += 1

	print("")
#print(statements)

	ops = ["*", "+", "-", "/", "%", "=", "<", ">", "&", "!"]
	symb = "()[]:{}"
	x = 0
	allcomlocs = []
	alloplocs = []
	for statement in statements:
	
		oplocs = []
		comlocs = []
		i = 0
		x += 1
		in_str = False
		for c in statement:
			if c in '"':
				if in_str:
					in_str = False
				else:
					in_str = True
				
				
			if c in ops and in_str == False:
				oplocs.append(i)
				
			if c == "," and in_str == False:
				comlocs.append(i)
		
			i += 1
		
		allcomlocs.append(comlocs)
		alloplocs.append(oplocs)
				
		#print(f"Line {x}: Ops: {oplocs}, Commas: {comlocs}")

#print(statements)

	i = 0
	for loc in allcomlocs:
		inserted = 0
		if loc != []:
			for comma in loc:
				try:
					if statements[i][comma + inserted + 1] != " ":
						commas += 1
				except:
					continue
					if inserted == 0:
						if p_c:
							print(statements[i])
					if p_c:
						print(f"Comma without space on line {i} at {comma}")
					statements[i] = statements[i][:comma + inserted] + " " + statements[i][comma + inserted:]
					inserted += 1
				#print(statements[i])
					commas_spaced += 1
		i += 1
	
	i = 0
	for loc in alloplocs:
		inserted = 0
		if loc != []:
			for op in loc:
				post, pre = False, False
				try: 
					if statements[i][op + inserted + 1] != " " and statements[i][op + inserted + 1] not in ops:
						post = True
					if statements[i][op + inserted - 1] != " " and statements[i][op + inserted - 1] not in ops:
						pre = True
				except Exception as e:
					if len(statements[i]) > op + inserted + 1:
						print(e, statements[i])
				pp = "["			
				if pre:
					pp += "Pre"
				pp += "/"
				if post:
					pp += "Post"
				pp += "]"
			
				if pre or post:
					if inserted == 0:
						if p_o: 
							print(statements[i])
					if p_o:
						print(f"Operator without {pp} space on line {i} at {op}")
					if pre:
						ops_spaced += 1
						inserted += 1
						statements[i] = statements[i][:op + inserted - 1] + " " + statements[i][op + inserted - 1:]
					if post:
						ops_spaced += 1
						inserted += 1
						statements[i] = statements[i][:op + inserted] + " " + statements[i][op + inserted:]
					if p_o:
						print(statements[i])
				
					pre, post = False, False
		i += 1

	x = 1, 2, 3, 4, 5, 6, 7, 8, 9

	with open(filename, "w") as f:
		i = 0
		for line in new:
			indent = "\t" * round(indents[i][2])
			f.write(indent + statements[i] + "\n")
			indent = "[tab]" * round(indents[i][2])
			printline = f"\033[42;m> {indent}\033[0m"
			if pout:
				print(printline, statements[i])
			i += 1


	if ops_spaced + commas_spaced + indents_fixed > 1:
		print("Cleaned")
		print(f"Indents Fixed: {indents_fixed}")
		print(f"Commas Spaced: {commas_spaced}")
		print(f"Operators Spaced: {ops_spaced}")
	else:
		print("Already Clean")
	
if __name__ == "__main__":
	clean(__file__)
	
