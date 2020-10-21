#!/bin/bash
export PROJ_DIR=$PWD
export LOG_FILE=$PROJ_DIR/app.log
export CRON_SPEC="*/6 * * * *"

echo "$CRON_SPEC curl -v  http://0.0.0.0:5000/api/elecciones/download_data $LOG_FILE 2>&1" > $PROJ_DIR/crontab
touch $LOG_FILE
crontab $PROJ_DIR/crontab
crontab -l
cron  && tail -f $LOG_FILE

