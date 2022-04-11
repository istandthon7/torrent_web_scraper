#!/bin/bash

# transmission setttings.json다음 설정을 변경한다.
# 전체경로를 사용해야 한다.
# "script-torrent-done-enabled": true,
# "script-torrent-done-filename": "/transmission_script/torrent_done.sh",

export PYTHONIOENCODING="utf8"
export LANG="ko_KR.UTF-8"
export LANGUAGE="ko_KR.UTF-8"
export LC_ALL="ko_KR.UTF-8"

log_file="/tmp/transmission.log"

echo "download dir: $TR_TORRENT_DIR" >> $log_file
echo "download name: $TR_TORRENT_NAME" >> $log_file
echo "$0"

if [ "$TR_TORRENT_DIR" == *"skip_dir" ]; then

	echo 'skipped notification' >> $log_file
else
	echo "notification step 1" >> $log_file

	if [[ "$TR_TORRENT_DIR" == *"tvshow"* ]]; then
		cd /transmission_script && ./rename_season_transmission.py "$TR_TORRENT_NAME" >> $log_file

		echo "notification step 2" >> $log_file

	fi
fi

