#! /bin/bash

trap ctrl_c INT

function ctrl_c() {
        echo "** Trapped CTRL-C"
        finished=1
}

################## VARS DECL AND INIT ##############
echo Start Wi-Fi DUMP gate 

################## INTERFACE INITIALIZATION #################
#iw dev
sudo iw phy phy0 interface add mon0 type monitor
sudo iw dev wlxe0469aa531bc del
sudo ifconfig mon0 up


finished=0
time=$(date +"%H%M")
data_day=$(date +"%y%m%d")
path="data/$data_day/"
timeout=60
mkdir -p $path

################### END VAR DECL ##############

while ! ((finished))
	do
	time=$(date +"%H%M")
	text_file="WiFi-$time.txt"
	path_full="$path$text_file"
	echo New file name $path_full, w/ timeout $timeout sec

	###### WIFI DUMP ######
	tshark -S -l -i mon0 -Y 'wlan.fc.type_subtype eq 4' \
	-T fields -e frame.time -e wlan.ta_resolved -e wlan.sa -e wlan_radio.signal_dbm -e wlan.ssid \
	-E separator="|" -a duration:$timeout > $path_full
done
####### END #######

echo Done