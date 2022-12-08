Left = -1
Right = 1

class TM:
	#states, a list of all the states used in the TM
	#inputs, a list of all the input characters used
	#tapesyms, a list of all the tape characters used
	#blank, the blank character
	#leftend, the left end marker (character)
	#trans, a list of the transitions of the TM. You will probably want to invent a type Trans
	#		or something like that, for transitions. Each transition tells the source and target states
	#		for the transition (i.e., the states that the transition connects), the symbol that should
	#		appear on the tape for the transition to be triggered, the symbol that should then be
	#		written on the tape, and finally the direction to move the readhead after that transition
	#		is triggered
	#start, the start state
	#final, a list of the final states

	#createTM
	def __init__(self, states, inputs, tapesyms, blank, leftend, trans, start, final):
		self.states = states
		self.inputs = inputs
		self.tapesyms = tapesyms
		self.blank = blank
		self.leftend = leftend
		self.trans = trans
		self.start = start
		self.final = final

	#showTM
	def __str__(self):
		fullStr = "States: " + self.lsStr(self.states)
		fullStr += "Alphabet: " + self.lsStr(self.inputs) 
		fullStr += "Tape symbols: " + self.lsStr(self.tapesyms)
		fullStr += "Blank: " + self.blank + "\n" 
		fullStr += "Leftend: " + self.leftend + "\n"
		fullStr += "Transitions: \n" 
		for trans in self.trans:
			fullStr += str(trans) + "\n"
		fullStr += "Start state: "+ str(self.start) + "\n"
		fullStr += "Final states: " + self.lsStr(self.final)
		return fullStr
	
	def lsStr(self, lst):
		outStr = ""
		for st in lst:
			outStr += str(st) + ", "

		return outStr[0:(len(outStr)-2)] + "\n"

class Trans:
	def __init__(self, sourceStates, appearTape, direction, targetState, writtenTape):
		self.sourceStates = sourceStates
		self.appearTape = appearTape
		self.direction = direction
		self.targetState = targetState
		self.writtenState = writtenTape

	def __str__(self):
		fullStr = str(self.sourceStates) + " === "
		fullStr += str(self.appearTape) + " / "
		fullStr += str(self.direction) + " "
		fullStr += str(self.targetState) + " ===> "
		fullStr += str(self.writtenState)
		return fullStr
		
		
class Config:
	def __init__(self, currState, blank, leftStr, rightStr):
		self.currState = currState
		self.blank = blank
		self.leftStr = leftStr
		self.rightStr = rightStr
		
	#showConfig
	def __str__(self):
		return "[" + str(self.currState) + ": " + '"' + self.leftStr + '"' + " " + '"' + self.rightStr + '"' + "]"

class History:
	def __init__(self, TM, steps):
		self.tm = TM
		self.steps = steps
		self.cfgLst = []

	#showHistory
	def __str__(self):
		outStr = ""
		for i in self.cfgLst:
			outStr += str(i) + "\n"
		return outStr
				
#newTM = TM(list(range(1,7)), "abc", "abc*! ", ' ', '!', newTrans, 1, [6])

#initialConfig
def initialConfig(TM,inputChar):
	return Config(TM.start, TM.blank, TM.leftend, inputChar)

#configs
def configs(TM, steps, inputString):
	print("configs")
	

#accepting
def accepting(TM, inputString):
	currCfg = initialConfig(TM, inputString)
	newHist = History([])
	newHist.cfgLst.append(currCfg)

	while(currCfg.currState not in TM.final):
		newCfg = Config
		for tr in TM.trans:
			if tr.sourceState == currCfg.currState:
				if len(currCfg.leftStr) > 0 and (tr.direction == Left and tr.appearTape == currCfg.leftStr[-1]):
					newLS = currCfg.leftStr[:-1]
					newRS = currCfg.leftStr[-1] + currCfg.rightStr
					newCfg = Config(tr.targetState, TM.blank, newLS, newRS)
					newHist.cfgLst.append(newCfg)
				elif len(currCfg.rightStr) > 0 and (tr.direction == Right and tr.appearTape == currCfg.rightStr[0]): 
					newRS = currCfg.rightStr[1:]
					newLS = currCfg.leftStr + currCfg.rightStr[0] 
					newCfg = Config(tr.targetState, TM.blank, newLS, newRS)
					newHist.cfgLst.append(newCfg)
					
				else:
					print("!No transition found!")

	return 
				
