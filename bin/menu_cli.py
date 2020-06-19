import os

def menu(data):
	while True:
		os.system("clear")
		print("")
		if "titel" in data:
			print(data["titel"])
			print("=" * len(data["titel"]))
			print("")
		l = 1
		for x in data["entries"]:
			line = ""
			if l < 10:
				line += " "
			line += str(l)+". "+x
			print(line)
			l += 1
		print("")
		print(" x: "+data["exit"])
		print("")
		selection = input("Bitte eine Auswahl treffen:")
		if selection == "x":
			return -1
		else:
			try:
				ret = int(selection)
				if ret < l:
					return ret
			except:
				pass 
