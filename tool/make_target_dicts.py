#!/usr/bin/python

import os
import glob
import sys

which = sys.argv[1]

for f in glob.glob("../target/%s/*"%(which)):
  fname = os.path.basename(f)
  job_dir = "/home/bbbig/capstone/work/%s/"%(which)+fname
  print job_dir
  dict_file = os.path.join(job_dir, fname+".dict")
  print "python3 create_dict.py %s > %s"%(f, dict_file)
  os.system("python3 create_dict.py %s > %s"%(f, dict_file))
