#!/bin/bash
export PROJ_DIR=$PWD
export LOG_FILE=$PROJ_DIR/app.log
export CRON_SPEC="*/2 * * * *"

echo "$CRON_SPEC cd $PROJ_DIR && $(which python3) $PROJ_DIR/main.py >> $LOG_FILE 2>&1" > $PROJ_DIR/crontab
touch $LOG_FILE
crontab $PROJ_DIR/crontab
crontab -l
cron  && tail -f $LOG_FILE

