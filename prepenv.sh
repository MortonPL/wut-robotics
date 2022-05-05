#!/usr/bin/bash

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

mkdir robosrc
touch .roboip
touch .secret
alias put=./put.sh
alias run=./run.sh
alias auto=put; run
