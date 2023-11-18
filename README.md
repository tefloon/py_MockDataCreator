# Mock personal data creator
A simple tool for creating fake polish personal data in JSON or CSV formats.
If works generally by randomly mixing and matching all the possible names, surnames and addresses 
of Polish citizens available in GUS' databases (they are public domain).

## How to run
To generate 500 records in JSON simply open console in the scripts folder and run:
```bash
  python .\MockDataCreator.py
```

## Options
Available options include:
  `-h`, `--help`   show this help message and exit
  `-n` NUMBER    Number of records
  `-f` FILENAME  Output filename
  `--no-phone`   Exclude phone numbers
  `--no-email`   Exclude e-mail adresses
  `-pr`          Include parent data?
  `--yaml`       Output YAML format as well
  `--uuid`       Use UUID instead of a number for id?
## Records
Each record generated contains:
- `id`: an incremental number, starting at 1
- `name`: a string denoting name of the person
- `surname`: a string denoting surname of the person
- `gender`: a string denoting gender. Possible values are "M" and "F"
- `address`: a string denoting the address of the person
- `parents`: a nested object for the contact information of the parents
	- `dad`: a nested object for the dad 
    - `name`: name of the dad
    - `surname`: surname of the dad
    - `phone`: a string containing a valid phone number
    - `email`: a string containing a valid email address
  -`mom`: a nested object for the mum, has the same fields as `dad` 
- `hash`: a unique hash created using `uuid4()` function

## Example
An example of the record is shown below:
```JSON
[
  {
    "id": 0,
    "name": "Janina",
    "surname": "Król",
    "gender": "F",
    "address": "al. Jerozolimskie 212",
    "city": "Warszawa",
    "parents": {
      "dad": {
        "name": "Józef",
        "surname": "Król"
      },
      "mom": {
        "name": "Zofia",
        "surname": "Król"
      }
    }
  },
  {
    "id": 1,
    "name": "Sławomir",
    "surname": "Zawadzki",
    "gender": "M",
    "address": "ul. Fraszki 11",
    "city": "Warszawa",
    "parents": {
      "dad": {
        "name": "Jarosław",
        "surname": "Zawadzki",
        "phone": "974611580",
        "email": "rogapal@wp.pl"
      },
      "mom": {
        "name": "Anna",
        "surname": "Zawadzka",
        "phone": "761576065",
        "email": "wnyi@o2.pl"
      }
    }
  }
]
```