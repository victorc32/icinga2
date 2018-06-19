# icinga2
Some Script for Monitoring Icinga2

Icinga2api

A NRPE command plugin for do interface bitween NRPE and icinga2 API/REST. Script writed in python 2.7.

2 options:

- icinga2-api.py ALL : display all hostnames and services
- icinga2-api.py <hostname> <servicename> :  classical request for mrpe command. It return results in NRPE format with all performance data if available.
  
  Donc forget, to :
  - enable arguments in nrpe.cfg
      cat /etc/nagios/nrpe.cfg | grep blame
      dont_blame_nrpe=1

   
  - declare command as: 
      cat /etc/nrpe.d/svg_monitoring.cfg
      # Monitoring to Icinga2 Core via API/REST:
      command[check_icinga2-api]=/usr/lib64/nagios/plugins/icinga2-api.py $ARG1$ $ARG2$

Examples:
LIST ALL:
---------
# /usr/lib64/nagios/plugins/icinga2-api.py ALL
server#@#ping4
server#@#ssh
server#@#Icinga
server#@#http
server#@#disk
...

for separate edit code for '#@#', if you want change it.

NRPE REQUEST:
-------------
# /usr/lib64/nagios/plugins/icinga2-api.py monitsvg.engsec load
API answer: load on :monitsvg.engsec OK : OK - Charge moyenne: 0.17, 0.13, 0.12 | load1=0.170;5.000;10.000;0; load5=0.130;4.000;6.000;0; load15=0.120;3.000;4.000;0;
# echo $?
0



