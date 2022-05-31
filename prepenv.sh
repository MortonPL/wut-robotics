#!/usr/bin/bash

mkdir robosrc
touch .roboip
touch .secret
alias put=./put.sh
alias run=./run.sh
alias auto=put; run
