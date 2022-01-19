#!/bin/env python3
import sys
import requests
import datetime
from urllib import request, parse
import json

def runCheckOptimal(myvars):
  MYURL="https://provisionapi.company.com/best_cluster"
  TESTNAME="OPTIMAL PLACEMENT CHECK"
  STATUS="SUCCESS"
  SUMMARY=""
  MYRC=0
  clusternumber=0
  octets=myvars["swvm"]["foremansubnet"].split(".")
  subnet=f"{octets[0]}.{octets[1]}.{octets[2]}.0"
  data = {"datacenter_name":myvars["swvm"]["datacenter"],"os_type":"Linux","vm_subnet":subnet}
  data=json.dumps(data)
  data=str(data).encode('utf-8')
  try:
    response = requests.post(url=MYURL,  data=data)
    myresult=json.loads(response.text)
    if "best_cluster" in myresult:
      if myvars["swvm"]["cluster"]!=myresult["best_cluster"]:
        STATUS="WARNING"
        SUMMARY=SUMMARY+f" The cluster you picked ({ myvars['swvm']['cluster']}) is sub-optimal. It's recommended that you instead use \"{myresult['best_cluster']}\""
      if myvars["swvm"]["datastore"]!=myresult["best_datastore"]:
        if "vvol" in myresult["best_datastore"].lower() and "vvol" not in myvars["swvm"]["datastore"].lower():
          STATUS="FAILED"
          SUMMARY=f" VVOLs are available in this cluster. You must use them, but you picked {myvars['swvm']['datastore']}. VVOL name is: \"{myresult['best_datastore']}\""
          return {"name":TESTNAME,"status":STATUS,"summary":SUMMARY,"rc":MYRC}
        if "vvol" in myvars["swvm"]["datastore"].lower() and "vvol" not in myresult["best_datastore"].lower():
          ok=True
        else:
          STATUS="WARNING"
          SUMMARY=SUMMARY+f" The datastore you picked ({myvars['swvm']['datastore']}) is sub-optimal. It's recommended you use {myresult['best_datastore']}"
      url=f"https://provisionapi.company.com/allvmnetworks/{myvars['swvm']['cluster']}/{myvars['swvm']['foremansubnet']}"
      actualnetworks=json.loads(requests.get(url, verify=False).content)
      if myvars["swvm"]["network"] not in actualnetworks["networkmatches"]:
        if "Error: No results found that satisfy your request." in str(actualnetworks):
          actualnetworks="No similar networks found. Please check what you supplied for your foreman subnet, what you supplied for VMware, and check vCenter itself."
        STATUS="WARNING"
        SUMMARY=SUMMARY+f" The VMware network you picked ({myvars['swvm']['network']}) may be incorrect. You should instead use one of these networks: \"{actualnetworks}\""

  except Exception as e:
    print("Exception in runCheckOptimal: "+str(e))

  return {"name":TESTNAME,"status":STATUS,"summary":SUMMARY,"rc":MYRC}

