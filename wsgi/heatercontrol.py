#!/usr/bin/python

import json
import bghive
import threading
import time
from scapy.all import *

class HeaterController(threading.Thread):
    def __init__(self, node, checkInterval, onIntervals):
        super(HeaterController, self).__init__()
        self.daemon = True
        with open("/etc/bghive.cfg") as f:
            cfg = json.load(f)
        self.__username = cfg['username']
        self.__password = cfg['password']
        self.__buttonmac = cfg['buttonmac']
        self.__state = False
        self.__onCount = 0
        self.__onIntervals = onIntervals
        self.__checkInterval = checkInterval
        self.__node = node
        self.__button = ButtonWatcher(self, self.__buttonmac)

    def run(self):
        self.__button.start()
        while True:
            try:
                self.check()
            except Exception, e:
                print "Warning: check failed: %s" % str(e)

            time.sleep(self.__checkInterval)

    def check(self):
        session = bghive.Session(self.__username, self.__password)
        node = session.get_node(self.__node)
        curState = True if node.get_attribute("state")['reportedValue'] == "ON" else False
        if curState:
            if not self.__state:
                self.__onCount = 0
            else:
                self.__onCount += 1
            
            if self.__onCount > self.__onIntervals:
                print "Turning off heater"
                node.set_attribute("state", "OFF")

        self.__state = curState

        print "state=%s, onCount=%s" % (self.__state, self.__onCount)

    def button(self):
        print "Heater button pressed"
        session = bghive.Session(self.__username, self.__password)
        node = session.get_node(self.__node)
        node.set_attribute("state", "ON")
        self.__onCount = 0

class ButtonWatcher(threading.Thread):
    def __init__(self, heater, mac):
        super(ButtonWatcher, self).__init__()
        self.daemon = True
        self.__heater = heater
        self.__mac = mac.lower()

    def run(self):
        def arp_action(pkt):
            if pkt[ARP].op == 1 and pkt[ARP].hwsrc.lower() == self.__mac:
                try:
                    self.__heater.button()
                except Exception, e:
                    print "Warning, button action failed: %s" % str(e)

        while True:
            sniff(prn=arp_action, filter="arp", store=0, count=10)

def start():
    controller = HeaterController("Conservatory", 300, 24)
    controller.start()

if __name__ == "__main__":
    controller = HeaterController("Conservatory", 3, 10)
    controller.run()
