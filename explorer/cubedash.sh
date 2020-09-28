#!/bin/bash

# Reference: https://bencane.com/2015/09/22/preventing-duplicate-cron-job-executions/

echo "Testing if another cron is running"

PIDFILE=/home/datacube/explorer/cubedash.pid
if [ -f $PIDFILE ]
then
  PID=$(cat $PIDFILE)
  ps -p $PID > /dev/null 2>&1
  if [ $? -eq 0 ]
  then
    echo "Process already running"
    exit 0
  else
    ## Process not found assume not running
    echo $$ > $PIDFILE
    if [ $? -ne 0 ]
    then
      echo "Could not create PID file"
      exit 1
    fi
  fi
else
  echo $$ > $PIDFILE
  if [ $? -ne 0 ]
  then
    echo "Could not create PID file"
    exit 1
  fi
fi

echo "$(date): Running cubedash-gen"

echo "$(date): Running cubedash-gen" >> /home/datacube/explorer/cubedash.log

/home/datacube/miniconda3/bin/cubedash-gen --force-refresh s2_sen2cor_ard_granule_EO3 1>> /home/datacube/explorer/cubedash.log 2>> /home/datacube/explorer/cubedash.log

echo "$(date): Finished cubedash-gen" >> /home/datacube/explorer/cubedash.log


rm $PIDFILE