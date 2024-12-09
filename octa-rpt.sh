source local.cfg

RPT_DATA_PATH=./data/reports
RPT_FILE=$RPT_DATA_PATH/rpt-`date +%m%d_%H%M.txt`

git -C $DATA_REPOSITORY/ log | head -n 5 | tail -n 1 >> $RPT_FILE
git -C $DATA_REPOSITORY/ diff `git -C $DATA_REPOSITORY/ log -n 2 | grep commit | sort -r | cut -f 2 -d " "`  >> $RPT_FILE

