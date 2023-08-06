
from os import system, name, path, popen
import time
import math
from . import cleanup
from . import simplelog
from copy import copy, deepcopy
from .ColouredStrings import *
from .ColouredStrings import _cs, _ct, ri

terminal_y, terminal_x = popen('stty size', 'r').read().split()

terminal_y, terminal_x = int(terminal_y), int(terminal_x)



start = "\033[" #escape character
end = "\033[0m" #escape sequence end

def init_log(filename = "log", f_level = simplelog.logging.DEBUG, s_level = simplelog.logging.ERROR, date=False, mode='w', log_level = simplelog.logging.DEBUG, coloured = True):
	""" initialise the simplelog logger """
	simplelog.init_log(filename, f_level, s_level, date, mode, log_level, coloured)


def log(msg, level = 0, _print = False, space=False):
	""" simple logging """
	simplelog.log(msg, level, _print, space)


def truncate(number, digits, pad = True) -> float:
	stepper = 10.0 ** digits
	out = math.trunc(stepper * number) / stepper
	if pad:
	   while len(str(out).split(".")[1]) < digits:
	   	out = str(out) + "0"
	return out
	   	
    

def clean(file = None):
	""" cleans up the file to make it more readable. Spacing commas and operators and making all indemts tabs """
	while not path.exists(file):
		file = input("File")
		if file == "q":
			return
	cleanup.clean(file)


class TFont():
	""" Font class for repetitive use of a ct() function with saved params """
	
	def __init__(self, fg = 14, bg = 0, b = False, u = False, invert = False):
		self.fg = fg #foreground
		self.bg = bg #background
		self.b = b #bold
		self.u = u #underline
		self.i = invert #invert


	def use(self, text, p = False):
		""" use the stored ct() function """
		out = _ct(text, self.fg, self.bg, self.b, self.u, self.i, p)
		return  out
	
	def invert(self):
		""" flipflop the inverted value """
		if self.i:
			self.i = False
		else:
			self.i = True
	
	def bold(self):
		""" flipflop the bold value """
		if self.b:
			self.b = False
		else:
			self.b = True
			
	def underline(self):
		""" flipflop the underline value """
		if self.u:
			self.u = False
		else:
			self.u = True


	def highlight(self, text, word, count =- 1, p = False):
		""" highlight the word in the text with the font, count is the amount of occurences to colour -1 is all """
		
		r = _ct(word, self.fg, self.bg, self.b, self.u, self.i, False)[0] #coloured replacement
		
		#replacing the word
		out = text.replace(word, r, count)
		if p: print(out)
		return out


def time_to_run(function, *args, ret = False, pargs = False,  p = True, ** kwargs):
	""" prints the time in seconds it takes to
	execute the function. to call put the
	function and then follow it with the
	arguments and kwargs like so:
	time_to_run(print(), "Hello World") """
	
	time_start = time.time()
	if ret:
		result = function(*args, **kwargs)
	else:
		function(*args, **kwargs)
		
	took = time.time() - time_start
	if pargs:
		if p: print(f"\n----{function.__name__} Took {took} seconds to run----\nArgs: {args}\nKwargs: {kwargs}\n")
	else:
		if p: print(f"\n----{function.__name__} Took {took} seconds to run----")
	if ret:
		return result, took
	return took

def clear(): 
	""" Clears the console """
	if name == 'nt': 
		_ = system('cls') 
	else: 
		_ = system('clear')
_c = clear

def rl(length = 1):
	""" carriage return via escape sequence"""
	print("", end = "\r")
	#space = " " * length
	#print (f"\033[A{space}\033[A", end = "")


