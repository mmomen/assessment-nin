Instructions
============

Preferably in Python (however any language is acceptable), as simple or as complex as you like, write a small daemon that will:

* Start listening on a HTTP or HTTPS port

* Accept PUT requests to /words/WORDNAME, with no request body
    
   * Store a running count of all words that have been sent to it

        * E.g. "word COUNT has been sent 5 times", "word ROFFLE has been sent 8 times", etc
        
   * Return a HTTP error code and JSON hash when the request is not one word in length or WORDNAME doesn't consists of only [a-zA-Z] characters:  


        {
            "error": "PUT requests must be one word in length"
        }  
            
   * On Success, return the integer count of how many times that word has been PUT to the api in a JSON hash


        {
            "words": {
                "WORDNAME": INTEGER_COUNT
            }
        }

* Accept GET requests to /words/WORDNAME

    * Return the integer count of how many times that word has been PUT to the api in a JSON hash, including words that have not been PUT before


        {
            "words": {
                "WORDNAME": INTEGER_COUNT
            }
        }

* Accept GET requests to /words

    * Return a JSON hash listing the count of every word it has received


        {
        	"words": {
        		"WORDNAME": INTEGER_COUNT,
        		"WORDNAME2": INTEGER_COUNT,
        		"WORDNAME3": INTEGER_COUNT
        	}
        }
