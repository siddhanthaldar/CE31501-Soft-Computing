import numpy as np
import random

def func(x1,x2):
	return (x1**2+x2-11)**2 + (x1+x2**2-1)**2

def gen_strings(num_bits, num_strings):
	strings = np.zeros((num_strings, num_bits*2))

	for i in range(num_strings):
		for j in range(num_bits*2):
			strings[i][j] = 1 if random.random() >= 0.5 else 0

	return strings

def actual_val(population, limits):  # limits represents range of the numbers = [min,max]
	# print(population)
	act_val = np.zeros((population.shape[0], 2))  # (x1,x2)
	diff = limits[1] - limits[0]
	str_len = population.shape[0]/2
	max_bit_val = 2**str_len-1

	for i in range(population.shape[0]):
		for j in range(act_val.shape[1]):
			s = 0
			for x in range(str_len):
				s += population[i][j*str_len + (str_len-1-x)] * 2**x
			act_val[i][j] = limits[0] + diff*s/max_bit_val

	return act_val

def Fx(a): #act_val
	F = np.zeros(a.shape[0])

	for i in range(a.shape[0]):
		f = func(a[i][0],a[i][1])
		F[i] = 1.0/(1.0+f)

	return F

def A(F):
	mean_F = 0
	for i in range(F.shape[0]):
		mean_F += F[i]
	mean_F /= F.shape[0]

	return F/mean_F

def B(A_arr):
	return A_arr/A_arr.shape[0]

def C(B_arr):
	C_arr = np.zeros(B_arr.shape)
	for i in range(1,C_arr.shape[0]):
		C_arr[i] = B_arr[i] + B_arr[i-1]
	return C_arr

def D(size):
	D_arr = np.zeros(size)
	for i in range(size):
		D_arr[i] = random.random()
	return D_arr

def E(C_,D_):
	E_arr = np.zeros(C_.shape[0])
	for i in range(C_.shape[0]):
		for j in range(C_.shape[0]-1):		
			if D_[i]>=C_[j] and D_[i]<C_[j+1]:
				E_arr[i] = j  # 0 indexed readings
	return E_arr

# def F(E):
# 	F_arr = np.zeros(E.shape[0])
# 	for i in range(E.shape[0]):
# 		F_arr[E[i]] += 1
# 	return F

def mating_pool_update(string, E_): #strings,E
	mating_pool = np.zeros(string.shape)
	for i in range(E_.shape[0]):
		mating_pool[i] = string[i]
	return mating_pool

def crossover(m_pool, c_prob): #mating_pool, crossover_prob
	crossover_mating_pool = m_pool
	num_crossover = m_pool.shape[0]/2
	crossover_point = np.zeros(num_crossover)
	for i in range(num_crossover):
		crossover_point[i] = random.randint(0,m_pool.shape[1]/2-2)

	# array to keep track of elements crossed over
	crossed = np.zeros(m_pool.shape[0])

	# single point crossover
	pt = 0
	for i in range(num_crossover):
		prob = random.random()
		if prob < 1-crossover_prob:
			continue

		j = random.randint(0,m_pool.shape[0]-1)
		k = random.randint(0,m_pool.shape[0]-1)

		while(crossed[j]!=0 or crossed[k]!=0):
			j = random.randint(0,m_pool.shape[0]-1)
			k = random.randint(0,m_pool.shape[0]-1)			

		crossed[j] = 1
		crossed[k] = 1

		cp = int(crossover_point[pt])  #crossover point converted to integer

		crossover_mating_pool[j][0:cp] = m_pool[k][0:cp]
		crossover_mating_pool[j][10:10+cp] = m_pool[k][10:10+cp]
		crossover_mating_pool[k][0:cp] = m_pool[j][0:cp]
		crossover_mating_pool[k][10:10+cp] = m_pool[j][10:10+cp]

		pt += 1

	return crossover_mating_pool

# mutation - flip one index
def mutation(mat_pool, mut_prob): # (mating_pool, mutation_prob)
	mutation_index = np.zeros(mat_pool.shape[0])
	for i in range(mat_pool.shape[0]):
		mutation_index[i] = random.randint(0, mat_pool.shape[1]/2-1)

	for i in range(mat_pool.shape[0]):
		if(random.random()<1-mut_prob):
			continue
		mat_pool[i][int(mutation_index[i])] = 1 - mat_pool[i][int(mutation_index[i])]

	return mat_pool

def iteration(mating_pool, limits, crossover_prob, mutation_prob):
	act_val = actual_val(mating_pool,limits)
	F = Fx(act_val)
	a = A(F)
	b = B(a)
	c = C(b)
	d = D(mating_pool.shape[0])
	e = E(c,d)
	# f = F(e)

	mating_pool = mating_pool_update(mating_pool,e)
	mating_pool = crossover(mating_pool, crossover_prob)
	mating_pool = mutation(mating_pool, mutation_prob)

	return F, mating_pool

def solve(num_bits, num_strings, crossover_prob,mutation_prob,limits):
	mating_pool = gen_strings(num_bits, num_strings)

	idx = -1
	thresh = 0.9
	count = 0

	# Check if converged
	while(idx<0):
		count += 1
		print(count)
		F, mating_pool = iteration(mating_pool, limits, crossover_prob, mutation_prob)
		print("******************************************")
		print(F)
		print("******************************************")
		for i in range(F.shape[0]):
			if(F[i]>thresh):
				idx = i 

	val = np.zeros((1,num_bits*2))
	val[0] = mating_pool[i]
	act_val = actual_val(val, limits)
	print(act_val)



if __name__ == "__main__":
	num_bits = 10
	num_strings = 20
	crossover_prob = 0.8
	mutation_prob = 0.05
	limits = np.zeros(2)
	limits[0] = 0
	limits[1] = 6

	solve(num_bits,num_strings,crossover_prob,mutation_prob,limits)
