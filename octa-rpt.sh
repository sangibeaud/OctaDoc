source local.cfg

git -C OT/ diff `git -C OT/ log -n 2 | grep commit | cut -f 2 -d " "`
