from sympy import symbols, linsolve

v_str = ["v{}".format(i) for i in range(26)]
v = symbols(",".join(v_str))

def config_exp(config_dict):
	eqns = [v[20], v[21], v[22], v[23], v[24], v[25]]
	for i in config_dict:
		if i < 20:
			if config_dict[i] == i:
				eqns.append(v[i] - 1 - v[i+1]/6 - v[i+2]/6 - v[i+3]/6 - v[i+4]/6 - v[i+5]/6 - v[i+6]/6)
			else:
				eqns.append(v[i] - v[config_dict[i]])

	vals = linsolve(eqns, v)
	return sum(vals.args[0][:6])/6

def prepare_conf_dict(ind1, ind2, ind3, ind4):
	conf_dict = {}
	for i in range(20):
		conf_dict[i] = i
	conf_dict[ind1] = ind1 + ladder1
	conf_dict[ind2] = ind2 + ladder2
	conf_dict[ind3] = ind3 - snake1
	conf_dict[ind4] = ind4 - snake2
	return conf_dict




ladder1 = 4
ladder2 = 8
snake1 = 9
snake2 = 7


conf_dict = prepare_conf_dict(0,1,14,15)		
ret = config_exp(conf_dict)
conf_dict2 = prepare_conf_dict(1,0,14,15)		
ret2 = config_exp(conf_dict2)



max_val = 0
max_args = []

for ind1 in range(20 - ladder1):
	for ind2 in range(20 - ladder2):
		for ind3 in range(snake1, 20):
			print("i1={},i2={},i3={},max_val={}".format(ind1,ind2,ind3, max_val))
			for ind4 in range(snake2, 20):
				points_set = set([ind1,ind2,ind3,ind4, ind1 + ladder1, ind2+ladder2, ind3 - snake1, ind4 - snake2])
				if len(points_set) == 8:
					conf_dict = prepare_conf_dict(ind1, ind2, ind3, ind4)		
					ret = config_exp(conf_dict)
					if ret > max_val:
						max_val = ret
						max_args = [ind1, ind2, ind3, ind4]


conf_dict[14] = 18
conf_dict[16] = 9
conf_dict[2] = 10
conf_dict[12] = 3

ret = config_exp(conf_dict)
