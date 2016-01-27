# !/usr/bin/env python
# -*- coding:utf-8 -*-
import re
import sys


def check_ip(string):
    ip_regex = r'(\d{1,3}\.){3}\d{1,3}'
    if re.match(ip_regex, string):
        return True
    return False


def main():
    ip = sys.argv[1]
    if check_ip(ip):
        print '{} is IPv4'.format(ip)
    else:
        print '{} is NOT IPv4'.format(ip)


if __name__ == '__main__':
    main()
