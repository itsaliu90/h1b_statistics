# Test code
print('Running script!')

import sys
import pdb
import operator

# Useful paths
path_to_input_file = sys.argv[1]
path_to_top_10_occupations_output_file = sys.argv[2]
path_to_top_10_states_output_file = sys.argv[3]

# Read input file into memory
input_file = open(path_to_input_file, "r")
print('Reading lines!')
input_file_array = input_file.readlines()
print('The length of the input array is:')
print len(input_file_array)

# First, let's pull out the Header row from the rest of the Body
header = input_file_array[0]
print('The header:')
print header

body = input_file_array[1:]
print('The body:')
print body

# Let's split the header into a real array
header_array = header.split(";")
print('The header array:')
print header_array

# And the body as well
body_array = []
for row in body:
	body_array += [row.split(";")]

print('The body array:')
print body_array

# Columns that I'm interested in:
status_header_variations = ["STATUS", "CASE_STATUS"]
state_header_variations = ["WORKSITE_STATE", "LCA_CASE_WORKLOC1_STATE", "EMPLOYER_STATE"]
occupation_header_variations = ["SOC_NAME", "LCA_CASE_SOC_NAME"]

# Identify the positions of these columns in the header_array

for variation in status_header_variations:
	if variation in header_array:
		status_column_index = header_array.index(variation)
		break

print('Status column index:')
print(status_column_index)

for variation in state_header_variations:
	if variation in header_array:
		state_column_index = header_array.index(variation)
		break

print('State column index:')
print(state_column_index)

for variation in occupation_header_variations:
	if variation in header_array:
		occupation_column_index = header_array.index(variation)
		break

print('Occupation column index:')
print(occupation_column_index)

# Now that we have the positions of the columns we care about,
# let's iterate through the body_array and do the aggregations in a Dict

occupations_dictionary = {}
states_dictionary = {}

for row in body_array:
	occupation = row[occupation_column_index].strip('\"')
	state = row[state_column_index]

	if row[status_column_index] == "CERTIFIED":
		if occupation not in occupations_dictionary:
			occupations_dictionary[occupation] = 1
		else:
			occupations_dictionary[occupation] += 1
		
		if state not in states_dictionary:
			states_dictionary[state] = 1
		else:
			states_dictionary[state] += 1

# Get the sum for each dictionary
occupations_sum = float(sum(occupations_dictionary.values()))
states_sum = float(sum(states_dictionary.values()))

print('Occupations Dictionary')
print(occupations_dictionary)

print('State Dictionary')
print(states_dictionary)

# Need to sort by Certified Applications
sorted_occupations_list = sorted(occupations_dictionary.items(), key=lambda x: (-x[1], x[0]))
sorted_states_list = sorted(states_dictionary.items(), key=lambda x: (-x[1], x[0]))

print('Sorted Occupations List')
print(sorted_occupations_list)

print('Sorted States List')
print(sorted_states_list)

# Write to Occupations file
top_10_occupations_file = open(path_to_top_10_occupations_output_file, "w")
top_10_occupations_file.write("TOP_OCCUPATIONS;NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE\n")
i = 0
while i < 10:
	if i > len(sorted_occupations_list) - 1:
		break
	occupation, count = sorted_occupations_list[i]
	top_10_occupations_file.write("%s;%s;%s%%\n" % (occupation, count, round(count/occupations_sum*100., 1)))
	i += 1
top_10_occupations_file.close()

# Write to States file
top_10_states_file = open(path_to_top_10_states_output_file, "w")
top_10_states_file.write("TOP_STATES;NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE\n")

j = 0
while j < 10:
	if j > len(sorted_states_list) - 1:
		break
	state, count = sorted_states_list[j]
	top_10_states_file.write("%s;%s;%s%%\n" % (state, count, round(count/states_sum*100., 1)))
	j += 1

top_10_states_file.close()