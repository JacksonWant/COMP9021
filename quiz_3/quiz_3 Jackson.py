# COMP9021 19T3 - Rachid Hamadi
# Quiz 3 *** Due Thursday Week 4


# Reading the number written in base 8 from right to left,
# keeping the leading 0's, if any:
# 0: move N     1: move NE    2: move E     3: move SE
# 4: move S     5: move SW    6: move W     7: move NW
#
# We start from a position that is the unique position
# where the switch is on.
#
# Moving to a position switches on to off, off to on there.

import sys

on = '\u26aa'
off = '\u26ab'
code = input('Enter a non-strictly negative integer: ').strip()
try:
    if code[0] == '-':
        raise ValueError
    int(code)
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()
nb_of_leading_zeroes = 0
for i in range(len(code) - 1):
    if code[i] == '0':
        nb_of_leading_zeroes += 1
    else:
        break
print("Keeping leading 0's, if any, in base 8,", code, 'reads as',
      '0' * nb_of_leading_zeroes + f'{int(code):o}.'
     )
print()

# INSERT YOUR CODE HERE
newcode = '0' * nb_of_leading_zeroes + f'{int(code):o}'
nodes = [[0, 0]]
nnodes = []
newnodes = []
#该类的对象负责记录点的轨迹和边界
class nodepostion(object):
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y
        self.edges = [0, 0, 0, 0] #RLUD
        self.distance = [] #RL UD

    def calaulatepoint(self, position):
        if position == '0' or position == '1' or position == '7':
            self.y += 1
        if position == '2' or position == '1' or position == '3':
            self.x += 1
        if position == '3' or position == '4' or position == '5':
            self.y -= 1
        if position == '5' or position == '6' or position == '7':
            self.x -= 1

    def recording(self):
        nodes.append([self.x, self.y])

    def updatenodes(self):
        for rnode in nodes:
            if nodes.count(rnode) % 2 != 0:
                nnodes.append(rnode)
        #对零值进行更新
        for everynode in nnodes:
            u = everynode[0] - nnodes[0][0]
            v = everynode[1] - nnodes[0][1]
            newnodes.append([u, v])
        for node in newnodes:
            if node[0] > self.edges[0]:
                self.edges[0] = node[0]
            elif node[0] < self.edges[1]:
                self.edges[1] = node[0]
            if node[1] > self.edges[2]:
                self.edges[2] = node[1]
            elif node[1] < self.edges[3]:
                self.edges[3] = node[1]
        for dist in range(0, 4, 2):
            self.distance.append(self.edges[dist] - self.edges[dist + 1] + 1)
        if newnodes == []:
            self.distance[0] = 0
            self.distance[1] = 0

    def updatematrix(self): #对坐标进行更新
        for node in newnodes:
            node[0] = node[0] - self.edges[1]
            node[1] = 0 - (node[1] - self.edges[2])

newnode = nodepostion()
for node in newcode[::-1]:
    newnode.calaulatepoint(node)
    newnode.recording()
newnode.updatenodes()
newnode.updatematrix()

#建立二维矩阵
mapmatrix = [['0' for i in range(newnode.distance[0])]for j in range(newnode.distance[1])]
#遍历矩阵
for replace in newnodes:
    mapmatrix[replace[1]][replace[0]] = '1'
for horizental in range(len(mapmatrix)):
    for vertical in mapmatrix[horizental]:
        if vertical == '0':
            print('\u26ab', end = "")
        elif vertical == '1':
            print('\u26aa', end = "")
    if horizental != len(mapmatrix) - 1:
        print()




