import os
import sys
import subprocess

x = input("Select an option: \n1. Start crawling from last checkpoint\n2. Scrap the new batch\n")
if x == '1':
    subprocess.call(['python3', 'spiderdb.py'])
elif x == '2':
    subprocess.call(['python3', 'maindb.py'])
else:
    print("Invalid option")
    sys.exit(1)