import random
import math
import numpy as np
import matplotlib.pyplot as plt
import time


print(random.__file__)
print(np.random.__file__)

SAMPLES = 100*1000

def inversion(mu = 0, sigma = 1):
	p0 = -0.32222431088
	q0 = 0.099348462606
	p1 = -1
	q1 = 0.588581570495
	p2 = -0.342242088547
	q2 = 0.531103462366
	p3 = -0.0204231210245
	q3 = 0.10353775285
	p4 = -0.0000453642210148
	q4 = 0.003860700634

	u = random.random()
	y = math.sqrt(-2*math.log(1-u))
	res = y + (p0 + p1*y + p2*y**2 + p3*y**3 + p4*y**4)/(q0 + q1*y + q2*y**2 + q3*y**3 + q4*y**4)
	
	return mu + res * sigma

def box_muller(mu = 0, sigma = 1):
	# For the code to be generic, I throw away half of the variables attained, since it's two for two
	u1 = random.random()
	u2 = random.random()
	y1 = math.sqrt(-2*math.log(u1)*sigma)*math.sin(2*math.pi * u2)
	y2 = math.sqrt(-2*math.log(u1)*sigma)*math.cos(2*math.pi * u2)
	return mu + y1, mu + y2

def marsaglia(mu = 0, sigma = 1):
	Z = random.random()
	theta = 2*math.pi * random.random()
	v1 = Z * math.cos(theta)
	v2 = Z * math.sin(theta)
	W = Z**2
	y1 = math.sqrt(-math.log(W)/W*sigma)*v1
	y2 = math.sqrt(-math.log(W)/W*sigma)*v2
	return mu + y1, mu + y2

def inversion_exp(lamb = 1):
	u = random.random()
	x = -math.log((1 - u))/lamb
	return x


def accept_reject(mu = 0, sigma = 1):
	delta = 1/sigma
	C = math.sqrt(2*math.e**(sigma**2*delta**2)/math.pi)

	# TODO - produce my own expovariate! using the geometric split method. 
	#x = random.expovariate(1)
	x = inversion_exp(delta)
	rhs = (math.sqrt(2/math.pi) * math.e**(delta*x - (x/sigma)**2/2))/(sigma * C)
	u = random.random()
	if u < rhs:
		return random.choice([mu-x,mu+x])
	else:
		return None

def uniform_ratio(mu = 0, sigma = 1):
	v1 = random.random()
	v2 = 2*math.sqrt(2/math.e)*(random.random() - 1/2)

	X = v2/v1
	if X**2 < -4 * math.log(v1):
		return mu + X * sigma
	else:
		return uniform_ratio(mu, sigma)

def calc_var(arr, mu = 0):
	return sum([(i-mu)**2 for i in arr])/SAMPLES



inversion_arr = []
start = time.time()
for i in range(100000):
	inversion_arr.append(inversion())
end = time.time()
inversion_time = end - start 


ar_arr = []
start = time.time()
i = 0
while i < SAMPLES:
	ret = accept_reject(5, 1)
	if ret is not None:
		i += 1
		ar_arr.append(ret)
end = time.time()
ar_time = end - start 

bm_arr = []
start = time.time()
for i in range(int(SAMPLES/2)):
	bm_arr += box_muller(0,2)
end = time.time()
bm_time = (end - start)

marsaglia_arr = []
start = time.time()
for i in range(int(SAMPLES/2)):
	marsaglia_arr += marsaglia(0,5)
end = time.time()
marsaglia_time = (end - start)

uniratio_arr = []
start = time.time()
for i in range(100000):
	uniratio_arr.append(uniform_ratio())
end = time.time()
uniratio_time = end - start 

python_arr = []
start = time.time()
for i in range(100000):
	python_arr.append(random.normalvariate(0,1))
end = time.time()
python_time = end - start 

gauss_python_arr = []
start = time.time()
for i in range(100000):
	gauss_python_arr.append(random.gauss(3,3))
end = time.time()
gauss_python_time = end - start 

numpy_arr = []
start = time.time()
for i in range(100000):
	numpy_arr.append(np.random.normal(0,1))
end = time.time()
numpy_time = end - start 

start = time.time()
numpy_arr2 = np.random.normal(0,1,SAMPLES)
end = time.time()
numpy_time2 = end - start 


x,y = np.histogram(inversion_arr, bins=100)
plt.plot(y[:-1],x, 'bo')
x,y = np.histogram(ar_arr, bins=100)
plt.plot(y[:-1],x, 'go')
x,y = np.histogram(bm_arr, bins=100)
plt.plot(y[:-1],x, 'co')
x,y = np.histogram(marsaglia_arr, bins=100)
plt.plot(y[:-1],x, 'yo')
x,y = np.histogram(uniratio_arr, bins=100)
plt.plot(y[:-1],x, 'mo')
x,y = np.histogram(python_arr, bins=100)
plt.plot(y[:-1],x, 'ko')
x,y = np.histogram(gauss_python_arr, bins=100)
plt.plot(y[:-1],x, 'ro')
x,y = np.histogram(numpy_arr, bins=100)
plt.plot(y[:-1],x, 'ko')
x,y = np.histogram(numpy_arr2, bins=100)
plt.plot(y[:-1],x, 'go')
plt.show()
print("inversion_time={},accept_reject_time={},box muller time={}, marsaglia time={}, uniform ratio time={}, python time={}, gauss python time={}, numpy time={},numpy time2 = {}".format(inversion_time, ar_time, bm_time, marsaglia_time, uniratio_time, python_time,gauss_python_time, numpy_time, numpy_time2))
print("mean inversion={}, mean accept reject={}, mean box muller={}, mean marsaglia={}, mean uniform ratio={}, mean python={}, mean gauss python ={}, mean numpy={}, mean numpy2 = {}".format(sum(inversion_arr)/SAMPLES, sum(ar_arr)/SAMPLES, sum(bm_arr)/SAMPLES, sum(marsaglia_arr)/SAMPLES, sum(uniratio_arr)/SAMPLES, sum(python_arr)/SAMPLES, sum(gauss_python_arr)/SAMPLES, sum(numpy_arr)/SAMPLES, sum(numpy_arr2)/SAMPLES))
print("var inversion={}, var accept reject={}, var box muller={}, var marsaglia={}, var uniform ratio={}, var python={}, var gauss python={}, var numpy={}, var numpy2={}".format(calc_var(inversion_arr), calc_var(ar_arr, sum(ar_arr)/SAMPLES), calc_var(bm_arr), calc_var(marsaglia_arr), calc_var(uniratio_arr), calc_var(python_arr), calc_var(gauss_python_arr), calc_var(numpy_arr),calc_var(numpy_arr2)))

time.sleep(10)
exit()

