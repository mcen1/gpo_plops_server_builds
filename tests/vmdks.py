#!/bin/env python3
def runVMDKTest(myvars):
  TESTNAME="VMDK CHECK"
  STATUS="SUCCESS"
  SUMMARY=""
  MYRC=0
  if "vmdks" in myvars['swvm'] and len(myvars['swvm']['vmdks'])>3:
    STATUS="FAILED"
    SUMMARY=SUMMARY+" VMDKs must be 3 items or fewer (OS disk is defined seperately). Supplied: "+str(myvars['swvm']['vmdks'])
    MYRC=1

  return {"name":TESTNAME,"status":STATUS,"summary":SUMMARY,"rc":MYRC}
