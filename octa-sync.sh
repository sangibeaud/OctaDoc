source local.cfg

#rsync -vnrc --exclude Base/AUDIO /run/media/stephane/OCTATRACK64/ OT/
RSYNC_CMD="rsync -vrc --exclude Base/AUDIO $OT_MOUNT/$OT_PROJECT_PATH $DATA_REPOSITORY/"

echo $RSYNC_CMD
echo 2 secs to cancel \(ctrl-C\)
sleep 1
echo 1 secs to cancel \(ctrl-C\)
sleep 1
echo $RSYNC_CMD
eval $RSYNC_CMD

