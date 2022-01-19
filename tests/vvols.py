#!/bin/env python3
def runVVOLTest(myvars):
  TESTNAME="VVOL CHECK"
  STATUS="SUCCESS"
  SUMMARY=""
  MYRC=0
  if ("vcenter1" in myvars['swvm']['vcenter'].lower() or "vcenter2" in myvars['swvm']['vcenter'].lower()) and "lnx" in myvars['swvm']['cluster'].lower() and "vvol" not in myvars['swvm']['datastore'].lower():
    STATUS="FAILED"
    SUMMARY=SUMMARY+" VMs in this cluster must be on a vVol."
    MYRC=1
    return {"name":TESTNAME,"status":STATUS,"summary":SUMMARY,"rc":MYRC}
  else:
    STATUS=f"NOT APPLICABLE for {myvars['swvm']['vcenter']} cluster {myvars['swvm']['cluster']} with {myvars['swvm']['datastore']}"
    SUMMARY=""
  if ("vcenter1" in myvars['swvm']['vcenter'].lower() or "vcenter2" in myvars['swvm']['vcenter'].lower()) and "lnx" in myvars['swvm']['cluster'].lower() and "vvol" in myvars['swvm']['datastore'].lower():
    return {"name":TESTNAME,"status":"SUCCESS","summary":SUMMARY,"rc":MYRC}
  if "vvol" in myvars['swvm']['datastore'].lower():
    return {"name":TESTNAME,"status":"SUCCESS","summary":SUMMARY,"rc":MYRC}

  return {"name":TESTNAME,"status":STATUS,"summary":SUMMARY,"rc":MYRC}
