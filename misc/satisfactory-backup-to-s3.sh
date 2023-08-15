#!/bin/bash

#Add newest backup to s3 bucket
cd /home/ubuntu/.config/Epic/FactoryGame/Saved/SaveGames/server
aws s3 cp "$(ls -Art | tail -n 1)" s3://satiscroften-backup

#Delete oldest backup from bucket
old_file=$(aws s3 ls s3://satiscroften-backup --recursive | sort | head -n 1 | tr -s ' ' | cut -d\  -f4-)
aws s3 rm "s3://satiscroften-backup/${old_file}"