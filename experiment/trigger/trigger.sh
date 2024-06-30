#!/bin/bash

USER_MAX=4
CONFIG_LOCUST="config/locust/cpu.json"

# user_cnt="1"
# python3 main.py -l ${config_locust} -c case${user_cnt} -p config/config_prom.json

function log() {
    timestamp=`date "+%Y-%m-%d %H:%M:%S"`
    echo "[${USER}][${timestamp}][${1}]: ${2}"
}

main() {


    for user_cnt in $(seq ${USER_MAX}); do
        python3 main.py -l ${CONFIG_LOCUST} -c case${user_cnt}
        mv *.csv result/
        sleep 30
    done

}

main "$@"
