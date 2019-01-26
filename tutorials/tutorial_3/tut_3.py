def vertice_gen(M):
	W = []

	for i in range(2**len(M)):
		x = []
		x.append(M[0][i%2])
		x.append(M[1][int((i%4)/2)])
		x.append(M[2][int((i%8)/4)])
		x.append(M[3][int((i%16)/8)])
		W.append(x)

	return W

def mul(X,W):
	res = []

	for i in range(len(X)):
		for j in range(len(X)):
			s = 0
			s2 = 0
			for k in range(len(X[i])):
				s+=X[i][k]*W[j][k]
				s2 += W[j][k]
			res.append(s/s2)
	return res

if __name__=="__main__":
	X = [[0.4,0.6],[0.7,0.96],[0.1,0.3],[0.0,0.2]]
	W = [[0.8,1.0],[0.5,0.9],[0.8,1.0],[0.5,0.9]]

	X = vertice_gen(X)
	W = vertice_gen(W)

	y = mul(X,W)
	res = [min(y),max(y)]

	print(res)