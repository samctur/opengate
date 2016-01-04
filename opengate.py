#!/bin/python2.7

"""
opengate is an opensource python2.X script scraping vpngate.net
of the best vpns at moment of call. Network connection mandatory.

Copyright (C) 2015  kamiunix

Author:
    kamiunix <kamiunix@gmail.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY: without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. see the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
"""

import os
import sys
import urllib2
import re
import getopt


class OpenNode(object):
    """
    VPN link objects
    """ 
    def __init__(self, site='www.vpngate.net/en/', string=None, country=None, ip=None, total=0,  mbps=0.0, ms=0, vpn=None):
        """Constructor"""

        self._site = site
        "site of interest"
        self._string = string
        "unparsed string from main page (str)"
        self._country = country
        "country of vpn (str)"
        self._ip = ip
        "vpn ip address (str)"
        self._total = total
        "total users at init (int)"
        self._mbps = mbps
        "speed of vpn (float)"
        self._ms = ms
        "ping data (int)"
        self._vpn = vpn 
        "link to vpn page (str)"
        self._data = None 
        "page data for download parsing (str)"
        self._downloads = None
        "download link, if parsed/followed (str)"

    site = property(fget = lambda self: self._site, doc="node's site of origin")
    string = property(fget = lambda self: self._string, doc="string parsed for data")
    country = property(fget = lambda self: self._country, doc="country of vpn")
    ip = property(fget = lambda self: self._ip, doc="ip address of vpn")
    total = property(fget = lambda self: self._total, doc="total users of vpn")
    mbps = property(fget = lambda self: self._mbps, doc="speed in mbps of vpn")
    ms = property(fget = lambda self: self._ms, doc = "ms of vpn")
    vpn = property(fget = lambda self: self._vpn, doc="link to vpn page")
    data = property(fget = lambda self: self._data, doc="page's contents")
    downloads = property(fget = lambda self: self._downloads, doc="download link")

    def __str__(self):
        """printable tuples"""
        print("{0} :: {1} :: {2} users :: {3} Mbps :: {4}ms\n{5}".format(self._country,self._ip,self._total,self._mbps,self._ms,self._vpn))

    @staticmethod
    def __doc__():
        """opennode documentation/information"""
        print("opennodes are used to store distinct vpn\
                information for use in opengate main functions")

    def compareTo(self, node):
        return self._mbps > node._mbps
        

class HeapGate(object):
    """
    Heap Datastructure.
    Mbps as order of priority.
    """

    def __init__(self, site = 'www.vpngate.net/en/', create_node=OpenNode):
        """Constructor"""
        self._heap = []
        "heap list"
        self._site = site
        "host site"
        self._create_node = create_node
        "easy node creation"
        self._countries = []

    site = property(fget = lambda self: self._site, doc="host webstie")
    heap = property(fget = lambda self: self._heap, doc="heap list")

    @staticmethod
    def __doc__():
        print("opengate is an attempt at vpn connection\
                scripting using vpngate's free vpns and\
                the open source openvpn software")

    def __str__(self):
        "Heap string"
        for x in self._heap:
            x.__str__()

    def size(self):
        "size of heap"
        return len(self._heap)

    def insert_node(self, node):
        "insert priority node"
        self._heap.append(node)

        index = len(self._heap) - 1
        pindex = (index - 1)/2
        parent = self._heap[pindex]

        while index > 0 and node.compareTo(parent) > 0:
            self._heap[index] = parent
            self._heap[pindex] = node
            index = pindex
            pindex = (index - 1)/2
            parent = self._heap[pindex]

    def delete_max(self):
        "remove highest priority"
        if not self._heap:
            return None
        x = self._heap[0]
        y = self._heap[len(self._heap)-1]
        del(self._heap[len(self._heap)-1])
        if len(self._heap) is 0:
            return x

        self._heap[0] = y
        index = 0
        lindex = index*2 + 1
        rindex = index*2 + 2
        found = False

        while not found:
            if lindex < len(self._heap) and rindex < len(self._heap):
                if self._heap[lindex].compareTo(self._heap[rindex]) > 0:
                    max_ = self._heap[lindex]
                    max_index = lindex
                else:
                    max_ = self._heap[rindex]
                    max_index = rindex
            
                if y.compareTo(max_) < 0:
                    self._heap[max_index] = y
                    self._heap[index] = max_
                    index = max_index
                else:
                    found = True
            elif lindex < len(self._heap):
                if y.compareTo(self._heap[lindex]) < 0:
                    self._heap[index] = self._heap[lindex]
                    self._heap[lindex] = y
                    index = lindex
                else:
                    found = True
            else:
                found = True
            lindex = index*2 + 1
            rindex = index*2 + 2
        return x
        
    def delete(self):
        "deletes heap"
        del(self._heap)


