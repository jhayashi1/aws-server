#!/bin/bash

#Add newest backup to s3 bucket
cd /home/enigmatica2/backups
aws s3 cp $(ls -t1 | head -n 1) s3://grug-backup

#Delete oldest backup from bucket
#old_file=$(aws s3 ls s3://grug-backup --recursive | sort | tail -n 1 | awk '{print $4}')
#aws s3 rm s3://grug-backup/${old_file}