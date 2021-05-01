#!/bin/bash

source /etc/profile.d/modules.sh
module load conda/2020.11-python3.8

CUR=$(dirname "$(realpath $0)")
ROOT="$CUR/.."
MAIN_NAME="start_oar"

MAIN_LOGS="$CUR/logs"
if [ -d $MAIN_LOGS ]; then
	rm -r $MAIN_LOGS
fi
mkdir -p $MAIN_LOGS

source $ROOT/venv/bin/activate

## With nohup
#nohup /usr/bin/time -o $MAIN_LOGS/time.txt python $CUR/$MAIN_NAME.py > $MAIN_LOGS/$MAIN_NAME.stdout 2> $MAIN_LOGS/$MAIN_NAME.stderr &
#echo "Program '$MAIN_NAME.py' started, run 'ps aux | grep $MAIN_NAME.py' to check"

## Without nohup
/usr/bin/time -o $MAIN_LOGS/time.txt python $CUR/$MAIN_NAME.py
