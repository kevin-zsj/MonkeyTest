#!/bin/bash

PRINT_ONLY=false
PRINT_AND_CSV=false
CSV_BY_DEVICE=false

MEAN=0
MEDIAN=0

function usage {
  echo "Usage: $0 <events_dir> to only print results"
  echo "Usage: $0 <events_dir> <build_number> <csv> to also store total values"
  echo "Usage: $0 <events_dir> <build_number> <csv> <all_events_dir>"
  echo "    events_dir        : directory where logs are stored."
  echo "    build_number      : the build number"
  echo "    csv               : csv with median values"
  echo "    all_events_dir    : where csv by device are stored"
}

function count {
  EVENTS=()
  TOTAL=0
  MAX=0
  MIN=125000
  DATE=`date +%Y%m%d`

  EVENTS_DIR=$1
  BUILD_LABEL=$2
  OUTPUT_CSV=$3
  ALL_EVENTS_CSV=$4

  for FILE in $(busybox find $EVENTS_DIR -name 'monkey_log_*' | busybox sort -t/ -k 8)
  do
    # Look for Events injected
    VALUE=$(grep 'Events injected' $FILE | busybox awk '{print $3} ' | busybox tr -d '\r')

    # Fallback #1, count ':Sending '
    if [ -z "$VALUE" ]; then
      VALUE=$(grep ':Sending ' $FILE | busybox wc -l)
    fi

    # Fallback #2, find last instance of '// Sending event '
    if [ -z "$VALUE" ]; then
      VALUE=$(grep ' Sending event ' $FILE | busybox tail -n 1 | busybox tr -d '\r' | busybox awk '{print $4}')
      VALUE=${VALUE:1}
    fi

    # Can't find a value, skip this file
    # When events were not found, they are stored as 0
    if ((VALUE == 0)); then
      continue
    fi

    EVENTS[${#EVENTS[*]}]=$VALUE
    if ((VALUE < MIN)); then
      MIN=$VALUE
    fi
    if ((VALUE > MAX)); then
      MAX=$VALUE
    fi
  done

  for EVENT in ${EVENTS[@]}
  do
    TOTAL=$((EVENT + TOTAL))
    if [ $CSV_BY_DEVICE = true ]
    then
      echo "$DATE,$EVENT" >> $ALL_EVENTS_CSV
    fi
  done

  MEDIAN_EVENT=$((${#EVENTS[*]}/2))
  # Sed command in BSD doesn't work with '\n' character
  SORTED_EVENTS=(`echo ${EVENTS[@]} | busybox tr ' ' '\n' | busybox sort -n`)

  if ((${#EVENTS[*]} > 0)); then
    MEAN=`busybox expr $TOTAL / ${#EVENTS[*]}`
    #MEAN=$[busybox expr $TOTAL / ${#EVENTS[*]}]
    MEDIAN=${SORTED_EVENTS[${MEDIAN_EVENT}]}
  else
    MEAN=0
    MEDIAN=0
    MIN=0
  fi

  echo ""
  echo "COUNT: ${#EVENTS[*]}"
  echo "TOTAL: $TOTAL"
  echo "----------------"
  echo "MEAN: $MEAN"
  echo "MEDIAN: $MEDIAN"
  echo "MAX: $MAX"
  echo "MIN: $MIN"
  echo ""

  if [ $PRINT_ONLY = true ]
  then
    echo "# Printed output only."
  else
    echo "# Appending to csv file: $OUTPUT_CSV"
    echo "$DATE,$BUILD_LABEL,$MEAN,$MEDIAN,''" >> $OUTPUT_CSV
  fi
}

# Number of args
if [ $# -eq 1 ]
then
  PRINT_ONLY=true
elif [ $# -eq 3 ]
then
  PRINT_AND_CSV=true
elif [ $# -eq 4 ]
then
  PRINT_AND_CSV=true
  CSV_BY_DEVICE=true
  mkdir $4/$2
else
  usage
  exit 0
fi

count $1 $2 $3 $4/$2/event.csv
if [ $CSV_BY_DEVICE = true ]
then
  NUM_DEVICES=0
  cd $1
  for DEVICE in $(ls -d *5555)
  do
    let NUM_DEVICES=$NUM_DEVICES+1
    count $1/$DEVICE $2 $4/$DEVICE.csv $4/$2/$DEVICE'_events.csv'
    echo "$DEVICE,$MEAN,$MEDIAN" >> $4/$2/'devices.csv'
  done
  echo "$2,$NUM_DEVICES" >> $4/'num_devices.csv'
  cp $4/$2/*.csv $4
fi
