# COMP9021 19T3 - Rachid Hamadi
# Quiz 7 *** Due Thursday Week 9
#
# Randomly generates a grid of 0s and 1s and determines
# the maximum number of "spikes" in a shape.
# A shape is made up of 1s connected horizontally or vertically (it can contain holes).
# A "spike" in a shape is a 1 that is part of this shape and "sticks out"
# (has exactly one neighbour in the shape).


from random import seed, randrange
import sys


dim = 10


def display_grid():
    for row in grid:
        print('   ', *row)


# Returns the number of shapes we have discovered and "coloured".
# We "colour" the first shape we find by replacing all the 1s
# that make it with 2. We "colour" the second shape we find by
# replacing all the 1s that make it with 3.
def colour_shapes():
    new_grid = []
    new_grid.append([0] * 12)
    for n_row in range(len(grid)):
        new_grid.append([0])
        new_grid[n_row + 1].extend(grid[n_row])
        new_grid[n_row + 1].extend([0])
    new_grid.append([0] * 12)#新地图
    new_dict = {}
    position_array = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    matrix_stack = []
    colour = 2
    pop_point = 0
    zero = 0
    count = 0
    for row in range(len(new_grid)):
        for col in range(len(new_grid[row])):
            if new_grid[row][col] == 1:
                new_dict[colour] = []
                matrix_stack.append([row, col])
                while len(matrix_stack) != 0:  #如果有元素那么开始进入递归
                    new_grid[matrix_stack[-1][0]][matrix_stack[-1][1]] = colour #改颜色
                    for posi in position_array:
                        last_value = matrix_stack[-1]
                        if new_grid[last_value[0] + posi[0]][last_value[1] + posi[1]] == 1:
                            matrix_stack.append([last_value[0] + posi[0], last_value[1] + posi[1]])#压栈
                            pop_point += 1
                    if pop_point == 0:
                        judge_point = matrix_stack.pop()
                        for around in position_array:
                            if new_grid[judge_point[0] + around[0]][judge_point[1] + around[1]] == colour:
                                count += 1
                            elif new_grid[judge_point[0] + around[0]][judge_point[1] + around[1]] == 0:
                                zero += 1
                        if count == 1 or zero == 4:
                            if new_dict[colour].count([judge_point[0], judge_point[1]]) == 0:
                                new_dict[colour].append([judge_point[0], judge_point[1]])
                        count = 0
                        zero = 0
                    pop_point = 0
                colour += 1
    return new_dict


def max_number_of_spikes(nb_of_shapes):
    max_length = 0
    for each in nb_of_shapes:
        max_length = max(max_length, len(nb_of_shapes[each]))
    return max_length
    # Replace pass above with your code


# Possibly define other functions here


try:
    for_seed, density = (int(x) for x in input('Enter two integers, the second '
                                               'one being strictly positive: '
                                              ).split()
                    )
    if density <= 0:
        raise ValueError
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()

seed(for_seed)
grid = [[int(randrange(density) != 0) for _ in range(dim)]
            for _ in range(dim)
       ]
print('Here is the grid that has been generated:')
display_grid()
nb_of_shapes = colour_shapes()
print('The maximum number of spikes of some shape is:',
      max_number_of_spikes(nb_of_shapes)
     )
