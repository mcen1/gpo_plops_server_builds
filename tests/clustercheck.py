#!/bin/env python3
import sys
import requests
import datetime
import urllib.request, json
from urllib.parse import quote

def runClusterTest(myvars):
  TESTNAME="CLUSTER CHECK"
  STATUS="SUCCESS"
  SUMMARY=""
  MYRC=0
  clusternumber=0
  if "vcenter1" not in myvars["swvm"]["vcenter"].lower() and "vcenter2" not in myvars["swvm"]["vcenter"].lower():
    return {"name":TESTNAME,"status":"NOT APPLICABLE","summary":"","rc":MYRC}
  try:
    with urllib.request.urlopen('https://provisionapi..company.com/cluster_number/'+quote(str(myvars['swvm']["cluster"]))) as url:
      clusternumbers=json.loads(url.read().decode())
    if "ERROR" in str(clusternumbers):
      return {"name":TESTNAME,"status":f"WARNING","summary": f"Error in clusternumber API call: {clusternumbers}. Check vCenter if your cluster {str(myvars['swvm']['cluster'])} still exists.","rc":MYRC}
    clusternumber=float(clusternumbers["provisioning_number"])

  except Exception as e:
    print('Cluster Test Request Response Failed: '+str(e))
    return {"name":TESTNAME,"status":"SKIPPED","summary":"Exception generated: "+str(e),"rc":MYRC}

  if clusternumber>=4:
    STATUS="FAILED"
    SUMMARY=SUMMARY+str(myvars['swvm']['cluster'])+" is over-provisioned. Cluster number is above 4: "+str(clusternumber)
    MYRC=1
  if "LnxRW2 (E5-2690 v3)" in myvars['swvm']['cluster']:
    STATUS="FAILED"
    SUMMARY=SUMMARY+" LnxRW2 (E5-2690 v3) is no longer available for provisioning."
    MYRC=1
  else:
    STATUS="SUCCESS"
    SUMMARY=""
  return {"name":TESTNAME,"status":STATUS,"summary":SUMMARY,"rc":MYRC}
