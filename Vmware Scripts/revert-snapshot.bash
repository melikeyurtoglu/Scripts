#!/bin/bash


snapshotname=$1

SNAPSHOT_ID=$($HOME/getsnapshotid.py "${snapshotname}")
#echo $SNAPSHOT_ID 

ssh root@${ESXI_ADDRESS} "vim-cmd vmsvc/snapshot.revert $vmid ${SNAPSHOT_ID} 0"
