#!/usr/bin/env python

#
#    AUTHOR: Victor CORREIA
#    https://github.com/victorc32
#

import requests, json, sys
import os


def list_all_services():

    bashCommand = "curl -k -s -u admin:admin --header 'Accept: application/json' 'https://127.0.0.1:5665/v1/objects/services'  | python -m json.tool | grep \"__name\" | awk '{print $2}' | sed  's/\"//g' | sed 's/,//g' | sed 's/!/#@#/g'"
    response=os.system(bashCommand)
    print response
    sys.exit(0)


def check_service(hostname,servicename):
    # Replace 'localhost' with your FQDN and certificate CN
    # for SSL verification

    # for delete warnings
    from requests.packages.urllib3.exceptions import InsecureRequestWarning
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

    request_url = "https://127.0.0.1:5665/v1/objects/services"
    headers = {
        'Accept': 'application/json',
        'X-HTTP-Method-Override': 'GET'
    }
    data = {
        "attrs": ["name", "state", "last_check_result"],
        "joins": ["host.name", "host.state", "host.last_check_result"],
        "filter": "match(\"*" + servicename + "\", service.name) && match(\"*" + hostname + "\", host.name)",
        "type": "Service"
    }

    r = requests.post(request_url,
                      headers=headers,
                      auth=('admin', 'admin'),
                      data=json.dumps(data),
                      # verify="pki/icinga2-ca.crt")
                      verify=False)

    # print "Request URL: " + str(r.url)

    # print "Status code: " + str(r.status_code)
    # print "\n\n\n"

    if (r.status_code == 200):
        # print "Result: " + json.dumps(r.json(), indent=4, sort_keys=True)

        data = json.dumps(r.json())
        d = json.loads(data)
        # print d

        # print "longeur reponse d : "+str(len(d["results"]))

        # if request have a response so len > 0
        if len(d["results"]) > 0:
            # print(d["results"])
            # print "Status: ",d["results"][0]["attrs"]["last_check_result"]["exit_status"]
            status = int(d["results"][0]["attrs"]["state"])
            # force to integer
            # print "Monitoring Status: ",status
            # print "Service Name: ", d["results"][0]["name"].split('!')[1]
            servicename = d["results"][0]["name"].split('!')[1]

            # print "Host Name: ", d["results"][0]["name"].split('!')[0]
            hostname = d["results"][0]["name"].split('!')[0]

            # check if performance data is present, so loop for format nrpe output
            if len(d["results"][0]["attrs"]["last_check_result"]["performance_data"]) > 0:
                # print "Perfdata number: ", str(len(d["results"][0]["attrs"]["last_check_result"]["performance_data"]))

                output = d["results"][0]["attrs"]["last_check_result"]["output"] + " | "

                for element in d["results"][0]["attrs"]["last_check_result"]["performance_data"]:
                    output = output + str(element) + " "

            else:
                output = d["results"][0]["attrs"]["last_check_result"]["output"]
         # if len equal 0 , bad service request, error on host or services associed.
        if len(d["results"]) == 0:
            status=3
            output= "Error formating request or unknown service"

        # NRPE Formating msg
        #check_ping -H 127.0.0.1 -w 10%,12% -c 20%,23%  -4
        #PING OK -  Paquets perdus = 0%, RTA = 0.04 ms|rta=0.039000ms;10.000000;20.000000;0.000000 pl=0%;10;20;0

        # return NRPE message
        if status == 0:
            print "API answer: "+servicename +" on :" +hostname +" OK : " +output
            sys.exit(0)

        if status == 1:
            print "API answer: "+servicename +" on :" +hostname +" Warning: " +output
            sys.exit(1)

        if status == 2:
            print "API answer: "+servicename +" on :" +hostname +" CRITICAL: " +output
            sys.exit(2)

        if status == 3:
            print "API answer: "+servicename +" on :" +hostname +" Unknown: " +output
            sys.exit(3)

# INIT

if len(sys.argv) < 3 and sys.argv[1] != "ALL":
    print "Please verify syntax"
    print " <icinga2api.py  ALL : for list all services for all device>"
    print " <icinga2api.py  <hostname> <servicename> : for return results in NRPE format"
elif sys.argv[1] == "ALL":
    list_all_services()
else:
    hostname=sys.argv[1]
    servicename=sys.argv[2]
    check_service(hostname, servicename)

