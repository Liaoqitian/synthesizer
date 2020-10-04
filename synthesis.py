from z3 import *
import sys
# num_instrs = int(sys.argv[1]) # how many instructions will we allow in our output program?
# try: 1 or 2

# four instructions: 0 - left, 1 - right, 2 - up, 3 - down

# length = 4, width = 3 matrix 
# 0  1  2  3 
# 4  5  6  7 
# 8  9  10 11

def run_instr(pos, instr, envir, length, width, obs):
	return if_wrapper(instr == 0,
			# left
				if_wrapper(pos % length - 1 >= 0, 
					if_wrapper(check_obstacle(pos - 1, obs), pos, pos - 1), pos),
				if_wrapper(instr == 1,
				# right
					if_wrapper(pos % length + 1 <= length - 1, 
						if_wrapper(check_obstacle(pos + 1, obs), pos, pos + 1), pos), 
					if_wrapper(instr == 2, 
						# up
						if_wrapper(pos / length - 1 >= 0, 
							if_wrapper(check_obstacle(pos - length, obs), pos, pos - length), pos), 
						if_wrapper(instr == 3,
							# down 
							if_wrapper(pos / length + 1 < width, 
								if_wrapper(check_obstacle(pos + length, obs), pos, pos + length), pos), 
							pos
							)
						)
					)
				)


debug = False
def if_wrapper(cond, t, f):
	if debug:
		if cond:
			return t
		return f
	return If(cond, t, f)			

def check_obstacle(pos, obs):
	return pos in obs

# what's the effect of running the whole program?  where does the robot end up?
def run_prog(pos, instrs, envir, length, width, obs):
	curr_pos = pos
	for i in range(len(instrs)):
		curr_pos = run_instr(curr_pos, instrs[i], envir, length, width, obs)
	return curr_pos

# let's make some Z3 bitvectors that we'll use to search the space of instructions
def gen_instrs(num_instrs):
	return [BitVec('x_' + str(i), 2) for i in range(num_instrs)]


# # let's make some Z3 bitvectors that we'll use to search the space of arguments
# def gen_args(num_instrs):
# 	return [Int('a_' + str(i)) for i in range(num_instrs)]

# a convenience function for printing the Z3 output to look like a sequence of instructions
def print_model(model, instrs):
	for i in range(len(instrs)):
		val = model.eval(instrs[i])
		# arg = args[i]
		if (val == 0):
			print("L")
		elif (val == 1):
			print("R")
		elif (val == 2):
			print("U")
		elif (val == 3): 
			print("D")
		else:
			print("-")

# instrs = [0, 1, 2, 3] # generate BVs to represent instructions
# args = [3, 0, 0, 2] # generate BVs to represent arguments
# goal = run_prog(7, instrs, args, 16) == 12 # where do we want our robot to move?

pos, envir, length, width, dest = 1, 16, 4, 4, 15
obs = [5]

# Iterative Deepening
num_instrs = 1
while num_instrs < envir: 
	s = Solver()
	instrs = gen_instrs(num_instrs) # generate BVs to represent instructions
	# args = gen_args(num_instrs) # generate BVs to represent arguments
	# instrs = [1, 3, 3, 3, 1]
	goal = run_prog(pos, instrs, envir, length, width, obs) == dest
	s.add(goal)
	# for i in range(num_instrs):
	# 	s.add(And(args[i] >= 0, args[i] < 4))

	satisfiable = s.check()
	print("satisfiable?", satisfiable, num_instrs)

	if (satisfiable == sat):
		model = s.model()
		print_model(model, instrs) # print the program if we found one
		print(model) # print the model, just to visualize what's happening underneath
		break 
	num_instrs += 1



