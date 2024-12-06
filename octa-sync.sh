source local.cfg

#rsync -vnrc --exclude Base/AUDIO /run/media/stephane/OCTATRACK64/ OT/
RSYNC_CMD="rsync -vrc --exclude Base/AUDIO $OT_MOUNT/$OT_PROJECT_PATH/$OT_PROJECT $DATA_REPOSITORY/$OT_PROJECT_PATH"

echo $RSYNC_CMD
echo 2 secs to cancel \(ctrl-C\)
sleep 1
echo 1 secs to cancel \(ctrl-C\)
sleep 1
echo $RSYNC_CMD
mkdir -p $DATA_REPOSITORY/$OT_PROJECT_PATH
eval $RSYNC_CMD