class CliArg(object):
    """
    keeps track of command line arguments passed
    """
    def __init__(self, site='www.vpngate.net/en/',v=False,  p='tcp', c=[], C=[], s=[], S=[], u=None, U=None, m=None, M=None):
        """Constructor"""
        self._site = site 
        "vpn website"
        self._verbose = v
        "verbose mode"
        self._proto = p
        "type of vpn channel"
        self._country_whitelist = c 
        "country whitelist"
        self._country_blacklist = C 
        "country blacklist"
        self._ip_whitelist = s 
        "ip whitelist"
        self._ip_blacklist = S 
        "ip blacklist"
        self._users_min = u
        "minimum users of vpn"
        self._users_max = U 
        "maximum users of vpn"
        self._mbps_min = m
        "minimum mbps of vpn"
        self._ms_max = M 
        "max ms of vpn"

    site = property(fget = lambda self: self._site, doc="site used in scraping")
    verbose = property(fget = lambda self: self._verbose, doc="verbose mode pairity")
    proto = property(fget = lambda self: self._proto, doc="protocol of vpn")
    ms_max = property(fget = lambda self: self._ms_max, doc="maximum latency of vpn")
    mbps_min = property(fget = lambda self: self._mbps_min, doc="minimum mbps of vpn")
    users_min = property(fget = lambda self: self._users_min, doc="minimum users on vpn")
    users_max = property(fget = lambda self: self._users_max, doc="maximum users on vpn")
    ip_whitelist = property(fget = lambda self: self._ip_whitelist,\
            doc="desired ip addresses")
    ip_blacklist = property(fget = lambda self: self._ip_blacklist,\
            doc="undesired ip addresses")
    country_whitelist = property(fget = lambda self: self._country_whitelist,\
            doc="desired vpn countries")
    country_blacklist = property(fget = lambda self: self._country_whitelist,\
            doc="undesired vpn countries")

    @staticmethod
    def __doc__():
        """Documentation"""
        print("struct storing argument information for priority parsing")

    def __str__(self):
        """String print of CliArg"""
        print("{0}, c={2}, C={3}, s={4}, S={5}, u={6}, U={7}, m={8}, M={9}".format(self._site, self._country_whitelist, self._country_blacklist, self._ip_whitelist, self._ip_blacklist, self._users_min, self._users_max, self._mbps_min, self._ms_max))


"""
Main methods
"""
def _getall(cliargs=CliArg(), heap=HeapGate()):
    """Get all VPN tupples"""
    site = 'http://'+cliargs._site 
    recomp = re.compile(r'<td class=\'vg_table_row_[0-1].*?\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}.*?Total.*?Ping:.*?Logging\spolicy.*?\n')
    count = 0
    try:
        response = urllib2.urlopen(site)
        data = response.read()
    except:
        print("  unable to establish network connection.\
                \n  .....\
                \n  check network connectivity and site status.")
        sys.exit(1)
    for x in re.findall(recomp, data):
        if cliargs._verbose:
            print("parsing...\n  {0}".format(x))
        "parse each vpn on site"
        count += _parse(x, cliargs, heap)
    print("found {0} matching VPNs".format(count))
    _getbest(cliargs, heap)

def _getbest(cliargs=CliArg(), heap=HeapGate()):
    """Get best vpn from AVL Heap"""
    found = False
    while not found and len(heap._heap) is not 0:
        max_node = heap.delete_max()
        max_node._downloads = _getvpn(max_node, cliargs)
        if max_node._downloads is not None:
            found = True
    print("Found a matching VPN\
      \n*\t*\t*\t*\t*")
    max_node.__str__()
    print("*\t*\t*\t*\t*")
    vpn = max_node._downloads
    print(vpn)
    print("*\t*\t*\t*\t*")
    try:
        response = urllib2.urlopen(vpn)
    except:
        print("  unable to establish network connection.\
                \n  .....\
                \n  check network connectivity and site status.")
        sys.exit(1)
    try:
        file_ = open('/tmp/vpngate.ovpn', 'w')
        file_.write(response.read())
        file_.close
    except:
        print("  unable to open ovpn file.\
                \n  .....\
                \n  check file permisions.")
        sys.exit(1)
    print("{0} created in {1}".format(file_, '/tmp/vpngate.ovpn'))

