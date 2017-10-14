#!/usr/bin/python3

import iptc
import subprocess
from time import sleep

INPUT = iptc.Chain(iptc.Table(iptc.Table.FILTER), "INPUT")

def setup():
    INPUT.flush()
    # iptables --append INPUT --jump DROP
    dropRule = iptc.Rule()
    dropRule.target = iptc.Target(dropRule, 'DROP')
    INPUT.insert_rule(dropRule)

    # iptables --append INPUT --jump LOG
    logRule = iptc.Rule()
    logRule.target = iptc.Target(logRule, 'LOG')
    INPUT.insert_rule(logRule)

    # iptables --append INPUT --match limit --limit 50/sec --jump ACCEPT
    limitRule = iptc.Rule()
    limitRule.target = iptc.Target(limitRule, 'ACCEPT')
    match = iptc.Match(limitRule, 'limit')
    match.limit = '10/sec'
    limitRule.add_match(match)
    INPUT.insert_rule(limitRule)

    # iptables --append INPUT -s 127.0.0.1 --jump ACCEPT
    loRule = iptc.Rule()
    loRule.src = "127.0.0.1"
    loRule.target = iptc.Target(loRule, 'ACCEPT')
    INPUT.insert_rule(loRule)

    # iptables --append INPUT -s 10.0.0.5 --jump ACCEPT
    jumpRule = iptc.Rule()
    jumpRule.src = "10.0.0.5"
    jumpRule.target = iptc.Target(jumpRule, 'ACCEPT')
    INPUT.insert_rule(jumpRule)

def teardown():
    INPUT.flush()

def readLog():
    mesg = subprocess.check_output(["dmesg"])
    subprocess.check_output(["dmesg", "--clear"])
    return mesg

def main():
    readLog()
    setup()
    while True:
        try:
            sleep(1)
            log = readLog()
            if log:
                print(log)
        except KeyboardInterrupt:
            break
    teardown()

if __name__ == '__main__':
    main()
