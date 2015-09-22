import lab3

pLessThan = lab3.unit_normal_cdf(-0.5/0.18)
pGreaterThan = 1 - lab3.unit_normal_cdf(0.5/0.18)

pError = 0.5*pLessThan + 0.5*pGreaterThan

if __name__ == '__main__':
	print pError