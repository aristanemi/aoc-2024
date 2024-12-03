import numpy as np
import pandas as pd
import sys

input_file=sys.argv[1]

with open(input_file) as f:
    lines = f.readlines()

lines = [x.strip() for x in lines]
left_list = []
right_list = []
for l in lines:
    splitted = l.split(sep='   ')
    left_list.append(int(splitted[0]))
    right_list.append(int(splitted[1]))

left_list = np.sort(left_list)
right_list = np.sort(right_list)
total_distance = 0
for i in range(len(left_list)):
    distance = abs(left_list[i] - right_list[i])
    total_distance = total_distance + distance

print('total distance:', total_distance)

# similarity score
l_unique_values, l_counts = np.unique(left_list, return_counts=True)
r_unique_values, r_counts = np.unique(right_list, return_counts=True)
similarity_score = 0
for i in range(len(l_unique_values)):
    index = np.where(r_unique_values == l_unique_values[i])
    if l_unique_values[i] in r_unique_values:
        similarity_score = similarity_score + l_counts[i] * r_counts[index] * l_unique_values[i]
print('similarity score:', similarity_score)