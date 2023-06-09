#!/usr/bin/bash

# prepenv.sh creates empty files and directories needed
# .roboip holds the IP address / hostname of the robot
# .secret holds the password to the robot
# put.conf is the configuration file for this script

# Made by Morton
# No Warranty on Software. You and your end users use the Software at your own risk.
# Author provides the Software to you "AS IS" and without warranty and you hereby
# indemnify Author for your use of the Software. You are not entitled to any hard copy
# documentation, maintenance, support or updates for the Software. AUTHOR EXPRESSLY
# DISCLAIMS ALL WARRANTIES RELATED TO THE SOFTWARE, EXPRESS OR IMPLIED, INCLUDING, BUT
# NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE. FURTHER, AUTHOR DOES NOT WARRANT OR MAKE ANY REPRESENTATIONS REGARDING THE
# USE OR THE RESULTS OF THE USE OF THE SOFTWARE OR RELATED DOCUMENTATION IN TERMS OF
# THEIR CORRECTNESS, ACCURACY, RELIABILITY OR OTHERWISE. SOME JURISDICTIONS DO NOT ALLOW
# THE EXCLUSION OF IMPLIED WARRANTIES, SO PORTIONS OF THE ABOVE EXCLUSION MAY NOT APPLY
# TO YOU.

# Clean white spaces helper - removes ""
clean_w() {
    eval ${1}="${!1//[$'\t\r\n']}"
}

# Clean white spaces helper - adds ""
s_clean_w() {
    eval ${1}='"${!1//[$'\t\r\n']}"'
}

# Read conf from secret files
read _ip <.roboip
read _password < .secret
clean_w _ip
clean_w _password

# Load env config
# Source: https://stackoverflow.com/a/30969768
set -o allexport
source put.conf
set +o allexport

s_clean_w _prompt1
s_clean_w _prompt2
clean_w _srcdir
clean_w _addr

# Set mode of action (arg files or srcdir)
if [[ ${1} != "" ]]; then
    _cmd="${1} ${_addr}:~/${1}"
    _cmd2=""
else
    _cmd="-r ${_srcdir} ${_addr}:~/"
    _cmd2="mv ${_srcdir}/* . ; rm -r ${_srcdir}"
fi

# Do the Mario
/usr/bin/expect << END
    spawn bash -c "scp $_cmd";
    expect "?assword: ";
    send "$_password\r";
    puts "\[STRENG GEHEIM\]"
    expect $_prompt1;

    spawn bash -c "ssh $_addr";
    expect "?assword: ";
    send "$_password\r";
    puts "\[STRENG GEHEIM\]"
    expect $_prompt2;
    send "$_cmd2\r";
    expect $_prompt2;
    send "exit\r";
    expect $_prompt1;
    exit
END
