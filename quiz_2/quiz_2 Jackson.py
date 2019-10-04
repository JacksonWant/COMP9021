# COMP9021 19T3 - Rachid Hamadi
# Quiz 2 *** Due Thursday Week 3


import sys
from random import seed, randrange
from pprint import pprint
from typing import List, Any

try:
    arg_for_seed, upper_bound = (abs(int(x)) + 1 for x in input('Enter two integers: ').split())
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()

seed(arg_for_seed)
mapping = {}
for i in range(1, upper_bound):
    r = randrange(-upper_bound // 8, upper_bound)
    if r > 0:
        mapping[i] = r
print('\nThe generated mapping is:')
print('  ', mapping)
# sorted() can take as argument a list, a dictionary, a set...
keys = sorted(mapping.keys())
print('\nThe keys are, from smallest to largest: ')
print('  ', keys)

cycles = []
reversed_dict_per_length = {}

# INSERT YOUR CODE HERE
#第一问深度优先搜索dfs
mapplinglist = sorted(list(mapping.keys()))
mappingvalue = list(mapping.values())
Visit = []#已访问节点
vcycle = []#成回路节点
def dfsmapping(viskey):
    if viskey != mapping[viskey]:
        vcycle.append(viskey)  # 将第一个节点添加到list链
        if mapping[viskey] in mapplinglist and mapping[viskey] not in Visit:#判断值是否是另一个点的键 且该点是新点
            if mapping[mapping[viskey]] not in vcycle:
                dfsmapping(mapping[viskey])
            else:
                if mapping[mapping[viskey]] == vcycle[0]:
                    vcycle.append(mapping[viskey])
                    Visit.append(mapping[viskey])
                    cycles.append(vcycle)

for Ckey in mapplinglist:
    if Ckey not in Visit:#判断该节点是否被访问
        Visit.append(Ckey)  # 将点标为已访问
        if Ckey == mapping[Ckey]:
            cycles.append([Ckey])
        else:
            dfsmapping(Ckey)
            vcycle = []#清空vcycle

#第二问

add = {}#安装字典
findt = []#排列好的list
maxlenth = 0#最大长度
for f in sorted(mappingvalue):
    if sorted(mappingvalue).count(f) > maxlenth:
        maxlenth = sorted(mappingvalue).count(f)

for k in range(1, maxlenth + 1):
    for i in sorted(mappingvalue):
        if sorted(mappingvalue).count(i) == k:
            add[i] = [x for x in mapplinglist if mapping[x] == i]
    if add != {}:
        reversed_dict_per_length[k] = add
    add = {}


print('\nProperly ordered, the cycles given by the mapping are: ')
print('  ', cycles)
print('\nThe (triply ordered) reversed dictionary per lengths is: ')
pprint(reversed_dict_per_length)
