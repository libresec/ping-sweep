# Ping Sweep
Wrapper around the ping utility included by the OS.

# CLI Interface
```
$ python ping_sweep.py 
Usage:
    ping-sweep.py <cidr> [--test]
    ping-sweep.py -f <file> [--test]
mbp:scripts joe$ python ping_sweep.py -h
ping-sweep.py

Usage:
    ping-sweep.py <cidr> [--test]
    ping-sweep.py -f <file> [--test]

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
```
