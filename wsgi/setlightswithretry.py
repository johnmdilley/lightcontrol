#!/usr/bin/python

import json
import time
import argparse
import bghive
import threading

class LightSetter(object):
    def __init__(self, node, attributes, timeout):
        with open("/etc/bghive.cfg") as f:
            cfg = json.load(f)
        self.__username = cfg['username']
        self.__password = cfg['password']
        self.__node = node
        self.__attributes = attributes
        self.__timeout = timeout
        self.__session = bghive.Session(self.__username, self.__password)

    def printNodes(self):
        for i in self.__session.nodes.keys():
            print "%s (%s)" % (i, repr(i))

    def __attempt(self):
        node = self.__session.get_node(self.__node)
        for a in self.__attributes:
            print "Attempting to set %s=%s on %s" % (a, self.__attributes[a], self.__node)
            node.set_attribute(a, self.__attributes[a])
    
    def run(self):
        timeout = time.time() + self.__timeout

        while True:
            try:
                self.__attempt()
            except Exception, e:
                print "Warning: Exception %s" % str(e)
            else:
                break

            if time.time() > timeout:
                raise Exception("Timed out")
            time.sleep(60)

    def printAttributes(self):
        node = self.__session.get_node(self.__node)
        print json.dumps(node.attributes, indent=2)

class ThreadedLightSetter(threading.Thread):
    def __init__(self, *args, **kwargs):
        super(ThreadedLightSetter, self).__init__()
        self.setter = LightSetter(*args, **kwargs)

    def run(self):
        self.setter.run()



if __name__ == "__main__":
    parser = argparse.ArgumentParser("Set attributes of a hive device")
    parser.add_argument("-t", "--timeout", type=int, default=3600, help="Timeout")
    parser.add_argument("-n", "--node", type=str, help="Node")
    parser.add_argument("-d", "--dump", action="store_true", help="Dump current attributes")
    parser.add_argument("attributes", nargs='*')
    args = parser.parse_args()
    attributes = dict([x.split("=") for x in args.attributes])
    setter = LightSetter(args.node, attributes, args.timeout)
    if not args.node:
        setter.printNodes()
    elif args.dump:
        setter.printAttributes()
    else:
        setter.run()
