import csv
import os
import random
import json
import yaml
import uuid
import string
import argparse


def GenerateJson(params):
    numberOfRecords = params.number
    outFileName = params.fileName

    dataDirName = "Data"
    dataDir = os.path.join(os.getcwd(), dataDirName)

    def ReadFile(fileName, n):
        rows = []

        with open(os.path.join(dataDir, fileName), "r", encoding="UTF-8") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                rows.append(row[0])
                n -= 1
                if n < 0:
                    break
        return rows

    def CreateAddresses(n):
        rows = ReadFile("adres.csv", n)
        rows.pop(0)  # get rid of first row

        addresses = []
        cities = []

        for row in rows:
            address = row.split(";")

            ulica_cz = address[5].split(" ")
            prefix = ""
            street = address[5]

            if ulica_cz[0] in ("aleja", "Aleja", "aleje", "Aleje"):
                prefix = "al. "
                street = prefix + " ".join(ulica_cz[1:])
            elif ulica_cz[0] == "ulica":
                prefix = "ul. "
                street = prefix + " ".join(ulica_cz[1:])

            number = address[6]
            city = address[2]

            addresses.append(f"{street} {number}")
            cities.append(address[2])

        return addresses, cities

    def CreateNames(sex, n):
        fileName = ""

        if sex == "F":
            fileName = "imieF.csv"
        else:
            fileName = "imieM.csv"

        rows = ReadFile(fileName, n)
        rows.pop(0)  # get rid of first row

        names = []

        for row in rows:
            names.append(row.split(",")[0].capitalize())

        return names

    def CreateSurnames(sex, n):
        fileName = ""

        if sex == "F":
            fileName = "nazF.csv"
        else:
            fileName = "nazM.csv"

        rows = ReadFile(fileName, n)
        rows.pop(0)  # get rid of first row

        surnames = []

        for row in rows:
            surnames.append(row.split(",")[0].capitalize())

        return surnames

    def CreatePhoneNumber():
        number = ""
        number += str(random.randint(6, 9))

        for i in range(8):
            number += str(random.randint(0, 9))

        return number

    def CreateEmailAddress():
        hosts = [
            "o2.pl",
            "gmail.com",
            "wp.pl",
            "onet.pl",
            "gazeta.pl",
            "yahoo.com",
            "gov.pl",
        ]

        user = "".join(
            random.choice(string.ascii_lowercase) for x in range(random.randint(4, 10))
        )
        host = hosts[random.randint(0, len(hosts) - 1)]

        address = user + "@" + host
        return address

    def CreateDataSet(n):
        numM = random.randrange(n // 4, (3 * n) // 4)
        numF = n - numM

        data = []

        adr, city = CreateAddresses(n)

        nameM = sorted(CreateNames("M", numM), key=lambda x: random.random())
        nameF = sorted(CreateNames("F", numF), key=lambda x: random.random())

        surnM = sorted(CreateSurnames("M", numM), key=lambda x: random.random())
        surnF = sorted(CreateSurnames("F", numF), key=lambda x: random.random())

        parents = []

        for i in range(numF):
            idd = uuid.uuid4() if params.uuid else 0
            surnameDad = surnF[i]

            if surnameDad[-1] == "a":
                surnameDad = surnameDad[:-1] + "i"
            if params.parents:
                parents = {
                    "dad": {
                        "name": nameM[random.randint(0, len(nameM) - 1)],
                        "surname": surnameDad,
                    },
                    "mom": {
                        "name": nameF[random.randint(0, len(nameF) - 1)],
                        "surname": surnF[i],
                    },
                }
                if args.phone:
                    parents["dad"]["phone"] = CreatePhoneNumber()
                    parents["mom"]["phone"] = CreatePhoneNumber()
                if args.email:
                    parents["dad"]["email"] = CreateEmailAddress()
                    parents["mom"]["email"] = CreateEmailAddress()

            item = (
                [idd, nameF[i], surnF[i], "F", adr[i], city[i], parents]
                if params.parents
                else [idd, nameF[i], surnF[i], "F", adr[i], city[i]]
            )
            data.append(item)

        for j in range(numM):
            idd = uuid.uuid4() if params.uuid else 0
            surnameMom = surnM[j]

            if surnameMom[-1] == "i":
                surnameMom = surnameMom[:-1] + "a"
            if params.parents:
                parents = {
                    "dad": {
                        "name": nameM[random.randint(0, len(nameM) - 1)],
                        "surname": surnM[j],
                        "phone": CreatePhoneNumber(),
                        "email": CreateEmailAddress(),
                    },
                    "mom": {
                        "name": nameF[random.randint(0, len(nameF) - 1)],
                        "surname": surnameMom,
                        "phone": CreatePhoneNumber(),
                        "email": CreateEmailAddress(),
                    },
                }
            item = (
                [idd, nameM[j], surnM[j], "M", adr[j], city[j], parents]
                if params.parents
                else [idd, nameM[j], surnM[j], "F", adr[j], city[j]]
            )
            data.append(item)

        return sorted(data, key=lambda x: random.random())

    #  Creating mock data
    # ====================
    data = CreateDataSet(args.number)

    #  Creating dictionary
    # =====================
    dataDict = []

    for i in range(len(data)):
        person = {
            "id": str(data[i][0]) if params.uuid else i,
            "name": data[i][1],
            "surname": data[i][2],
            "gender": data[i][3],
            "address": data[i][4],
            "city": data[i][5],
        }
        if params.phone:
            person["phone"] = CreatePhoneNumber()
        if params.email:
            person["email"] = CreateEmailAddress()
        if params.parents:
            person["parents"] = data[i][6]

        dataDict.append(person)

    #  Writing data as json
    # ======================
    with open(f"{outFileName}.json", "w", encoding="UTF-8", newline="") as f:
        json.dump(dataDict, f, ensure_ascii=False, indent=2)

    if params.yaml:
        with open(f"{outFileName}.yaml", "w", encoding="UTF-8", newline="") as f:
            yaml.dump(dataDict, f, allow_unicode=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Script for generating mock data of Polish citizens"
    )

    parser.add_argument(
        "-n",
        type=int,
        default=500,
        dest="number",
        help="Number of records",
    )

    parser.add_argument(
        "-f", type=str, default="result1.json", dest="fileName", help="Output filename"
    )

    parser.add_argument(
        "--no-phone",
        action="store_false",
        default=True,
        dest="phone",
        help="Include phone numbers?",
    )

    parser.add_argument(
        "--no-email",
        action="store_false",
        default=True,
        dest="email",
        help="Include e-mail adresses?",
    )

    parser.add_argument(
        "-pr",
        action="store_true",
        default=False,
        dest="parents",
        help="Include parent data?",
    )

    parser.add_argument(
        "--yaml",
        action="store_true",
        default=False,
        dest="yaml",
        help="Output YAML format as well",
    )

    parser.add_argument(
        "--uuid",
        action="store_true",
        default=False,
        dest="uuid",
        help="Use UUID instead of a number for id?",
    )

    args = parser.parse_args()

    GenerateJson(args)
