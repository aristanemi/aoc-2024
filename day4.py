import numpy as np
import sys
import logging
import re
logging.basicConfig(level=logging.INFO)

# Store input into lines
# Lines as numpy matrix, then easy to flip, get diagonal elements
# Search for XMAS in all directions from the same matrix: rows, columns, flipped rows, flipped columns, diagonals and anti-diagonals

input_file=sys.argv[1]
with open(input_file) as f:
    lines = f.readlines()

line_arrays = [np.array([c for c in l.strip()]) for l in lines]
complete_matrix = np.array(line_arrays)

def find_xmas(lines):
    pat = re.compile(r'XMAS')
    total_found = 0
    for l in lines:
        found = pat.findall(l)
        total_found += len(found)
        found = pat.findall(l[::-1])
        total_found += len(found)
    return total_found

rows_as_strings = [''.join(row) for row in complete_matrix]
cols_as_strings = [''.join(col) for col in complete_matrix.T]
diagonals_as_strings = [complete_matrix.diagonal(i) for i in range(-complete_matrix.shape[0]+1, complete_matrix.shape[1])]
antidiagonals_as_strings = [np.fliplr(complete_matrix).diagonal(i) for i in range(-complete_matrix.shape[0]+1, complete_matrix.shape[1])]

total_found = 0
total_found += find_xmas(rows_as_strings)
total_found += find_xmas(cols_as_strings)
total_found += find_xmas([''.join(row) for row in diagonals_as_strings])
total_found += find_xmas([''.join(row) for row in antidiagonals_as_strings])

print(f'total_found = {total_found}')

def search_x_mas(small_matrix):
    num_found = 0
    mas=np.array([c for c in 'MAS'])
    sam=np.array([c for c in 'SAM'])
    d1=np.diag(small_matrix)
    d2=np.diag(np.fliplr(small_matrix))
    if np.array_equal(d1, mas) and np.array_equal(d1, d2):
        num_found += 1
    if np.array_equal(d1, sam) and np.array_equal(d1, d2):
        num_found += 1
    return num_found

row_ids,col_ids = np.where(complete_matrix == 'A')
num_rows,num_cols = complete_matrix.shape
total_x_mas = 0
for i,j in zip(row_ids, col_ids):
    if i == 0 or j == 0 or i == num_rows-1 or j == num_cols-1:
        continue

    logging.debug(f'found at {i},{j}')
    # get 3x3 matrix around 'A'
    sub_matrix = complete_matrix[i-1:i+2,j-1:j+2]
    total_x_mas += search_x_mas(sub_matrix)
    total_x_mas += search_x_mas(np.rot90(sub_matrix))
print(f'total_x_mas = {total_x_mas}')