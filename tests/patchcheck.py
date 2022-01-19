#!/bin/env python3
import sys
import requests
import datetime
import urllib.request, json 

with urllib.request.urlopen("https://provisionapi.company.com/overloaded_patch_windows") as url:
  overloaded = json.loads(url.read().decode())

def isRemoteUS(myvars):
  if "vcenter1" in  myvars["swvm"]["vcenter"].lower() and (str(myvars["usremotesite"]).lower()=="true" or str(myvars["usremotesite"]).lower()=="true"):
    return True
  return False

def isRemotevCenter(myvars):
  if "vcenter1" not in myvars["swvm"]["vcenter"].lower() and "vcenter2" not in myvars["swvm"]["vcenter"].lower():
    return True
  return False

# Whether or not we care about this site being scheduled via this IaC workflow
def iCareDeeply(myvars):
  if "vcenter2" in myvars["swvm"]["vcenter"].lower():
    return True
  ingredient1=isRemoteUS(myvars)
  if ingredient1:
    return False
  ingredient2=isRemotevCenter(myvars)
  if ingredient2:
    return False
  return True

def runpatchcheck(myvars):
    TESTNAME = "POST DEPLOYMENT PATCH CHECK"
    STATUS = "SUCCESS"
    SUMMARY = ""
    MYRC=0
    gooby_pls = ["monday","tuesday","wednesday","thursday","friday","saturday","sunday"]
    time_fmt = "%H:%M"
    icaredeeply=iCareDeeply(myvars)
    if "cplnxtest" in myvars["swvm"]["name"]:
      return {"name":TESTNAME,"status":"NOT APPLICABLE","summary":"CPLNXTEST servers are exempt from this. Please, for the love of god, don't abuse this.","rc":MYRC}
    if  ("patchweekint" not in myvars or "patchday" not in myvars or "patchtime" not in myvars) and not icaredeeply:
      return {"name":TESTNAME,"status":"NOT APPLICABLE","summary":"REMOTE SITES AND VCENTERS ARE NOT SCHEDUABLE VIA THIS WORKFLOW","rc":MYRC}  
    # Verify server is not in a remote site. They should be added to existing site windows
    if ("patchweekint"  in myvars or "patchday"  in myvars or "patchtime"  in myvars) and not icaredeeply:
       STATUS = "FAILED"
       SUMMARY = SUMMARY+" This server cannot be scheduled for patching. For remote sites, please add them to the existing appropriate site patching window, and remove the patching variables in your config."
       MYRC=MYRC+1
       return {"name":TESTNAME,"status":STATUS,"summary":SUMMARY,"rc":MYRC}

    # If we see the server is not remote, lets make sure all variables are present.
    if ("patchweekint" not in myvars or "patchday" not in myvars or "patchtime" not in myvars):
        STATUS = "FAILED"
        SUMMARY = SUMMARY+"Since this server is not at a remote site, a patching event is required. Please make sure all patch variables are present. An example would be \n\n  patchweekint: \"1\"\n\n  patchday: \"Monday\"\n\n  patchtime: \"09:00\""
        MYRC=MYRC+1
        return {"name":TESTNAME,"status":STATUS,"summary":SUMMARY,"rc":MYRC}

    # Check our patch integral is an integer
    if not str(myvars["patchweekint"]).isdigit():
        STATUS = "FAILED"
        SUMMARY = SUMMARY+" Patch week integral '"+str(myvars["patchweekint"])+"' is not valid. A number to represent the number week is required between 1 and 5. An example would be: \n\n\tpatchweekint:\"1\" "
        MYRC=MYRC+1

    # Check weekday is valid
    if str(myvars["patchday"]).lower() not in gooby_pls:
        STATUS = "FAILED"
        SUMMARY = SUMMARY+" Patch week '"+str(myvars["patchday"])+"' is not valid. Please verify weekday for patching. An example would be: \n\n\tpatchday: \"Monday\""
        MYRC=MYRC+1

    # Check patch time is valid
    try:
        validtime = datetime.datetime.strptime(str(myvars["patchtime"]), time_fmt)
    except ValueError:
        STATUS = "FAILED"
        SUMMARY = SUMMARY+" patchtime: '"+str(myvars["patchtime"])+"' is incorrect, please use HOUR:MIN format for example, \n\n\tpatchtime: \"09:00\""
        MYRC=MYRC+1

    # formatting check for compatibility with overloaded window check
    try:
      if int(myvars["patchtime"].split(":")[0])<10 and not str(myvars["patchtime"]).startswith("0"):
        STATUS = "FAILED"
        SUMMARY = SUMMARY+" Patch time hours below 10 o'clock must start with 0, example: 09:00"
        MYRC=MYRC+1
    except Exception as e:
      print("Format check error: "+str(e))
      STATUS = "FAILED"
      SUMMARY = SUMMARY+" Patch time hour seems to not be an integer before :. "+str(e)
      MYRC=MYRC+1


    # overloaded window check
    windowconcat=str(myvars["patchweekint"])+" "+str(myvars["patchday"])+" "+str(myvars["patchtime"])
    if windowconcat in overloaded['overloaded_windows']:
      STATUS = "FAILED"
      SUMMARY = SUMMARY+" Patch window is overloaded. Please pick a different one. "
      MYRC=MYRC+1

    try:
        response = requests.get('https://calendar.company.com/ords/apex_ts/rcal/gethostevent/?host='+str(myvars['swvm']["name"]))
    except Exception as e:
        print('Patch check Request Response Failed: '+str(e))

    # Check this server isnt already scheduled (server being rebuilt)
    wowzers = len(response.json()['items'])
    if wowzers > 0:
        STATUS = "WARNING"
        SUMMARY = SUMMARY+" Patching event(s) for '"+str(myvars['swvm']["name"]+"."+myvars['swvm']["domain"])+"' already exist. This automation will not be adding new events if one already exists."


    return {"name":TESTNAME,"status":STATUS,"summary":SUMMARY,"rc":MYRC}
