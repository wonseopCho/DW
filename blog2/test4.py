s = [1,1,2,4,5,8,15,19]
pairs = list(zip(s[0:], s[1:]))
print(pairs)
pairs.sort(key=lambda x:x[1]-x[0])
print("k",pairs)
print(min(s))

a= [i for i in range(6)]
test =list(filter(lambda x: x>4, a)) 

print(test)

xx=[x//2 for x in range(1, 11)]
print(xx)

my_list = range(16)
print(list(filter(lambda x: x % 3 == 0, my_list)))


def FirstFactorial(num):
    total = 1
    for i in range(1,num+1):
        total *= i# code goes here 
    return total
    
# keep this function call here  
print(FirstFactorial(4))



import math

def maxnumber():
	num = []
	for i in range(3):
		num.append(int(input("num plz %d" %(i+1))))
	return(max(num))

print(maxnumber())