#!/bin/env python3
import requests
import json
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

def runForemanSubnetTest(myvars):
  TESTNAME="FOREMAN SUBNET CHECK"
  STATUS="SUCCESS"
  SUMMARY=""
  MYRC=0
  if 'ip' not in myvars['swvm']:
    return {"name":TESTNAME,"status":"FAILED.","summary":"IP address is missing in yaml.","rc":MYRC}
  if myvars['swvm']['ip']=="autogen":
    return {"name":TESTNAME,"status":"NOT APPLICABLE.","summary":"Skipped due to autogen.","rc":MYRC}
  ipnet=myvars['swvm']['ip'].split(".")
  foremannet=myvars['swvm']['foremansubnet'].split(".")
  if ipnet[0]+"."+ipnet[1]+"."+ipnet[2]+".0" != foremannet[0]+"."+foremannet[1]+"."+foremannet[2]+".0":
    STATUS="FAILED"
    SUMMARY=SUMMARY+"IP address's first 3 octets don't match foremansubnet's first 3 octets."
    MYRC=1
  url=f"https://provisionapi.company.com/foremannets/{myvars['swvm']['foremansubnet']}"
  foremannetworks=json.loads(requests.get(url, verify=False).content)
  if "true" not in str(foremannetworks['inforeman']).lower():
    STATUS="FAILED"
    SUMMARY=SUMMARY+f"Foreman subnet as written {myvars['swvm']['foremansubnet']} is not in Foreman. Please create it."
    MYRC=1
  return {"name":TESTNAME,"status":STATUS,"summary":SUMMARY,"rc":MYRC}
