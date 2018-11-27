from multiping import multi_ping
from time import gmtime,strftime
import logging
vpnlist = []
vpnDownList = []


class Server:
    def __init__(self):
        self.IP_address = ""
        self.state = ""

    def setServerState(self,state):
        self.state = state
        return 0

    def getServerState(self):
        return self.state

    def getServerAddr(self):
        return self.IP_address


class VPN:
    def __init__(self, name, mbrs=[]):
        self.name = name
        self.members = mbrs
        self.state = ""
        logging.debug('Created VPN instance %s. ', str(name))

    def getmembers(self):
        return self.members

    def setmembers(self,ms):
        self.members = ms
        return 0

    def getstate(self):
        return self.state

    def setstate(self,state):
        self.state = state


def readfile(file):
    logging.info('Started reading VPN Servers file %s.', file)
    global vpnList
    try:
        with open(file) as fp:
            for line in fp.readlines():
                ll = line.strip().split(": ")
                vpn_name = ll[0]
                logging.debug('VPN %s is found.', vpn_name)
                cvpn = VPN(vpn_name)
                cvpn.members = ll[1].split(", ")
                cvpn.state = True
                vpnlist.append(cvpn)

    except:
        print("Can't find Host file.")
        raise
    logging.info('VPN  list is %s.', str(vpnlist))
    return vpnlist


def checkVPN(vpn):
    logging.info('Started checking VPN %s', vpn)
    global vpnDownList
    vpn.state = "UP"
    memberList = vpn.getmembers()
    response, no_response = multi_ping(memberList, timeout=2, retry=3)
    if not response:
        vpn.state = "DOWN"
        vpnDownList.append(vpn)
    logging.debug('DOWN VPN  list is %s.', vpnlist)
    return 0


def vpnRecord(dvpnlist):
    # t = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    logging.info('Started writting down vpn list %s to file.', str(dvpnlist))
    fn = 'downvpn.log'
    try:
        with open(fn, 'w') as hdr:
            hdr.write("Please check the following VPN tunnels!" + '\r\n')
            for v in dvpnlist:
                name = v.name
                ml = v.members
                hdr.write(name + ":DOWN: " + str(ml))
    except:
        print("Can't find Host file.")
        raise
    return 0



