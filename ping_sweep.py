#!/usr/bin/env python
"""ping_sweep.py

Usage:
    ping_sweep.py <cidr> [--test]
    ping_sweep.py -f <file> [--test]

Options:
    -h, --help  Display usage.
    --test      Prints out list of addresses to sweep. Does
                not send any pings.
    --version   Display version.

Arguments:
    cidr        Any CIDR notataion, like 10.10.10.10/31. Other
                values, like 10, or 192.168 may be interpretted as
                valid CIDR. Use --test to see the list of addresses
                produced.
    file        File containing one IP address or CIDR block per
                line. Invalid values are skipped.
"""
import os
import subprocess
from multiprocessing.dummy import Pool as Threadpool
import sys
import docopt
import netaddr

__version__ = '1.0'


def file_to_iplist(ip_file):
    """Return list of IP addresses in file."""
    try:
        with open(ip_file) as file_handle:
            entries = file_handle.read().splitlines()
    except IOError as err:
        print err.strerror
        sys.exit(0)

    ip_list = []
    for entry in entries:
        if netaddr.valid_ipv4(entry):
            ip_list.append(entry)
        else:
            try:
                cidr = [str(ip) for ip in list(netaddr.IPNetwork(entry))]
                ip_list.extend(cidr)
            except netaddr.core.AddrFormatError:
                pass
    return ip_list


def ping_ip(ip_address):
    """Print IP if ICMP response."""
    result = subprocess.call(['ping', '-c', '1', ip_address],
                             stdout=open(os.devnull, 'w'),
                             stderr=open(os.devnull, 'w'))
    if result == 0:
        print ip_address
    else:
        pass


def scan_targets(ip_list):
    """Ping each IP in network in a separate thread."""
    pool = Threadpool(255)
    pool.map(ping_ip, ip_list)
    pool.close()
    pool.join()


def main(args):
    """Parse CLI args and scan targets."""
    if args['<cidr>']:
        try:
            ip_list = [str(x) for x in list(netaddr.IPNetwork(args['<cidr>']))]
        except netaddr.core.AddrFormatError as err:
            print err.message
            sys.exit(0)
    elif args['<file>']:
        ip_list = file_to_iplist(args['<file>'])

    if args['--test']:
        print ip_list
        sys.exit(0)

    scan_targets(ip_list)

if __name__ == "__main__":
    main(docopt.docopt(__doc__, version=__version__))
