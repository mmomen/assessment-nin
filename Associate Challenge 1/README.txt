This vagrant system (CentOS Linux 6.5) is meant to host a single PHP page
showing the configuration of PHP on this system. But it is currently
misconfigured. It is your job to fix the 3 following misconfigurations.

$ vagrant up challenge

1. Apache is showing a 404 when we load the vagrant system and attempt
   to load "http://127.0.0.1:8080/info.php". But the info.php file is
   present in /var/www/info.php. Investigate the apache config and logs,
   and fix it so that the info.php file loads correctly.

2. Once problem #1 is solved, rename the "info.php" file to "index.php"

3. Once problem #2 is solved, change the apache config to present a
   self-signed SSL certificate when accessed at
   https://127.0.0.1:8443/index.php . Generate the self-signed certificate,
   install it in apache, and verify that the connection to
   https://127.0.0.1:8443/index.php is encrypted with the certificate. Note
   that the port number on the guest is not 8443 - see the Vagranfile.

Once you have solved all 3 problems, bundle your fixes into a script or
some other deployable mechanism, and modify the Vagrantfile to deploy the
fixes when the system is provisioned. Ensure your fixes work after
destroying and recreating the vagrant box.

$ vagrant destry challenge
$ vagrant up challenge
$ # Perform your tests again

Bundle your deployable fixes with the Vagrantfile and return them.
