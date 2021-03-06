#!/bin/sh

SHOOTER="./shooter.py"

#
# This script wrap the shooter.py script. do not include any of the globaleaks files

# dt "identificative number" "portion of command line" "description" "assertion description"
dt() {
    dumpfile="/tmp/dumptest_$1"
    echo > $dumpfile

    echo -n "$1) $3 ..."
    ret=`$SHOOTER $2`
    if [ $? != 0 ]; then 
        echo "\tError [$2]" 
        echo "Error [$2]\n\n$ret" >> $dumpfile
        echo "saved error in $dumpfile"
        exit
    fi
    echo " done."

    echo "$3" >> $dumpfile
    echo "$2" >> $dumpfile
    if [ ! -z "$4" ]; then
        echo $4 >> $dumpfile
    fi
    echo "\n\n" >> $dumpfile

    $SHOOTER D1 GET dump count verbose >> $dumpfile
}

dt "1" "D2 DELETE task alljobs" "Disabling all the scheduled jobs"

dt "2" "D1 GET dump contexts print-context_gus" "dumping context_gus available"
context_list=$ret

dt "2" "D1 GET dump receivers print-receiver_gus" "dumping receivers_gus available"
receivers_list=$ret

receiver_option=""
for r in $receivers_list; do
    receiver_option=`echo "\"$r\",$receiver_option"`
done
r_ready=`echo $receiver_option | sed -es/,$//`

dt "3" "D1 GET dump itip print-itip_elements" "dumping number of internaltips, before the tests"
beforecount=$ret

cnt=0
for context_gus in $context_list; do

    cnt=$(($cnt+1))

    dt "\t4x" "U2 POST cid $context_gus print-submission_gus" "opening a new submission"
    submission_gus=$ret
    dt "\t5+" "U3 PUT cid $context_gus sid $submission_gus raw $r_ready print-receipt" "completing submission and getting receipt"
    receipt=$ret
    echo "completed submission receipt $receipt for context $context_gus"


done


# Force tip schedule creation
dt "6" "D2 GET task delivery" "Forcing delivery asyncronous operation"

dt "3" "D1 GET dump itip print-itip_elements" "dumping number of internaltips, after tests"
aftercount=$ret

echo "[*] before: $beforecount after: $aftercount"