def _getvpn(node, cliargs=CliArg()):
    """Get download link of given opennode"""
    header = 'http://www.vpngate.net'
    site = 'http://'+node._vpn
    try:
        response = urllib2.urlopen(site)
        data = response.read()
    except:
        print("  unable to establish network connection.\
                \n  .....\
                \n  check network connectivity and site status.")
        sys.exit(1)
    vpn = None
    vpn_ = []
    "find desired protocol"
    if cliargs._proto in 'udp':
        vpns_ = re.findall(r'(/common/openvpn[^\'" >]+)', data)
        for x in range(len(vpns_)):
            if str(vpns_[x]).find('udp') >= 0:
                vpn_.append(vpns_[x])
    else:
        vpns_ = re.findall(r'(/common/openvpn[^\'" >]+)', data)
        for x in range(len(vpns_)):
            if str(vpns_[x]).find('tcp') >= 0:
                vpn_.append(vpns_[x])
    print vpns_
    if vpn_:
        "remove garbage"
        vpn = vpn_[0]
        pos = vpn.find('amp;')
        while pos  is not -1:
            vpn = vpn[:pos]+vpn[pos+4:]
            pos = vpn.find('amp;')
    if vpn:
        return header + vpn
    return None

def _parse(x, cliargs=CliArg(), heap=HeapGate()):
    """Parse given html segment"""
    country = re.findall(r'/images/flags/(..)\.png', x)
    if not country:
        return 0
    country = country[0]
    ip = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', x)
    if not ip:
        return 0
    ip = ip[0]
    users = re.findall(r'Total.*?(\d{1,3}.*?)users', x)
    if not users:
        return 0
    users = int(users[0].replace(',',''))
    mbps = re.findall(r'(\d{1,3}\.\d{1,2})\sMbps', x)
    if not mbps:
        return 0
    mbps = float(mbps[0])
    ms = re.findall(r'(\d{1,10})\sms', x)
    if not ms:
        return 0
    ms = int(ms[0])
    vpn = re.findall(r'(do_openvpn[^\'" >]+)', x)
    if not vpn:
        return 0
    vpn = cliargs._site+vpn[0]
    node = OpenNode(string=x,country=country,ip=ip,total=users,mbps=mbps,ms=ms,vpn=vpn)
    "check if vpn fits wanted cli arguments"
    if _parse_cliargs(node, cliargs, heap):
        heap.insert_node(node)
        return 1
    return 0

def _parse_cliargs(node, cliargs=CliArg(), heap=HeapGate()):
    "parse VPNs found, only adding if desired"
    if cliargs._country_whitelist:
        if cliargs._country_whitelist in "--list":
            if node._country in heap._countries:
                return False
            else:
                print(node._country)
                heap._countries.append(node._country)
        elif node._country not in cliargs._country_whitelist:
            return False
    if cliargs._country_blacklist:
        if cliargs._country_blacklist in "--list":
            if node._country in heap._countries:
                return False
            else:
                print(node._country)
                heap._countries.append(node._country)
        elif node._country in cliargs._country_:
            return False
    if cliargs._ip_whitelist:
        if node._ip not in cliargs._ip_whitelist:
            return False
    if cliargs._ip_blacklist:
        if node._ip in cliargs._ip_blacklist:
            return False
    if cliargs._users_min is not None:
        if node._total < cliargs._users_min:
            return False
    if cliargs._users_max is not None:
        if node._total > cliargs._users_max:
            return False
    if cliargs._mbps_min is not None:
        if node._mbps < cliargs._mbps_min:
            return False
    if cliargs._ms_max is not None:
        if node._ms > cliargs._ms_max:
            return False
    return True

