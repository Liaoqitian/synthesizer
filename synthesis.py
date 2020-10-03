from z3 import *
import sys
num_instrs = int(sys.argv[1]) # how many instructions will we allow in our output program?
# try: 1 or 2

# four instructions: 0 - left, 1 - right, 2 - up, 3 - down

# def run_instr(pos, instr, arg, envir):
# 	return if_wrapper(instr == 0,
# 		# left
# 			if_wrapper(pos % 4 - arg >= 0, pos - arg, pos - pos % 4),
# 			if_wrapper(instr == 1,
# 			# right
# 				if_wrapper(pos % 4 + arg <= 3, pos + arg, pos + 3 - pos % 4), 
# 				if_wrapper(instr == 2, 
# 					# up
# 					if_wrapper(pos / 4 - arg >= 0, pos - arg * 4, pos % 4), 
# 					if_wrapper(instr == 3,
# 						# down 
# 						if_wrapper(pos / 4 + arg <= 3, pos + arg * 4, envir - 4 + pos % 4), 
# 						pos
# 						)
# 					)
# 				)
# 			)

# length = 4, width = 3 matrix 
# 0  1  2  3 
# 4  5  6  7 
# 8  9  10 11


def run_instr(pos, instr, arg, envir, length, width):
	return If(instr == 0,
		# left
			If(pos % length - arg >= 0, pos - arg, False),
			If(instr == 1,
			# right
				If(pos % length + arg <= length - 1, pos + arg, False), 
				If(instr == 2, 
					# up
					If(pos / length - arg >= 0, pos - arg * length, False), 
					If(instr == 3,
						# down 
						If(pos / length + arg <= width - 1, pos + arg * length, False), 
						pos
						)
					)
				)
			)

# def run_instr(pos, instr, arg, envir, length, width):
# 	return If(instr == 0,
# 		# left
# 			If(pos % length - arg >= 0, pos - arg, pos - pos % length),
# 			If(instr == 1,
# 			# right
# 				If(pos % length + arg <= length - 1, pos + arg, pos + length - 1 - pos % length), 
# 				If(instr == 2, 
# 					# up
# 					If(pos / length - arg >= 0, pos - arg * length, pos % length), 
# 					If(instr == 3,
# 						# down 
# 						If(pos / length + arg <= width - 1, pos + arg * length, envir - (length - 1) + pos % length), 
# 						pos
# 						)
# 					)
# 				)
# 			)

debug = True
def if_wrapper(cond, t, f):
	if debug:
		if cond:
			return t
		return f
	return If(cond, t, f)			

# what's the effect of running the whole program?  where does the robot end up?
def run_prog(pos, instrs, args, envir, length, width):
	curr_pos = pos
	for i in range(len(instrs)):
		curr_pos = run_instr(curr_pos, instrs[i], args[i], envir, length, width)
	return curr_pos

# let's make some Z3 bitvectors that we'll use to search the space of instructions
def gen_instrs(num_instrs):
	return [Int('x_' + str(i)) for i in range(num_instrs)]


# let's make some Z3 bitvectors that we'll use to search the space of arguments
def gen_args(num_instrs):
	return [Int('a_' + str(i)) for i in range(num_instrs)]

# a convenience function for printing the Z3 output to look like a sequence of instructions
def print_model(model, instrs, args):
	for i in range(len(instrs)):
		val = model.eval(instrs[i])
		arg = model.eval(args[i])
		# val = instrs[i]
		# arg = args[i]
		if (val == 0):
			print("L", arg)
		elif (val == 1):
			print("R", arg)
		elif (val == 2):
			print("U", arg)
		elif (val == 3): 
			print("D", arg)
		else:
			print("-")

instrs = gen_instrs(num_instrs) # generate BVs to represent instructions
args = gen_args(num_instrs) # generate BVs to represent arguments
goal = run_prog(1, instrs, args, 16, 4, 4) == 15

# instrs = [0, 1, 2, 3] # generate BVs to represent instructions
# args = [3, 0, 0, 2] # generate BVs to represent arguments
# goal = run_prog(7, instrs, args, 16) == 12 # where do we want our robot to move?

s = Solver()
s.add(goal)
for i in range(num_instrs):
	s.add(And(args[i] >= 0, args[i] < 4))

satisfiable = s.check()
print("satisfiable?", satisfiable)

if (satisfiable == sat):
	model = s.model()
	print_model(model, instrs, args) # print the program if we found one
	print(model) # print the model, just to visualize what's happening underneath