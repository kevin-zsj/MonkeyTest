#!/system/bin/sh
i=72;
while [[ $i -gt 0 ]];do
	echo "time " $i "start...";
	dt=`date +%H%M%S`;

	pid_logcat=`ps -A|grep logcat|busybox awk '{print $2}'`
	for id3 in $pid_logcat 
	do 
   		kill -9 $id3 
   		echo "kill logcat" 
	done
	logcat >> /mnt/sdcard/logcat_$dt.txt &

	monkey --ignore-timeouts --ignore-security-exceptions --pkg-blacklist-file /sdcard/black.txt --throttle 500 -s $dt -v -v -v 125000 >> /sdcard/monkey_log_$dt.txt;
	((i--));
	sleep 10;
	echo "time " $i "finished";
done;