#accepts
def accepts(TM, inputString):
	for ch in inputString:
		if ch not in TM.alphabet:
			return False
	return True

def main():
	#sourceStates, appearTape, direction, targetState, writtenTape
	newTrans = []
	newTrans.append(Trans(1, " ", 'R', 6, " ")) # checkRight 1 ' ' 6
	newTrans.append(Trans(1, "*", 'R', 1, '*')) # loopRight 1 "*"
	newTrans.append(Trans(1, "a", 'R', 2, '*')) # goRight 1 'a' '*' 2
	newTrans.append(Trans(2, "a", 'R', 2, "a")) # loopRight 2 "a"
	newTrans.append(Trans(2, "*", 'R', 2, "*")) # loopRight 2 "*"
	newTrans.append(Trans(2, "b", 'R', 3, '*')) # goRight 2 'b' '*' 3
	newTrans.append(Trans(3, "b", 'R', 3, "b")) # loopRight 3 "b"
	newTrans.append(Trans(3, "*", 'R', 3, "*")) # loopRight 3 "*"
	newTrans.append(Trans(3, "c", 'R', 4, '*')) # goRight 3 'c' '*' 4
	newTrans.append(Trans(4, "c", 'R', 4, "c")) # loopRight 4 "c"
	newTrans.append(Trans(4, "*", 'R', 4, "*")) # loopRight 4 "*"
	newTrans.append(Trans(4, " ", 'L', 5, " ")) # checkLeft 4 ' ' 5
	newTrans.append(Trans(5, "a", 'L', 5, "a")) # loopLeft 5 "a"
	newTrans.append(Trans(5, "b", 'L', 5, "b")) # loopLeft 5 "b"
	newTrans.append(Trans(5, "c", 'L', 5, "c")) # loopLeft 5 "c"
	newTrans.append(Trans(5, "*", 'L', 5, "*")) # loopLeft 5 "*"
	newTrans.append(Trans(5, '!', 'R', 1, "!")) #checkRight 5 '!' 1
	# list, list, list, char, char, list, state(string?), list
	# [1 .. 6] "abc" "abc*! " ' ' '!' trans 1 [6]
	#Example TM to work off of
	newTM = TM(list(range(1,7)), "abc", "abc*! ", ' ', '!', newTrans, 1, [6])
	print(newTM)
	print("\n\n")
	#newConfig = Config(1, " ", "!", "aabbcc")
	#print(newConfig)
	newConfig = initialConfig(newTM, "aabbcc")
	print(newConfig)
	print()
	
	newHist = History([])
	for i in range(0,10):
		newHist.cfgLst.append(newConfig)

	for item in newHist.cfgLst:
		print("[" + str(item) + "]")

	# config has leftStr rightStr           "!aa bbcc"
	# initially 				  leftStr = "!" and rightStr = "aabbcc"
	# cursor moves right one then leftStr = "!a" rightStr = "abbcc"

if __name__ == "__main__":
	main()

# For Problem 1 TM Simulator involving the History "Type". Is it supposed to generate and store all 
# possible runs of configurations for the TM in n number of steps, or does it serve as a history for 
# all configurations generated while running through the input string.
#
# We are also confused about why it's a double list when the haskell output looked something like 
# [[1: "!a" "abbcc"]]
# [[2: "!*a" "bbcc"]]
# [[2: "!*ab" "bcc"]] ...
# with only one item per outer list