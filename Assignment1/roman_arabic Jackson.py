import sys
import re

#字母表的顺序必须是固定的dictionary或者list
arab_roman = [(1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'),
     (100, 'C'), (90, 'XC'), (50, 'L'), (40, 'XL'), (10, 'X'),
    (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I')]
romanchar = {'M': 1000, 'D': 500, 'C': 100, 'L': 50, 'X': 10, 'V': 5, 'I': 1}
arab_romax = ''#阿拉伯转罗马
romax_arab = 0 #罗马转阿拉伯
customlist = []
combinelist = []
dictcustom = {}

def Sure(arbitrarily):#输出函数
    print('Sure! It is ' + str(arbitrarily))

def encodingformat(fiststring,thirdstring):#检查输入格式
    if fiststring.isalpha() == False or thirdstring.isalpha() == False:
        return False
    for each in thirdstring:#判断字母表是否冲突
        if thirdstring.count(each) > 1:
            return False
    for k in fiststring:#检查包含关系
        if k not in thirdstring:
            return False
    return True

def highcheck(inputint, customlist):

    beginint = int(str(customlist[0][0])[0])
    multiple = int(10**(len(str(customlist[0][0])) - 1))
    if beginint == 5:
        if inputint > ((beginint + 4) * multiple - 1):
            return False
        else:
            return True
    elif beginint == 1:
        if inputint >= ((beginint + 3) * multiple):
            return False
        else:
            return True

def alphaencoding(enstring, customlist, combinelist):#编写字母表
    newenstring = ''
    newenstring = newenstring.join(list((reversed(enstring))))#字母表反转
    for find in range(len(newenstring)):
        if find % 2 == 0:
            customlist.append((int(10**(find/2)), newenstring[find]))
        elif find % 2 != 0:
            customlist.append((5 * int(10 ** ((find - 1) // 2)), newenstring[find]))
    if len(customlist) != 1:
        for findtuple in range(len(customlist)):
            if findtuple != 0:
                if findtuple % 2 != 0:
                    number = int(customlist[findtuple][0] / 10 * 2)
                else:
                    number = int(customlist[findtuple][0] / 10)
                for value in customlist:
                    if value[0] == number:
                        combinelist.append((customlist[findtuple][0] - number, value[1] + customlist[findtuple][1]))
                        break
    temperorylist = customlist
    customlist = customlist + combinelist
    customlist.sort(reverse = True)
    temperorylist.sort(reverse = True)
    for v,k in temperorylist:
        dictcustom[k] = v
    return customlist, dictcustom

#第一问递归深度优先搜索dfs
def ArabictooRoman(arabnumber, arab_romax, encoding):
    while arabnumber != 0:
        for subtractor in encoding:
            if subtractor[0] <= arabnumber:
                arabnumber -= subtractor[0]
                arab_romax += subtractor[1]
                break
    return arab_romax

def RomantooAribic(Validchar, romax_arab, newalphabet):
    register = 0
    if len(Validchar) == 1:
        romax_arab = newalphabet[Validchar[0]]
        return romax_arab

    for one in range(len(Validchar)):
        if register == 1:
            register = 0
            continue
        if one != len(Validchar) - 1:
            if (newalphabet[Validchar[one]] >= newalphabet[Validchar[one + 1]]):
                romax_arab += newalphabet[Validchar[one]]
            else:
                romax_arab += newalphabet[Validchar[one + 1]] - newalphabet[Validchar[one]]
                register = 1
        else:
            if newalphabet[Validchar[-2]] >= newalphabet[Validchar[-1]]:
                romax_arab += newalphabet[Validchar[-1]]
    return romax_arab

def gformatcheck(newstring):
    if re.search(r'((\D)(\2))(\1)', newstring) != None:
        return False

def checkgroup(whichre, firsthalf):
    maxlen = 0
    which = 0
    trigger = 1
    halfone = 0
    halftwo = ''
    maxstring = ''
    while trigger == 1:
        for each in whichre:
            if each.match(firsthalf) != None:
                if len(each.match(firsthalf).group()) > maxlen:
                    maxstring = each.match(firsthalf).group()
                    maxlen = len(each.match(firsthalf).group())
                    which = whichre.index(each)

        if firsthalf == maxstring:
            trigger = 0
        else:

            for repeat in firsthalf[maxlen:]:
                if repeat in maxstring:
                    halfone = 1
                    halftwo = maxstring[:maxstring.index(repeat)]
            if halfone != 1:
                trigger = 0
            else:
                firsthalf = halftwo
                maxlen = 0
        if firsthalf == '':
            trigger = 0
            which = 5
            maxlen = 0

    return which, maxlen




def getvalue(check, rearray):
    newslice = ''
    newone = ''
    newtwo = ''
    count = 0
    newcheck = []
    for ind in check:
        if ind not in newcheck:
            newcheck.append(ind)
            count += 1
        elif ind in newcheck:
            newcheck.append(ind)
        if count <= 5:
            newone = ''.join(str(idx) for idx in newcheck)

    #重新编码

    for anychar in newone:
        if anychar not in newslice:
            newslice = newslice + anychar
    for char in newone:
        for key in newslice:
            if char == key:
                newtwo = newtwo + str(newslice.index(key))
    newone = newtwo
    which, lenth = checkgroup(rearray, newone)  # 调用匹配函数
    newone = newone[:lenth]
    newcheck = newcheck[lenth:]

    #将后续字符以零为开始赋值

    if len(newcheck) != 0:
        newvalue = newcheck[0]
        for each in range(len(newcheck)):
            newcheck[each] = newcheck[each] - newvalue
            if newcheck[each] < 0:
                which = 5

    return newone, newcheck, which



def addchar(firsthalf, check, getcode):
    if len(check) != 0:
        getcode = getcode + '_'
    return getcode

def grammarcheck(checkstring):
    check = []
    firsthalf = ''
    lasthalf = ''
    encoding = ''
    getencod = ''
    firstre = re.compile(r'0?(0{1,2}(1(2?2{1,2}3?|32)?)?)?')
    secondre = re.compile(r'01(2{1,3}3?)?')
    thirdre = re.compile(r'0{1,3}1{2}(12?|2)?')
    fourthre = re.compile(r'01(20|0(0){0,2}2?)')
    fifthre = re.compile(r'0120(2{1,3})3?')
    checkstring = list(reversed(checkstring))
    rearray = [firstre, secondre, thirdre, fourthre, fifthre]
    for ind in checkstring:
        check.append(checkstring.index(ind))
    for u in range(1, len(check)):
        if check[u] == 10:
            if 9 not in check:
                for i in range(1, len(check)):
                    if check[i] == 10:
                        check[i] = 9
    for anychar in checkstring:
        if anychar not in encoding:
            encoding = encoding + anychar
    while len(encoding) > 0:
        firsthalf, check, which = getvalue(check, rearray)
        if which == 0:
            firstmatch = firstre.match(firsthalf).group()
            if '3' in firstmatch and firstmatch.count('2') == 1:
                getencod = getencod + encoding[0] + encoding[1] + encoding[3] +encoding[2]
                encoding = encoding[4:]
            elif '3' in firstmatch and firstmatch.count('2') > 1:
                getencod = getencod + encoding[0] + encoding[1] + encoding[2] +encoding[3]
                encoding = encoding[4:]
            elif '2' in firstmatch:
                getencod = getencod + encoding[0] + encoding[1] + encoding[2]
                getencod = addchar(firsthalf, check, getencod)
                encoding = encoding[3:]
            elif '1' in firstmatch:
                getencod = getencod + encoding[0] + encoding[1]
                encoding = encoding[2:]
            else:
                getencod = getencod + encoding[0]
                getencod = addchar(firsthalf, check, getencod)
                encoding = encoding[1:]
        elif which == 1:
            secondmatch = secondre.match(firsthalf).group()
            if secondmatch == '0123':
                getencod = getencod + encoding[1] + encoding[0] + encoding[3] +encoding[2]
                encoding = encoding[4:]
            else:
                getencod = getencod + encoding[1] + encoding[0]
                encoding = encoding[2:]
                if '3' in secondmatch:
                    getencod = getencod + encoding[0] + encoding[1]
                    encoding = encoding[2:]
                elif '2' in secondmatch:
                    getencod = getencod + encoding[0]
                    getencod = addchar(firsthalf, check, getencod)
                    encoding = encoding[1:]
        elif which == 2:
            thirdmathch = thirdre.match(firsthalf).group()
            if '2' in thirdmathch:
                getencod = getencod + encoding[0] + '_' + encoding[1] + encoding[2]
                encoding = encoding[3:]
            else:
                getencod = getencod + encoding[0] + '_' + encoding[1]
                getencod = addchar(firsthalf, check, getencod)
                encoding = encoding[2:]
        elif which == 3:
            forthmathch = fourthre.match(firsthalf).group()
            if forthmathch == '0120':
                getencod = getencod + encoding[1] + '_' + encoding[0] + encoding[2]
                encoding = encoding[3:]
            else:
                if '2' in forthmathch:
                    getencod = getencod + encoding[1] + '_' + encoding[0] + encoding[2]
                    encoding = encoding[3:]
                else:
                    getencod = getencod + encoding[1] + '_' + encoding[0]
                    getencod = addchar(firsthalf, check, getencod)
                    encoding = encoding[2:]

        elif which == 4:

            fifthmatch = fifthre.match(firsthalf).group()
            getencod = getencod + encoding[1] + '_' + encoding[0] + '_' +encoding[2]
            encoding = encoding[3:]
            if '3' in fifthmatch:
                getencod = getencod + encoding[0]
                encoding = encoding[1:]
        else:
            getencod = ''
            break
    getencod = getencod[::-1]
    return getencod



try:
    sentense = input('How can I help you? ')
    inputformat = 'Please convert '
    if sentense[0:15] != inputformat:
        raise ValueError
    else:
        senslice = sentense[15:].split()
        #第一问的情况
        if len(senslice) == 1:
            if senslice[0].isdigit():#阿拉伯数字转罗马数字
                if senslice[0][0] != '0' and 4000 > int(senslice[0]) > 0:#判断输入是否是合法阿拉伯数字
                    arabnumber = int(senslice[0])
                    arab_romax = ArabictooRoman(arabnumber, arab_romax, arab_roman)
                    Sure(arab_romax)
                else:
                    raise IOError
            elif senslice[0].isalpha():
                for each in senslice[0]:
                    if each not in romanchar:
                        raise IOError
                romax_arab = RomantooAribic(senslice[0], romax_arab, romanchar)
                # 验证函数
                arab_romax = ArabictooRoman(romax_arab, arab_romax, arab_roman)
                if arab_romax != senslice[0]:
                    raise IOError
                else:
                    Sure(romax_arab)
        #第二问情况
        elif len(senslice) == 3 and senslice[1] == 'using':
            if senslice[0].isdigit() and senslice[2]:#当第一位为数字时 第三位为含有小写字母的英文
                if senslice[0][0] == '0':
                    raise IOError
                customlist, dictcustom = alphaencoding(senslice[2], customlist, combinelist)
                if highcheck(int(senslice[0]), customlist) == False:
                    raise IOError
                arab_romax = ArabictooRoman(int(senslice[0]), arab_romax, customlist)
                Sure(arab_romax)
            elif senslice[0].isdigit() == False and senslice[2].isdigit() == False:#检查两边是不是英文
                if encodingformat(senslice[0], senslice[2]) == False:#当第一位为英文 第三位也必须为英文 且后包含前
                    raise IOError
                customlist, dictcustom = alphaencoding(senslice[2], customlist, combinelist)
                romax_arab = RomantooAribic(senslice[0], romax_arab, dictcustom)
                # 验证函数
                if highcheck(romax_arab, customlist) == False:
                    raise IOError
                arab_romax = ArabictooRoman(romax_arab, arab_romax, customlist)
                if arab_romax != senslice[0]:
                    raise IOError
                else:
                    Sure(romax_arab)
            else:
                raise ValueError

        #第三问情况
        elif len(senslice) == 2 and senslice[1] == 'minimally':

            if senslice[0].isdigit() == False:
                for any in senslice[0]:
                    if any.isdigit() == True:
                        raise IOError
                if gformatcheck(senslice[0]) == False:
                    raise IOError
                #if mformatcheck(senslice[0]) == False:
                    #raise IOError
                else:
                    newalpha = grammarcheck(senslice[0])#得到字母序列！
                    if len(newalpha) == 0:
                        raise IOError

                    customlist,dictcustom = alphaencoding(newalpha, customlist, combinelist)#制成字母表！
                    romax_arab = RomantooAribic(senslice[0], romax_arab, dictcustom)
                    arab_romax = ArabictooRoman(romax_arab, arab_romax, customlist)
                    if arab_romax != senslice[0]:
                        raise IOError
                    else:
                        print('Sure! It is ' + str(romax_arab) + ' using ' + newalpha)

            else:
                raise IOError
        else:
            raise ValueError

except ValueError:
    print('I don\'t get what you want, sorry mate!')
    sys.exit()
except IOError:
    print('Hey, ask me something that\'s not impossible to do!')
    sys.exit()



