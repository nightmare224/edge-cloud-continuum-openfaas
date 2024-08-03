#!/bin/bash


DELAY_CLASS1="10ms"
DELAY_CLASS2="20ms"
DELAY_CLASS3="60ms"
DELAY_CLASS4="0ms"

function filter_to_class() {
    log "INFO" "Apply filter class$3 on interface $1 for ip $2 "
    tc filter add dev $1 parent 1:0 protocol ip prio 1 u32 match ip dst $2 flowid 1:$3
}

# interface, ip
function filter_to_class1() {
    filter_to_class $1 $2 "1"
}

function filter_to_class2() {
    filter_to_class $1 $2 "2"
}

function filter_to_class3() {
    filter_to_class $1 $2 "3"
}

function filter_to_class4() {
    filter_to_class $1 $2 "4"
}

function default_filter_to_class3() {
    tc filter add dev $1 parent 1:0 protocol ip prio 100 u32 match u32 0 0 flowid 1:3
}

function default_filter_to_class4() {
    tc filter add dev $1 parent 1:0 protocol ip prio 100 u32 match u32 0 0 flowid 1:4
}

function apply_filter() {
    # apply the filter
    local inventory_file=$1
    local group_name=$2
    local self_ip=$3
    local filter_func=$4
    hostnames=$(jq -e --arg group_name ${group_name} '.[$group_name].hosts' ${inventory_file})
    
    local ret_val=$?
    if [[ ${ret_val} != 0 ]]; then
        log "INFO" "No more cluster"
        return ${ret_val}
    fi
    for hostname in $(echo ${hostnames} | jq @sh | tr -d \'\"); do 
        # echo ${hostname}
        ip=$(jq -r --arg hostname ${hostname} '._meta.hostvars[$hostname].ansible_host' ${inventory_file})
        # echo ${ip}
        if [[ "${ip}" != "${self_ip}" ]]; then
            $filter_func ${interface} ${ip}
        fi
    done
}

function check_qdisc() {
    local interface=$1
    msg=$(tc qdisc show dev ${interface})
    if ! echo ${msg} | grep -q "qdisc netem 10: parent 1:1 limit 1000 delay ${DELAY_CLASS1}"; then
        return 1
    fi
    if ! echo ${msg} | grep -q "qdisc netem 20: parent 1:2 limit 1000 delay ${DELAY_CLASS2}"; then
        return 1
    fi
    if ! echo ${msg} | grep -q "qdisc netem 30: parent 1:3 limit 1000 delay ${DELAY_CLASS3}"; then
        return 1
    fi
}

function log() {
  timestamp=`date "+%Y-%m-%d %H:%M:%S"`
  echo "[${USER}][${timestamp}][${1}]: ${2}"
}

main() {
    inventory_file=$1
    self_ip=$2
    self_group=$3
    interface=$(ip route show default | awk '{print $5}')
    # interface="enp0s5"
    log "INFO" "IP: ${self_ip}, Group: ${self_group}, Interface: ${interface}"

    if check_qdisc ${interface}; then
        log "INFO" "The emulator has already applied"
        exit 0
    fi

    tc qdisc add dev ${interface} root handle 1:0 prio bands 4 2>&1 
    ret_val=$?
    if [[ ${ret_val} != 0 ]]; then
        log "ERROR" "Add root qdisc failed"     
        exit 1
    fi
    tc qdisc add dev ${interface} parent 1:1 handle 10:1 netem delay ${DELAY_CLASS1}
    tc qdisc add dev ${interface} parent 1:2 handle 20:1 netem delay ${DELAY_CLASS2}
    tc qdisc add dev ${interface} parent 1:3 handle 30:1 netem delay ${DELAY_CLASS3}
    # default class and filter (for client)
    tc qdisc add dev ${interface} parent 1:4 handle 40:1 netem delay ${DELAY_CLASS4}
    
    if [[ ${inventory_file} == "" ]]; then
        log "INFO" "No inventory file provided, all traffic is set to ${DELAY_CLASS4} delay."
        default_filter_to_class4 ${interface}
        exit 0
    fi

    # Is edge cluster
    if echo ${self_group} | grep -q "edge"; then
        log "INFO" "Apply filter for the edge node."
        # To other edge cluster
        cluster_id=1
        for (( ; ; )); do
            group_name="edge_cluster${cluster_id}"
            # same edge region
            if [[ "${group_name}" == "${self_group}" ]]; then
                filter_func="filter_to_class1"
            # different edge region
            else
                filter_func="filter_to_class2"
            fi
            # apply the filter
            apply_filter ${inventory_file} ${group_name} ${self_ip} ${filter_func}
            ret_val=$?
            if [[ ${ret_val} != 0 ]]; then
                break
            fi
            ((cluster_id++))
        done
        # To cloud cluster
        cluster_id=1
        for (( ; ; )); do
            group_name="cloud_cluster${cluster_id}"
            apply_filter ${inventory_file} ${group_name} ${self_ip} "filter_to_class3"
            ret_val=$?
            if [[ ${ret_val} != 0 ]]; then
                break
            fi
            ((cluster_id++))
        done
        log "INFO" "Default filter of edge is set to ${DELAY_CLASS4} delay."
        default_filter_to_class4 ${interface}
    # Is cloud cluster
    elif echo ${self_group} | grep -q "cloud"; then
        log "INFO" "Apply filter for the cloud node."
        # To edge cluster
        cluster_id=1
        for (( ; ; )); do
            group_name="edge_cluster${cluster_id}"
            apply_filter ${inventory_file} ${group_name} ${self_ip} "filter_to_class3"
            ret_val=$?
            if [[ ${ret_val} != 0 ]]; then
                break
            fi
            ((cluster_id++))
        done
        # To cloud cluster
        cluster_id=1
        for (( ; ; )); do
            group_name="cloud_cluster${cluster_id}"
            apply_filter ${inventory_file} ${group_name} ${self_ip} "filter_to_class1"
            ret_val=$?
            if [[ ${ret_val} != 0 ]]; then
                break
            fi
            ((cluster_id++))
        done
        log "INFO" "Default filter of cloud is set to ${DELAY_CLASS3} delay."
        default_filter_to_class3 ${interface}
    elif echo ${self_group} | grep -q "client"; then
        log "INFO" "Apply filter for the client node."
        # To edge cluster
        cluster_id=1
        for (( ; ; )); do
            group_name="edge_cluster${cluster_id}"
            apply_filter ${inventory_file} ${group_name} ${self_ip} "filter_to_class4"
            ret_val=$?
            if [[ ${ret_val} != 0 ]]; then
                break
            fi
            ((cluster_id++))
        done
        # To cloud cluster
        cluster_id=1
        for (( ; ; )); do
            group_name="cloud_cluster${cluster_id}"
            apply_filter ${inventory_file} ${group_name} ${self_ip} "filter_to_class3"
            ret_val=$?
            if [[ ${ret_val} != 0 ]]; then
                break
            fi
            ((cluster_id++))
        done
        log "INFO" "Default filter of client is set to ${DELAY_CLASS4} delay."
        default_filter_to_class4 ${interface}
    fi


}

main "$@"