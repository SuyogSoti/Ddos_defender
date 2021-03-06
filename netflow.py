#!/usr/bin/python3

import iptc
import subprocess
import re
import itertools
from time import sleep

def setup():
    INPUT = iptc.Chain(iptc.Table(iptc.Table.FILTER), 'INPUT')
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
    match.limit = '2/sec'
    limitRule.add_match(match)
    INPUT.insert_rule(limitRule)

    # iptables --append INPUT -s 127.0.0.1 --jump ACCEPT
    host3 = iptc.Rule()
    host3.src = '10.0.0.8'
    host3.target = iptc.Target(host3, 'ACCEPT')
    INPUT.insert_rule(host3)

    # iptables --append INPUT -s 127.0.0.1 --jump ACCEPT
    host4 = iptc.Rule()
    host4.src = '10.0.0.9'
    host4.target = iptc.Target(host4, 'ACCEPT')
    INPUT.insert_rule(host4)

    # iptables --append INPUT -s 127.0.0.1 --jump ACCEPT
    loRule = iptc.Rule()
    loRule.src = '127.0.0.1'
    loRule.target = iptc.Target(loRule, 'ACCEPT')
    INPUT.insert_rule(loRule)

    # iptables --append INPUT -s 10.0.0.5 --jump ACCEPT
    jumpRule = iptc.Rule()
    jumpRule.src = '10.0.0.5'
    jumpRule.target = iptc.Target(jumpRule, 'ACCEPT')
    INPUT.insert_rule(jumpRule)

def teardown():
    INPUT = iptc.Chain(iptc.Table(iptc.Table.FILTER), 'INPUT')
    INPUT.flush()

def readLog():
    dmesg = subprocess.check_output(['dmesg'])
    subprocess.check_output(['dmesg', '--clear'])
    return dmesg

def getCounts():
    aPackets = 0
    dPackets = 0
    table = iptc.Table(iptc.Table.FILTER)
    table.refresh()
    INPUT = iptc.Chain(table, 'INPUT')
    for rule in INPUT.rules:
        if rule.target.name == 'ACCEPT':
            packets, _ = rule.get_counters()
            aPackets += packets

        if rule.target.name == 'DROP':
            packets, _ = rule.get_counters()
            dPackets += packets

    # clear counts
    try:
        subprocess.check_output(['iptables', '-Z'])
    except Exception:
        pass

    return aPackets, dPackets

def processLogs(log):
    sources = {}
    def processLine(line):
        m = re.search('SRC=([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})', line)
        if m is not None:
            sourceIP = m.group(1)
            sources[sourceIP] = sources.get(sourceIP, 0) + 1

    for line in log.split(b'\n'):
        processLine(str(line))

    return sources

def save(times, requestData, droppedData, blocked):
    with open('vis.js') as inFile:
        data = inFile.read().split('\n')

    with open('vis.js', 'w') as outFile:
        time = 'var timeLabels = [%s]' % ','.join(times)
        requests = 'var requestData = [%s]' % ','.join(requestData)
        dropped = 'var droppedData = [%s]' % ','.join(droppedData)
        blocked = 'var commonlyBlocked = {%s}' % ','.join(['"%s": %s' % (k, v) for k, v in blocked.items()])

        out = '\n'.join(data[:4] + [time, requests, dropped, blocked] + data[8:])
        outFile.write(out)

def main():
    readLog()
    setup()
    times = []
    requestData = []
    droppedData = []
    blocked = {}
    for i in itertools.count():
        try:
            sleep(1)
            sources = processLogs(readLog())
            for source, count in sources.items():
                blocked[source] = blocked.get(source, 0) + count
            aPackets, dPackets = getCounts()

            times.append(str(i))
            requestData.append(str(aPackets))
            droppedData.append(str(dPackets))
            save(times, requestData, droppedData, blocked)
        except KeyboardInterrupt:
            break
    teardown()

if __name__ == '__main__':
    main()
