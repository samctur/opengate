# Opengate Project

short script to check available VPNs on vpngate.net
and parse the desired vpn.

Created by:

  * samuelct <sam.champagne@dal.ca>


## Building

Start by grabbing the code using Git. If you're planning to contribute, fork the project on GitHub.

    `git clone https://github.com/kamiunix/opengate.git`
    `git submodule update --init`

## Dependencies

  * python2.7.X

  * openvpn

## Usage

Once installed you can run the following command for details:

$ opengate -h

## Install

  1. If you do not have a home bin directory:

  `mkdir ~/bin; cp ./opengate.py ~/bin/opengate; chmod 700 ~/bin/opengate`

   Otherwise, simply move the script into your bin directory.

  2. If you have not added your home directory to $PATH, append the
  following to your .bashrc or .profile:

  `PATH="$HOME/bin:$PATH"`

  3. Simplified:

  `./install.sh `

## Docker deployement

A demonstration of the application is available through a docker image available at samuelct/opengate. Do note that openvpn
may or may not work depending on how you have started the ducker image.

`docker pull samuelct/opengate`
  
## Structure

This application uses two Object structures. One to store command line arguments (CliArgs), and one to to store parsed vpn objects (OpenNode). It further uses a max heap data structure to organize the resulting nodes by fastest speed in Mbps.
