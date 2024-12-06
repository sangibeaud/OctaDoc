source local.cfg

mkdir $DATA_REPOSITORY
git -C $DATA_REPOSITORY init
echo $DATA_REPOSITORY >> .gitignore

#sync to data repository
# octa-sync.sh

#ready to go
