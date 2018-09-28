# How to run the solution and test

1. Install tavern for testing: `pip install tavern[pytest]`
2. Run server: `python server2.py`
3. Run test cases: `py.text tests/test_cases.tavern.yaml`

## Test Cases - `test_cases.tavern.yaml`

1. PUT of word
1. PUT of word and expect interation
1. PUT of new word, with trailing slash
1. PUT with request body (expect failure)
1. PUT with special character (expect failure)
1. PUT with 2 words (expect failure)
1. PUT with wrong first level (expect failure)
1. PUT with bad path (1) (expect failure)
1. PUT with bad path (2) (expect failure)
1. PUT with numeric character (expect failure)
1. GET /words for total results
1. GET a single word
1. GET another single word