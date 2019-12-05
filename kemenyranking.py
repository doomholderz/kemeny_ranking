import random
import math
import copy
import time
import sys

# Get file passed as argument, and store info in contents variable
file_to_open = str(sys.argv[1])
results = open(file_to_open, "r")
contents = results.read().split("\n")

# Initial ranking
initial_solution = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35]

# Initial temperature value
initial_temperature = 100
# Temperature length value
temperature_length = 20

# Dictionary storing info about the nodes that a specific node loses to, and by how much
lost_dict = {}
# Dictionary storing info about the nodes that a specific node beats, and by how much
won_dict = {}

# Stores information about the participants names, and their IDs
participants = {}
for i in range(35):
	participant_number = contents[i+1][:(contents[i+1]).find(",")]
	participant_name = contents[i+1][(contents[i+1].find(",")) + 1:]
	participants[participant_number] = participant_name

# Reads all of the edges and weights in the .wmg file
for i in range(len(contents) - 38):
	line = contents[i+37]
	line = list(line.split(","))

	# Gets the winning node, losing node, and score for each edge 
	score = line[0]
	won = line[1]
	lost = line[2]

	# Adds edge to the won dictionary
	if won in won_dict.keys():
		won_dict[won].append((lost, score))
	else:
		won_dict[won] = [(lost, score)]

	# Adds edge to the lost dictionary
	if lost in lost_dict.keys():
		lost_dict[lost].append((won, score))
	else:
		lost_dict[lost] = [(won, score)]

# Function for cooling temperature during SA algorithm
def cooling_ratio(temperature):
	a = 0.9
	return temperature * a

# Finds the Kemeny score of the initial solution
def find_cost(solution):
	score = 0
	# For each of the nodes in the initial solution
	for value in solution:
		# If the value loses to some nodes (in lost_dict)
		if str(value) in lost_dict:
			# For each of the nodes this value loses to
			for loss in lost_dict[str(value)]:
				# Finds the index of the node the value loses to
				victor_index = solution.index(int(loss[0]))
				# Find the index of the current value
				current_index = solution.index(value)
				# If the node the current value loses to comes later in the ranking
				if current_index < victor_index:
					# Add to the score the weight by which it loses 
					score += int(loss[1])
	return score

# Finds the Kemeny score of the solution taking into acount previous score, and nodes switched
def iterative_cost(solution, past_score, node1, node2):
	# Get the nodes that have been switched, and the range between them
	first_node = solution[node1]
	second_node = solution[node2]
	node_range = node2 - node1
	
	# For each of the nodes between the first node and second node
	for i in range(1, node_range+1):
		
		# Checks if node1 now adds to the Kemeny score with its new improved position
		if str(first_node) in lost_dict.keys():
			for z in lost_dict[str(first_node)]:
				if str(z[0]) == str(solution[node1 + i]):
					past_score += int(z[1])

		# Checks if node1 now lowers the Kemeny score with its new improved position
		if str(first_node) in won_dict.keys():
			for x in won_dict[str(first_node)]:
				if str(x[0]) == str(solution[node1 + i]):
					past_score -= int(x[1])
		
		# Checks if node2 now adds to the Kemeny score with its new worsened position
		if str(second_node) in won_dict.keys():
			for l in won_dict[str(second_node)]:
				if str(l[0]) == str(solution[node1 + i]):
					past_score += int(l[1])

		# Checks if node2 now lowers the Kemeny score with its new worsened position
		if str(second_node) in lost_dict.keys():
			for y in lost_dict[str(second_node)]:
				if str(y[0]) == str(solution[node1 + i]):
					past_score -= int(y[1])

	return past_score

# Function to find a neighbouring solution
def neighbour(solution):
	solution2 = solution
	
	# Creates a random index of the first node to switch in the neighbour
	first_swap_index = random.randint(0, len(solution) - 2)
	# Finds the value associated with that index in the solution
	first_swap_value = solution[first_swap_index]
	
	# Creates a random index of the second node to switch in the neighbour
	second_swap_index = random.randint(0, len(solution) - 1)
	# Ensures the second_swap_index is different from the first (so the switched values are unique)
	while second_swap_index == first_swap_index:
		second_swap_index = random.randint(0, len(solution) - 1)
	# Finds the value associated with that index in the solution
	second_swap_value = solution[second_swap_index]

	# Switches the values at those positions
	solution2[first_swap_index] = second_swap_value
	solution2[second_swap_index] = first_swap_value

	# Appends the new neighbour to the return_value array
	return_value = []
	return_value.append(solution2)

	# Adds the two indexes to the return_value array (ensuring node1 is the node in better rank position)
	if first_swap_index < second_swap_index:
		return_value.append(first_swap_index)
		return_value.append(second_swap_index)
	else:
		return_value.append(second_swap_index)
		return_value.append(first_swap_index)

	return return_value

