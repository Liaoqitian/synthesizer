from z3 import *
​
x = Int('x')
s = Solver()
# ifs are going to be a little different for constraints...
s.add(If(True, x==3, x==10)) 
s.check()
print(s.model())
​
# what's the effect of running one instruction?  where does the robot end up?
def run_instr(pos, instr, envir):
	return If(instr == 0,
			# left
			If(pos - 1 >= 0, pos - 1, 0),
		If(instr == 1,
			# right
			If(pos + 1 <= (envir - 1), pos + 1, envir - 1),
		pos))
​
# what's the effect of running the whole program?  where does the robot end up?
def run_prog(pos, instrs, envir):
	curr_pos = pos
	for i in range(len(instrs)):
		curr_pos = run_instr(curr_pos, instrs[i], envir)
	return curr_pos
​
# let's make some Z3 bitvectors that we'll use to search the space of instructions
def gen_instrs(num_instrs):
	return [BitVec('x_'+str(i),1) for i in range(num_instrs)] # try bitwidth 1 and 2 with num_instrs 6
​
# a convenience function for printing the Z3 output to look like a sequence of instructions
def print_model(model, instrs):
	for i in range(len(instrs)):
		val = model.eval(instrs[i])
		if (val == 0):
			print "L"
		elif (val == 1):
			print "R"
		else:
			print "-"
​
import sys
​
num_instrs = int(sys.argv[1]) # how many instructions will we allow in our output program?
# try: 5, 6, 7
​
instrs = gen_instrs(num_instrs) # generate BVs to represent instructions
goal = run_prog(7, instrs, 16) == 12 # where do we want our robot to move?
​
s = Solver()
​
s.add(goal)
satisfiable = s.check()
print "satisfiable?", satisfiable
​
if (satisfiable == sat):
	model = s.model()
	print_model(model, instrs) # print the program if we found one
	print model # print the model, just to visualize what's happening underneath