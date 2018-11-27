from monitorTools import *
from SentEmail import Sendemails
import logging


def main():
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
    logging.info('Started')
    # read vpn and server file
    vpnlist = readfile("ServerList.txt")
    # check VPN reachiblity via servers
    for v in vpnlist:
        checkVPN(v)
    # save VPN status in file
    vpnRecord(vpnDownList)
    # Send VPN failure notification
    Sendemails()
    logging.info('Finished')


if __name__ == '__main__':
    main()
