import numpy as np

def score(var,inp):
	if inp>=var[0][1] and inp<var[0][3]:
		z = (var[0][3]-float(inp))/(var[0][3]-var[0][1]) * var[0][2]
	else:
		z = 0

	if inp>=var[1][0] and inp<=var[1][1]:
		l = (float(inp)-var[1][0])/(var[1][1]-var[1][0])*var[1][2]
	elif inp>var[1][1] and inp<=var[1][3]:
		l = (var[1][3]-float(inp))/(var[1][3]-var[1][1])*var[1][2]	

	if inp>=var[2][0] and inp<=var[2][1]:
		h = (inp-var[2][0])/(var[2][1]-var[2][0])*var[2][2]
	else:
		h = 0
		
	return [z,l,h]

def res(params, inp, weights):
	# Processes
	process = ['autoclaving', 'annealing', 'sintering', 'transport']

	scores = []
	for i in range(3):
		scores.append(score(params[i], inp[i]))

	autoclaving = scores[0][2]*weights[0] + scores[1][2]*weights[1] + scores[2][0]*weights[2]
	annealing = scores[0][2]*weights[0] + scores[1][1]*weights[1] + scores[2][0]*weights[2]
	sintering = scores[0][1]*weights[0] + scores[1][0]*weights[1] + scores[2][1]*weights[2]
	transport = scores[0][0]*weights[0] + scores[1][0]*weights[1] + scores[2][2]*weights[2]
	procs = [autoclaving, annealing, sintering, transport]
	procs = np.asarray(procs)
	index = np.argmax(procs)

	print(process[index])



if __name__ == "__main__":
	# Points as x1,x2,y2,x3
	# Pressure
	p_min = 0
	p_max = 8
	z_pres = [0.0,0.0,1.0,0.5]
	l_pres = [0.0,0.5,1.0,1.0]
	h_pres = [0.5,1.0,1.0,1.0]
	pres = [z_pres, l_pres, h_pres]

	# Temperature
	t_min = 0
	t_max = 800
	z_temp = [0.0,0.0,1.0,0.25]
	l_temp = [0.0,0.25,1.0,0.5]
	h_temp = [0.25,1.0,1.0,1.0]
	temp = [z_temp, l_temp, h_temp]

	# Flow rate
	f_min = 0
	f_max = 80
	z_flow = [0.0,0.0,1.0,0.125]
	l_flow = [0.0,0.125,1.0,0.25]
	h_flow = [0.125,1.0,1.0,1.0]
	flow = [z_flow, l_flow, h_flow]

	params = [pres, temp, flow]

	# Weights
	w_pres = 0.5
	w_temp = 0.25
	w_flow = 0.25
	w = [w_pres, w_temp, w_flow]

	# Given crisp values
	p = 5.0
	t = 150.0 
	f = 5.0

	# Normalize
	p = (p-p_min)/(p_max-p_min)
	t = (t-t_min)/(t_max-t_min)
	f = (f-f_min)/(f_max-f_min)
	inp = [p,f,t]

	res(params, inp, w)		


