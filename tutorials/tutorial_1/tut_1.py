import matplotlib.pyplot as plt

def add(a,b):  #0th index is min and 1th index is max
	return [a[0]+b[0],a[1]+b[1]]

def sub(a,b):
	return [a[0]-b[1],a[1]-b[0]]

def mul(a,b):
	mult = []
	mult.append(a[0]*b[0])
	mult.append(a[0]*b[1])
	mult.append(a[1]*b[0])
	mult.append(a[1]*b[1])

	return [min(mult), max(mult)]

def div(a,b):
	div = []
	div.append(a[0]/b[0])
	div.append(a[0]/b[1])
	div.append(a[1]/b[0])
	div.append(a[1]/b[1])

	return [min(div), max(div)]

def generate_bounds(a, alpha_max, num_cuts):
	x = []
	y = []
	for i in range(num_cuts+1):
		y.append(float(alpha_max)/num_cuts*i)
		x.append([(a[1]-a[0])/float(alpha_max)*y[i]+a[0], float(y[i]*(a[1]-a[3])/float(alpha_max)+a[3])])

	return x,y

def operation(a,b,op,num_cuts):  # a[0], a[1], a[2],  a[3]  --> x1, x2, y2, x3

	alpha_max = min(a[2], b[2])
	x_a,y_a = generate_bounds(a,alpha_max, num_cuts)
	x_b,y_b = generate_bounds(b,alpha_max, num_cuts)

	res_x = []
	res_y = []

	if op=='add':		
		for i in range(len(y_a)):
			res_y.append(y_a[i])
			res_x.append(add(x_a[i], x_b[i]))
	if op=='sub':		
		for i in range(len(y_a)):
			res_y.append(y_a[i])
			res_x.append(sub(x_a[i], x_b[i]))
	if op=='mul':		
		for i in range(len(y_a)):
			res_y.append(y_a[i])
			res_x.append(mul(x_a[i], x_b[i]))
	if op=='div':		
		for i in range(len(y_a)):
			res_y.append(y_a[i])
			res_x.append(div(x_a[i], x_b[i]))

	# plt.subplot(311)
	x = [a[0], a[1], a[3]]
	y = [0,a[2],0]
	plt.plot(x,y,color='blue',label="Membership Function 1")

	# plt.subplot(312)
	x = [b[0], b[1], b[3]]
	y = [0,b[2],0]
	plt.plot(x,y,color='green',label="Membership Function 2")

	# plt.subplot(313)
	x = []
	y = []
	for i in range(len(y_a)):
		x.append(res_x[i][0])
		y.append(res_y[i])
	for i in range(1,len(y_a)):
		x.append(res_x[len(y_a)-1-i][1])
		y.append(res_y[len(y_a)-1-i])	
	plt.plot(x,y,color='red',label="Result after operation")
	plt.legend()
	plt.show()

if __name__=="__main__":
	# Points in the form [x1, x2, y2, x3]	
	a = [3,5,1,8]
	b = [2,4,1,7]
	op = 'div'
	operation(a,b,op, 10)
