#!/usr/bin/env python
"""ping-sweep.py

Usage:
    ping-sweep.py <cidr>
    ping-sweep.py -f <file>
"""
import os
import subprocess
from multiprocessing.dummy import Pool as Threadpool
import docopt
import netaddr


def ping_ip(ip):
    """Print IP if ICMP response."""
    result = subprocess.call(['ping', '-c', '1', ip],
                             stdout=open(os.devnull, 'w'),
                             stderr=open(os.devnull, 'w'))
    if result == 0:
        print ip
    else:
        pass


def main(ip_list):
    """Ping each IP in network in a separate thread."""
    pool = Threadpool(255)
    pool.map(ping_ip, ip_list)
    pool.close()
    pool.join()

if __name__ == "__main__":
    args = docopt.docopt(__doc__)
    if args['<cidr>']:
        network = list(netaddr.IPNetwork(args['<cidr>']))
        ip_list = [str(x) for x in network]
    elif args['<file>']:
        with open(args['<file>']) as f:
            ip_list = f.read().splitlines()
    main(ip_list)
