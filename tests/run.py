#!/bin/env python3
# these tests are meant to test elements of the yaml variables
# for sanity/compliance. This suite is not meant to test
# more advanced systems that require username/passwords.
# That is meant more for the roles/preflightchecks
import sys
import yaml
from remotesite import *
from foremansubnet import *
from fileexists import *
from vvols import *
from vlans import *
from vmdks import *
from puppetfacts import *
from pingtest import *
from configcheck import *
from groupfailpage import *
from zabbixsanity import *
from clustercheck import *
from patchcheck import *
from autogencheck import *
from checkoptimal import *
from asmcheck import *

def runIACTests(fromgh,filepath):
  myresults=[]
  MYRC=0
  myresults.append(runFileTest(filepath))
  if not fromgh:
    from termcolor import colored
  else:
    def colored(tosay,color,attrs="none"):
      return tosay


  # should only have reached this point if file exists
  myyaml = open(filepath)
  try:
    myvars = yaml.load(myyaml, Loader=yaml.FullLoader)
  except Exception as e:
    print("Error parsing yaml file: "+str(e))
    sys.exit(55)
  configTestRes=runConfigTest(myvars)
  myresults.append(configTestRes)
  if "FAIL" in str(configTestRes):
    print(f"Missing or incorrect mandatory values in YAML file. Not running any subsequent tests until all requiremed variables are present and valid. Results: {configTestRes}")
    sys.exit(56)
  myresults.append(runRemoteSiteTest(myvars))
  myresults.append(runForemanSubnetTest(myvars))
  myresults.append(runAutogenTests(myvars))
  myresults.append(runVVOLTest(myvars))
  myresults.append(runVMDKTest(myvars))
  myresults.append(runASMTests(myvars))
  myresults.append(runPuppetFactTest(myvars))
  myresults.append(runClusterTest(myvars))
  myresults.append(runPingTest(myvars))
  myresults.append(runVLANTest(myvars))
  myresults.append(runfailgrouptest(myvars,filepath))
  myresults.append(runZabbixSanity(myvars,filepath))
  myresults.append(runCheckOptimal(myvars))
  myresults.append(runpatchcheck(myvars))

  # cycle through results and increment myrc if any test fails
  for result in myresults:
    color='blue'
    if result["status"]=="SUCCESS":
      color='green'
    if result["status"]=="FAILED":
      color='red'
    if result["status"]=="WARNING":
      color='yellow'
    if result["status"]!="SUCCESS" and result["status"]!="NOT APPLICABLE" :
      print(f""+result['name']+": "+colored(result["status"],color)+". "+colored(result["summary"],color))
    MYRC=MYRC+result['rc']
  print("\n")
  if MYRC!=0:
    print(colored('FAILED', 'red', attrs=[ 'blink']))
  else:
    print(colored('SUCCEEDED', 'green'))
  print("\n")
  return MYRC

if __name__ == "__main__":
  THERC=runIACTests(False,sys.argv[1])
  sys.exit(THERC)
