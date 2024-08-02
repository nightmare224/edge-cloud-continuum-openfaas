
function log() {
  timestamp=`date "+%Y-%m-%d %H:%M:%S"`
  echo "[${USER}][${timestamp}][${1}]: ${2}"
}

main() {
    interface=$(ip route show default | awk '{print $5}')
    log "INFO" "Interface: ${interface}"
    tc qdisc del dev ${interface} root 2>/dev/null
    # sudo tc qdisc add dev ${interface} root pfifo
    sudo tc qdisc show dev ${interface}

}

main "$@"