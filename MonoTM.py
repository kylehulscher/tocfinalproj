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
		self.history = History

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
	def __init__(self, sourceState, appearTape, direction, targetState, writtenTape):
		self.sourceState = sourceState
		self.appearTape = appearTape
		self.direction = direction
		self.targetState = targetState
		self.writtenState = writtenTape

	def __str__(self):
		fullStr = str(self.sourceState) + " === "
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

	def __repr__(self):
   		return f'[{self.currState}: "{self.leftStr}" "{self.rightStr}"]'

class History:
	def __init__(self, TM):
		self.tm = TM
		self.cfgLst = []

	#showHistory
	def __str__(self):
		outStr = ""
		for i in self.cfgLst:
			print(str(i))
		return outStr

#initialConfig
def initialConfig(TM,inputChar):
	return Config(TM.start, TM.blank, TM.leftend, inputChar)

#configs
def configs(TM, steps, inputString):
	accepting(TM, inputString, steps)
	print("\n\n HISTORY: \n")
	print(str(TM.history))
	

#accepting
def accepting(TM, inputString, steps):
	currCfgs = [initialConfig(TM, inputString)]
	TM.history = History([])
	TM.history.cfgLst.append(currCfgs)

	for step in range(steps):
		TM.history.cfgLst.append([])
		#while(cfg.currState not in TM.final): <<- make into an if statement to check if in an accepting state
		for cfg in TM.history.cfgLst[step]:
			if cfg.currState in TM.final:
				return cfg
			for tr in TM.trans:
				if tr.sourceState == cfg.currState:
					if len(cfg.leftStr) > 0 and (tr.direction == Left and tr.appearTape == cfg.leftStr[-1]):
						newLS = cfg.leftStr[:-1]
						newRS = cfg.leftStr[-1] + cfg.rightStr
						newCfg = Config(tr.targetState, TM.blank, newLS, newRS)
						TM.history.cfgLst[step + 1].append(newCfg)
					elif len(cfg.rightStr) > 0 and (tr.direction == Right and tr.appearTape == cfg.rightStr[0]):
						newRS = cfg.rightStr[1:]
						newLS = cfg.leftStr + cfg.rightStr[0] 
						newCfg = Config(tr.targetState, TM.blank, newLS, newRS)
						TM.history.cfgLst[step + 1].append(newCfg)

					else:
						print("!No transition found!")

	return None
				
#accepts
def accepts(TM, inputString):
	for ch in inputString:
		if ch not in TM.alphabet:
			return False
	return True

def main():

	#sourceState, appearTape, direction, targetState, writtenTape
	newTrans = []
	# State 1
	newTrans.append(Trans(1, "a", Right, 2, "a"))
	newTrans.append(Trans(1, "a", Right, 5, "a"))
	# State 2
	newTrans.append(Trans(2, "b", Right, 3, "b"))
	newTrans.append(Trans(2, "b", Right, 2, "b"))
	# State 3
	newTrans.append(Trans(3, "c", Right, 2, "c"))
	newTrans.append(Trans(3, "c", Right, 3, "c"))
	# State 4
	newTrans.append(Trans(4, "a", Right, 5, "a"))
	newTrans.append(Trans(4, "a", Right, 4, "a"))
	# State 5
	newTrans.append(Trans(5, "b", Right, 4, "b"))
	newTrans.append(Trans(5, "b", Right, 6, "b"))


	#Example TM to work off of
	newTM = TM(list(range(1,7)), "abc", "abc*! ", ' ', '!', newTrans, 1, [6])
	print(newTM)
	print("\n\n")
	
	configs(newTM, 5, "abba")




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