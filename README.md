# ISS Now 
# How to run it

Create a new virtualenv and install the requirements from requirements.txt
```bash
virtualenv venv
pip install -r requirements.txt
source venv/bin/activate
python issnow.py
```
# Guidelines
## Details

There is an API (http://api.open-notify.org/) that provides information on the International Space Station. Documentation is provided via the website, along with sample request/response.

## Task

Implement a Python script that will accept the following command line arguments, along with any required information, and print the expected results

* `loc`

> print the current location of the ISS
> 
> Example: “The ISS current location at {time} is {LAT, LONG}”

* `pass`

> print the passing details of the ISS for a given location
>
> Example: “The ISS will be overhead {LAT, LONG} at {time} for {duration}”

* `people`

> for each craft print the details of those people that are currently in space
