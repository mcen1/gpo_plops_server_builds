import sys

def runfailgrouptest(myvars,filepath):
    TESTNAME = "POST DEPLOYMENT ROLE CHECK"
    STATUS = "SUCCESS"
    SUMMARY = ""
    MYRC=0
    folder = filepath.split("/")[1]
    badboys=['awcs','mes']
    if folder.lower() in badboys and 'production' in str(myvars['swvm']['pupconfigfile']).lower() and 'vmdeploymentpost' not in myvars:
        STATUS = "FAILED"
        SUMMARY = SUMMARY+" Server type '"+folder+"' requires a vmdeploymentpost variable. For AWCS and MES, a valid variable might be: \n\n\tvmdeploymentpost: \"addpatchfailgroup\" "
        MYRC=MYRC+1
    return {"name":TESTNAME,"status":STATUS,"summary":SUMMARY,"rc":MYRC}
