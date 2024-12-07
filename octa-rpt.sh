source local.cfg

git -C $DATA_REPOSITORY/ diff `git -C OT/ log -n 2 | grep commit | sort -r | cut -f 2 -d " "`
