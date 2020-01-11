# COMP9021 19T3 - Rachid Hamadi
# Assignment 2 *** Due Sunday Week 10

import sys

class MazeError(Exception):
    def __init__(self, message):
        self.message = message


class Maze:
    boolean = 0
    data = ''
    filename = ''
    data_matrix = []
    data_row = []
    len_each_line = 0
    fline_matrix = []
    sline_matrix = []
    final_matrix = []
    data_row = []
    new_matrix = []
    matrix = []
    area_number = 0
    yellow_line = {}
    each_yellow = []
    gate_list = []
    cross_group = []
    generated_matrix = []
    inaccessible_list = []
    anna_list = []
    dict_num = {}
    line_stack = []  # 用栈来计算连续横线
    pack_list = []
    walls = ['% Walls\n']
    pillars = ['% Pillars\n']
    cul_de_sacs_list = ['% Inner points in accessible cul-de-sacs\n']
    Entry_exit = ['% Entry-exit paths without intersections\n']
    def __init__(self, filename):
        self.filename = filename
        new_file = open(filename)
        self.data = new_file.read()
        new_file.close()
        self.check_function()
        self.encode_matrix()# 将矩阵编码
        # REPLACE PASS ABOVE WITH YOUR CODE
    def check_function(self):
        self.data = self.data.replace(' ', '')
        check_set = {'0', '1', '2', '3', '\n', ' '}  # 判断是不是正确输入
        for each in self.data:
            if each not in check_set:
                raise MazeError('Incorrect input.')
        self.data = self.data.split('\n')

        for each_line in self.data:  # 将字符串倒入矩阵
            if len(each_line) > 0:
                for each_char in each_line:
                    self.data_row.append(int(each_char))
                self.data_matrix.append(self.data_row)
                self.data_row = []
        len_each_line = len(self.data_matrix[0])
        for each_line in self.data_matrix:
            if len(each_line) != len_each_line:
                raise MazeError('Incorrect input.')

        if 2 > len(self.data_matrix) or len(self.data_matrix) > 41 or len_each_line > 31 or len_each_line < 2:
            raise MazeError('Incorrect input.')
        for each_char in self.data_matrix[-1]:
            if each_char == 2 or each_char == 3:
                raise MazeError('Input does not represent a maze.')
        for each_line in self.data_matrix:  # 检查矩阵
            if each_line[-1] == 1 or each_line[-1] == 3:
                raise MazeError('Input does not represent a maze.')
    # POSSIBLY DEFINE OTHER METHODS
    def encode_matrix(self):
        for each_line in self.data_matrix:
            for each_char in each_line:
                if each_char == 0:
                    self.fline_matrix.extend([1, 0])
                    self.sline_matrix.extend([0, 0])
                elif each_char == 1:
                    self.fline_matrix.extend([1, 1])
                    self.sline_matrix.extend([0, 0])
                elif each_char == 2:
                    self.fline_matrix.extend([1, 0])
                    self.sline_matrix.extend([1, 0])
                elif each_char == 3:
                    self.fline_matrix.extend([1, 1])
                    self.sline_matrix.extend([1, 0])
            self.final_matrix.append(self.fline_matrix)
            self.final_matrix.append(self.sline_matrix)
            self.fline_matrix = []
            self.sline_matrix = []



    def analyse(self):
        self.boolean += 1
        self.find_gate()
        self.set_of_walls()
        self.area_number = self.inaccessible_point()
        self.accessible_areas(self.area_number)
        self.cul_de_sacs(self.area_number)
        self.entry_exit()
        # REPLACE PASS ABOVE WITH YOUR CODE

    def find_gate(self):
        count = 0
        for row in range(len(self.final_matrix[0]) - 1):
            if self.final_matrix[0][row] == 0:
                self.gate_list.append((0, row))
                count += 1
        for row in range(len(self.final_matrix[0]) - 1):
            if self.final_matrix[-2][row] == 0:
                self.gate_list.append((len(self.final_matrix) - 2, row))
                count += 1
        for row in range(len(self.final_matrix) - 1):
            if self.final_matrix[row][0] == 0:
                self.gate_list.append((row, 0))
                count += 1
            if self.final_matrix[row][-2] == 0:
                self.gate_list.append((row, len(self.final_matrix[row]) - 2))
                count += 1
        if self.boolean == 1:
            if count == 0:
                print('The maze has no gate.')
            if count == 1:
                print('The maze has a single gate.')
            if count >= 2:
                print('The maze has %d gates.' % (count))

    def search(self, row, col, my_color, matrix, number):
        position_array = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        if len(matrix) > row >= 0 and len(matrix[0]) > col >= 0 and matrix[row][col] == number:
            matrix[row][col] = my_color
            self.anna_list.append((row, col))
            for r, c in position_array:
                self.search(row + r, col + c, my_color, matrix, number)
        else:
            return

    def larger_matrix(self, matrix):  # 矩阵扩边
        matrix = []
        list_ele = [0]
        width = len(self.new_matrix[0]) + 2
        matrix.append(width * [0])
        for each in self.new_matrix:
            list_ele.extend(each)
            list_ele.extend([0])
            matrix.append(list_ele)
            list_ele = [0]
        matrix.append(width * [0])
        return matrix

    def set_of_walls(self):
        my_color = 2
        self.new_matrix = list(self.final_matrix)
        self.matrix = self.larger_matrix(self.matrix)
        for i in range(1, len(self.matrix) - 1):  # 柱子消失之术
            for j in range(1, len(self.matrix[i]) - 1):
                if self.matrix[i][j] == 1 and self.matrix[i + 1][j] == 0 and self.matrix[i][j + 1] == 0 and \
                        self.matrix[i + 1][j + 1] == 0 and self.matrix[i - 1][j] == 0 and self.matrix[i][j - 1] == 0 and self.matrix[i - 1][
                    j - 1] == 0 and \
                        self.matrix[i - 1][j + 1] == 0 and self.matrix[i + 1][j - 1] == 0:
                    self.matrix[i][j] = 0

        for row in range(len(self.matrix)):
            for col in range(len(self.matrix[row])):
                if self.matrix[row][col] == 1:
                    self.search(row, col, my_color, self.matrix, 1)
                    my_color += 1
        my_color -= 2
        indicator = 0
        for row in self.matrix:
            for col in row:
                if col != 0:
                    indicator = 1
                    break
        if self.boolean == 1:
            if indicator == 0:
                print('The maze has no wall.')
            if my_color == 1:
                print('The maze has walls that are all connected.')
            elif indicator != 0:
                print('The maze has %d sets of walls that are all connected.' % (my_color))

    def decode(self):
        in_count = 0
        for row in range(1, len(self.matrix) - 1, 2):
            for col in range(1, len(self.matrix[row]) - 1, 2):  # 找点！五种情况
                if self.matrix[row][col] == 1:
                    if self.matrix[row][col + 1] != 1 or self.matrix[row + 1][col] != 1 or self.matrix[row + 1][col + 1] != 1:
                        in_count += 1
        return in_count

    def inaccessible_point(self):
        my_color = 1
        in_count = 0
        self.new_matrix = list(self.final_matrix)
        self.matrix = self.larger_matrix(self.matrix)
        self.search(0, 0, my_color, self.matrix, 0)
        my_color += 1
        for row in range(len(self.matrix)):
            for col in range(len(self.matrix[row])):
                self.anna_list = []
                if self.matrix[row][col] == 0:
                    self.search(row, col, my_color, self.matrix, 0)
                    self.inaccessible_list.extend(self.anna_list)
                    my_color += 1
        my_color -= 2
        in_count = self.decode()
        if self.boolean == 1:
            if in_count == 0:
                print('The maze has no inaccessible inner point.')
            elif in_count == 1:
                print('The maze has a unique inaccessible inner point.')
            else:
                print('The maze has %d inaccessible inner points.' % (in_count))
        return my_color

    def accessible_areas(self, area_number):

        my_color = 2
        self.matrix = []
        ele = []
        for row in range(len(self.final_matrix) - 1):
            for col in range(len(self.final_matrix[0]) - 1):
                ele.append(self.final_matrix[row][col])
            self.matrix.append(ele)
            ele = []

        for row in range(len(self.matrix)):
            for col in range(len(self.matrix[0])):
                if self.matrix[row][col] == 0:
                    self.search(row, col, my_color, self.matrix, 0)
                    my_color += 1
        my_color -= 2
        my_color = my_color - area_number
        if self.boolean == 1:
            if my_color == 0:
                print('The maze has no accessible area.')
            elif my_color == 1:
                print('The maze has a unique accessible area.')
            else:
                print('The maze has %d accessible areas.' % (my_color))

    def grouping(self, each, new_lost_group, cout):
        position_array = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for r, c in position_array:
            if (each[0] + r, each[1] + c) in new_lost_group:
                self.dict_num[cout].append((each[0] + r, each[1] + c))
                new_lost_group.remove((each[0] + r, each[1] + c))
                self.grouping((each[0] + r, each[1] + c), new_lost_group, cout)
        return

    def cul_de_sacs(self, area_number):
        self.matrix = []
        combine = [0]
        num_count = 0
        group = {}
        lost_group = []
        group_list = []
        dict_list = []
        in_count = 0
        first_line = [0] * (len(self.final_matrix[0]) + 1)
        self.matrix.append(first_line)
        for each_line in self.final_matrix:
            combine.extend(each_line)
            self.matrix.append(combine)
            combine = [0]

        my_color = 2
        for row in range(0, len(self.matrix)): #染色
            for col in range(0, len(self.matrix[0])):
                if self.matrix[row][col] == 0:
                    self.search(row, col, my_color, self.matrix, 0)
                    my_color += 1

        for row in range(len(self.matrix)): #染色
            for col in range(len(self.matrix[0])):
                if self.matrix[row][col] > 2:
                    self.matrix[row][col] = 1
         # 弄好点集
        for row in range(len(self.matrix)):
            for col in range(len(self.matrix[0])):
                if self.matrix[row][col] == 2:
                    group_list.append((row, col))
        group[2] = group_list
        group_list = []

        for each_group in group:
            one_each_group = list(group[each_group])

            while len(one_each_group) != 0:
                count = 0
                for each in group[each_group]:
                    if each in one_each_group:

                        for posi in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                            if (each[0] + posi[0], each[1] + posi[1]) in one_each_group:
                                num_count += 1
                        if num_count <= 1:
                            lost_group.append(each)
                            one_each_group.remove(each)
                            count += 1
                        num_count = 0
                if count == 0:
                    break

        # 解码
        if len(lost_group) == 0 and self.boolean == 1:
            print('The maze has no accessible cul-de-sac.')
            return 0
        else:
            self.cross_group = list(lost_group)
            cout = 1
            new_lost_group = list(lost_group)
            for each in lost_group:
                if each in new_lost_group:
                    self.dict_num[cout] = []
                    if len(lost_group) != 0:
                        self.dict_num[cout].append(each)
                        new_lost_group.remove(each)
                        self.grouping(each, new_lost_group, cout)
                    cout += 1

        if self.boolean == 1:
            if (list(self.dict_num.keys())[-1]) == 0:
                print('The maze has no accessible cul-de-sac.')
            if (list(self.dict_num.keys())[-1]) == 1:
                print('The maze has accessible cul-de-sacs that are all connected.')
            if (list(self.dict_num.keys())[-1]) > 1:
                print('The maze has %d sets of accessible cul-de-sacs that are all connected.' % (
                            list(self.dict_num.keys())[-1]))
    def entry_exit(self):
        count = 1
        entry_list = []
        for x, y in self.gate_list: #门的位置
            entry_list.append((x + 1, y + 1))
        lost_entry = list(entry_list)
        for row in range(len(self.matrix)):#矩阵变色
            self.matrix[row][0] = 0
            self.matrix[row][-1] = 0
        for line in range(len(self.matrix[0])):
            self.matrix[0][line] = 0
            self.matrix[-1][line] = 0
        for x, y in self.cross_group:#错路变色
            self.matrix[x][y] = 0

        for r, w in entry_list:#找通路
            if (r, w) in lost_entry:
                lost_entry.remove((r, w))
                self.each_yellow.append((r, w))
                self.search_exit(r, w, lost_entry)
                if self.each_yellow[-1] in entry_list and len(self.each_yellow) >= 2:
                    self.yellow_line[count] = self.each_yellow
                    count += 1
                self.each_yellow = []
        if self.boolean == 1:
            if len(self.yellow_line) == 0:
                print('The maze has no entry-exit path with no intersection not to cul-de-sacs.')
            elif len(self.yellow_line) == 1:
                print('The maze has a unique entry-exit path with no intersection not to cul-de-sacs.')
            elif len(self.yellow_line) > 1:
                print('The maze has %d entry-exit paths with no intersections not to cul-de-sacs.' %(len(self.yellow_line)))



    def search_exit(self, r, w, lost_entry):
        fnum = 0
        snum = 0
        count = 0
        self.matrix[r][w] = 1
        if (r, w) in lost_entry:
            lost_entry.remove((r, w))
            return
        for posi in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            if self.matrix[r + posi[0]][w + posi[1]] == 2:
                fnum = posi[0]
                snum = posi[1]
                count += 1
        if count == 1:
            self.each_yellow.append((fnum + r, w + snum))
            self.search_exit(fnum + r, w + snum, lost_entry)
        else:
            return

    def display(self):
        self.boolean = -1
        self.analyse()
        self.generated_matrix = list(self.final_matrix)
        self.generated_matrix = self.larger_matrix(self.generated_matrix)
        for i in range(1, len(self.generated_matrix) - 1): #找柱子并染色
            for j in range(1, len(self.generated_matrix[i]) - 1):
                if self.generated_matrix[i][j] == 1 and self.generated_matrix[i + 1][j] == 0 and self.generated_matrix[i][j + 1] == 0 and \
                        self.generated_matrix[i + 1][j + 1] == 0 and self.generated_matrix[i - 1][j] == 0 and self.generated_matrix[i][j - 1] == 0 and \
                        self.generated_matrix[i - 1][j - 1] == 0 and \
                        self.generated_matrix[i - 1][j + 1] == 0 and self.generated_matrix[i + 1][j - 1] == 0:
                    self.generated_matrix[i][j] = 4
        if len(self.dict_num) != 0:
            for each_list in self.dict_num: #红叉
                for r, l in self.dict_num[each_list]:
                    self.generated_matrix[r][l] = 2
        if len(self.yellow_line) != 0:
            for each_list in self.yellow_line: #黄线
                for r, l in self.yellow_line[each_list]:
                    self.generated_matrix[r][l] = 3
        if len(self.inaccessible_list) != 0: #封闭图形
            for x, y in self.inaccessible_list:
                self.generated_matrix[x][y] = 0
        for row in range(1, len(self.generated_matrix) - 1, 2):#开始遍历矩阵
            for col in range(1, len(self.generated_matrix[row]) - 1, 2):
                self.check_picture(row, col)#画横线和叉叉和柱子

        if len(self.line_stack) != 0:#捕获最后一项
            self.walls.append('    \draw (' + str(self.line_stack[-2][0]) + ',' + str(self.line_stack[-2][1]) + ') -- (' + str(self.line_stack[-1][0]) + ',' + str(self.line_stack[-1][1]) + ');\n')
            self.line_stack = []

        for col in range(1, len(self.generated_matrix[row]) - 1, 2): #开始遍历矩阵
            for row in range(1, len(self.generated_matrix) - 1, 2):
                self.draw_col(row, col)#画竖线

        if len(self.line_stack) != 0:  # 捕获最后一项
            self.walls.append('    \draw (' + str(self.line_stack[-2][0]) + ',' + str(self.line_stack[-2][1]) + ') -- (' + str(self.line_stack[-1][0]) + ',' + str(self.line_stack[-1][1]) + ');\n')
            self.line_stack = []

        self.draw_line() #画虚线
        self.pack_sort()
        self.draw()

    def check_picture(self, row, col):#画横线和叉叉的情况
        if self.generated_matrix[row][col] == 1 and self.generated_matrix[row][col + 1] == 1 :# 1的情况
            if len(self.line_stack) == 0:
                self.line_stack.append((int(col/2 - 0.5), int(row/2 - 0.5)))
                self.line_stack.append((int(col/2 + 0.5), int(row/2 - 0.5)))
            else:
                if self.line_stack[-1] == (int(col/2 - 0.5), int(row/2 - 0.5)):
                    self.line_stack.pop()
                    self.line_stack.append((int(col / 2 + 0.5), int(row / 2 - 0.5)))
                elif self.line_stack[-1] != (int(col/2 - 0.5), int(row/2 - 0.5)):

                    self.walls.append('    \draw (' + str(self.line_stack[-2][0]) + ',' + str(self.line_stack[-2][1]) + ') -- (' + str(self.line_stack[-1][0]) + ',' + str(self.line_stack[-1][1]) + ');\n')
                    self.line_stack = []
                    self.line_stack.append((int(col/2 - 0.5), int(row/2 - 0.5)))
                    self.line_stack.append((int(col / 2 + 0.5), int(row / 2 - 0.5)))

        if self.generated_matrix[row][col] == 1 and self.generated_matrix[row + 1][col] == 2 and \
                self.generated_matrix[row][col + 1] == 1 and self.generated_matrix[row + 1][col + 1] == 2:  # 1错的情况
                self.cul_de_sacs_list.append('    \\node at (' + str(col / 2) + ',' + str(row / 2) + ') {};\n')

        elif self.generated_matrix[row][col] == 1 and self.generated_matrix[row + 1][col] == 1 and \
            self.generated_matrix[row][col + 1] != 1 and self.generated_matrix[row + 1][col + 1] != 1\
                and self.generated_matrix[row][col + 1] == self.generated_matrix[row + 1][col + 1]:# 2的情况
            if self.generated_matrix[row + 1][col + 1] == 2:# 2错的情况
                self.cul_de_sacs_list.append('    \\node at (' + str(col / 2) + ',' + str(row / 2) + ') {};\n')

        elif self.generated_matrix[row][col] == 1 and self.generated_matrix[row + 1][col] == 1 and \
            self.generated_matrix[row][col + 1] == 1 and self.generated_matrix[row + 1][col + 1] != 1:# 3的情况
            if self.generated_matrix[row + 1][col + 1] == 2:#3错的情况
                self.cul_de_sacs_list.append('    \\node at (' + str(col / 2) + ',' + str(row / 2) + ') {};\n')

        elif self.generated_matrix[row][col] == 1 and self.generated_matrix[row + 1][col] == 2 and \
            self.generated_matrix[row][col + 1] == 2 and self.generated_matrix[row + 1][col + 1] == 2:# 0错的情况
            self.cul_de_sacs_list.append('    \\node at (' + str(col / 2) + ',' + str(row / 2) + ') {};\n')

        elif self.generated_matrix[row][col] == 4: #绿柱
            self.pillars.append('    \\fill[green] (' + str(int(col/2 - 0.5)) + ',' + str(int(row/2 - 0.5)) + ') circle(0.2);\n')
            for p, c in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:#四角搜索
                if self.generated_matrix[row + p][col + c] == 3:
                    first_ele = (((col - c) / 2 - 0.5), ((row + p) / 2 - 0.5))
                    second_ele = (((col + c) / 2 - 0.5), ((row + p) / 2 - 0.5))
                    if [first_ele, second_ele] not in self.pack_list and [second_ele, first_ele] not in self.pack_list:
                        self.pack_list.append([first_ele, second_ele])

                    first_ele = (((col + c) / 2 - 0.5), ((row + p) / 2 - 0.5))
                    second_ele = (((col + c) / 2 - 0.5), ((row - p) / 2 - 0.5))
                    if [first_ele, second_ele] not in self.pack_list and [second_ele, first_ele] not in self.pack_list:
                        self.pack_list.append([first_ele, second_ele])


    def draw_col(self, row, col):
        if self.generated_matrix[row][col] == 1 and self.generated_matrix[row + 1][col] == 1 :# 2的情况
            if len(self.line_stack) == 0:
                self.line_stack.append((int(col/2 - 0.5), int(row/2 - 0.5)))
                self.line_stack.append((int(col/2 - 0.5), int((row + 1)/2)))
            else:
                if self.line_stack[-1] == (int(col/2 - 0.5), int(row/2 - 0.5)):
                    self.line_stack.pop()
                    self.line_stack.append((int(col / 2 - 0.5), int((row + 1)/2)))
                elif self.line_stack[-1] != (int(col/2 - 0.5), int(row/2 - 0.5)):
                    self.walls.append('    \draw (' + str(self.line_stack[-2][0]) + ',' + str(self.line_stack[-2][1]) + ') -- (' + str(self.line_stack[-1][0]) + ',' + str(self.line_stack[-1][1]) + ');\n')
                    self.line_stack = []
                    self.line_stack.append((int(col/2 - 0.5), int(row/2 - 0.5)))
                    self.line_stack.append((int(col / 2 - 0.5), int((row + 1)/2)))

    def draw_line(self):
        for row in range(len(self.generated_matrix)): #涂黑矩阵
            for col in range(len(self.generated_matrix[row])):
                if self.generated_matrix[row][col] == 0 or self.generated_matrix[row][col] == 2:
                    self.generated_matrix[row][col] = 1
        for col in range(len(self.generated_matrix[-2])):#修正矩阵
            if self.generated_matrix[-3][col] == 3 and self.generated_matrix[-3][col - 1] == 1 and \
                    self.generated_matrix[-3][col + 1] == 1:
                self.generated_matrix[-2][col] = 3
        for row in range(len(self.generated_matrix)):# 修正矩阵
            if self.generated_matrix[row][-3] == 3 and self.generated_matrix[row + 1][-3] == 1 and \
                    self.generated_matrix[row - 1][-3] == 1:
                self.generated_matrix[row][-2] = 3

        for row in range(1, len(self.generated_matrix) - 1, 2):#开始遍历矩阵
            for col in range(1, len(self.generated_matrix[row]) - 1, 2):
                if self.generated_matrix[row][col] == 1 and self.generated_matrix[row][col + 1] == 1 and \
                        self.generated_matrix[row + 1][col] == 3 and self.generated_matrix[row + 1][col + 1] == 3:  # 1的情况
                    first_ele = (((col - 2) / 2), (row / 2))
                    second_ele = ((col / 2), (row / 2))
                    if [first_ele, second_ele] not in self.pack_list and [second_ele, first_ele] not in self.pack_list:
                        self.pack_list.append([first_ele, second_ele])
                    #self.Entry_exit.append('    \draw[dashed, yellow] (' + str((col - 2) / 2) + ',' + str(row / 2) + ') -- (' + str(col / 2) + ',' + str(row / 2) + ');\n')
                elif self.generated_matrix[row][col] == 1 and self.generated_matrix[row + 1][col] == 1 and \
                        self.generated_matrix[row][col + 1] == 3 and self.generated_matrix[row + 1][col + 1] == 3:  # 2的情况
                    first_ele = ((col / 2), (row / 2 - 1))
                    second_ele = ((col / 2),  (row / 2))
                    if [first_ele, second_ele] not in self.pack_list and [second_ele, first_ele] not in self.pack_list:
                        self.pack_list.append([first_ele, second_ele])
                    #self.Entry_exit.append('    \draw[dashed, yellow] (' + str(col / 2) + ',' + str(row / 2 - 1) + ') -- (' + str(col / 2) + ',' + str(row / 2) + ');\n')

                elif self.generated_matrix[row][col] == 1 and self.generated_matrix[row + 1][col] == 3 and \
                        self.generated_matrix[row][col + 1] == 3 and self.generated_matrix[row + 1][col + 1] == 3:  # 0的情况
                    first_ele = (((col - 2) / 2), (row / 2))
                    second_ele = ((col / 2), (row / 2))
                    if [first_ele, second_ele] not in self.pack_list and [second_ele, first_ele] not in self.pack_list:
                        self.pack_list.append([first_ele, second_ele])
                    first_ele = ((col / 2), (row / 2 - 1))
                    second_ele = ((col / 2), (row / 2))
                    if [first_ele, second_ele] not in self.pack_list and [second_ele, first_ele] not in self.pack_list:
                        self.pack_list.append([first_ele, second_ele])

    def pack_sort(self):
        newlist = []
        for each in self.pack_list:
            box_list = []
            if each[1][0] - each[0][0] == 1:
                newlist.append(each)
            if each[1][0] - each[0][0] == -1:
                box_list.append((each[1][0], each[1][1]))
                box_list.append((each[0][0], each[0][1]))
                newlist.append(box_list)


        self.line_stack = []#栈连接
        newlist = sorted(newlist, key=(lambda x: x[0][1]))
        for each in newlist:
            if len(self.line_stack) == 0:
                self.line_stack.append(each[0])
                self.line_stack.append(each[1])
            elif self.line_stack[-1] == each[0]:
                self.line_stack.pop()
                self.line_stack.append(each[1])
            elif self.line_stack[-1] != each[0]:
                self.Entry_exit.append('    \draw[dashed, yellow] (' + str(self.line_stack[-2][0]) + ',' + str(self.line_stack[-2][1]) + ') -- (' + str(self.line_stack[-1][0]) + ',' + str(self.line_stack[-1][1]) + ');\n')
                self.line_stack = []
                self.line_stack.append(each[0])
                self.line_stack.append(each[1])
        if len(self.line_stack) != 0:
            self.Entry_exit.append('    \draw[dashed, yellow] (' + str(self.line_stack[-2][0]) + ',' + str(self.line_stack[-2][1]) + ') -- (' + str(self.line_stack[-1][0]) + ',' + str(self.line_stack[-1][1]) + ');\n')

        newlist = []
        for each in self.pack_list:
            box_list = []
            if each[0][1] - each[1][1] == -1:
                newlist.append(each)
            if each[0][1] - each[1][1] == 1:
                box_list.append((each[1][0], each[1][1]))
                box_list.append((each[0][0], each[0][1]))
                newlist.append(box_list)

        newlist = sorted(newlist, key=(lambda x: x[0]))
        self.line_stack = []#栈连接
        for each in newlist:
            if len(self.line_stack) == 0:
                self.line_stack.append(each[0])
                self.line_stack.append(each[1])
            elif self.line_stack[-1] == each[0]:
                self.line_stack.pop()
                self.line_stack.append(each[1])
            elif self.line_stack[-1] != each[0]:
                self.Entry_exit.append('    \draw[dashed, yellow] (' + str(self.line_stack[-2][0]) + ',' + str(self.line_stack[-2][1]) + ') -- (' + str(self.line_stack[-1][0]) + ',' + str(self.line_stack[-1][1]) + ');\n')
                self.line_stack = []
                self.line_stack.append(each[0])
                self.line_stack.append(each[1])
        if len(self.line_stack) != 0:
            self.Entry_exit.append('    \draw[dashed, yellow] (' + str(self.line_stack[-2][0]) + ',' + str(self.line_stack[-2][1]) + ') -- (' + str(self.line_stack[-1][0]) + ',' + str(self.line_stack[-1][1]) + ');\n')

    def draw(self):
        tex_file_name = self.filename.split('.')[0] + ".tex"
        tex_file = open(tex_file_name, 'w')
        head = ["\\documentclass[10pt]{article}\n",
                "\\usepackage{tikz}\n",
                "\\usetikzlibrary{shapes.misc}\n",
                "\\usepackage[margin=0cm]{geometry}\n",
                "\\pagestyle{empty}\n",
                "\\tikzstyle{every node}=[cross out, draw, red]\n",
                "\n",
                "\\begin{document}\n",
                "\n",
                "\\vspace*{\\fill}\n",
                "\\begin{center}\n",
                "\\begin{tikzpicture}[x=0.5cm, y=-0.5cm, ultra thick, blue]\n"
                ]
        border = ["\\end{tikzpicture}\n", "\\end{center}\n", "\\vspace*{\\fill}\n", "\n", "\\end{document}\n"]
        tex_file.writelines(head)
        tex_file.writelines(self.walls)
        tex_file.writelines(self.pillars)
        tex_file.writelines(self.cul_de_sacs_list)
        tex_file.writelines(self.Entry_exit)
        tex_file.writelines(border)


