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
