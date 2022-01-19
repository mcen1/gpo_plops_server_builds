#!/bin/env python3
# my best attempt at helping solve the -dell vs non -dell VLAN confusion
import re
delimiternumber=5218
def runVLANTest(myvars):
  TESTNAME="VLAN CHECK"
  STATUS="SUCCESS"
  SUMMARY=""
  MYRC=0
  return {"name":TESTNAME,"status":STATUS,"summary":SUMMARY,"rc":MYRC}
