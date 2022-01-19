import sys

def runZabbixSanity(myvars,filepath):
    TESTNAME = "ZABBIX SANITY"
    STATUS = "SUCCESS"
    SUMMARY = ""
    MYRC=0
    if 'production' in str(myvars['swvm']['pupconfigfile']).lower() and "PROD - High" not in str(myvars['zabhostgroups']):
        STATUS = "WARNING"
        SUMMARY = SUMMARY+" Server has production in its pupconfigfile variable, but does not belong to a production Zabbix host group. I hope this is expected for your purposes. "
        MYRC=0
    return {"name":TESTNAME,"status":STATUS,"summary":SUMMARY,"rc":MYRC}
