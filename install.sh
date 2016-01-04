#!/bin/bash

git=`pwd`

echo "looking for ${USER}/bin"
echo "..."
cd
if [ -d bin ]; then
  echo "${USER}/bin found"
  cd bin
  cp ${git}/opengate.py ./opengate
  chmod 700 opengate
else
  echo "creating ${USER}/bin"
  mkdir bin
  cd !\$
  cp ${git}/opengate.py ./opengate
  chmod 700 opengate
fi

echo `ls -l | grep opengate`

echo "looking for path"
echo "..."

if [ `echo $PATH | grep "${USER}/bin"` == "" ]; then
  echo "adding path to .bashrc"
  echo 'PATH=$HOME/bin:$PATH' >> ~/.bashrc
else
  echo "path found"
fi

echo "script installed!" 
echo "try   opengate -h"
echo "-------------------------------------------"
echo "|    check README if an error occurs      | "
echo "| submit the error if it is undocumented  | "
echo "---------Go support vpngate.net!-----------"
