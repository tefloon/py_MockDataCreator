import csv
import os
import random
import json

outFileName = 'result.csv'
dataDirName = 'Data'
dataDir = os.path.join(os.getcwd(), dataDirName)

def ReadFile(fileName, n):
	rows = []

	with open(os.path.join(dataDir, fileName), "r", encoding='UTF-8') as csvfile:
		reader = csv.reader(csvfile)
		for row in reader:
			rows.append(row[0])
			n -= 1
			if n < 0:
				break
	return rows

def CreateAddresses(n):
	rows = ReadFile('adres.csv', n)
	rows.pop(0)	# get rid of first row

	addresses = []
	cities = []

	for row in rows:
		address  = row.split(';')
		
		ulica_cz  = address[5].split(" ")
		prefix = ''
		street = address[5]
		
		if ulica_cz[0] in ('aleja', 'Aleja', 'aleje', 'Aleje'):
			prefix = 'al. '
			street = prefix + " ".join(ulica_cz[1:])
		elif ulica_cz[0] == 'ulica':
			prefix = 'ul. '
			street = prefix + " ".join(ulica_cz[1:])

		number  = address[6]
		city = address[2]

		addresses.append(f"{street} {number}")
		cities.append(address[2])

	return addresses, cities

def CreateNames(sex, n):
	fileName = ''

	if sex == 'F':
		fileName = 'imieF.csv'
	else:
		fileName = 'imieM.csv'

	rows = ReadFile(fileName, n)
	rows.pop(0)	# get rid of first row

	names = []

	for row in rows:
		names.append(row.split(',')[0].capitalize())

	return names

def CreateSurnames(sex, n):
	fileName = ''

	if sex == 'F':
		fileName = 'nazF.csv'
	else:
		fileName = 'nazM.csv'

	rows = ReadFile(fileName, n)
	rows.pop(0)	# get rid of first row

	surnames = []

	for row in rows:
		surnames.append(row.split(',')[0].capitalize())

	return surnames

def CreateDataSet(n):
	numM = random.randrange(n)
	numF = n - numM

	data = []

	adr, city = CreateAddresses(n)

	nameM = sorted(CreateNames('M', numM), key = lambda x: random.random() )
	nameF = sorted(CreateNames('F', numF), key = lambda x: random.random() )

	surnM = sorted(CreateSurnames('M', numM), key = lambda x: random.random() )
	surnF = sorted(CreateSurnames('F', numF), key = lambda x: random.random() )

	i = 0

	for i in range(numF):
		item = [ nameF[i], surnF[i], 'F', adr[i], city[i]]
		data.append(item)

	for j in range(numM):
		item = [ nameM[j], surnM[j], 'M', adr[i], city[i]]
		i += 1
		data.append(item)

	return data

#  Creating mock data
# ====================
data = CreateDataSet(500)

#  Writing data as csv
# =====================
fields = ['Name', 'Surname', 'Gender', 'Address', 'City']
with open(outFileName, "w", encoding='UTF-8', newline='') as csvfile:
    # creating a csv writer object 
    csvwriter = csv.writer(csvfile) 
        
    # writing the fields 
    csvwriter.writerow(fields) 
        
    # writing the data rows 
    csvwriter.writerows(data)

#  Creating dictionary
# =====================
dataDict = {'students': []}

for i in range(len(data)):
	person = {
		'name': data[i][0],
		'surname': data[i][1],
		'gender': data[i][2],
		'address': data[i][3],
		'city': data[i][4]
	}
	dataDict['students'].append(person)

#  Writing data as json
# ======================
with open("result.json", "w", encoding='UTF-8', newline='') as f:
   json.dump(dataDict, f, ensure_ascii=False, indent=2)