This vagrant system (CentOS Linux 6.5) has a script which executes once
per minute and generates a file in /tmp/wattime. These files are not important
and should be cleaned up after the process exits. It is your job to write a
process that cleans up the leftover files.

$ vagrant up challenge
$ vagrant provision challenge

1. Write a python script that cleans up anything in /tmp/wattime older
than 30 minutes to keep the disk clean. For extra credit, the list of
files cleaned up should appear in syslog.

2. Add the python script to CRON running every 10 minutes as the root user.

Once you have solved both problems, bundle your fixes into a script or
some other deployable mechanism, and modify the Vagrantfile to deploy the
fixes when the system is provisioned. Ensure your fixes work after
destroying and recreating the vagrant box.

$ vagrant destroy challenge
$ vagrant up challenge
$ vagrant provision challenge
$ # Perform your tests again

Bundle your deployable fixes with the Vagrantfile and return them.
