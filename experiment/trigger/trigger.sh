#!/bin/bash

USER_START=1
USER_END=11

# centralized, federated, decentralized
ARCH="decentralized"
CONFIG_LOCUST="config/locust/${ARCH}/cpu.json"
CONFIG_PROM="config/prom/${ARCH}/config_prom.json"
ANSIBLE_PATH="/home/thl/edge-cloud-continuum-openfaas/deployment/ansible"

function log() {
    timestamp=`date "+%Y-%m-%d %H:%M:%S"`
    echo "[${USER}][${timestamp}][${1}]: ${2}"
}

main() {


    for user_cnt in $(seq ${USER_START} ${USER_END}); do
        # deploy on cloud and clean all edge
        # ansible-playbook -i ${ANSIBLE_PATH}/inventory/federated.ini ${ANSIBLE_PATH}/experiment.yaml
        
        # sleep 30
        # trigger the trigger point once to prevent cold start, and also to gave a record of fastest trigger
        sleep 3
        curl http://192.168.100.105:8080/function/floating-point-operation-sine
        # curl http://192.168.100.102:8080/function/sorter
        # curl http://192.168.100.103:8080/function/sorter
        # curl http://192.168.100.111:8080/function/sorter
        # curl http://145.100.135.86:31112/function/sorter
        sleep 3
        #
        python3 main.py -l ${CONFIG_LOCUST} -p ${CONFIG_PROM} -c case${user_cnt}
        mkdir -p result/${ARCH} 2> /dev/null
        ls *.csv 2>/dev/null && mv *.csv result/${ARCH}
    done

}

main "$@"
