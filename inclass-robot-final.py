from z3 import *
import sys

num_instrs = int(sys.argv[1]) # how many instructions will we allow in our output program?
# try: 1 or 2

# what's the effect of running one instruction?  where does the robot end up?
def run_instr(pos, instr, arg, envir):
	return If(arg > 0,
			If(instr == 0,
				# left
				If(pos - arg >= 0, pos - arg, 0),
			If(instr == 1,
				# right
				If(pos + arg <= (envir - 1), pos + arg, envir - 1),
			pos)),
			pos)

# what's the effect of running the whole program?  where does the robot end up?
def run_prog(pos, instrs, args, envir):
	curr_pos = pos
	for i in range(len(instrs)):
		curr_pos = run_instr(curr_pos, instrs[i], args[i], envir)
	return curr_pos

# let's make some Z3 bitvectors that we'll use to search the space of instructions
def gen_instrs(num_instrs):
	return [BitVec('x_'+str(i),2) for i in range(num_instrs)]

# let's make some Z3 bitvectors that we'll use to search the space of arguments
def gen_args(num_instrs):
	return [Int('a_'+str(i)) for i in range(num_instrs)]

# a convenience function for printing the Z3 output to look like a sequence of instructions
def print_model(model, instrs, args):
	for i in range(len(instrs)):
		val = model.eval(instrs[i])
		arg = model.eval(args[i])
		if (val == 0):
			print "L", arg
		elif (val == 1):
			print "R", arg
		else:
			print "-"

instrs = gen_instrs(num_instrs) # generate BVs to represent instructions
args = gen_args(num_instrs) # generate BVs to represent arguments
goal = run_prog(7, instrs, args, 16) == 12 # where do we want our robot to move?

s = Solver()
s.add(goal)
satisfiable = s.check()
print "satisfiable?", satisfiable

if (satisfiable == sat):
	model = s.model()
	print_model(model, instrs, args) # print the program if we found one
	print model # print the model, just to visualize what's happening underneath
