import os
import subprocess

class Fuzzer(object):
  
  def __init__(self, binary_path, which):
    self.seeds = ["fuzz"]
    self.which = which
    self.binary_path = binary_path
    self.job_dir = os.path.join("/home/bbbig/capstone/work", which)
    
    if not os.path.exists(self.job_dir):
      try:
        os.mkdir(self.job_dir)
      except:
        print "mkdir %s failed"%(self.job_dir)

    self.job_dir = os.path.join(self.job_dir, os.path.basename(self.binary_path))

    if not os.path.exists(self.job_dir):
      try:
        os.mkdir(self.job_dir)
      except:
        print "mkdir %s failed"%(self.job_dir)

    self.in_dir = os.path.join(self.job_dir, "input")
    self.out_dir = os.path.join(self.job_dir, "out")
    self.resuming = bool(os.listdir(self.out_dir)) if os.path.isdir(self.out_dir) else False

    self.procs = []
    
    self.make_env()

    dict_file = os.path.join(self.job_dir, os.path.basename(binary_path)+".dict")
    if os.path.exists(dict_file):
      self.dict = dict_file
    else:
      self.dict = None

  def start_fuzzer(self):
    args = ["afl-fuzz"]

    args += ["-i", self.in_dir]
    args += ["-o", self.out_dir]
    args += ["-m", "none"]

    args += ["-M", "master"]

    if self.dict:
      args += ["-x", self.dict]
      print "using dict %s"%(self.dict)
    
    args += ["-Q"]    
    args += ["--"]
    args += [self.binary_path]

    outfile = 'fuzzer.log'
    outfile = os.path.join(self.job_dir, outfile)


    with open(outfile, "w") as fp:
      return subprocess.Popen(args, stdout=fp, close_fds = True)

  def start(self):
    master = self.start_fuzzer()
    self.procs.append(master)


  def make_env(self):

    if self.resuming:
      self.in_dir = "-"
    else:
      if not os.path.exists(self.in_dir):
        try:
          os.mkdir(self.in_dir)

          #make seed file
          open(os.path.join(self.in_dir, "seed"),"w").write("fuzz") 

        except:
          print "mkdir %s failed"%(self.in_dir)
      if not os.path.exists(self.out_dir):
        try:
          os.mkdir(self.out_dir)
        except:
          print "mkdir %s failed"%(self.out_dir)


  def kill(self):
    for proc in self.procs:
      proc.terminate()
      proc.wait()

  def get_crash_num(self):
    
    crash_dir = os.path.join(self.out_dir, "master")
    crash_dir = os.path.join(crash_dir, "crashes")
    return len(os.listdir(crash_dir))

