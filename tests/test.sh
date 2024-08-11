#!/bin/bash

set -e

# Copyright 2024 Ankur Sinha
# Author: Ankur Sinha <sanjay DOT ankur AT gmail DOT com> 
# File : tests/test.sh
#

# all info options, from bash completion file
all_options="--sysinfo --sysinfo-short --audioinfo --sysinfo-audio --videoinfo --sysinfo-video --netinfo --sysinfo-net --diskinfo --sysinfo-net --dnfinfo --sysinfo-dnf --btrfsinfo --sysinfo-btrfs --pci-verbose --sysinfo-pci-verbose --usb-verbose --sysinfo-usb-verbose"

for option in $all_options
do
    ../fpaste $option --printonly
done
