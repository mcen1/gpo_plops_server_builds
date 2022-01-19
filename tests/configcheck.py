#!/bin/env python3
def nullOrEmpty(variableset,mykey):
  try:
    if len(str(variableset[mykey]))<2:
      return True
  except Exception as e:
    print("FAILED: Empty or null key: "+str(e))
    return True
  return False

validdomains=["company.com","subdomain.company.com"]


def runConfigTest(myvars):
  TESTNAME="CONFIG BASICS CHECK"
  STATUS="SUCCESS"
  SUMMARY=""
  MYRC=0
  checkitems=['guestid','architecture','foremanpxe','puppetfacts','pupconfigfile','foremanptable','foremansubnet','foremanos','datastore','network','folder','cluster','datacenter','vcenter','ip','domain','name','applicationsolution','requester','builder']
  for item in checkitems:
    if nullOrEmpty(myvars['swvm'],str(item)):
      STATUS="FAILED"
      SUMMARY=SUMMARY+" variable '"+item+"' is missing or empty in the swvm hierarchy in the YAML file."
      MYRC=MYRC+1
  toplevelitems=['vmspec','zabtemplate','zabhostgroups','latencyspec','vmdeploymentplan','foremanmedia','swvmconfigversion','usremotesite']
  for item in toplevelitems:
    if nullOrEmpty(myvars,str(item)):
      STATUS="FAILED"
      SUMMARY=SUMMARY+" variable '"+item+"' is missing or empty in YAML config file."
      MYRC=MYRC+1
  if "swvm" in myvars:
    if "osdisk" in myvars["swvm"]:
      if type(myvars["swvm"]["osdisk"]) != int:
        STATUS="FAILED"
        SUMMARY=SUMMARY+f" 'osdisk' variable '{myvars['swvm']['osdisk']}' is not valid. It must be an integer and not {type(myvars['swvm']['osdisk'])}"
        MYRC=MYRC+1
    if "domain" in myvars["swvm"]:
      if myvars["swvm"]["domain"] not in validdomains:
        STATUS="FAILED"
        SUMMARY=SUMMARY+" domain "+myvars["swvm"]["domain"]+" is not valid. Valid domains: "+str(validdomains)
        MYRC=MYRC+1

  return {"name":TESTNAME,"status":STATUS,"summary":SUMMARY,"rc":MYRC}
