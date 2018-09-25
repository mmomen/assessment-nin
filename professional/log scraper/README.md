Instructions
============

In this directory there is an Apache logfile with several entries, "puppet_access_ssl.log". Preferably in Python (however any language is acceptable), as simple or as complicated as you like, write something that will print to the screen:

* How many times the URL "/production/file_metadata/modules/ssh/sshd_config" was fetched
    * Of those requests, how many times the return code from Apache was not 200
* The total number of times Apache returned any code other than 200
* The total number of times that any IP address sent a PUT request to a path under "/dev/report/"
    * A breakdown of how many times such requests were made by IP address

This solution must run & print accurate results.
