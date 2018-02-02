'''
def secret(n, arr1, arr2):
    print(['{0:b}'.format((i | j)).zfill(n).replace('0', ' ').replace('1', '#') for i, j in zip(arr1, arr2)])


secret(5, [9, 20, 28, 18, 11], [30, 1, 21, 17, 28])



import re


def dart(s):
    pat = re.compile(r'(\d|10)([SDT])([\*#]?)')
    temp = []
    proc = {'S': lambda x: x, 'D': lambda x: x**2, 'T': lambda x: x**3}
    print(pat.findall(s))
    for n, t, b in pat.findall(s):
        p = proc[t](int(n))
        if b == '#':
            p *= -1
        elif b == '*':
            p *= 2
            if temp:
                temp[-1] *= 2
        temp.append(p)
        print(temp)
    return sum(temp)


print(dart('1S2D*3T'))
print(dart('1D2S#10S'))
print(dart('1D2S0T'))
print(dart('1S*2T*3S'))
print(dart('1D#2S*3S'))
print(dart('1T2D3D#'))
print(dart('1D2S3T*'))

data = """
park 800905-1049118
kim  700905-1059119
"""

result = []
for line in data.split("\n"):
    word_result = []
    for word in line.split(" "):
        if len(word) == 14 and word[:6].isdigit() and word[7:].isdigit():
            word = word[:6] + "-" + "*******"
        word_result.append(word)
    result.append(" ".join(word_result))
print("\n".join(result))


import re

data = """
park 800905-1049118
kim  700905-1059119
"""

pat = re.compile("(\d{6})[-]\d{7}")
print(pat.sub("\g<1>-*******", data))


import re


def dart(inp):
    shot = re.findall(r'\d{1,2}[SDT][*#]?', inp)

    opt = [1,1,1]
    for i, s in enumerate(shot):
        if s[-1] == '#':
            opt[i] *= -1
            shot[i] = shot[i][:-1]
        elif s[-1] == '*':
            opt[i] *= 2
            shot[i] = shot[i][:-1]
            if i:
                opt[i-1] *= 2

    point = [(int(s[:-1]) ** '0SDT'.find(s[-1]) * o) for s, o in zip(shot, opt)]

    return sum(point)


print(dart('1S2D*3T'))
print(dart('1D2S#10S'))
print(dart('1D2S0T'))
print(dart('1S*2T*3S'))
print(dart('1D#2S*3S'))
print(dart('1T2D3D#'))
print(dart('1D2S3T*'))


p = re.compile(".+:")
m = p.search("http://google.com")
print(m.group())

def finbonachi(a):
	next_num = 0
	result = [1, 2]
	for i in range(3,a+1):
		next_num = result[i-2] + result[i-3]
		result.append(next_num)

	print(result)

finbonachi(10)


import math, os, re

def path_sum():
	path_sum = 0
	pre_index = 0
	result = []
	pwd = os.path.dirname(__file__)
	file = open("D:\\WEB\\DW\\blog2\\triangle.txt")
	list_file = file
	for i, numbers_set in enumerate(list_file):
		numbers_set = numbers_set[:-1].split(" ")
		#print(numbers_set)
		if i == 0:
			path_sum += int(numbers_set[i])
			result.append(int(numbers_set[i]))
			print("pre_index", pre_index)
		else :
			if (path_sum+int(numbers_set[pre_index])) > (path_sum+int(numbers_set[pre_index+1])):
				path_sum += int(numbers_set[pre_index])
				result.append(int(numbers_set[pre_index]))
				pre_index = pre_index
			else :
				path_sum += int(numbers_set[pre_index+1])
				result.append(int(numbers_set[pre_index+1]))
				pre_index = pre_index+1
			print("pre_index", pre_index)
	print("sum", path_sum)
	print("result", result)
	file.close()
#x= [[3], [7,4], [2,4,6], [8,5,9,3]]
path_sum()


import math, os, re

def four_sum():
	file = open("D:\\WEB\\DW\\blog2\\square.txt")
	list_file = file
	total =1
	pre_total = 1
	biggest_four = []
	total_list = []
	temp_biggest_four2 = []
	for i, numbers_set in enumerate(list_file):
		numbers_set = numbers_set.split()
		total_list.append(numbers_set)
		
	for k in range(20):
		for j in range(17):
			total = 1
			temp_biggest_four = []
			for x in range(j, j+4):
				total *= int(total_list[k][x])
				temp_biggest_four.append(total_list[k][x])
				if total >= pre_total :
					pre_total = total
					biggest_four = temp_biggest_four
			total = 1
			temp_biggest_four = []
			for x in range(j, j+4):
				total *= int(total_list[x][k])
				temp_biggest_four.append(total_list[x][k])
				if total >= pre_total :
					pre_total = total
					biggest_four = temp_biggest_four
			total = 1
			temp_biggest_four = []
			for x in range(4):
				total *= int(total_list[j+x][j+x])
				temp_biggest_four2.append(total_list[j+x][j+x])
				if total >= pre_total :
					pre_total = total
					biggest_four = temp_biggest_four
			total = 1
			temp_biggest_four = []
			for x in range(4):
				if x+k < 20 :
					total *= int(total_list[x+k][j+3-x])
					temp_biggest_four.append(total_list[x+k][j+3-x])
					if total >= pre_total :
						pre_total = total
						biggest_four = temp_biggest_four
	print(biggest_four)
	file.close()

four_sum()

def solution(ages):
    answer = 0
    ages_list= list(range(10001))
    ages_number = list(range(100))
    candle_set = list(range(10))
    candle_set_count = 1
    
    for i in range(len(ages)):
        age_number = str(ages[i])
        candle_number = list(age_number)
        for j in candle_number :
        	j = int(j)
        	print(j)
        	if j in candle_set:
        		candle_set.remove(j)
        		print(candle_set)
        	elif (j == 6) and (j not in candle_set) and (9 in candle_set):
        		candle_set.remove(9)
        	elif (j == 9) and (j not in candle_set) and (6 in candle_set):
        		candle_set.remove(6)
        	elif j not in candle_set:
        		candle_set_count +=1
        		candle_set += list(range(10))
        		candle_set.remove(j)
        		print("!!!add!!!",candle_set)
    return candle_set_count

a=[44, 33, 69, 62]
print(solution(a))


def consecutive_num_list(a):
	a = a.split(" ")
	result = []
	length = len(a)
	for i in range(length):
		if len(result) == 0:
			result.append(a[i])
		elif int(result[-1]) < int(a[i]):
			result.append(a[i])
	return(result)

a="9 10 20 40 25 20 50 30 70 85"
print(consecutive_num_list(a))

gen = [str(i * int(str(i)[::-1])) for i in range(100, 1001) if str(i)[-1] != "0"]
print(gen)

count = 0
for s in gen:
    # 각 자리 수가 증가하지 않을 경우 false --> all true인 경우 count + 1
    if all([int(s[i]) <= int(s[i + 1]) for i in range(len(s) - 1)]):
        count += 1
print(count)
# ans: 21

student_tuples = [
     ('john', 'A', 15),
     ('jane', 'B', 12),
     ('dave', 'B', 10),
     ]
print(sorted(student_tuples, key=lambda student: student[1]))



#코딩 도장 - 오락가락수가 아닌수
#숫자를 왼쪽부터 오른쪽으로 읽어나갈 때, 오른쪽에 나오는 숫자가 왼쪽 숫자보다 작지 않다면 그 수를 증가수라고 합시다. 
#예를 들어 134468은 증가수입니다. 
#마찬가지로 오른쪽에 나오는 숫자가 왼쪽 숫자보다 크지 않다면 그 수를 '감소수'라고 합시다. 66420은 감소수입니다. 
#증가수도 감소수도 아닌 나머지 수들은 오락가락수라고 하겠습니다. 예를 들어 155349는 오락가락수입니다.
#수가 커질수록 오락가락수일 가능성은 높아집니다. 1,000,000 미만의 수 중 12,951개, 10^10 미만에서는 277,032개만이 증가수이거나 감소수입니다.
#10^100(구골) 미만의 자연수들 중에 오락가락수가 아닌 수는 모두 몇 개입니까?
# 아래 코드의 문제점 너무 큰 수 처리가 안됌 - 증가수 감소수 중복수 같은 수학 원리 필요
def find_num(n):
	
	a= [str(i) for i in range(1,10**n)]
	count = 0
	for i in a:
		if all([int(i[j]) <= int(i[j+1]) for j in range(len(i) - 1)]):
			print(i)
			count += 1
		elif all([int(i[j]) >= int(i[j+1]) for j in range(len(i) - 1)]):
			print(i)
			count += 1
	return(count)

print(find_num(6))


#앞에서부터 읽을 때나 뒤에서부터 읽을 때나 모양이 같은 수를 대칭수(palindrome)라고 부릅니다. 
#두 자리 수를 곱해 만들 수 있는 대칭수 중 가장 큰 수는 9009 (= 91 × 99) 입니다. 
#세 자리 수를 곱해 만들 수 있는 가장 큰 대칭수는 얼마입니까?
def palindrome():
	lst = [int(str(i)[:3])*int(str(i)[3:]) for i in range(100000,999999)]
	return(max([i for i in lst if str(i) == str(i)[::-1]]))

print(palindrome())


def finbonachi(a):
	next_num = 0
	ans = 0
	x = 1  # Represents the current Fibonacci number being processed

	y = 2  # Represents the next Fibonacci number in the sequence
	while x <= 4000000:

		if x % 2 == 0:
			ans += x
		x, y = y, x + y
	print(ans)

finbonachi(4000000)


from string import ascii_lowercase

def caesar(s, n):
    result = ""
    alphalst = list(ascii_lowercase)
    slst = list(s)
    print(slst)
    for i in slst:
    	if i != " ":
    		index_find = alphalst.index(i.lower())
    		new_index = index_find + n
    		if new_index >25:
    			new_index = new_index % 26
    			print(new_index)
    		if i.isupper():
    			result += alphalst[new_index].upper()
    		else:
	            result += alphalst[new_index]
    	else :
    		result += " "
    return result
    # 주어진 문장을 암호화하여 반환하세요.
	

# 실행을 위한 테스트코드입니다.
print('s는 "a B z", n은 4인 경우: ', caesar("a B z", 124))

import string

def caesar(s, n):
    alphabet_lower = list(string.ascii_lowercase)
    alphabet_upper = list(string.ascii_uppercase)
    s = list(s)
    print(s)
    for i, char in enumerate(s):
        if char in alphabet_lower:
            position = (alphabet_lower.index(char) + n) % 26
            s[i] = alphabet_lower[position]
        elif char in alphabet_upper:
            position = (alphabet_upper.index(char) + n) % 26
            s[i] = alphabet_upper[position]
        else:
            pass
    return ''.join(s)
print('s는 "a B z", n은 4인 경우: ' + caesar("a B z", 4))

def change124(n):
    answer = ""
    while n >0:
        n, a = divmod(n, 3)
        if a==0: n -=1
        answer = "412"[a] +answer
        print(answer)

    return answer


# 아래는 테스트로 출력해 보기 위한 코드입니다.
print(change124(15))


def findLargestSquare(board):
    answer = 0
    result = []
    boardlen =len(board)
    print(boardlen)

    for y in range(len(board)):
        for x in range(len(board[y])):
        		#print("y,x",y,x)
        		if x == y:
        			print("break")
	        		for i in range(y+1):
	        			for j in range(x+1):
	        				#print("j,x",j,x)
	        				result.append(board[i][j])
	        				print(i,j,board[i][j],result)
	        				if (len(result) != 1) and all(result[n] == 'O' and result[n] == result[n+1] for n in range(len(result)-1)):
	        					answer = i*j
	        				else : print(i,j, "it is X")
	        	result = []


    return answer

#아래 코드는 출력을 위한 테스트 코드입니다.

testBoard = [
['X','O','O','O','X'],
['X','O','O','O','O'],
['X','X','O','O','O'],
['X','X','O','O','O'],
['X','X','X','X','X']]
print(findLargestSquare(testBoard))

def hopscotch(board, size):
    accum = [0] * len(board[0])
    print(accum)
    for row in board:
        tmp = accum[:]
        print(tmp)
        for i in range(len(row)):
            accum[i] = row[i] + max(tmp[:i] + tmp[i+1:])

    return max(accum)

board =  [[ 1, 2, 3, 5 ], [ 5, 6, 7, 8 ], [4, 3, 2, 1]]
print(hopscotch(board, 3))


def solution(strs):
	answer = ""
	tmp = ""
	for i in range(len(strs)):
		if len(answer) == 0:
			print("길이",len(answer))
			for y in range(len(strs[i])):
				if strs[i][y] == strs[i+1][y] :
					answer += (strs[i][y])
					print("ans",answer)
				elif y == 0 and strs[0][y] != strs[0+1][y]:
					print(y," added")
					answer += (" ")
					print(len(answer))
					break
				elif y > 0 and strs[0][y] != strs[0+1][y]:
					break
		elif len(answer) > 0 :
			for y in range(len(strs[i])):
				if len(answer) > y and answer[y] == strs[i][y]:
					tmp += strs[i][y]
					pass
				else :
					break
			answer = tmp
			print(answer)
			tmp = ""
	return(answer)
a = ["abcaefg", "abcdefg", "abcdhfg"]
a = ["ab", "swers", "sws"]
print(solution(a))


def solution(strs):
	answer = []
	tmp = []
	for i in range(len(strs)):
		if i == 0:
			for y in range(len(strs[i])):
				answer.append(strs[i][y])
		elif i > 0 :
			for y in range(len(strs[i])):
				if len(answer) > y and answer[y] == strs[i][y]:
					tmp.append(strs[i][y])
				else :
					break
			answer = tmp[:]
			del tmp[:]
	return("".join(answer))
a = ["abcaefg", "abcdefg", "abcdhfg"]
a = ["a", "abcdefg", "a"]
print(solution(a))


def rm_small(mylist):
    smal = min(my_list)
    my_list.remove(1)
    return my_list

my_list = [4, 3, 2, 1]
print("결과 {} ".format(rm_small(my_list)))


def alpha_string46(s):
    check = 0
    for i in s:
        if i.isnumeric():
            check +=1
        else:
            break
    if check == len(s):
        return True
    else :
        return False



# 아래는 테스트로 출력해 보기 위한 코드입니다.
print( alpha_string46("a234") )
print( alpha_string46("1234") )


def no_continuous(s):
    lst = [i for i in range(len(s)-1) if s[i] != s[i+1]]
    return lst

# 아래는 테스트로 출력해 보기 위한 코드입니다.
print( no_continuous( "133303" ))


def string_middle(str):
    index = divmod(len(str), 2)
    print(index)
    if index[1] == 1:
        return(str[index[0]])
    else:
        return(str[index[0]], str[index[0]-1])

# 아래는 테스트로 출력해 보기 위한 코드입니다.
print(string_middle("powasder"))


import math
def nextSqure(n):
    if int(math.sqrt(n)) == math.sqrt(n):
    	return("yes")
    else : return('no')
 
# 아래는 테스트로 출력해 보기 위한 코드입니다.
print("결과 : {}".format(nextSqure(111)));


def digit_reverse(n):
    n = str(n)
    bn = list(n[::-1])

    print(bn)

# 아래는 테스트로 출력해 보기 위한 코드입니다.
print("결과 : {}".format(digit_reverse(12345)));


def nextBigNumber(n):
    answer = 0
    bin_num = bin(n)[2:]
    one_count = bin_num.count('1')
    next_num = n + 1
    while True:
        bin_next_num = bin(next_num)[2:]
        next_count = bin_next_num.count('1')
        if next_count == one_count :
            return(next_num)
            break
        else:
            next_num +=1
        
    

#아래 코드는 테스트를 위한 출력 코드입니다.
print(nextBigNumber(78))

print(int('0b110110',2))


def findLargestSquare(board):
    # 'O'에 해당하는 것을 1로, 'X'에 해당하는 값을 0으로 바꿔준다.
    table = [[1 if x == "O" else 0 for x in sub_board] for sub_board in board]
    max_square = 0
    for x in range(1, len(table)):
        for y in range(1, len(table[x])):
            # 만약 table[x][y]의 값이 0(즉, 'X')라면 정사각형을 만들 수 없으므로 건너 뛴다.
            if table[x][y] == 0:
                continue
            # 해당 좌표 기준(x,y) : 왼쪽검사(x, y-1), 위쪽 검사(x-1, y), 11시 방향 대각선 검사(x-1, y-1)
            else:
                # 최소값을 하나 뽑아낸다. 차례대로 min(왼쪽 좌표, 위쪽 좌표, 왼쪽 대각선 좌표)를 의미한다.
                _min = min([table[x][y-1], table[x-1][y], table[x-1][y-1]])
                table[x][y] = _min + 1

                # 만약, max_square보다 큰 값이 등장하면, 교체해준다.
                if max_square < table[x][y]:
                    max_square = table[x][y]

    # 넓이를 반환해야 하므로 제곱을 해서 반환한다.
    return max_square**2

#아래 코드는 출력을 위한 테스트 코드입니다.

testBoard = [
['X','O','O','O','X'],
['X','O','O','O','O'],
['X','X','O','O','O'],
['X','X','O','O','O'],
['X','X','X','X','X']]
print(findLargestSquare(testBoard))

def jumpCase(num):
	next_num = 0
	ans = 0
	result = [0,1]
	for i in range(2,num+2):
		result.append(result[i-1] + result[i-2])
		print(result)
	return(result[-1])
print(jumpCase(4))

def hopscotch(board, size):
    accum = [0] * len(board[0])
    print(accum)
    for row in board:
        tmp = accum[:]
        print(tmp)
        for i in range(len(row)):
            accum[i] = row[i] + max(tmp[:i] + tmp[i+1:])
            print("accum",accum)

    return max(accum)

board =  [[ 1, 2, 3, 5 ], [ 5, 6, 7, 8 ], [4, 3, 2, 1]]
print(hopscotch(board, 3))


def solution(strs):
	answer = []
	tmp = []
	for i in range(len(strs)):
		if i == 0:
			for y in range(len(strs[i])):
				answer.append(strs[i][y])
		elif i > 0 :
			for y in range(len(strs[i])):
				if len(answer) > y and answer[y] == strs[i][y]:
					tmp.append(strs[i][y])
				else :
					break
			answer = tmp[:]
			del tmp[:]
	return("".join(answer))
a = ["abcaefg", "abcdefg", "abcdhfg"]
a = ["a", "abcdefg", "a"]
print(solution(a))

def expressions(num):
    answer = 0
    total = 0
    result = []
    for j in range(1,(num+1)):
        total = 0
        result = []
        for i in range(j,num+1):
            total +=i
            result.append(i)
            if total > num and i > num:
                break
            elif total == num:
                answer += 1
                print(result)
                break
    return answer

# 아래는 테스트로 출력해 보기 위한 코드입니다.
print(expressions(1590))

def expressions(num):
    answer = 1 # 모든 num은 자기 자신을 답으로 가진다.
    _sum = 0
    left = 0

    while left != (num // 2 + 1): # left가 도달할 곳은 절반(num//2)면 충분하다.
        if _sum < num:
            for right in range(left+1, num // 2 + 1 + 1): # right는 left + 1까지 체크
                _sum += right # 합이 더 작다면, 계속해서 right를 더해준다.
                if _sum == num: # right를 더해주다가, num과 일치하면 횡재했다.
                    answer += 1 # 경우의 수를 하나 찾았으므로 +1 해준다.
                    left += 1 # left를 오른쪽으롷 한칸 옮겨서 기준점을 다시 설정한다.
                    _sum = 0  # sum을 0으로 초기화해줘야 다음 계산도 가능하다.
                    break

                elif _sum > num: # right를 더한 결과 num을 초과하면
                    left += 1 # left를 한 칸 옮겨주고,
                    _sum = 0  # _sum을 0으로 초기화 한다.
                    break
    return answer

print(expressions(1590))    

def T(N, Beg, Aux, End):
	if N == 1:
		print(Beg, '->', End)
	else:
		T(N-1, Beg, End, Aux)
		T(1, Beg, Aux, End)
		T(N-1, Aux, Beg, End)


def T(N, Beg, Aux, End, result):
	if N == 1:
		result.append([Beg,End])
	else:
		T(N-1, Beg, End, Aux,result)
		T(1, Beg, Aux, End,result)
		T(N-1, Aux, Beg, End,result)
	return(result)

def hanoi(n):
	result = []
	answer = T(n,1,2,3,result)
	return(answer)

print(hanoi(3))


def solution(n):

    while len(str(n)) >1 :
    	n = str(n)
    	total = 0
    	for i in range(len(n)):
    		total += int(n[i])
    	n = total
    print(n)
solution(456789)


def solution(ages):
    answer = 0
    candle_set = list(range(10))
    new_candle_set = list(range(10))
    candle_set_count = 1
    age_length = len(ages)
    for i in range(age_length):
        age_number = str(ages[i])
        for j in age_number :
        	j = int(j)
        	print(j)
        	if j in candle_set:
        		candle_set.remove(j)
        		print(candle_set)
        	elif (j == 6) and (j not in candle_set) and (9 in candle_set):
        		candle_set.remove(9)
        	elif (j == 9) and (j not in candle_set) and (6 in candle_set):
        		candle_set.remove(6)
        	elif j not in candle_set:
        		candle_set_count +=1
        		candle_set = new_candle_set + candle_set
        		candle_set.remove(j)
        		print("!!!add!!!",candle_set)
    return candle_set_count


def solution(n):

    while len(str(n)) > 1:
    	n = str(n)
    	total = 0
    	for i in range(len(n)):
    		total += int(n[i])
    	n = total
    return(n)

print(solution(456789))



def eatCookie(cookies):

	max_nun = max(cookies)
	min_num = min(cookies)
	i = min_num
	result = []

	for i in range(len(cookies)):
		for j in range(i, len(cookies)):
			
	return(result)
	

# 아래는 테스트로 출력해 보기 위한 코드입니다.
print(eatCookie([1, 4, 2, 6, 3, 4, 1, 5]))


def cha(t, c, d):
    #print (d)
    if ( len(c) == 1 ) :
        if t % c[0] == 0 :
            return 1
        else :
            return 0
    a = []

    while ( t >=0 ) :
        if (t,c[-2]) not in d.keys() :
            d[(t,c[-2])] = cha( t, c[:-1], d )
            print(d)
        a.append ( d[(t,c[-2])] )  
        print(a)
        t -= c[-1]
    return sum(a)

def change(total, coin):
    dic = {}
    return cha( total, sorted(coin) , dic)


# 아래는 테스트로 출력해 보기 위한 코드입니다.
print(change(5, [1, 2, 5]))


def maxSubArray(ls):
    if len(ls) == 0:
       raise Exception("Array empty") # should be non-empty

    runSum = maxSum = ls[0]
    i = 0
    start = finish = 0

    for j in range(1, len(ls)):
    	if ls[j] > (runSum + ls[j]):
    		runSum = ls[j]
    		i = j
    	else :
    		runSum += ls[j]
    	if runSum > maxSum :
            maxSum = runSum
            start = i
            finish = j

    print ("maxSum =>", maxSum)
    print ("start =>", start, "; finish =>", finish)

maxSubArray([-2, 11, -4, 13, -5, 2])
maxSubArray([-15, 29, -36, 3, -22, 11, 19, -5])


def maximumSum(a, m):
    # Complete this function
    max_num = 0
    for i in range(len(a)):
    	for j in range(len(a) - i) :
    		cal = sum(a[j:len(a)-i]) % m
    		if cal > max_num :
    		    max_num = cal

    return max_num

a = [3, 3, 9, 9, 5]
m = 7
result = maximumSum(a, m)
print(result)


def solve(grades):
    # Complete this function
    ans = []
    for i in grades:
    	h, t = divmod(i,5)
    	if i < 38:
    		ans.append(i)
    	elif t < 3:
    		ans.append(i)
    	elif t >=3 :
    		ans.append((h+1)*5)

    return(ans)


a = [73, 67, 38, 33]
print(solve(a))


def countApplesAndOranges(s, t, a, b, apples, oranges):
    # Complete this function
    house = [i for i in range(s,t+1)]
    apple_tree = a
    orange_tree = b
    apple_count = 0
    orange_count = 0
    for i in apples:
    	if apple_tree + i in house:
    		apple_count += 1
    for j in oranges:
    	if orange_tree + j in house:
    		orange_count += 1

    print(apple_count, orange_count)

def countApplesAndOranges(s, t, a, b, apples, oranges):
    # Complete this function
    apple_tree = a
    orange_tree = b
    apple_count = 0
    orange_count = 0
    for i in apples:
    	if apple_tree + i >= s and apple_tree + i <= (t):
    		apple_count += 1
    for j in oranges:
    	if orange_tree + j >= s and orange_tree + j <= (t):
    		orange_count += 1

    print(apple_count)
    print(orange_count)

countApplesAndOranges(7, 11, 5, 15, [-1, 2, 1], [5, -6])
countApplesAndOranges(2, 3, 1, 5, [2], [-2])


def kangaroo(x1, v1, x2, v2):
    # Complete this function
    if x2>x1 and v2>=v1:
    	return("NO")
    else :
    	while x1 < x2:
    		x1 = v1 + x1
    		x2 = v2 + x2
    		if x1 == x2 :
    			return("YES")
    			break
    			
    		elif x1>x2 :
    			return("NO")
    			break

print(kangaroo(0,3,4,2))
print(kangaroo(1928,4306,5763,4301))
print(kangaroo(1571,4240,9023,4234))
print(kangaroo(43, 2, 70, 2))

def knapSack(W, wt, val, n):
    K = [[0 for x in range(W+1)] for x in range(n+1)]
    print(K)
    for i in range(n+1):
        for w in range(W+1):
            if i==0 or w==0:
                K[i][w] = 0
            elif wt[i-1] <= w:
                K[i][w] = max(val[i-1] + K[i-1][w-wt[i-1]],  K[i-1][w])
            else:
                K[i][w] = K[i-1][w]
    print(K)
    return K[n][W]
val = [60, 100, 120]
wt = [10, 20, 30]
W = 40
n = len(val)
print(knapSack(W, wt, val, n))


def cha(t, c, d):
    #print (d)
    if (len(c) == 1):
        if t % c[0] == 0:
            return 1
        else:
            return 0
    a = []

    while (t >= 0):
        if (t, c[-2]) not in d.keys():
            d[(t, c[-2])] = cha(t, c[:-1], d)
            print(d)
        a.append(d[(t, c[-2])])
        print(a)
        t -= c[-1]
    return sum(a)

def change(total, coin):
    dic = {}
    return cha(total, sorted(coin), dic)


# 아래는 테스트로 출력해 보기 위한 코드입니다.
print(change(15, [1, 2, 5]))

def breakingRecords(scores):
    # Complete this function
    _max = _min = scores[0]
    _cmax = _cmin = 0
    for score in scores:
    	if score < _min:
    		_cmin += 1
    		_min = score
    	elif score > _max:
    		_cmax += 1
    		_max = score
    print(_cmax, _cmin)

a = [10, 5, 20, 20, 4, 5, 2, 25, 1]

print(breakingRecords(a))

def getTotalX(a, b):
    # Complete this function
    ans = []
    for i in range(max(a), min(b)):
    	print(i,len([1 for ai in a if not i % ai]))

    if len(a) != 1:
    	test = [max(a)] + [b[0]] + list(set([i*j for i in a for j in a if i*j >= max(a)]))
    	for i in a:
    		for j in test:
    			if j % i != 0:
    				test.remove(j)
 
    elif len(a) == 1 and len(b) == 1:
    	test = [i for i in range(int(a[0]), int(b[0]+1))]
    else:
    	test = a

    test.sort()
    print(b)
    print("test",test)
    if a[-1] <= b[0]:
    	for i in test:
    		if all([o % i == 0 for o in b]):
    			ans.append(i)
    	ans = set(ans)
    	print(ans)
    	return(len(ans))
    else:
    	return(0)

#아래 로직은 a딕의 모든 요소를 가지고 a 요소 최대값과 b 딕의 최소값 사이의 값을 직접 나누어 봐서
#그길이가 a딕의 길이와 같으면 전부 나누어 지는 수인지를 확인 b딕도 같은 방법으로 확인 후 같으면 카운트 증가
#	for i in range(max(A), min(B)+1):
#	    if len([1 for ai in A if not i % ai]) != n:
#	        continue
#	    if len([1 for bi in B if not bi % i]) != m:
#	        continue
#	    num += 

a = [2, 4]
b = [16, 32, 96]

a = [100, 99, 98, 97, 96, 95, 94, 93, 92, 91]
b = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

a = [2]
b = [20,30,12]

a = [2, 6]
b = [12]

a = [3, 9, 6]
b = [36, 72]

a = [1]
b = [100]

a = [2, 3, 6]
b = [42, 84]
print(getTotalX(a, b))
'''

def solve(n, s, d, m):
	print(n, s, d, m)
	_sum = 0
	counter = 0
	if m == 1:
		return(s.count(d))
	else:
		for i in range(len(s)-m+1):
			_sum = 0
			for j in range(i,i+m):
				_sum += s[j]
			if _sum == d:
				print("sum",s[j],_sum)
				counter += 1
		return(counter)


n = 5
s = [1, 2, 1, 3, 2]
d = 3
m = 2

n = 19
s = [2, 5, 1, 3, 4, 4, 3, 5, 1, 1, 2, 1, 4, 1, 3, 3, 4, 2, 1]
d = 18
m = 7
print(solve(n, s, d, m))