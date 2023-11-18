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
- `-n` or `--number`: number of records to create
- `-o` or `--out`: name of the output file (defaults to `results`)
- `--csv`: save the records in a `CSV` file instead of the default `JSON`

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
  {
    "id": 1,
    "name": "Lesław",
    "surname": "Piasecki",
    "gender": "M",
    "address": "al. Jerozolimskie 195A",
    "city": "Warszawa",
    "parents": {
      "dad": {
        "name": "Ludwik",
        "surname": "Piasecki",
        "phone": "917748355",
        "email": "olrtp@wp.pl"
      },
      "mom": {
        "name": "Nina",
        "surname": "Piasecka",
        "phone": "705225779",
        "email": "ckcqr@yahoo.com"
      }
    },
    "hash": "906e6dc8-03bf-4797-b440-5ac9d025a562"
  },

```