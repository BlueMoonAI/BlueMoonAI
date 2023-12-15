import os
import sys
import ssl
import bluemoonai_version

from updater import Updater

print('[System ARGV] ' + str(sys.argv))

root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(root)
os.chdir(root)

from app import *