def main(argv):
    """parse cli arguments"""

    try: 
        opts, args = getopt.getopt(argv[1:], 'hvc:C:s:S:u:U:m:M:P:', \
                ['help', 'ping', 'country-whitelist=', 'country-blacklist=', 'ip-whitelist=', 'ip-blacklist=', 'max-users=', 'min-users=', 'min-mbps=', 'max-ms=', 'proto=', 'list'])
    except getopt.GetoptError:
        print("  unable to parse commandline arguments;\
                \n  getopts parsing error.\
                \n  .....\n")
        usage(argv[0])
        sys.exit(1)
    cliargs = CliArg()
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            usage(argv[0])
            sys.exit(0)
        elif opt in ('--list'):
            _get_countries()
            sys.exit(0)
        elif opt in ('--ping'):
            sys.exit(0)
        elif opt in ('-v'):
            cliargs._verbose = arg
        elif opt in ('-c', '--country-whitelist'):
            cliargs._country_whitelist = arg
        elif opt in ('-C', '--country-blacklist'):
            cliargs._country_blacklist = arg
        elif opt in ('-s', '--ip-whitelist'):
            cliargs._ip_whitelist = arg
        elif opt in ('-S', '--ip-blacklist'):
            cliargs._ip_blacklist = arg
        elif opt in ('-u', '--min-users'):
            cliargs._users_min = int(arg)
        elif opt in ('-U', '--max-users'):
            cliargs._users_max = int(arg)
        elif opt in ('-m', '--min-mbps'):
            cliargs._mbps_min = float(arg)
        elif opt in ('-M', '--max-ms'):
            cliargs._ms_max = int(arg)
        elif opt in ('-P', '--proto'):
            if arg in 'udp':
                cliargs._proto = 'udp'
    _getall(cliargs)

def _get_countries():
    """Countries available for parsing"""
    print('-c, -C [country]\
            \n [country]=\
            \n AR\t: Argentina\
            \n AT\t: Austria\
            \n BR\t: Brazil\
            \n BY\t: Belarus\
            \n CA\t: Canda\
            \n DE\t: Germany\
            \n FR\t: France\
            \n GB\t: Great Britain\
            \n GH\t: Ghana\
            \n HU\t: Hungary\
            \n ID\t: Indonesia\
            \n IL\t: Israel\
            \n JP\t: Japan\
            \n KR\t: Korea\
            \n MA\t: Morocco\
            \n MY\t: Malaysia\
            \n NL\t: Netherlands\
            \n NO\t: Norway\
            \n OM\t: Oman\
            \n PK\t: Pakistan\
            \n RU\t: Russia\
            \n SA\t: Saudi Arabia\
            \n TH\t: Thailand\
            \n TW\t: Taiwan\
            \n UA\t: Ukraine\
            \n US\t: United States\
            \n UY\t: Uruguay\
            \n VE\t: Venezuela\
            \n VN\t: Vietnam\
            \n .....\n common usage: opengate -c JP')

def usage(argv=None):
    """Usage of program"""
    print("Usage: opengate [OPTION]...\n".format(argv))
    #check ls or other
    print("Options: \
            \n  -h, --help\t\t\t\tdisplay this help and exit\
            \n  -v\t\t\t\t\tverbose output\
            \n  --ping\t\t\t\tping status of site\
            \n  --list\t\t\t\tlists commonly available countries\
            \n  -c, --country-whitelist\t\tcountries to include in search.\
            \n\t\t\t\t\t  ex: -c 'JP KR US'\
            \n\t--list\t\t\t\tqueries currently available countries\
            \n  -C, --country-blacklist\t\tcountries to exclude from search.\
            \n\t\t\t\t\t  ex: -c JP\
            \n\t--list\t\t\t\tqueries currently available countries\
            \n  -s, --ip-whitelist\t\t\tip address to include in search.\
            \n  -S, --ip-blacklist\t\t\tip address to exclude from search.\
            \n  -u, --min-users\t\t\tminimum users on VPNs\
            \n  -U, --max-users\t\t\tmaximum users on VPNs\
            \n  -m, --min-mbps\t\t\tminimum mega-bytes-per-second of VPNs\
            \n\t\t\t\t\t  float point values only.\
            \n  -M, --max-ms\t\t\t\tmaximum lag for VPNs\
            \n\t\t\t\t\t  integer values only.\
            \n  -p, --proto\t\t\t\tovpn file conection type.\
            \n\t\t\t\t\t  either 'tcp' or 'udp'\
            \n\nExit status:\
            \n 0 if OK,\
            \n 1 if minor (e.g.,  cannot access site),\
            \n 2 if serious poblem.")

if __name__== '__main__':
    main(sys.argv[:])