def loading_bar(dur = 0, fg = 14, bg = 3, char = " ", done = " Done ", tick = True, pct = 0, hide = True, linger = 2):
	""" prints a loading bar. if tick is true it fake progresses to complete with a delay of s otherwise it prints once with pct being percent. done is the message to print at the end of the bar when wt 100% """
	#1 bar segment
	segment = _ct(char, fg, bg)[0] 
	
	#fake progress
	elapsed = 0
	if dur == 0:
		for k in range(0, 51):
			bar = segment * k
			if k == 100:
				percent = _ct(done, fg, bg)[0]
			else:
				percent = _ct(str(round(51 / 100) * k * 2) + "%",  14)[0]
	
			print("\r" + bar + percent, end = "")
		print("\r" + bar + percent, done, end = "")
	else:
		s = dur/51
		for k in range(0, tx-len(done)):
			bar = segment * k
			if k == 100:
				percent = _ct(done, fg, bg)[0]
			else:
				percent = _ct(str(round(tx-len(done) / 100) * k * 2) + "%",  14)[0]
				
			time.sleep(s)
			print("\r" + bar + cs(">", bg) + percent, end = "")
			
		print("\r" + bar + cs(done, bg, "gray"), end="")
		if hide:
			time.sleep(linger)
			print("\r", end="")
		else:
			print()
		
			
			
	
def loading_wheel(string = "Please wait... ", complete = False, completem="Done",  frame = 0, Anim = ["|", "/", "-", "\\", "|", "/", "-", "\\","|", "/", "-", "\\", "|", "/", "-", "\\"], delay = .1, fg = 14, bg = 0, rainbow = False, dur = 0, hide=True, linger=2, center = False, rb=False):
	""" loading wheel text widget. prints the given frame from the given Animation. with built in delay and bg/fg colours """
	rainbows = [1,3,2,6,4,5,8,10,9,13,11,12]
	global ri
	for ai, f in enumerate(Anim): #colouring frames
		if rainbow:
			Anim[ai] = _ct(Anim[ai], rainbows[ri], bg)[0]
			ri += 1
			if ri >= len(rainbows):
				ri = 0
		else:
			Anim[ai] = _ct(Anim[ai], fg, bg)[0]
			
		ai += 1
		
	
	#printing it out
	elapsed = 0
	while True:
		fra = frame % len(Anim) #current frame
		if dur != 0 and elapsed >= dur:
			if rb:
				wheel = cs(completem,fg,bg).rainbow()
			else:
				wheel = cs(completem,fg,bg)
			if center:
				print("\r", wheel.center(), end = "\r", sep="")
			else:
				print("\r", wheel, end="\r", sep="")
			if hide:
				time.sleep(linger)
				print("\r", end = "")
			break
		else:
			if complete == False:
				wheel = string + Anim[fra]
			else: # add the completion message
				wheel = string + completem
			print("\r" + wheel + "  ", end = "")
			if complete:
				break
		time.sleep(delay)
		elapsed += delay
		frame+=1
	

def faster(f1, f2, fname1="Function 1", fname2="Function 2", thresh = 0.002):
	
	print(f"Running: {fname1}")
	o1, t1 = time_to_run(f1, ret=True, p=False)
	print(f"Running: {fname2}")
	o2, t2 = time_to_run(f2, ret=True, p=False)
	

	if (t2 >= t1 and (t2 - t1) <= thresh) or (t1 >= t2 and (t1 - t2) <= thresh) or t2 == t1:
		print(f"{fname2} and {fname1} both took ~{t1} secs")
	elif t2 < t1:
		print(f"{fname2} faster than {fname1} by {t1-t2} seconds")
	else:
		print(f"{fname1} faster than {fname2} by {t2-t1}")
		
	return o1, o2
	
#Loading wheel anims
anim_bubble = ["•", "°", "o", "0", "O", "@","•", "°", "o", "0", "O", "@"]
anim_spin = ["|", "/", "-", "\\", "|", "/", "-", "\\","|", "/", "-", "\\", "|", "/", "-", "\\"]
anim_arrow = [">==", "=>=", "==>", "===",">==", "=>=", "==>", "==="]

