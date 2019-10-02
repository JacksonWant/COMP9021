import sys
import time
from random import seed, randrange
#导入random模块中seed,randrange函数
start=time.clock()
try:
    arg_for_seed, upper_bound = (abs(int(x)) + 1 for x in input('Enter two integers: ').split())
    #abs返回函数的绝对值，arg_for_seed, upper_bound得到输入整数的绝对值加一

except ValueError:
    #如果输入不是整数则执行except程序块
    print('Incorrect input, giving up.')
    sys.exit()

seed(arg_for_seed) #按一定规律出随机数
mapping = {} #mapping是一个空字典
for i in range(1, upper_bound):
    r = randrange(-upper_bound // 2, upper_bound) #randrange() 方法返回指定递增基数集合中的一个随机数
    #返回从[-upper_bound // 2 到 upper_bound） //除向下取整
    if r > 0:
        mapping[i] = r #添加键值对到mapping中
print('\nThe generated mapping is:')
print('  ', mapping)

mapping_as_a_list = []
one_to_one_part_of_mapping = {}
nonkeys = []
# INSERT YOUR CODE HERE
# JacksonWant
mapkeys = list(mapping.keys())
mapvalues = list(mapping.values())
maplen = len(mapping.values())
mapping_as_a_list = [None]
for i in range(1, upper_bound):
    if i not in mapkeys:
        nonkeys.append(i)
        mapping_as_a_list.append(None)
    else:
        mapping_as_a_list.append(mapping[i])
for i in mapvalues:
    if mapvalues.count(i) == 1:
        one_to_one_part_of_mapping[mapkeys[mapvalues.index(i)]] = mapvalues[mapvalues.index(i)]

print()
print('EDIT THIS PRINT STATEMENT')
print('The mappings\'s so-called \"keys\" make up a set whose number of elements is '+ str(maplen) + '.')
print('\nThe list of integers between 1 and', upper_bound - 1, 'that are not keys of the mapping is:')
print('  ', nonkeys)
print('\nRepresented as a list, the mapping is:')
print('  ', mapping_as_a_list)
# Recreating the dictionary, inserting keys from smallest to largest,
# to make sure the dictionary is printed out with keys from smallest to largest.
one_to_one_part_of_mapping = {key: one_to_one_part_of_mapping[key]
                                      for key in sorted(one_to_one_part_of_mapping)
                             }
print('\nThe one-to-one part of the mapping is:')
print('  ', one_to_one_part_of_mapping)
end=time.clock()
print("final is in ", end-start)
