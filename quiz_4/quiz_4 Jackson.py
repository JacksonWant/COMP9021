# COMP9021 19T3 - Rachid Hamadi
# Quiz 4 *** Due Thursday Week 5
#
# Prompts the user for an arity (a natural number) n and a word.
# Call symbol a word consisting of nothing but alphabetic characters
# and underscores.
# Checks that the word is valid, in that it satisfies the following
# inductive definition:
# - a symbol, with spaces allowed at both ends, is a valid word;
# - a word of the form s(w_1,...,w_n) with s denoting a symbol and
#   w_1, ..., w_n denoting valid words, with spaces allowed at both ends
#   and around parentheses and commas, is a valid word.


import sys
#使用栈
def is_valid(word, arity):
    # REPLACE THE RETURN STATEMENT ABOVE WITH YOUR CODE
    alert = 0
    bracket = 0
    comma = ''
    comma = comma.join(word.split())
    for check in range(len(comma)):
        if comma[check].isdigit() == True:
            return False
        elif comma[check].isalpha() == True or comma[check] == '_':
            alert = 1 #alert代表有字母
        elif comma[check] == '(' and check != (len(comma) - 1):
            bracket = 1  #bracket代表有括号
            if comma[-1] != ')':
                return False #判断最后一位是否为右括号
            if comma[check + 1] == '(' or comma[check + 1] == ','or comma[check + 1] == ')':#左括号的后面不能出现(,
                return False
        elif comma[check] == ',' and check != (len(comma) - 1):
            if comma[check + 1] == ',' or comma[check + 1] == '(' or comma[check + 1] == ')':#逗号的后面不能出现,()
                return False
    if alert > 0 and bracket != 1 and arity != 0:
        return False #当输入为全字母时 arity必须为0
    if alert == 0: #如果没有字母出现 证明错
        return False

    Stack = []
    Numbaccount = []
    for char in word:
        if char == '(':
            Stack.append('(')
            Numbaccount.append(1)
        elif char == ')':
            if Stack != []:
                if Numbaccount[-1] != arity:
                    return False
                Stack.pop()
                Numbaccount.pop()
            else:
                return False#多右括号
        elif char == ',':
            Numbaccount[-1] += 1
    return False if Stack != [] else True


try:
    arity = int(input('Input an arity : '))
    if arity < 0:
        raise ValueError
except ValueError:
    print('Incorrect arity, giving up...')
    sys.exit()
word = input('Input a word: ')
if is_valid(word, arity):
    print('The word is valid.')
else:
    print('The word is invalid.')

