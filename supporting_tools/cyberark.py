#!/bin/env python3
import http.client
import json
import sys
import time
import os
CAURL='cyberark.company.com'
CCPURL='ccp.company.com'
CERT_FILE = os.environ['CYBERARK_CERT']
PKEY_FILE = os.environ['CYBERARK_PKEY']


def onboardSA(servername,servertype,mypass,myuser):
  if "gsc" in servertype:
    mysafe='SW-Lin-Svr-Root-Consumer'
    myvault='SWLinServerRoot'
  else:
    mysafe='SW-Lin-Svr-Root-Corp'
    myvault='SWLinServerRoot'
  #session cred is in this safe not our other potential consumer safe
  mysession=getCACred('SW-Lin-Svr-Root-Corp')
  if len(mysession)>0:
    print((mysession+" "+mysafe+" "+myvault+" "+servername+" "+myuser+" "+mypass))
    myid=addAccount(mysession,mysafe,myvault,servername,myuser,mypass)
  else:
    print("error acquiring session")
  #print str(myid)

# idea is gcd_dev for servertype
def onboard(servername,servertype,mypass):
  if "gsc" in servertype.lower():
    mysafe='SW-Lin-Svr-Root-Consumer'
    myvault='SWLinServerRoot'
  else:
    mysafe='SW-Lin-Svr-Root-Corp'
    myvault='SWLinServerRoot'
  #session cred is in this safe not our other potential consumer safe
  mysession=getCACred('SW-Lin-Svr-Root-Corp')
  myuser="root"
  myid=addAccount(mysession,mysafe,myvault,servername,'root',mypass)
  if "_" in str(myid):
    import time
    time.sleep(5)
    changeAccount(mysession,myid)
  caLogoff(mysession)

def caLogoff(session):
  SUBURL='/PasswordVault/api/auth/CyberArk/Logon'
  headers={"Authorization": session.replace('"',''), "Content-Type": "application/json"}
  params={}
  conn2 = http.client.HTTPSConnection(CAURL,
           key_file = PKEY_FILE, cert_file = CERT_FILE )
  conn2.request('POST', SUBURL,json.dumps(params),headers)


def getCACred(mysafe):
  APPID='GCD-Unix-Onboard'
  OBJ='SWCyberArkVaultAIM_10.140.15.51_REST_GCD-Unix-Onboard'
  SUBURL="/AIMWebService/api/Accounts?AppID="+APPID+"&Safe="+mysafe+"&Object="+OBJ+""
  conn = http.client.HTTPSConnection(CCPURL,
           key_file = PKEY_FILE, cert_file = CERT_FILE )
  conn.putrequest('GET', SUBURL)
  conn.endheaders()
  response = conn.getresponse()
  myjson=json.loads(response.read())
  SUBURL='/PasswordVault/api/auth/CyberArk/Logon'
  #return {'username':myjson['UserName'].replace('"',''),'password':myjson['Content'].replace('"','')}
  myuser=json.dumps(myjson['UserName'])
  mypass=json.dumps(myjson['Content'])
  params ={"username": myuser.replace('"',''),"password": mypass.replace('"','')}
  headers = {"Content-Type": "application/json",
             "Accept": "application/json"}
  conn2 = http.client.HTTPSConnection(CAURL,
           key_file = PKEY_FILE, cert_file = CERT_FILE )
  conn2.request('POST', SUBURL,json.dumps(params),headers)
  response = conn2.getresponse()
  #print response.status, response.reason
  if response.status!=200:
    raise Exception("ERROR acquiring cyberark initial API credentials: "+str(response.status))
  return str(response.read().decode())

def addRancherAccount(session,safe,platform,hostname,username,password):
  # use v9 api. https://docs.cyberark.com/Product-Doc/OnlineHelp/PAS/Latest/en/Content/WebServices/Add%20Account.htm
  # note the json changes for params. the json is encompassed by {"account":{}}
  ObjectName=safe+'_'+hostname+'_'+username
  SUBURL='/PasswordVault/api/Accounts'
  SUBURL='/PasswordVault/WebServices/PIMServices.svc/Account'
  headers={"Authorization": session.replace('"',''), "Content-Type": "application/json"}
  params ={"account":{"address": hostname,"username": username,"platformID": platform,"safe": safe,"password": password, "properties": [{"Key":"ExtraPass1Name", "Value":"SWSSHKey_cpranchn01_rancheruseme"},{"Key":"ExtraPass1Folder", "Value":"Root"},{"Key":"ExtraPass1Safe", "Value":"SW-Lin-Svr-Root-Corp"}]}}
  #params ={"name": ObjectName,"address": hostname,"userName": username,"platformId": platform,"safeName": safe,"secretType": "password","secret": password, "platformAccountProperties": {"ExtraPass1Name":"SWSSHKey_cpranchn01_rancheruseme","ExtraPass1Folder":"Root","ExtraPass1Safe":"SW-Lin-Svr-Root-Corp"},"properties": [{"Key":"ExtraPass1Name", "Value":"SWSSHKey_cpranchn01_rancheruseme"},{"Key":"ExtraPass1Folder", "Value":"Root"},{"Key":"ExtraPass1Safe", "Value":"SW-Lin-Svr-Root-Corp"}], "secretManagement": {"automaticManagementEnabled": "true"}}
  conn2 = http.client.HTTPSConnection(CAURL,
           key_file = PKEY_FILE, cert_file = CERT_FILE )
  conn2.request('POST', SUBURL,json.dumps(params),headers)
  response = conn2.getresponse()
  if int(response.status)==201:
    myjson=str(response.read())
    return myjson
    print((str(response.status)))
  else:
    print((response.read()))
    caLogoff(session)
    raise Exception(response.status)

