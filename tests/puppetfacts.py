#!/bin/env python3
def runPuppetFactTest(myvars):
  TESTNAME="PUPPETFACTS CHECK"
  STATUS="SUCCESS"
  SUMMARY=""
  MYRC=0
  if "custom_admin_localfacts" not in myvars['swvm']['puppetfacts']:
    STATUS="FAILED"
    SUMMARY=SUMMARY+" custom_admin_localfacts is missing in puppetfacts block."
    MYRC=1
  elif "custom_admin_localfacts=true" not in myvars['swvm']['puppetfacts']:
    STATUS="FAILED"
    SUMMARY=SUMMARY+" custom_admin_localfacts must be true. There is no reason to use the legacy corp Puppet fact deployment method."
    MYRC=1
  else:
    STATUS="SUCCESS"
    SUMMARY=""
  return {"name":TESTNAME,"status":STATUS,"summary":SUMMARY,"rc":MYRC}
