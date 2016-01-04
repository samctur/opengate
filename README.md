#opengate project

short script to check available VPNs on vpngate.net
and parse the desired vpn.

Dependencies:

  python2.7.X

  openvpn

Usage:

Currently only obtains openvpn formats from vpn servers.
Once installed, openvpn -h for detailed usage.
man page to be added...

Install:

  If you do not have a home bin directory:
  mkdir ~/bin; cp ./opengate.py ~/bin/opengate; chmod 700 ~/bin/opengate

  Otherwise, simply move the script into your bin directory.

  If you have not added your home directory to $PATH, append the
  following to your .bashrc or .profile:
  PATH="$HOME/bin:$PATH"

  Simplified:
  run ./install.sh 
  
