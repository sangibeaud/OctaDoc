test -e local.cfg || echo "Set your local.cfg first !" && exit -1

source local.cfg

mkdir $DATA_REPOSITORY
git -C $DATA_REPOSITORY init
echo /$DATA_REPOSITORY/ >> .gitignore

#sync to data repository
# octa-sync.sh

#ready to go
