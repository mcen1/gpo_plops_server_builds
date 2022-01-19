#!/bin/env python3
import os.path
from os import path
import sys

def runFileTest(mypath):
  TESTNAME="FILE EXISTS CHECK"
  STATUS="SUCCESS"
  SUMMARY=""
  MYRC=0
  if not path.exists(mypath):
    STATUS="FAILED"
    SUMMARY=SUMMARY+mypath+" not found."
    MYRC=1
    # don't bother running other tests if our yaml doesn't exist
    print({"name":TESTNAME,"status":STATUS,"summary":SUMMARY,"rc":MYRC})
    sys.exit(1)
    quit()
  return {"name":TESTNAME,"status":STATUS,"summary":SUMMARY,"rc":MYRC}
