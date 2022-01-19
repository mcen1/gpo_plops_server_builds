#!/bin/env python3
import sys
import ast
from run import *

myfiles=ast.literal_eval(str(sys.argv[1]))
tocheck=[]
for item in myfiles:
  if item.startswith("server_vars/") and not item.startswith("server_vars/specs/"):
    tocheck.append(item) 

if len(tocheck)==0:
  print("Nothing to validate.")
  quit()

MYRC=0
for item in tocheck:
  print(f"Testing {item}...")
  MYRC=MYRC+runIACTests(True,item)

sys.exit(MYRC)

