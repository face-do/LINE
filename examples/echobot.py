#!/usr/bin/env python2
# encoding: utf-8

# Echo LINE messages if sender is not you.

import getpass
from line import LineClient, LineGroup, LineContact

try:
    USR_LINE_ID = raw_input("Enter your LINE ID(e-mail): ").strip()
    USR_LINE_PASSWORD = getpass.getpass("Enter your LINE PASSWORD: ").strip()
    client = LineClient(USR_LINE_ID,USR_LINE_PASSWORD,com_name=__file__)
    #client = LineClient("ID", "PASSWORD")
    #client = LineClient(authToken="AUTHTOKEN")
except e:
    print "Login Failed ERROR: %s" % e

print "Your authtoken is : %s" % client.authToken
me = client.profile
print "Your profile is : %s" % repr(me)

while True:
    op_list = []
    for op in client.longPoll():
        op_list.append(op)
    for op in op_list:
        sender   = op[0]
        #receiver = op[1]
        message  = op[2]
        if message is None:
            continue
        msg = message.text
        print "%s: %s" % (sender.name, msg)
        if sender != me:
            sender.sendMessage("%s" % msg)
