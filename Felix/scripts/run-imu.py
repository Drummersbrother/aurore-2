import sys
import os

def log(message: str):
    os.system("~/scripts/log.sh \"%s\"" % message)


log("found file %s" % sys.argv[1])
