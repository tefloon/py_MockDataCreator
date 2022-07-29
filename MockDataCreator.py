import csv
import os
import random
import json
import yaml
import uuid
import string

numberOfRecords = 500
outFileName = 'results'
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

def CreatePhoneNumber():
	number = ""
	number += str(random.randint(6,9))

	for i in range(8):
		number += str(random.randint(0,9))

	return number

def CreateEmailAddress():
	hosts = ['o2.pl', 'gmail.com', 'wp.pl', 'onet.pl', 'gazeta.pl', 'yahoo.com', 'gov.pl']
	
	user = ''.join(random.choice(string.ascii_lowercase) for x in range(random.randint(4,10)))
	host = hosts[random.randint(0, len(hosts) - 1)]

	address = user + '@' + host
	return address

def CreateDataSet(n):
	numM = random.randrange(n//4, (3*n)//4)
	numF = n - numM

	data = []

	adr, city = CreateAddresses(n)

	nameM = sorted(CreateNames('M', numM), key = lambda x: random.random() )
	nameF = sorted(CreateNames('F', numF), key = lambda x: random.random() )

	surnM = sorted(CreateSurnames('M', numM), key = lambda x: random.random() )
	surnF = sorted(CreateSurnames('F', numF), key = lambda x: random.random() )

	parents = []


	for i in range(numF):
		ha = str(uuid.uuid4())

		surnameDad = surnF[i]

		if surnameDad[-1] == "a":
			surnameDad = surnameDad[:-1] + "i"

		parents = {
			"dad": {
				"name": 	  	nameM[random.randint(0, len(nameM) - 1)],
				"surname": 	surnameDad,
				"phone": 	CreatePhoneNumber(),
				"email":		CreateEmailAddress()
			},
			"mom": {
				"name": 	  	nameF[random.randint(0, len(nameF) - 1)],
				"surname": 	surnF[i],
				"phone": 	CreatePhoneNumber(),
				"email":		CreateEmailAddress()
			},
		}
		item = [ nameF[i], surnF[i], 'F', adr[i], city[i], parents, ha]
		data.append(item)

	for j in range(numM):
		ha = str(uuid.uuid4())

		surnameMom = surnM[j]

		if surnameMom[-1] == "i":
			surnameMom = surnameMom[:-1] + "a"


		parents = {
			"dad": {
				"name": 	  	nameM[random.randint(0, len(nameM) - 1)],
				"surname": 	surnM[j],
				"phone": 	CreatePhoneNumber(),
				"email":		CreateEmailAddress()
			},
			"mom": {
				"name": 	  	nameF[random.randint(0, len(nameF) - 1)],
				"surname": 	surnameMom,
				"phone": 	CreatePhoneNumber(),
				"email":		CreateEmailAddress()
			},
		}
		item = [ nameM[j], surnM[j], 'M', adr[j], city[j], parents, ha]
		data.append(item)


	return sorted(data, key = lambda x: random.random() )

def GenerateCSV():
	#  Creating mock data
	# ====================
	data = CreateDataSet(numberOfRecords)

	#  Writing data as csv
	# =====================
	fields = ['name', 'surname', 'gender', 'address', 'city', 'hash']
	with open(f"{outFileName}.csv", "w", encoding='UTF-8', newline='') as csvfile:
	    # creating a csv writer object 
	    csvwriter = csv.writer(csvfile) 
	        
	    # writing the fields 
	    csvwriter.writerow(fields) 
	        
	    # writing the data rows 
	    csvwriter.writerows(data)

def GenerateJson():
	#  Creating mock data
	# ====================
	data = CreateDataSet(numberOfRecords)

	#  Creating dictionary
	# =====================
	dataDict = []

	for i in range(len(data)):
		person = {
			"id": i+1,
			"name": data[i][0],
			"surname": data[i][1],
			"gender": data[i][2],
			"address": data[i][3],
			"city": data[i][4],
			"parents": data[i][5],
			"hash": data[i][6]
		}
		dataDict.append(person)

	#  Writing data as json
	# ======================
	with open(f"{outFileName}.json", "w", encoding='UTF-8', newline='') as f:
	   json.dump(dataDict, f, ensure_ascii=False, indent=2)

	#  Uncomment following 2 lines for YAML version:
	# ===============================================
	# with open(f"{outFileName}.yaml", "w", encoding='UTF-8', newline='') as f:
	#    yaml.dump(dataDict, f, allow_unicode=True)


GenerateJson()