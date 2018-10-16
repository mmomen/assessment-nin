# How to run the solution and test

1. Install tavern for testing: `pip install tavern[pytest]`
1. Run server: `python server.py`
1. In another terminal window, run test cases: `py.text tests/test_cases.tavern.yaml` or `tavern-ci tests/test_cases.tavern.yaml`
1. In window running the server, press ctrl+c to shut down.

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
1. GET /words/ for total results
1. GET a single word
1. GET another single word
1. Unsupported GET request