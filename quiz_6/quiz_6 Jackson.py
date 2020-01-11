# COMP9021 19T3 - Rachid Hamadi
# Quiz 6 *** Due Thursday Week 8
#
# Randomly fills an array of size 10x10 with 0s and 1s, and outputs the size of
# the largest parallelogram with horizontal sides.
# A parallelogram consists of a line with at least 2 consecutive 1s,
# with below at least one line with the same number of consecutive 1s,
# all those lines being aligned vertically in which case the parallelogram
# is actually a rectangle, e.g.
#      111
#      111
#      111
#      111
# or consecutive lines move to the left by one position, e.g.
#      111
#     111
#    111
#   111
# or consecutive lines move to the right by one position, e.g.
#      111
#       111
#        111
#         111


from random import seed, randrange
import sys

dim = 10


def display_grid():
    for row in grid:
        print('   ', *row)

def change_matrix(l_matrix, r_matrix):
    for row_index in range(10):
        r_array = []
        l_array = []
        r_array.extend(row_index * [0])
        l_array.extend((10-row_index) * [0])
        r_array.extend(r_matrix[row_index])
        l_array.extend(l_matrix[row_index])
        r_matrix[row_index] = r_array
        l_matrix[row_index] = l_array
        r_matrix[row_index].extend((10 - row_index) * [0])
        l_matrix[row_index].extend(row_index * [0])
    return l_matrix, r_matrix

def area_height(area_matrix, matrix_row, matrix, colnumber):

    for matrix_col in range(colnumber):#遍历高度并记录
        if matrix[matrix_row][matrix_col] == 0:
            area_matrix[matrix_col] = 0
        else:
            area_matrix[matrix_col] = area_matrix[matrix_col] + 1
    return area_matrix

def find_matrix(area_matrix, matrix_row, area_stack, colnumber, max_area):
    if matrix_row != 0:
        for area_col in range(colnumber):  # 找矩形
            area_stack.append(area_col)
            if area_matrix[area_col] > area_matrix[area_col + 1]:
                while len(area_stack) != 0 and area_matrix[area_stack[-1]] > area_matrix[area_col + 1]:
                    element = area_stack.pop()
                    if area_matrix[element] > 1 and area_col >= 1:
                        if area_stack == []:
                            max_area = max(max_area, area_matrix[element] * (area_col + 1))
                        elif area_col - area_stack[-1] > 1:
                            max_area = max(max_area, area_matrix[element] * (area_col - area_stack[-1]))
        area_stack = []
        return max_area, area_stack
    else:
        return 0, area_stack

#使用动态规划算法 对三种情况进行讨论
def size_of_largest_parallelogram():
    area_matrix = []#高度矩阵
    larea_matrix = []
    rarea_matrix = []
    area_stack = []#单调递增栈
    rarea_stack = []
    larea_stack = []
    max_area = 0#最大面积
    lmax_area = 0
    rmax_area = 0
    r_matrix = []#左矩形
    l_matrix = []#右矩形
    area_matrix = [0] * 11
    larea_matrix = [0] * 21
    rarea_matrix = [0] * 21
    for matrix_row in range(10):
        r_matrix = list(grid)
        l_matrix = list(grid)
        l_matrix, r_matrix = change_matrix(l_matrix, r_matrix)
        area_matrix = area_height(area_matrix, matrix_row, grid, 10)
        max_area, area_stack = find_matrix(area_matrix, matrix_row, area_stack, 10, max_area)
        larea_matrix = area_height(larea_matrix, matrix_row, l_matrix, 20)
        lmax_area, larea_stack = find_matrix(larea_matrix, matrix_row, larea_stack, 20, lmax_area)
        rarea_matrix = area_height(rarea_matrix, matrix_row, r_matrix, 20)
        rmax_area, rarea_stack = find_matrix(rarea_matrix, matrix_row, rarea_stack, 20, rmax_area)

    max_area = max(max_area, lmax_area, rmax_area)
    return max_area
    # REPLACE PASS ABOVE WITH YOUR CODE


# POSSIBLY DEFINE OTHER FUNCTIONS



# COMP9021 19T3 - Rachid Hamadi
# Quiz 5 *** Due Thursday Week 7
#
# Implements a function that, based on the encoding of
# a single strictly positive integer that in base 2,
# reads as b_1 ... b_n, as b_1b_1 ... b_nb_n, encodes
# a sequence of strictly positive integers N_1 ... N_k
# with k >= 1 as N_1* 0 ... 0 N_k* where for all 0 < i <= k,
# N_i* is the encoding of N_i.
#
# Implements a function to decode a positive integer N
# into a sequence of (one or more) strictly positive
# integers according to the previous encoding scheme,
# or return None in case N does not encode such a sequence.


import sys
import re

def encode(list_of_integers):
    totallist = ''
    newlist = [bin(each)[2:]for each in list_of_integers]
    for element in newlist:
        for eachele in element:
            totallist = totallist + 2*eachele
        totallist = totallist + '0'
    return int(totallist[:-1], 2)
    pass
    # REPLACE pass ABOVE WITH YOUR CODE


def decode(integer):
    codelist = []
    eachstring = ''
    integerbt = bin(integer)[2:]
    integerre = re.compile(r'(?:00|11)*')
    allinger = integerre.findall(integerbt)
    encodelist = list(filter(None, allinger))
    for every in encodelist:
        integerbt = ''.join(integerbt.split(every,1))
    if '1' in integerbt or integerbt.count('0') != len(encodelist) - 1:
        return None
    if 3 > integer >= 0:
        return None
    for enchcode in encodelist:
        for charindex in range(0, len(enchcode), 2):
            eachstring += str(enchcode[charindex])
        eachstring = int(eachstring,2)
        if eachstring == 0:
            return None
        codelist.append(eachstring)
        eachstring = ''
    return codelist
    # REPLACE pass ABOVE WITH YOUR CODE


# We assume that user input is valid. No need to check
# for validity, nor to take action in case it is invalid.
print('Input either a strictly positive integer')
the_input = eval(input('or a nonempty list of strictly positive integers: '))
if type(the_input) is int:
    print('  In base 2,', the_input, 'reads as', bin(the_input)[2 :])
    decoding = decode(the_input)
    if decoding is None:
        print('Incorrect encoding!')
    else:
        print('  It encodes: ', decode(the_input))
else:
    print('  In base 2,', the_input, 'reads as',
          f'[{", ".join(bin(e)[2: ] for e in the_input)}]'
         )
    print('  It is encoded by', encode(the_input))


seed(for_seed)
grid = [[int(randrange(density) != 0) for _ in range(dim)]
        for _ in range(dim)
        ]
print('Here is the grid that has been generated:')
display_grid()
size = size_of_largest_parallelogram()
if size:
    print('The largest parallelogram with horizontal sides '
          f'has a size of {size}.'
          )

else:
    print('There is no parallelogram with horizontal sides.')

