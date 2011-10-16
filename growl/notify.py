from growl import GROWL_UDP_PORT, GROWL_APPLICATION, \
    GrowlRegistrationPacket, GrowlNotificationPacket
from socket import AF_INET, SOCK_DGRAM, socket
import sys

addr = ("metalgear.home.net", GROWL_UDP_PORT)
password = "growl"
s = socket(AF_INET, SOCK_DGRAM)

if len(sys.argv) <= 1:
    print("You must pass either 'register' or 'send' as the first argument")
    sys.exit(1)

if sys.argv[1] == "register":
    p = GrowlRegistrationPacket(application = GROWL_APPLICATION, password = password)
    p.addNotification()
    s.sendto(p.payload(), addr)
elif sys.argv[1] == "send":
    if (len(sys.argv) <= 2 or sys.argv[2] == ""):
        print("You must pass a message title string as the second argument") 
        sys.exit(1)
    else:
        title = sys.argv[2]

    if (len(sys.argv) <= 3 or sys.argv[3] == ""):
        print("You must pass a message body string as the third argument") 
        sys.exit(1)
    else:
        description = sys.argv[3]

    p = GrowlNotificationPacket(title = title, description = description, priority = 0, sticky = False, password = password)
    s.sendto(p.payload(), addr)
    s.close()
else:
    print("How the hell did you get here...?")