def addAccount(session,safe,platform,hostname,username,password):
  ObjectName=safe+'_'+hostname+'_'+username
  SUBURL='/PasswordVault/api/Accounts'
  headers={"Authorization": session.replace('"',''), "Content-Type": "application/json"}
  params ={"name": ObjectName,"address": hostname,"userName": username,"platformId": platform,"safeName": safe,"secretType": "password","secret": password,"platformAccountProperties": {},"secretManagement": {"automaticManagementEnabled": "true"}}
  conn2 = http.client.HTTPSConnection(CAURL,
           key_file = PKEY_FILE, cert_file = CERT_FILE )
  conn2.request('POST', SUBURL,json.dumps(params),headers)
  response = conn2.getresponse()
  if int(response.status)==201:
    myjson=json.loads(response.read())
    return myjson["id"]
  else:
    raise Exception(response.read())
    caLogoff(mysession)
def getPassword(session,id):
  myresp=""
  headers={"Authorization": session.replace('"',''), "Content-Type": "application/json"}
  SUBURL="/PasswordVault/API/Accounts/"+str(id)+"/Password/Retrieve"
  conn2 = http.client.HTTPSConnection(CAURL,
           key_file = PKEY_FILE, cert_file = CERT_FILE )
  conn2.request('POST', SUBURL,json.dumps({}),headers)
  response = conn2.getresponse()
  if int(response.status) == 200:
    myresp=response.read()
    caLogoff(session)
    return myresp.replace('"','')
  else:
    caLogoff(session)
    print(("response.status"+str(response.status)))
    print(("response.read"+str(response.read())))
    raise Exception(response.status)
    caLogoff(mysession)

def listAllRoot(session):
  keepgoing=True
  tosay=""
  offset=0
  user="root"
  headers={"Authorization": session.replace('"',''), "Content-Type": "application/json"}
  SUBURL="/PasswordVault/API/Accounts?search="+str(user)
  params="{}"
  while keepgoing:
    conn2 = http.client.HTTPSConnection(CAURL,
             key_file = PKEY_FILE, cert_file = CERT_FILE )
    conn2.request('GET', SUBURL,json.dumps(params),headers)
    response = conn2.getresponse()
    #print response.status, response.reason
    myresp=json.loads(response.read())
    try:
      tosay=tosay+str(json.dumps(myresp['value']))
    except:
      ok=False
    try:
      SUBURL="/PasswordVault/"+myresp['nextLink']
      if not myresp['nextLink']:
        keepgoing=False
    except:
      keepgoing=False
  caLogoff(session)
  return tosay.replace('][',',')


def listSafe(session,safe,name,user):
  keepgoing=True
  tosay=""
  offset=0
  headers={"Authorization": session.replace('"',''), "Content-Type": "application/json"}
  SUBURL="/PasswordVault/API/Accounts?search="+str(user)+"%20"+str(name)+"&offset="+str(offset)
  params="{}"
  while keepgoing:
    conn2 = http.client.HTTPSConnection(CAURL,
             key_file = PKEY_FILE, cert_file = CERT_FILE )
    conn2.request('GET', SUBURL,json.dumps(params),headers)
    response = conn2.getresponse()
    #print response.status, response.reason
    myresp=json.loads(response.read())
    try:
      tosay=tosay+str(json.dumps(myresp['value']))
    except:
      ok=False
    try:
      SUBURL="/PasswordVault/"+myresp['nextLink']
      if not myresp['nextLink']:
        keepgoing=False
    except:
      keepgoing=False
  return tosay.replace('][',',')

def changeAccount(session,id):
  headers={"Authorization": session.replace('"',''), "Content-Type": "application/json"}
  params={"ChangeEntireGroup": "true"}
  SUBURL="/PasswordVault/API/Accounts/"+str(id)+"/Change"
  conn2 = http.client.HTTPSConnection(CAURL,
           key_file = PKEY_FILE, cert_file = CERT_FILE )
  conn2.request('POST', SUBURL,json.dumps(params),headers)
  response = conn2.getresponse()
  print((response.status))
  myresp=response.read()
  return response.status


#print getPassword(getCACred('SW-Lin-Svr-Root-Corp'),'79_1039')
#print getPassword(getCACred('SW-Lin-Svr-Root-Corp'),'79_1039')
#onboard('cposdts1','gcd_production','test')
#addAccount(getCACred('SW-Lin-Svr-Root-Corp'),'SW-Lin-Svr-Root-Corp','SWLinServerRoot','cposdts1demo','root','test')
#listAllRoot(getCACred('SW-Lin-Svr-Root-Corp'))
if str(sys.argv[1])=="add":
  print(addAccount(getCACred('SW-Lin-Svr-Root-Corp'),str(sys.argv[2]),'SWLinServerRoot',str(sys.argv[3]),'root',str(sys.argv[4])))
if str(sys.argv[1])=="change":
  time.sleep(600)
  print(changeAccount(getCACred('SW-Lin-Svr-Root-Corp'),str(sys.argv[2])))
