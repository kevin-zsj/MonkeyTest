@echo off
set local_path=%cd%

adb remount
echo Pushing Test tools ...
adb push %local_path%\startMonkey.sh /sdcard/
echo Pushing analysis tools ...
adb push %local_path%\event_counter.sh /sdcard/
echo Pushing black names ...
adb push %local_path%\data\black.txt /sdcard/
echo Run test ...
adb shell "sh /sdcard/startMonkey.sh >/dev/null 2>&1 &"

pause
