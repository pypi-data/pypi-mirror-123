"""Coloured strings and splashcreens. """
from copy import deepcopy, copy
from collections import UserString
from os import popen
import random
from time import sleep
from functools import partial

start = "\033[" #escape character
end = "\033[0m" #escape sequence end

terminal_y, terminal_x = popen('stty size', 'r').read().split()

ty, tx = int(terminal_y), int(terminal_x)

ri = 0

#Colour dictionary
colours = { "black":0, "red":1,"green":2,
					"yellow":3,"blue":4,"purple":5,
					"cyan":6,"gray":7,"lred":8,
					"lgreen":9,"lyellow":10,
					"lblue":11,"lpurple":12,
					"lcyan":13,"white":14 }
					
colours_list = [ "black", "red", "green",
						   "yellow", "blue", "purple",
						   "cyan", "gray", "lred",
						   "lgreen", "lyellow", "lblue",
						   "lpurple", "lcyan", "white" ]


def _ct(text, fg = 14, bg = 0, bold = False, underline = False, invert = False, p = False):
	""" Colours text
	text: The text to colour (str)
	fg: the foreground colour (int or str) correlates to the colour dict
	bg: the background colour (int or str) correlates to the colour dict
	bold: makes the text bold (bool)
	underline: underlines the text (bool)
	invert: inverts the texts colours (bool)
	p: if True prints the coloured text (bool)
	
	returns tuple (coloured text, uncoloured text)
	"""
	# if string get colour from colour dict
	if fg in colours_list:
		fg = colours[fg]
	elif type(fg) == str:
		fg = int(fg)
	if bg in colours_list:
		bg = colours[bg]
	elif type(bg) == str:
		bg = int(bg)
	
	#set font strings
	bold = "\033[1m" if bold else ""
	underline = "\033[4m" if underline else ""
	invert = "\033[7m" if invert else ""
	tstart = bold + underline + invert + start
	
	# if colour > 7 set bright colours
	try:
		if fg <= 6:
			fg += 30
		else:
			fg += 83
		if bg <= 6:
			bg += 40
		else:
			bg += 93
	except:
		fg = 14
		bg = 0
	
	#putting it all together
	tstart = tstart + str(fg) + ";" + str(bg)
	out = tstart + "m" + str(text) + end
	
	#printing and returning the result as a tuple [0] is the coloured text [1] is uncoloured
	if p: print(out) 
	return [out, text]

