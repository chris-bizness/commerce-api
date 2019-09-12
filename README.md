
# commerce-api
A simple commerce API written for Albert.


## Installation

**Note: Development completed in Python 3.7.4**

In your virtualenv of choice
```bash
./setup.sh
```
or, if you'd like to do it manually...
```bash
pip install -U -r requirements/build.txt
python manage.py migrate
```

## Running it locally
```bash
./dev_server.sh
```
or, if you'd like to do it manually...
```bash
python manage.py runserver --settings=project.settings.dev 8000
```
In a browser, navigate to [localhost:8000](localhost:8000)

## Run tests
```bash
py.test
```

## Features
Currently, the API has 2 endpoints:
- /card-number/generate
    - GET
        - Since the CC num is generated, it didn't seem to merit a high level of security
    - query string parameters:
        - issuer
            - accepts a string representing 1 or the 4 major card issuers: Visa, AmEx, MasterCard & Discover
            - It's somewhat lenient in that "amex"/"am ex"/"american express" are all valid and caps don't matter, but it could be more user-friendly
            - if issuer is set, neither of the other query params can be
        - prefix
            - accepts a string of digits (and some separators like dashes, spaces, periods, etc.)
            - returns a card number with this as the start of the digits
        - length
            - how many digits the returned card number should contain
            - accepts 8-19
    - return value
        - returns a JSON dict with the top-level keys:
            - number (the card number)
            - details
                - this is a nested dict with the same data as the validate endpoint
- /card-number/validate
    - POST
        - I felt this was more secure to transmit CC numbers over
    - POST body:
        - number
            - must be a string (so we don't lose leading 0s)
            - accepts digits and some common separators (spaces, dashes, periods, etc.)

## Future Work
- Add a client to retrieve information about more issuers without having to implement each manually
  - the current setup was intended to be the fallback, but I ran out of time before I could implement the client
- Move the card issuers into a model with a lightweight CRUD API around them
- Get hired?

## Notes from the dev
I've used Django for years, but this was my first time using Django REST Framework, so I may have missed some features that would make the code cleaner or didn't follow standards in some places. The "self"-documenting schemas gave me the most trouble for sure - definitely missed something that should have made that much easier. Let me know! I'd love the feedback.
