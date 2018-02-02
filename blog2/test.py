
def solution(a):
  x =[]
  y =[]
  answer =[]
  result =[]
  for number in a:
  	if number[0] not in x:
  		x.append(number[0])
  		if number[1] not in y:
	  		y.append(number[1])
	  	else:
	  		pass
  	elif number[1] not in y:
  		y.append(number[1])
  for xnum in x:
  	for ynum in y:
  		result.append([xnum, ynum])
  for answer in result :
  	if answer not in a:
  		print(answer)

a = [[1, 4], [3, 4], [3, 10]]
solution(a)