class Coloured_Str(UserString):
	
	def __init__(self, text="", fg=14, bg=0, b=False, u=False, i=False, subs = None, pre = False, justification = -1, width = tx):
		self.width = width
		self.justification = justification
		self.pre = pre
		self.coloured = None
		length = [0,len(text)-1] if len(text) > 1 else [0,0]
		self.data = ""
		if text != "":
			cformat = [text, fg, bg, b, u, i, length]
		
			self.substrings = [cformat]
		
			self.plain = cformat[0]
			self.csubstrings = [_ct(*cformat[0:-1])]
			self.refresh()

		else:
			self.plain = ""
			self.substrings = []
			
		if subs != None:
			for sub in subs:
				self.substrings.append(sub)
				self.refresh()
			
		
			
	def refresh(self):
		self.plain = ""
		for string in self.substrings:
			self.plain += string[0]
		self.data = self.plain
		if self.pre:
			self.coloured = self.flatten()
		else:
			self.coloured = "Not precomputed, use str(Coloured_Str) instead"

			
			
			
	def __len__(self, colour = False):
		self.refresh()
		if not colour:
			return len(self.plain)
		return len(str(self))
	
	def __str__(self, x = True):
		if len(self) > self.width and x and self.justification != -1:
			#print("multiline width:", self.width)
			new = self.split_length(self.width)
			return new.__str__(False)
		
		out = ""
		if self.justification == 0:
			if len(self) < tx:
				new = copy(self)
				new.justification = -1
				new = new.center(tx)
				for string in new.substrings:
					out += _ct(*string[:-1])[0]
				return str(out)
			
		elif self.justification == 1:
			if len(self) < tx:
				space = tx - len(self)
				space = " " * space
				new = copy(self)
				new = space + new
				for string in new.substrings:
					out += _ct(*string[:-1])[0]
				return str(out)
		for string in self.substrings:
			out += _ct(*string[:-1])[0]
		return str(out)
		
	def __repr__(self):
		if len(self.substrings) < 2:
			if len(self.substrings) == 0:
				return "Coloured_Str(empty = True)"
			f = str(self.substrings[0][0:5])[1:-1]
			return f"Coloured_Str({f})"
		return f"Coloured_Str(subs = {tuple(self.substrings)})"
		
	def __add__(self, other):
		
		new = deepcopy(self)
		if type(other) != Coloured_Str:
			new.substrings.append([(str(other)), 14, 0, False, False, False, [len(new), len(new)+len(str(other))-1]])
			new.refresh()
			return new
		"""
		if len(new.substrings[-1]) == 7:
			i = new.substrings[-1][-1][1]-1
		else:
			i = 0
			
		for string in other.substrings:
			
			new.substrings.append(string)
			
			#print(new.substrings[-1])
			if len(new.substrings[-1]) == 7:
				new.substrings[-1][-1][0] = i+2
			i += len(string[0])-1
			if len(new.substrings[-1]) == 7:
				new.substrings[-1][-1][1] = i+2
			i+=1
		"""
		new.substrings = new.substrings + other.substrings
		new.refresh()
		return new
		
	def __radd__(self, other):
		if other == "":
			return copy(self)
		new = Coloured_Str()
		new.substrings.append([str(other), 14, 0, False, False, False, [len(new), len(new)+len(str(other))-1]])
		
		for string in self.substrings:
			new.substrings.append(deepcopy(string))
		
		new.refresh()
		return new
		
	def __mul__(self, other):
		if type(other) == int:
			new = deepcopy(self)
			for _ in range(1, other):
				new += deepcopy(self)
			new.refresh()
			return new
	
	def split_length(self, length = tx):
		cw = 0
		lines = []
		out = ""
		for i in self.plain:
			cw+=1
			if cw >= length:
				lines.append(out + i)
				out = ""
				cw = 0
			else:
				out += i
				
		if out != "":
			lines.append(out)
			
		out = ""
		
		#print(lines)
		for i, line in enumerate(lines):
			if self.justification == 0:
				if length < tx:
					space = " " * (tx - length)
				else:
					space = tx - len(line)
					if space > 0:
						#print("space")
						space = " " * space 
					else:
						space = ""
				if i == len(lines)-1:
					#print("break")
					out += "\n" + line
				else:
					#print("line")
					out += line
			
			if self.justification == 1:
				if length < tx:
					space = " " * (tx - length)
				else:
					space = tx - len(line)
					if space > 0:
						#print("Right")
						space = " " * space 
					else:
						space = ""
						
				if i == len(lines)-1:
					#print("break")
					out += "\n" + line
				else:
					#print("line")
					out += line
		i = 1
		si = 0
		subs = deepcopy(self.substrings)
		string = ""
		l = 0
		#print(list(out))
		x = ""
		for char in out:
			
			if char == "\n":
				#print(si)
				l = si
				continue
			#print(subs[si])
			if i > len(subs[si][0]):
				subs[si][0] = x + string
				i = 1
				#print(f"added {string}")
				string = ""
				si += 1
				x = ""
			else:
				string += char
				i += 1
				if i > len(subs[si][0]):
					subs[si][0] = x + string
					i = 1
					#print(f"added {string}")
					string = ""
					si += 1
					x = ""
					
				#print(f"string: {string}")
				
		#print(subs[l])
		if self.justification == 1:
			i = len(self) % length
			#print(i, "chars after space")
			ssi = len(self.substrings)
			for string in subs[::-1]:
				ssi -= 1
				si = len(string[0])
				for char in string[0][::-1]:
					i -= 1
					si -= 1
					if i == 0:
						#print("start", si)
						string[0] = string[0][0:si] +space + string[0][si:]
						subs[ssi][0] = string[0]
			#subs[l][0] = space + subs[l][0]
			
		if self.justification == 0:
			hspace = " " * int(len(space)/2)
			
			i = len(self) % length
			#print(i, "chars after space")
			ssi = len(self.substrings)
			for string in subs[::-1]:
				ssi -= 1
				si = len(string[0])
				for char in string[0][::-1]:
					i -= 1
					si -= 1
					if i == 0:
						#print("start", si)
						string[0] = string[0][0:si] +hspace + string[0][si:]
						subs[ssi][0] = string[0]
						subs[-1][0] = subs[-1][0] + hspace
			#subs[l][0] = hspace + subs[l][0]
			#subs[-1][0] = subs[-1][0] + hspace
		#print(subs[i])
		out = cs(subs=subs)
				
		
		"""
		new = copy(self)
		cw = 0
		strings = []
		newsubs = []
		s=""
		for i, sub in enumerate(new.substrings):
			newsub = copy(sub)
			for char in sub[0]:
				if cw + 1 > length + 2:
					newsub[0] = s
					s=""
					newsubs.append(newsub)
					cw = 0
					s += char
					strings.append(newsubs)
					newsubs = []
					newsub = copy(sub) 
				else:
					newsub[0] = s
					cw += 1
					s += char
			#newsubs.append(newsub)
		#print(strings)
		out = ""
		for string in strings:
			part = cs(subs=string)
			out += part + "\n" 
		"""	
		return out
				
					
					
				
			
			
			
		
	def center(self, n = tx, bg = 0, bg2 = None, pulse = False, offset = False, edge = False):
		#self.split_length()
			
		ls, rs = "", ""
		
		if pulse:
			if type(bg) == int:
				if bg2 is not None:
					light = bg
					dark = bg2
				elif bg > 7:
					light = bg
					dark = bg - 7
				else:
					dark = bg
					light = bg + 7
				if dark == 0 or light == 0:
					light, dark = 0, 0
			else:
				if bg[0] == "l":
					light = bg
					dark = bg[1:]
				else:
					dark = bg
					light = "l" + bg
				if dark == 0 or light == 0:
					light, dark = 0, 0
		#print("plain")
		#print(self.plain.center(n))
		for char in list(self.plain.center(n)):
			if char == " ":
				ls += " "
			else:
				break
		
		for char in list(self.plain.center(n))[::-1]:
			if char == " ":
				rs += " "
			else:
				break
		new = deepcopy(self)
		while len(ls + new + rs) > n:
			#print("too long")
			#print(list((ls+new+rs).plain))
			if len(ls + new) > n:
				#print("ls + string too long")
				#print(ls+new)
				break
			rs = rs[:-1]
		
		if pulse:
			outl = ""
			outr = ""
			
			if offset is True:
				bg = dark
			else:
				bg = light
				
			#print("pulsing")
				
			for char in ls:
				if bg == light:
					bg = dark
				else:
					bg = light
				outl += Coloured_Str(char, 0, bg)
			for char in new.plain:
				if bg == light:
					bg = dark
				else:
					bg = light	
			for char in rs:
				if bg == light:
					bg = dark
				else:
					bg = light
				outr += Coloured_Str(char, 0, bg)
			outl.refresh()
			new.refresh()
			outr.refresh()
			if edge is not False:
				outl.substrings[0][2] = edge
				outr.substrings[-1][2] = edge
			return outl + new + outr
				
		#print("out")
		lsf = ls[0]
		ls = ls[0:-1]
		rsl = rs[-1]
		rs = rs[0:-1]
		ls = Coloured_Str(ls, bg, bg, False, False, False)
		rs = Coloured_Str(rs, bg, bg, False, False, False)
		
		if edge is False:
			lsf = Coloured_Str(lsf, bg, bg, False, False, False)
			rsl = Coloured_Str(rsl, bg, bg, False, False, False)
		else:
			lsf = Coloured_Str(lsf, edge, edge, False, False, False)
			rsl = Coloured_Str(rsl, edge, edge, False, False, False)	
		return lsf + ls + new + rs + rsl
		
	def flatten(self):
		return Coloured_Str(str(self))
	
	def flatten_subs(self, fg = None, bg = None, b= False, u = False, i = False):
		if fg is None:
			fg = self.substrings[0][1]
		if bg is None:
			bg = self.substrings[0][2]
		s = ""
		for string in self.substrings:
			s += string[0]
			
		new = Coloured_Str(s, fg, bg, b, u, i)
		return new
	
	def flat_mul(self, other, fg = None, bg = None, b= False, u = False, i = False):
		if fg is None:
			fg = self.substrings[-1][1]
		if bg is None:
			bg = self.substrings[-1][2]
			
		if type(other) == int:
			s = self.plain
			for _ in range(1, other):
				s += self.plain
			new = Coloured_Str(s, fg, bg, b, u, i)
			return new
		
	def rainbow(self, bg = None, b=None, u=None, inv=None, rb=False, rbbg=False, mutate = False, debug = False):
		
		if bg is None:
			bg = self.substrings[0][2]
		if b is None:
			b = self.substrings[0][3]
		if u is None:
			u = self.substrings[0][4]
		if inv is None:
			inv = self.substrings[0][5]
		global ri
		new = self.plain
		bow = [1,3,2,6,4,5,8,10,9,13,11,12]
		for i, char in enumerate(new):
			if rb:
				bg = bow[ri]
			if debug: print(char)
			if i == 0:
				out = Coloured_Str(justification=self.justification)
				if rbbg:
					out.substrings.append([char, 0, bg, b, u, inv, [i,i]])
				else:
					out.substrings.append([char, bow[ri], bg, b, u, inv, [i,i]])
			else:
				if rbbg:
					out.substrings.append([char, 0, bg, b, u, inv, [i,i]])
				else:
					out.substrings.append([char, bow[ri], bg, b, u, inv, [i,i]])
			
			if ri >= 11:
				ri = 0
			else:
				if char != " ":
					ri +=1
					
		if mutate is True:
			self.substrings = out.substrings
			self.refresh()
			return self
		else:
			if debug: print("returned")
			out.refresh()
			return out
			
	def __getitem__(self, key):
			
		if type(key) == slice:
			if type(key.start) == float or type(key.stop) == float:
				if type(key.start) == float:
					kstart = str(key.start).split(".")
					kstart[0] = int(kstart[0])
					kstart[1] = int(kstart[1])
				elif key.start == None:
					kstart = [0,0]
				else:
					kstart = [key.start, 0]
					
				if type(key.stop) == float:
					kstop = str(key.start).split(".")
					kstop[0] = int(kstop[0])
					kstop[1] = int(kstop[1])
				elif key.stop == None:
					kstop = [len(self.substrings),None]
				else:
					kstop = [key.stop, None]
					
				out = ""
				if key.step < 0:
					kstart, kstop = kstop, kstart
				
				for i in range(kstart[0],kstop[0], key.step):
					string = self.substrings[i-1]
					text = ""
					for char in string[0][::key.step]:
						text+=char
							
					if i == kstop[0]:
						out += Coloured_Str(text[:kstop[1]], string[1], string[2], string[3], string[4])
					if i == kstart[0]:
						out += Coloured_Str(text[kstart[1]:], string[1], string[2], string[3], string[4])
					else:
						if len(string) == 6:
							out += Coloured_Str(text, string[1], string[2], string[3], string[4])
						else:
							out += Coloured_Str(text, string[1], string[2], string[3], string[4])
						
				return out
				
			elif key.step is True or type(key.step) == tuple:
				kstart, kstop = key.start, key.stop
				if key.start == None:
					kstart = 0
				if key.stop == None:
					kstop = len(self.substrings)
				elif key.stop < 0:
					kstop = key.stop * -1
					kstop = len(self.substrings) - kstop
				
				out = ""
				if type(key.step) == tuple:
					for sub in range(kstart, kstop, key.step[0]):
						form = self.substrings[sub]
						out += Coloured_Str(form[0], form[1], form[2], form[3], form[4], form[5])
					return out
				for sub in range(kstart, kstop):
					form = self.substrings[sub]
					out += Coloured_Str(form[0], form[1], form[2], form[3], form[4], form[5])
				return out
			text = self.plain[key.start:key.stop:key.step]
			return text
			
		elif type(key) == float:
			k = str(key)
			k = k.split(".")
			form = self.substrings[int(k[0])]
			start = self.substrings[int(k[0])][0]
			print(start)
			if int(k[1]) > len(start):
				index = int(k[1]) % len(start)
			else:
				index = int(k[1])
			text = start[index]
			return Coloured_Str(text, form[1], form[2], form[3], form[4], form[5])
			
		else:
			return self.substrings[key][0]
			
	def casefold(self):
		new = ""
		for sub in self.substrings:
			add = Coloured_Str(text = sub[0].casefold(), fg = sub[1], bg = sub[2], b = sub[3], u = sub[4], i = sub[5])
			
			new += add
		return new
		
	def capitalize(self):
		new = ""
		for sub in self.substrings:
			add = Coloured_Str(sub[0].capitalize(), fg = sub[1], bg = sub[2], b = sub[3], u = sub[4], i = sub[5])
			
			new += add
		return new
	
	def lower(self):
		lower = ""
		for string in self.substrings:
			lower += Coloured_Str(text = string[0].lower(), fg = string[1], bg = string[2], b = string[3], u = string[4], i = string[5])
		return lower
	
	def upper(self):
		upper = ""
		
		for string in self.substrings:
			upper += Coloured_Str(text = string[0].upper(), fg = string[1], bg = string[2], b = string[3], u = string[4], i = string[5])
		return upper
	
	def __eq__(self, other):
		if self.plain == other:
			return True
		else:
			return False
			
	def __ne__(self, other):
		return not self == other
		
	def __bool__(self):
		if self.plain == "":
			return False
		return True
		
	def __iter__(self):
		i = []
		for string in self.substrings:
			for char in string[0]:
				i.append(Coloured_Str(char, string[1], string[2], string[3], string[4]))
		return iter(i)
		
	def count(self, sub, start=0, stop = None):
		c = 0
		for ch in self.plain[start:stop]:
			if ch == sub:
				c += 1
		return c
		
	def endswith(self, sub, start=0, stop=None):
		if self.plain.endswith(sub, start, stop):
			return True
		return False
		
	def find(self, sub, start = 0, stop = None):
		return self.plain.find(sub, start, stop)
		
		
