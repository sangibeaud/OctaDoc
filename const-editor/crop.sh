#!/bin/bash

SKIP=${SKIP:="0"} 
COUNT=${COUNT:="1234"}  

#test -e $1 || echo " $0 : the first argument musy be an existing file name " && exit

#dd if=bank01.strd bs=4096 skip=${SKIP}  count=${COUNT} iflag=skip_bytes,count_bytes > offset_${SKIP}_len_${COUNT}.bin
dd if=$1 bs=4096 skip=${SKIP}  count=${COUNT} iflag=skip_bytes,count_bytes
