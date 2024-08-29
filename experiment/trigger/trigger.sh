#!/bin/bash

USER_START=1
USER_END=13

# centralized, federated, decentralized
ARCH="centralized"
# centralized, distributed
ARRIVAL="centralized"
# floating-point-operation-sine, resize-image
WORKLOAD="resize-image"
CONFIG_LOCUST="config/locust/${ARCH}/cpu-${ARRIVAL}.json"
CONFIG_PROM="config/prom/${ARCH}/config_prom.json"
ANSIBLE_PATH="/home/thl/edge-cloud-continuum-openfaas/deployment/ansible"

function log() {
    timestamp=`date "+%Y-%m-%d %H:%M:%S"`
    echo "[${USER}][${timestamp}][${1}]: ${2}"
}
function scale_to_one() {
    user=$1
    password=$2
    host=$3
    log "INFO" "Scale on ${host}"
    status_code=$(curl --location --silent --output /dev/null --write-out "%{http_code}" \
        "http://${user}:${password}@${host}/system/scale-function/${WORKLOAD}" \
        --header 'Content-Type: application/json' \
        --data '{
            "serviceName": "'"${WORKLOAD}"'",
            "namespace": "openfaas-fn",
            "replicas": 1
        }'
    )
    if [ "$status_code" -eq 202 ]; then
        log "INFO" "Scale successfully. Wait for 3 seconds ..."
        sleep 3
        log "INFO" "Done"
        return 0
    else
        return 1
    fi
}

function initialize_decentralized() {
    dirty=0

    scale_to_one "admin" "KNuOALKrKsSFtkOXucIX" "145.100.135.86:31112"
    ret_val=$? 
    if [ ${ret_val} -eq 0 ]; then
        dirty=1
    fi
    
    scale_to_one "admin" "IXuJycmvzEQWvGuQJnQr" "192.168.100.111:8080"
    ret_val=$? 
    if [ ${ret_val} -eq 0 ]; then
        dirty=1
    fi

    scale_to_one "admin" "IXuJycmvzEQWvGuQJnQr" "192.168.100.103:8080"
    ret_val=$? 
    if [ ${ret_val} -eq 0 ]; then
        dirty=1
    fi

    scale_to_one "admin" "IXuJycmvzEQWvGuQJnQr" "192.168.100.102:8080"
    ret_val=$? 
    if [ ${ret_val} -eq 0 ]; then
        dirty=1
    fi

    scale_to_one "admin" "fgHJzWYgeoOHkzeEBzRH" "192.168.100.105:8080"
    ret_val=$? 
    if [ ${ret_val} -eq 0 ]; then
        dirty=1
    fi

    if [ ${dirty} -eq 1 ]; then
        log "INFO" "Scale on somewhere. Wait 60 seconds..."
        sleep 60
        log "INFO" "Done"
    fi

}

function initialize_federated() {
    dirty=0

    scale_to_one "admin" "KNuOALKrKsSFtkOXucIX" "145.100.135.86:31112"
    ret_val=$? 
    if [ ${ret_val} -eq 0 ]; then
        dirty=1
    fi
    

    scale_to_one "admin" "IXuJycmvzEQWvGuQJnQr" "192.168.100.103:31112"
    ret_val=$? 
    if [ ${ret_val} -eq 0 ]; then
        dirty=1
    fi

    scale_to_one "admin" "fgHJzWYgeoOHkzeEBzRH" "192.168.100.105:31112"
    ret_val=$? 
    if [ ${ret_val} -eq 0 ]; then
        dirty=1
    fi

    if [ ${dirty} -eq 1 ]; then
        log "INFO" "Scale on somewhere. Wait 60 seconds..."
        sleep 60
        log "INFO" "Done"
    fi

}



function initialize_centralized() {
    dirty=0

    scale_to_one "admin" "KNuOALKrKsSFtkOXucIX" "145.100.135.86:31112"
    ret_val=$? 
    if [ ${ret_val} -eq 0 ]; then
        dirty=1
    fi

    if [ ${dirty} -eq 1 ]; then
        log "INFO" "Scale on somewhere. Wait 60 seconds..."
        sleep 60
        log "INFO" "Done"
    fi

}


function try_invocation () {
    if [[ ${ARCH} = "centralized" ]]; then
        host="145.100.135.86:31112"
    elif [[ ${ARCH} = "federated" ]]; then
        host="192.168.100.105:31112"
    elif [[ ${ARCH} = "decentralized" ]]; then
        host="192.168.100.105:8080"
    fi

    curl http://${host}/function/${WORKLOAD}
    log "INFO" "Sleep 5 seconds ..."
    sleep 5
    log "INFO" "Done"
}

main() {


    for user_cnt in $(seq ${USER_START} ${USER_END}); do

        #initialize_decentralized
        # initialize_federated
        initialize_centralized
        try_invocation

        python3 main.py -c case${user_cnt} -l ${CONFIG_LOCUST} -p ${CONFIG_PROM}
        
        mkdir -p result/${ARCH} 2> /dev/null
        ls *.csv 2>/dev/null && mv *.csv result/${ARCH}
    done

}

main "$@"