class _cs(str):
	def __init__(self):
		pass
		
	def __add__(self, literal):
		rbb=False
		rbbg=False
		if literal[len(literal)-1] == "c":
			just = 0
		elif literal[len(literal)-1] == "r":
			just = 1
		else:
			just = -1
		if literal[len(literal)-2:] == "db":
			print("Debug")
			debug = True
			rainbow = False
		elif literal[len(literal)-2:] == "rb":
			rainbow = True
			debug = False
		elif literal[len(literal)-3:] == "rbb":
			rbb = True
			debug = False
			rainbow=True
		elif literal[len(literal)-4:] == "rbbg":
			rbbg=True
			debug=False
			rainbow=True
		else:
			debug = False
			rainbow = False
			
		default = ["", 14, 0, False, False, False, (0,0)]
		strings = []
		string = deepcopy(default)
		format = False
		f = 1
		l = 0
		bit = ""
		for char in literal:
			if char == ":":
				if format == True:
					format = False
					string[6] = [l, len(string[0])+l]
					l = len(string[0]) + 1
					strings.append(string)
					f = 1
					string = deepcopy(default)
				else:
					format = True
			elif format:
				if char == ",":
					if bit in ["True", "true"]:
						string[f] = True
					elif bit in ["False", "false"]:
						string[f] = False
					else:
						try:
							string[f] = int(bit)
						except:
							string[f] = bit
					f += 1
					bit = ""
				elif f <= 5:
					bit += char
			else:
				string[0] += char
		if debug: print(strings)
		if rbbg:
			for string in strings:
				string[1] = 0
			return cs(subs=strings, justification = just).rainbow(rb=True, rbbg=True)
		if rbb:
			return Coloured_Str(subs=strings, justification=just).rainbow(rb=True)
		if rainbow:
			return Coloured_Str(subs=strings, justification=just).rainbow()
		return Coloured_Str(subs=strings, justification=just)
		
