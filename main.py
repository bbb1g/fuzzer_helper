import fuzzer
import os
import time
import sys
import glob
import itertools

def usage():
  print "Usage : [me] TargetFolder"
  exit()

def gen_from_list(l):
  while True:
    for element in l:
      yield element

if __name__ == "__main__":

  target_dir = "/home/bbbig/capstone/target"
  sec = 30

  if len(sys.argv) < 2:
    usage()
  
  which = sys.argv[1]
  if not os.path.exists(os.path.join(target_dir, which)):
    usage()

  target = os.path.join(target_dir, which)
  target_bins = glob.glob(target + "/*")

  get_bin = gen_from_list(target_bins)

  while True:
    bin1 = get_bin.next()
    bin2 = get_bin.next()

    bin1_id = os.path.basename(bin1)
    bin2_id = os.path.basename(bin2)

    fuzzer1 = fuzzer.Fuzzer(bin1, which)
    fuzzer2 = fuzzer.Fuzzer(bin2, which)

    print "fuzzing %s..."%(bin1_id)
    fuzzer1.start()

    print "fuzzing %s..."%(bin2_id)
    fuzzer2.start()

    time.sleep(sec)
    
    bin1_crash_num = fuzzer1.get_crash_num()
    bin2_crash_num = fuzzer2.get_crash_num()

    print "%s Crash count : %d"%(bin1_id, bin1_crash_num)
    print "%s Crash count : %d"%(bin2_id, bin2_crash_num)

    fuzzer1.kill()
    fuzzer2.kill()