# Simmulated annealing function using solution, the initial cost (worked out later) and the current temperature)
def simmulated_annealing(initial_solution, initial_cost, temp):

	uphill_moves = 0
	output = []

	# Deep copies initial solution so we can compare to this later
	init_solution = copy.deepcopy(initial_solution)
	init_cost = initial_cost
	# Get the neighbour array using neighbour function
	solution_tuple = neighbour(initial_solution)

	# Get the neighbour ranking 
	newx_solution = solution_tuple[0]
	# Get the two nodes switched
	node1_index = solution_tuple[1]
	node2_index = solution_tuple[2]

	# Get the cost of the neighbour using iterative_cost function
	newx_cost = iterative_cost(newx_solution, init_cost, node1_index, node2_index)

	# If the neighbour cost is better than the original cost
	if newx_cost <= init_cost:
		# Return this solution, the cost associated with it, and the number of uphill moves thusfar
		output.append(newx_solution)
		output.append(newx_cost)
		output.append(uphill_moves)
		
		return output

	else:
		# Find out the change in cost ∆C
		change_in_cost = newx_cost - init_cost
		# Provided the temp isn't equal to 0 (divide by zero error)
		if temp != 0:
			# Use simmulated annealing pseudocode equation
			if (random.uniform(0, 1)) < math.exp(-change_in_cost / temp):
				# Will be undertaking an uphill move
				uphill_moves += 1
				# Output new solution, new cost, and number of uphill moves
				output.append(newx_solution)
				output.append(newx_cost)
				output.append(uphill_moves)
				
				return output
		
		# Output the old solution, associated cost, and uphill moves (neighbourhood isn't good enough)	
		output.append(init_solution)
		output.append(init_cost)
		output.append(uphill_moves)
		return output
	
# Set the count for stopping criteria
count = 0
num_non_improve = 200
# Set the number of uphill moves to 0
uphill_moves = 0
# Get the time before computing
millis = int(round(time.time() * 1000))

# Compute cost of initial solution
initial_cost = find_cost(initial_solution)
# Get the initial solution for the simmulated annealing function
initial_solution2 = simmulated_annealing(initial_solution, initial_cost, initial_temperature)[0]
# Set the temperature to the initial temperature
temperature = initial_temperature

# While stopping criteria isn't met
while count < num_non_improve:
	# For length of temperature range
	for i in range(temperature_length):
		# Get deep copy of solution that we can use to compare to later
		init_solution2 = copy.deepcopy(initial_solution2)

		# Get information about simmulated annealing on this solution
		new_array = simmulated_annealing(initial_solution2, initial_cost, temperature)
		
		# Get the solution after a round of simmulated annealing
		initial_solution2 = new_array[0]
		# Get associated cost of this solution
		initial_cost = new_array[1]
		
		# If the solution hasn't been improved
		if init_solution2 == initial_solution2:
			# Add to the count
			count += 1
		else:
			count = 0
		# Add to uphill moves if one was made
		uphill_moves += new_array[2]

	# Cool temperature based on the cooling ratio function
	temperature = cooling_ratio(temperature)

# Get end time
millis2 = int(round(time.time() * 1000))
# Find out time taken in computation
time_difference = millis2 - millis

# Return table of rankings and related information
print("Rank\tID\tName")
print("----------------------------------")
rank = 0
for i in initial_solution2:
	rank += 1
	print(str(rank) + "\t" + str(i) + "\t" + participants[str(i)])
print("\nOverall Kemeny Cost: " + str(find_cost(initial_solution2)))
print("Overall time for computation: " + str(time_difference) + "ms")
print("Overall uphill moves: " + str(uphill_moves) + "\n")