def seperator(length = tx, order = (1,8,3,10,2,9,6,13,4,11,5,12), avail = (1,3,2,6,4,5,8,10,9,13,11,12), colour = None, ld = True, edge = False, offset = False):
	out = ""
	i=0
	if colour != None:
		if type(colour) == int:
			if colour > 7:
				light = colour
				dark = colour - 7
			else:
				dark = colour
				light = colour + 7
		else:
			if colour[0] == "l":
				light = colour
				dark = colour[1:]
			else:
				dark = colour
				light = "l" + colour
		if ld:
			if offset:
				dark, light = light, dark
			order = (dark, light)
		else:
			order = colour,
			
	for _ in range(0, length):
		if order != None:
			if i >= len(order):
				i = 0
			out += Coloured_Str(" ", 0, order[i])
			i+=1
		else:
			out += Coloured_Str(" ", 0, random.choice(avail))
	
	if edge:
		out.substrings[0][2] = edge
		out.substrings[-1][2] = edge
	return out

class Splash():
	"""Splash screen for scripts"""
	def __init__(self, title = "Title", sub ="Sub", auth = "By Me", ver = "1.0.0", bg = 0, bg2 = None, textfg = 9, textbg = 0, pulse = False, edges = 2, post = ""):

		if "/" in title:
			f = title
			t = ""
			for char in f[::-1]:
				if char == "/":
					break
				t += char
			title = t[::-1]
		if sub == "Sub":
			sub = "---"
		self.title = title
		self.sub = sub
		self.auth = auth
		self.ver = ver
		self.edges = edges
		self.bg = bg
		self.bg2 = bg2
		self.x = int(terminal_x)
		self.y = int(int(terminal_y)/2)+1
		self.textbg = textbg
		self.textfg = textfg
		self.pulse = pulse
		self.post = post
		self.create()
		
	def create(self):
		self.out = ""
		if self.edges:
			tb_edge = str(seperator(order =(self.edges,)))
		else:
			if self.bg == 0:
				tb_edge = ""
			else:
				if self.pulse:
					if self.bg2 is not None:
						tb_edge = str(seperator(order = (self.bg2, self.bg)))
					else:
						tb_edge = str( seperator(colour=self.bg))
				else:
					if self.bg2 is not None:
						tb_edge = str(seperator(order = (self.bg2, self.bg)))
					else:
						tb_edge = str(seperator(order = (self.bg,), offset=True))
		if self.bg == 0:
			bg_sep = str(seperator(order=(0,), edge=self.edges))
		else:
			if self.pulse:
				if self.bg2 is not None:
					bg_sep = str(seperator(order = (self.bg, self.bg2), offset=True, edge = self.edges))
				else:
					bg_sep = str(seperator(colour=self.bg, offset = True, edge=self.edges))
			else:
				bg_sep = str(seperator(order=(self.bg,), edge=self.edges))
				
		title = cs(self.title, self.textfg, self.textbg, False, True)

		if self.bg2 is not None:
			title = str(title.center(bg=self.bg, bg2 = self.bg2, pulse=self.pulse, offset=False, edge = self.edges))
		else:
			title = str(title.center(bg=self.bg, pulse=self.pulse, offset=False, edge = self.edges))
		
		
		sub = cs(self.sub, self.textfg, self.textbg)
		if self.bg2 is not None:
			sub = str(sub.center(bg=self.bg, bg2 = self.bg2, pulse=self.pulse, edge = self.edges))
		else:
			sub = str(sub.center(bg=self.bg, pulse=self.pulse, edge = self.edges))
		
		
		auth = cs(self.auth, self.textfg, self.textbg)
		if self.bg2 is not None:
			auth = str(auth.center(bg=self.bg, bg2 = self.bg2, pulse=self.pulse, edge = self.edges))
		else:
			auth = str(auth.center(bg=self.bg, pulse=self.pulse, edge = self.edges))
		
		
		ver = cs(self.ver, self.textfg, self.textbg)
		if self.bg2 is not None:
			ver = str(ver.center(bg=self.bg, bg2=self.bg2, pulse=self.pulse, edge = self.edges))
		else:
			ver = str(ver.center(bg=self.bg, pulse=self.pulse, edge = self.edges))
		
		
		self.out += tb_edge + "\n" + bg_sep + "\n" + title + "\n" + bg_sep + "\n" + sub + "\n" + bg_sep + "\n" + auth + "\n" + bg_sep + "\n" + ver + "\n" + bg_sep + "\n" + tb_edge
		
	def __str__(self):
		return self.out
		
	def print(self, clear = False, linger = 0):
		
		if self.post != "":
			print(self) 
			print(self.post)
			print()
		else:
			print(self)
			print()
		
		sleep(linger)
		
		if clear is True:
			import mptc as m
			m.clear()
			
		return self

		
csl = _cs()
cs = Coloured_Str
cs_c = partial(Coloured_Str, justification = 0)
cs_r = partial(Coloured_Str, justification = 1)


if __name__ == "__main__":
	n = cs("Coloured Strings", u=True).rainbow()
	x = Splash(n , "Colour those strings bitch", "by Matt Harris","1.0.0", 8, textbg=1, textfg=14, edges = 14, pulse=True, post = __doc__).print()

	x = cs_r("testitouttestitouttestitouttestiouttestitouttestitouttestitouttestitouttestitouttestitouttestitouttestiouttestitouttestitouttestitouttestitouttestitouttestitouttestitouttestiouttestitouttestitouttestitouttestitout", 2)
	
	x = x.rainbow()
	x.justification = 0
	print(x)
"""
i = "." 


x = cs(str(i))
y = cs_c(str(i))
z = cs_r(str(i))

for _ in range(0,32):
	x.rainbow(mutate = True)
	y.rainbow(mutate = True)
	z.rainbow(mutate = True)

	x += "L"
	y += "C"
	z += "R"
		
	print(x)
	print(y)
	print(z)
"""