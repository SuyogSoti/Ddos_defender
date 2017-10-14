#!/usr/bin/python3

import iptc
import subprocess
from time import sleep

INPUT = iptc.Chain(iptc.Table(iptc.Table.FILTER), "INPUT")

def setupLogging():
    rule = iptc.Rule()
    rule.target = iptc.Target(rule, 'LOG')
    INPUT.insert_rule(rule)
    return INPUT.rules[-1]

def teardownLogging(loggingRule):
    INPUT.delete_rule(loggingRule)

def readLog():
    mesg = subprocess.check_output(["dmesg"])
    subprocess.check_output(["dmesg", "--clear"])
    return mesg

def main():
    readLog()
    loggingRule = setupLogging()
    while True:
        try:
            sleep(1)
            print(readLog())
        except KeyboardInterrupt:
            break
    teardownLogging(loggingRule)

if __name__ == '__main__':
    main()
