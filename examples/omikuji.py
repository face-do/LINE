#!/usr/bin/env python2
# encoding: utf-8

# Echo LINE messages if sender is not you.

import getpass
from line import LineClient, LineGroup, LineContact
import threading
from code import interact
import random

unsei = ["大吉","中吉","吉","小吉","末吉","凶","大凶"]

class LINEbot(threading.Thread):
    def __init__(self, client):
        super(LINEbot, self).__init__()
        self.client = client
        self.life = 1
    def onOperation(self,op):
            sender   = op[0]
            #receiver = op[1]
            message  = op[2]
            if message is None:
                return
            msg = message.text
            print "%s: %s" % (sender.name, msg)
            if "おみくじ" in msg:
                sender.sendMessage("あなたの運勢は %s" % random.choice(unsei))
    def run(self):
        while self.life:
            op_list = []
            for op in self.client.longPoll():
                op_list.append(op)
            for op in op_list:
                self.onOperation(op)
    def stop(self):
        self.life = 0

if __name__ == "__main__":
    from os.path import expanduser
    home = expanduser("~")
    session_file = "%s/LINE.session" % home
    com_name = __file__
    session = None
    try:
        session = file(session_file,"r").read()
        print "Loaded AuthToken: %s" % session
    except IOError as e:
        client = None
    if session:
        try:
            print "Trying login..."
            client = LineClient(authToken=session,com_name=com_name)
        except Exception as e:
            print e
            client = None
    if client is None:
        print "falling back to manual login..."
        try:
            USR_LINE_ID = raw_input("Enter your LINE ID(e-mail): ").strip()
            USR_LINE_PASSWORD = getpass.getpass("Enter your LINE PASSWORD: ").strip()
            client = LineClient(USR_LINE_ID,USR_LINE_PASSWORD,com_name=com_name)
        except Exception as e:
            print "Login Failed ERROR: %s" % e
    if client is None:
        exit(-1)
    print "Your authtoken is : %s" % client.authToken
    with open(session_file,"w") as f:
        f.write(client.authToken)
    me = client.profile
    print "Your profile is : %s" % repr(me)
    bot = LINEbot(client)
    bot.start()
    try:
        import atexit
        atexit.register(bot.stop)
        import rlcompleter
        rlcompleter.readline.set_history_length(100)
        rlcompleter.readline.parse_and_bind("tab: complete")
    except:
        pass
    import sys
    sys.ps1 ="\x1B[1m\x1B[31m>\x1B[33m>\x1B[32m>\x1B[0m "
    interact(banner="console mode. LINEBot instance = bot", local=locals())
    bot.stop()
