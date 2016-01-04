#opengate project

short script to check available VPNs on vpngate.net
and parse the desired vpn.

Created by:

  * kamiunix <kamiunix@tuta.io>


## Building

Start by grabbing the code using Git. If you're planning to contribute, fork the project on GitHub.

    $ git clone https://github.com/kamiunix/opengate.git
    $ git submodule update --init

## Dependencies

  * python2.7.X

  * openvpn

## Usage

Currently only obtains openvpn formats from vpn servers. Please run openvpn -h for detailed usage once installed.
A man page is on its way...

## Install

  1. If you do not have a home bin directory:

  $ mkdir ~/bin; cp ./opengate.py ~/bin/opengate; chmod 700 ~/bin/opengate

    Otherwise, simply move the script into your bin directory.

  2. If you have not added your home directory to $PATH, append the
  following to your .bashrc or .profile:

    PATH="$HOME/bin:$PATH"

  3. Simplified:

  $ ./install.sh 
  

