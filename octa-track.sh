source local.cfg

TRACKED="Base/REM2023A/ Base/REDFX/"
TRACKED="$OT_PROJECT_PATH/$OT_PROJECT"
EXCLUDING="dummy"


#rsync -vnrc --exclude Base/AUDIO /run/media/stephane/OCTATRACK64/ OT/

echo "Describe changes since last sync. One line only"
read MESSAGE

#echo 5 secs to cancel \(ctrl-C\)
#sleep 5
#echo 1 secs to cancel \(ctrl-C\)
#sleep 1
for TRACKING in $TRACKED
do
    echo "Tracking $TRACKING"
    #rsync -vrc /run/media/stephane/OCTATRACK64/${TRACKING} --exclude ${EXCLUDING} OT/${TRACKING}

    echo "git -C $DATA_REPOSITORY add $TRACKING/"
    git -C $DATA_REPOSITORY add $TRACKING/

    echo "processing $TRACKING ( in $DATA_REPOSITORY/$TRACKING )"
    pushd OT/${TRACKING}
    pwd
    #ls
    #git status
    #ls | grep -E -o "bank[0-9]*.(work|strd)" 


    echo generate hexdump of files for better diffing 
    for f in `git status | grep -E "(modified|added)"| grep -E -o "bank[0-9]*.(work|strd)"`; 
    do
        echo hexdump -C ${f} ${f}.hexdump
        hexdump -C ${f} >  ${f}.hexdump
    done

    for f in `git status | grep -E "(modified|added)" |grep -E -o "arr[0-9]*.(work|strd)"`; 
    do
        echo hexdump -C ${f} ${f}.hexdump
        hexdump -C ${f} >  ${f}.hexdump
    done

    for f in `git status | grep -E "(modified|added)" | grep -E -o "(project|markers).(work|strd)"`; 
    do
        echo hexdump -C ${f} ${f}.hexdump
        hexdump -C ${f} >  ${f}.hexdump
    done
    popd

done

echo Done processing files.

#changes to the data
#pushd OT
git -C $DATA_REPOSITORY add $TRACKING/*
echo Done adding files.
git -C $DATA_REPOSITORY commit -a -m "${MESSAGE}"
echo Done commiting

git -C $DATA_REPOSITORY status
#popd

