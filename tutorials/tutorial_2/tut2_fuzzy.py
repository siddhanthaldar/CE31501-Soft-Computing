import numpy as np

def intervals(params,inp):
	ac_z = [[params[0][2][0],params[0][2][3]],[params[1][2][0],params[1][2][3]],[params[2][0][0],params[2][0][3]]]
	ann_z = [[params[0][2][0],params[0][2][3]],[params[1][1][0],params[1][1][3]],[params[2][0][0],params[2][0][3]]]
	sin_z = [[params[0][1][0],params[0][1][3]],[params[1][0][0],params[1][0][3]],[params[2][1][0],params[2][1][3]]]
	trans_z = [[params[0][0][0],params[0][0][3]],[params[1][0][0],params[1][0][3]],[params[2][2][0],params[2][2][3]]]
	i_z = [[inp[0][0],inp[0][3]],[inp[1][0],inp[1][3]],[inp[2][0],inp[2][3]]]
	z = [ac_z,ann_z,sin_z,trans_z, i_z]

	ac_h = [params[0][2][1],params[1][2][1],params[2][0][1]]
	ann_h = [params[0][2][1],params[1][1][1],params[2][0][1]]
	sin_h = [params[0][1][1],params[1][0][1],params[2][1][1]]
	trans_h = [params[0][0][1],params[1][0][1],params[2][2][1]]
	i_h	= [inp[0][1],inp[1][1],inp[2][1]]
	h = [ac_h,ann_h,sin_h,trans_h,i_h]

	return z,h

def pseudo_expectation(z, h, num_cuts):
	x = []
	y = []
	s = 0
	for i in range(num_cuts+1):
		y=1.0/num_cuts*i
		x=(h-z[0])/1.0*y+z[0]
		s += y*x

	for i in range(num_cuts):
		y = 1.0/num_cuts*(num_cuts-1-i)
		x = y*(h-z[1])/1.0+z[1]
		s += y*x

	return s

	
def res(params, inp, weights):
	# Processes
	process = ['autoclaving', 'annealing', 'sintering', 'transport']

	# intervals
	z,h = intervals(params, inp)
	z = np.asarray(z)
	h = np.asarray(h)

	# functions
	ac_z = z[0][0]*weights[0]+z[0][1]*weights[1]+z[0][2]*weights[2]
	ann_z = z[1][0]*weights[0]+z[1][1]*weights[1]+z[1][2]*weights[2]
	sin_z = z[2][0]*weights[0]+z[2][1]*weights[1]+z[2][2]*weights[2]
	trans_z = z[3][0]*weights[0]+z[3][1]*weights[1]+z[3][2]*weights[2]
	i_z = z[4][0]*weights[0]+z[4][1]*weights[1]+z[4][2]*weights[2]

	ac_h = h[0][0]*weights[0]+h[0][1]*weights[1]+h[0][2]*weights[2]
	ann_h = h[1][0]*weights[0]+h[1][1]*weights[1]+h[1][2]*weights[2]
	sin_h = h[2][0]*weights[0]+h[2][1]*weights[1]+h[2][2]*weights[2]
	trans_h = h[3][0]*weights[0]+h[3][1]*weights[1]+h[3][2]*weights[2]
	i_h = h[4][0]*weights[0]+h[4][1]*weights[1]+h[4][2]*weights[2]

	# Pseudo expectation scores
	ac = pseudo_expectation(ac_z, ac_h, 10)
	ann = pseudo_expectation(ann_z, ann_h, 10)
	sin = pseudo_expectation(sin_z, sin_h, 10)
	trans = pseudo_expectation(trans_z, trans_h, 10)
	i = pseudo_expectation(i_z, i_h, 10)
	scores = [abs(i-ac),abs(i-ann),abs(i-sin),abs(i-trans)]
	
	# # The Most Possible Criterion
	# scores = [abs(i_h-ac_h),abs(i_h-ann_h),abs(i_h-sin_h),abs(i_h-trans_h)]

	scores = np.asarray(scores)
	index = np.argmin(scores)

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

	# Given fuzzy values
	p = [0.125,0.25,1.0,0.375]
	t = [0.125,0.375,1.0,0.625] 
	f = [0.0,0.0,1.0,0.25]
	inp = [p,f,t]

	res(params, inp, w)		


