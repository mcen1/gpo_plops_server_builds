#!/bin/env python3
import os
import socket
def runPingTest(myvars):
  TESTNAME="PINGCHECK CHECK"
  STATUS="SUCCESS"
  SUMMARY=""
  MYRC=0
  autogen=False
  teardown=False
  if myvars['swvm']["ip"]=="autogen":
    autogen=True
  try:
    if myvars['swvm']['teardown']=="yes" or str(myvars['swvm']['teardown']).lower()=="true":
      teardown=True
  except:
    pass
  if teardown:
    return {"name":TESTNAME,"status":"NOT APPLICABLE","summary":"Skipped due to teardown","rc":MYRC}
  if not autogen:
    response = os.system("ping -W 3 -c 1 " + myvars['swvm']["ip"]+" > /dev/null 2>&1")
    if response == 0:
      STATUS="FAILED"
      SUMMARY=SUMMARY+" "+str(myvars['swvm']["ip"])+" is responding to pings."
      MYRC=1
  response = os.system("ping -W 3 -c 1 " + str(myvars['swvm']["name"]+"."+myvars['swvm']["domain"]) +" > /dev/null 2>&1")
  if response == 0:
    STATUS="FAILED"
    SUMMARY=SUMMARY+" "+str(myvars['swvm']["name"]+"."+myvars['swvm']["domain"])+" is responding to pings."
    MYRC=1
  try:
    if not autogen:
      socket.gethostbyname(myvars['swvm']["name"]+"."+myvars['swvm']["domain"])
  except:
    STATUS="FAILED"
    SUMMARY=SUMMARY+" "+str(myvars['swvm']["name"]+"."+myvars['swvm']["domain"])+" is not in DNS."
    MYRC=1
  return {"name":TESTNAME,"status":STATUS,"summary":SUMMARY,"rc":MYRC}
