#!/bin/bash

USER_START=0
USER_END=0

# centralized, federated, decentralized
ARCH="federated"
CONFIG_LOCUST="config/locust/${ARCH}/cpu.json"
CONFIG_PROM="config/prom/${ARCH}/config_prom.json"

function log() {
    timestamp=`date "+%Y-%m-%d %H:%M:%S"`
    echo "[${USER}][${timestamp}][${1}]: ${2}"
}

main() {


    for user_cnt in $(seq ${USER_START} ${USER_END}); do
        python3 main.py -l ${CONFIG_LOCUST} -p ${CONFIG_PROM} -c case${user_cnt}
        mkdir -p result/${ARCH} 2> /dev/null
        ls *.csv 2>/dev/null && mv *.csv result/${ARCH}
        # sleep 30
    done

}

main "$@"
