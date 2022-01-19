#!/bin/env python3
def runRemoteSiteTest(myvars):
  TESTNAME="REMOTE SITE CHECK"
  STATUS="SUCCESS"
  SUMMARY=""
  MYRC=0
  if 'usremotesite' in myvars:
    if myvars['usremotesite'] and "vcenter1" not in myvars['swvm']['vcenter']:
      STATUS="FAILED"
      SUMMARY=SUMMARY+"usremotesite is true, but vCenter isn't vcenter1."
      MYRC=1
  return {"name":TESTNAME,"status":STATUS,"summary":SUMMARY,"rc":MYRC}
