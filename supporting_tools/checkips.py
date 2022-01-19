#!/bin/env python3
import os
import socket
import sys

argsan=sys.argv[1]

argsan=argsan.replace('[','').replace(']','').replace("'",'')

#print("argsan is: "+argsan)

def checkPing(ipaddress):
  response = os.system("ping -w 3 -c 1 " + ipaddress+" > /dev/null 2>&1")
  if response == 0:
    return True
  return False

def checkDNS(ipaddress):
  myresult=False
  try:
    myresult=socket.gethostbyaddr(ipaddress)
    return True
  except Exception as e:
    if "Unknown host" in str(e):
      return False
  return myresult


for argumenta in argsan.split(","):
  argumenta=argumenta.replace(" ","")
  ispinging=checkPing(argumenta)
  isindns=checkDNS(argumenta)
  if not ispinging and not isindns:
    print(str(argumenta))
    quit()

print("Every IP given either pings or is in DNS. Error!")
sys.exit(66)

