#!/bin/bash

snapshotname=$1
snapshotname=$(echo $snapshotname | cut -d "-" -f3)

ssh root@${ESXI_ADDRESS} "vim-cmd vmsvc/snapshot.create vmid ${snapshotname}"
