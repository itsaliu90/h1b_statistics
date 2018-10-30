import sys
import operator

# Useful paths
path_to_input_file = sys.argv[1]
path_to_top_10_occupations_output_file = sys.argv[2]
path_to_top_10_states_output_file = sys.argv[3]

# Read input files into memory
print('Reading input file...')
input_file = open(path_to_input_file, "r")
input_file_array = input_file.readlines()

# First, let's pull out the header row from the rest of the body in the .csv
header = input_file_array[0]
body = input_file_array[1:]

# Let's split the header into a list for easier manipulation.
header_array = header.split(";")

# And now the body as well, iterating through each row.
body_array = []
for row in body:
	body_array += [row.split(";")]

# Next, I want to set variables for the columns that I'm interested in.  I reviewed the 2014-2016 files,
# as well as the test file and found a few variations, which are listed out below in the order of precedence.
status_header_variations = ["STATUS", "CASE_STATUS"]
state_header_variations = ["WORKSITE_STATE", "LCA_CASE_WORKLOC1_STATE", "EMPLOYER_STATE"]
occupation_header_variations = ["SOC_NAME", "LCA_CASE_SOC_NAME"]

# Next, I want to identify the positions of these columns in the header_array
for variation in status_header_variations:
	if variation in header_array:
		status_column_index = header_array.index(variation)
		break

for variation in state_header_variations:
	if variation in header_array:
		state_column_index = header_array.index(variation)
		break

for variation in occupation_header_variations:
	if variation in header_array:
		occupation_column_index = header_array.index(variation)
		break

# Now that we have the positions of the columns we care about,
# let's iterate through the body_array and do the aggregations in a Dict data structure.

occupations_dictionary = {}
states_dictionary = {}

for row in body_array:

# Strip double-quotes around some fields...
	occupation = row[occupation_column_index].strip('\"')
	state = row[state_column_index]

# Return only certified applications...
	if row[status_column_index] == "CERTIFIED":
		if occupation not in occupations_dictionary:
			occupations_dictionary[occupation] = 1
		else:
			occupations_dictionary[occupation] += 1
		
		if state not in states_dictionary:
			states_dictionary[state] = 1
		else:
			states_dictionary[state] += 1

# Get the sum for each dictionary, which we'll use for the aggregation calculations later on.
occupations_sum = float(sum(occupations_dictionary.values()))
states_sum = float(sum(states_dictionary.values()))

# Need to sort by certified applications and break ties based on spelling:
sorted_occupations_list = sorted(occupations_dictionary.items(), key=lambda x: (-x[1], x[0]))
sorted_states_list = sorted(states_dictionary.items(), key=lambda x: (-x[1], x[0]))

# Finally, let's write to Occupations file
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

# And write to the States file
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

# Thanks for the fun project!