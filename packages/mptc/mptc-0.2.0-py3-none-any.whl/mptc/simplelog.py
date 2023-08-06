import logging
import time


logger=None
coloured_prints = True

def init_log(filename = "log", f_level = logging.DEBUG, s_level = logging.ERROR, date=False, mode='w', log_level = logging.DEBUG, coloured = True):
	
	global logger
	global coloured_prints
	
	coloured_prints = coloured
	
	if filename[len(filename)-3:] == ".py":
		filename = filename[:len(filename)-3]
	elif filename[len(filename)-4:] == ".log":
		filename = filename[:len(filename)-4]
		
	filename+=".log"
	
	logger = logging.getLogger(__name__)
	logger.setLevel(log_level)
	
	sh = logging.StreamHandler()
	sh.setLevel(s_level)
	
	fh = logging.FileHandler(filename, mode=mode)
	fh.setLevel(f_level)
	
	
	if date:
		date = "[%Y-%m-%d "
	else:
		date = "["
		
		
	time_format = date + "%H:%M:%S]"
		
	formatter = logging.Formatter("%(asctime)s[%(levelname)s]: %(message)s", time_format)
		
	
	sh.setFormatter(formatter)
	fh.setFormatter(formatter)
	
	logger.addHandler(fh)
	#logger.addHandler(sh)

def log(msg, level = 0, _print = False, space=False):
	c=38
	bg=48
	global coloured_prints
	
	if space:
		msg+="\n"
	
	if level == 0 or level == "debug":
		logger.debug(msg)
	elif level == 1 or level == "info":
		logger.info(msg)
		c = 32
	elif level == 2 or level == "warning":
		logger.warning(msg)
		c = 33
	elif level == 3 or level == "error":
		logger.error(msg)
		c = 31
	elif level == 4 or level == "exception":
		logger.exception(msg, exc_info=True)
		c = 31
	elif level == 5 or level == "critical":
		logger.critical(msg)
		c = 31
	else:
		print("Invalid level")
		
	if _print:
		if coloured_prints:
			out = f"\033[{c};{bg}m{msg}\033[0m"
		else:
			out = msg
		print(out)

