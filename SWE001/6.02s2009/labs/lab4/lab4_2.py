# template for Lab #4, Task #2
import lab4
import numpy
 
def findErrorLocation(rowErrors,columnErrors):
	for i in range(len(rowErrors)):
		if rowErrors[i]:
			row = i
	for i in range(len(columnErrors)):
		if columnErrors[i]:
			column = i
	return [row,column] 
 
def correct_errors(binmsg): 
	numErrors = 0
	data = binmsg[:8]
	rowParity = binmsg[8:10]
	columnParity = binmsg[10:14]
	parity = binmsg[14]
	dataRow1 = data[:4]
	dataRow2 = data[4:8]
	column1 = [data[0],data[4]]
	column2 = [data[1],data[5]]
	column3 = [data[2],data[6]]
	column4 = [data[3],data[7]]
	rowErrors = []
	for row in range(2):
		rowErrors.append(False)
	columnErrors = []
	for column in range(4):
		columnErrors.append(False)
	totalError = False
	
	# test for total parity
	if lab4.even_parity(binmsg) != 0:
		numErrors += 1
		totalError = True
	
	# test for row parity
	if lab4.even_parity(dataRow1) != rowParity[0]:
		numErrors += 1
		rowErrors[0] = True
	if lab4.even_parity(dataRow2) != rowParity[1]:
		numErrors += 1
		rowErrors[1] = True
		
	# test for column parity
	if lab4.even_parity(column1) != columnParity[0]:
		numErrors += 1
		columnErrors[0] = True
	if lab4.even_parity(column2) != columnParity[1]:
		numErrors += 1
		columnErrors[1] = True
	if lab4.even_parity(column3) != columnParity[2]:
		numErrors += 1
		columnErrors[2] = True
	if lab4.even_parity(column4) != columnParity[3]:
		numErrors += 1
		columnErrors[3] = True
	
	rowErrors = numpy.array(rowErrors)
	columnErrors = numpy.array(columnErrors)
	numRowErrors = sum(1*rowErrors)
	numColumnErrors = sum(1*columnErrors)
	
	if numErrors == 0:	# no errors
		return data
	elif numRowErrors == numColumnErrors == 1 and totalError:	# single bit error
		errorLocation = findErrorLocation(rowErrors,columnErrors)	# find bit
		errorIndex = 4*errorLocation[0] + errorLocation[1]
		if binmsg[errorIndex] == 1:	# correct it
			binmsg[errorIndex] = 0
		else:
			binmsg[errorIndex] = 1
		return binmsg[:8]
	elif numErrors < 3 and totalError: #just a parity error
		return data
	else:
		raise lab4.DecodingError,"uncorrectable error!"

if __name__ == '__main__':
    lab4.test_correct_errors(correct_errors)