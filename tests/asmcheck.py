#!/bin/env python3

def runASMTests(myvars):
  TESTNAME="ASM CHECK"
  STATUS="SUCCESS"
  SUMMARY=""
  MYRC=0
  controllernumbers={"0":[],"1":[],"2":[],"3":[]}
  if "oracle_asm_disks" not in myvars['swvm']:
    return {"name":TESTNAME,"status":STATUS,"summary":SUMMARY,"rc":MYRC}
  for item in myvars['swvm']['oracle_asm_disks']:
    if "path" in item:
      continue
    if int(item["scsi_controller"])<0 or int(item["scsi_controller"])>=4:
      STATUS="FAILED"
      SUMMARY=SUMMARY+" A SCSI controller numbered "+str(item["scsi_controller"])+" is not valid. Must be 0,1, or 3."
      MYRC=MYRC+1
    if int(item["unit_number"])==7 or int(item["unit_number"])>15:
      STATUS="FAILED"
      SUMMARY=SUMMARY+" A unit_number numbered "+str(item["unit_number"])+" is not valid. Cannot be 7 or greater than 15."
      MYRC=MYRC+1
    try:
      if str(item["unit_number"]) in controllernumbers[str(item["scsi_controller"])]:
        STATUS="FAILED"
        SUMMARY=SUMMARY+" A duplicate unit_number "+str(item["unit_number"])+" exists for SCSI controller "+str(item["scsi_controller"])+"."
        MYRC=MYRC+1
      controllernumbers[str(item["scsi_controller"])].append(str(item["unit_number"]))
    except:
      pass

  return {"name":TESTNAME,"status":STATUS,"summary":SUMMARY,"rc":MYRC}
