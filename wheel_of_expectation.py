values = [0 for i in range(67)]

values[-1] = 6600
values[-2] = 7100*11/12
values[-3] = 1/12 * values[-2] + 7050*10/12
values[-4] = 1/12 * values[-3] + 1/12 * values[-2] + 7000 * 9/12

for i in range(11):
	for j in range(i):
		values[-2 - i] += 1/12 * values[-2-i + j]
	values[-2-i] += (7100 - 50*i) * (11 - i)/12


for i in range(54,-1,-1):
	for j in range(1,12):
		values[i] += values[i+j]/12

print(values[0])

