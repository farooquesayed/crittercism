#!/bin/bash
######################################################
# Copyright (C) Yahoo!, Inc. All Rights Reserved
#
######################################################
#Exports to python test framework
CONFIG_FILE=
export TEST_TYPE=
export LOG_DIR=
export DEPLOYMENT="VM"

#Constants
DIR=/home/y/lib/python2.6/site-packages/yopenstackqe_tests
LOG_DIR=
PARALLEL_PROCESS=
TEST_DURATION_HOURS=
OUTPUT_STRING="Running "


###########################Function Defination #########################
function removeOldLogFiles() {
    echo "Cleaning up the log file from previous run : rm -f ${LOG_DIR}/*${TEST_TYPE}.log"
    # Logger should have an option to do that for us. Doing it temporarily
    $(rm -f ${LOG_DIR}/*${TEST_TYPE}.log ${LOG_DIR}/failed-test.txt )
}

function runTest() {
    # Create the log folder incase it is not present
    mkdir -p ${LOG_DIR}
    
    #EXEC_CMD="$BIN $DIR --with-xunit --xunit-file=$LOG_DIR/nosetests.xml $TEST_TYPE_ARG  ${PARALLEL_PROCESS_ARG} -v --debug-log=$LOG_DIR/debug.log"
    EXEC_CMD="$BIN $DIR --with-xunit --xunit-file=$LOG_DIR/nosetests.xml $TEST_TYPE_ARG  ${PARALLEL_PROCESS_ARG} -v "
    echo "Executing command : ${EXEC_CMD}"
    echo "${OUTPUT_STRING} [${TEST_TYPE} test] ..."
    
    # Actually Executing the test and redirecting stdout to stderr as shell buffer stdout making it non-interactive
    output=$(${EXEC_CMD} 1>&2)
    exitCode=$?
}

function reRunFailedTest() {
    local RETRY_NUMBER=$1
    BIN="${BIN} --failed "
    testPassed=$(egrep -c 'errors="0".*failures="0"'  ${LOG_DIR}/nosetests.xml)
    if [[ ${testPassed} == 1 ]] ; then
        exit 0
    fi
    #Copy the nosetest.xml from first run to preserve the numbers
    cp ${LOG_DIR}/nosetests.xml ${LOG_DIR}/nosetests.${RETRY_NUMBER}.xml
    echo "Rerunning the test after 1 minute ... "
    sleep 60
    runTest
}

function generateResultFile() {
  # Generate one XML file from all the run for hudson for proper accounting
  echo "Combile all the nosstest.xml files"   
}

function get_param() { 
  local param
  export get_param_section=$1
  export get_param_key=$2
  param=$(perl -e '$_=join "", <>;  print /\[\Q$ENV{get_param_section}\E\](?:[^\[]+)+^\s*\Q$ENV{get_param_key}\E\s*=\s*(.*)/m' "$CONFIG_FILE")
  if [[ "x$param" = "x" ]] ; then
     echo "Can't find '$2' in section '$1' in '$CONFIG_FILE'";
     exit 1;
  fi
  echo "$param"
}

if [ -e ./yopenstackqe_tests/yopenstackqe_tests/ ]; then
  DIR=./yopenstackqe_tests/
fi

set -- `getopt "s:x:f:t:d:p:g:n:c:e:i:v:h" "$@"`

#############################################################################
#                      Function to print usage                              #
#############################################################################
usage () {
  echo "NEED TO BE UPDATED Usage $0 [Options]"
  echo "  Options are:"
  echo "         -h"
  echo "         -f config file on which you want to run test"
  echo "         -t test run.Eg are smoke, regression, functional, etc. Default is smoke"
  echo "         -d log directory default /home/y/logs/yopenstackqe_tests/"
  echo "         -p Parallel process count. Nosetest does not generate noseunit.xml file when shoose this option"
  echo "         -g To run a specific group or genre"
  echo "         -n Test Duration in hours to run long running test"
  echo "         -i new image version uploaded for testing"
  echo "         -v current cloud-init version expected in the new image uploaded"
  echo "         -c To generate the code coverage numbers"
  echo "         -e Deployment or Environment type to run the test against (VM - Virtual Machines /BM - Bare Metal / NGN - Next Generation Network)"
  echo ""
  echo "  -h"
  echo "     Print this help"
  echo ""
  echo " Additional details can be found under this link"
  echo "   http://twiki.corp.yahoo.com/view/Yahoo/OpenStackQeAutomationNotes#How_to_Run_Automation"
  echo ""
}

while [ $# -ge 1 ]
do
  case "$1" in
    -f) CONFIG_FILE="$2";;
    -t) TEST_TYPE="$2";;
    -d) LOG_DIR="$2";;
    -p) PARALLEL_PROCESS="$2";;
    -g) GENRE="$2";;
    -n) TEST_DURATION_HOURS="$2";;
    -c) COVERAGE="$2";;
    -i) IMAGE_UPLOADED="$2";;
    -v) CLOUDINIT_VERSION="$2";;
    -e) DEPLOYMENT="$2";;
    -h) usage ; exit 0;;
  esac
  shift
  shift
done

if [ "X${CONFIG_FILE}" = "X" ] ; then
	   CONFIG_FILE=/home/y/conf/yopenstackqe_tests/cli.conf.qe4
fi

if [[ "X${TEST_TYPE}" = "X" &&  "X${GENRE}" == "X" ]] ; then
       TEST_TYPE="smoke"
       TEST_TYPE_ARG=" -a ${TEST_TYPE}=TRUE "
elif [[ "X${TEST_TYPE}" = "XREGRESSION" || "X${TEST_TYPE}" = "Xregression" ]] ; then
	   TEST_TYPE_ARG=
else
	   TEST_TYPE_ARG=" -a ${TEST_TYPE}=TRUE"	   
fi

if [ "X${GENRE}" != "X" ] ; then
      TEST_TYPE=${GENRE}  
      TEST_TYPE_ARG=" -a genre=${GENRE} "
      OUTPUT_STRING="Running group "
fi

if [ "X${LOG_DIR}" = "X" ] ; then
	   LOG_DIR="/home/y/logs/yopenstackqe_tests/"
fi

if [ "X${PARALLEL_PROCESS}" != "X" ] ; then
       PARALLEL_PROCESS_ARG=" --processes=${PARALLEL_PROCESS} --process-timeout=5000 "
fi

if [ "X${TEST_DURATION_HOURS}" = "X" ] ; then
       TEST_DURATION_HOURS=0.002
fi

#Constructing executing command line

BIN="/home/y/bin/nosetests  --nocapture --with-id --id-file ${LOG_DIR}/failed-test.txt "

#BIN="/usr/bin/nosetests  --nocapture  --with-coverage --cover-html-dir=${LOG_DIR} --with-id --id-file ${LOG_DIR}/failed-test.txt "


# Export all the variable which needs to be accessed from python
export CONFIG_FILE
export TEST_TYPE
export LOG_DIR
export TEST_DURATION_HOURS
export IMAGE_UPLOADED
export CLOUDINIT_VERSION
export DEPLOYMENT


removeOldLogFiles

if [ -n "$COVERAGE" ]; 
then
    export OS_USERNAME="$(get_param 'compute' 'username')"
    export OS_PASSWORD="$(sudo keydbgetkey "$OS_USERNAME")"
    export OS_TENANT_NAME="$(get_param 'compute' 'tenant_name')"
    export OS_AUTH_URL="$(get_param 'osNative' 'OS_AUTH_URL')"
    ssh_user="$(get_param 'compute'  'yahoo_ssh_user')"
    ssh_key="$(get_param 'compute'  'key_filename')"

    hosts="$(nova host-list | perl -ne 'print /\| ([\w\.]+) +\| (?:compute|scheduler)/, " "')"
    for a in $(echo $hosts); do 
        echo $a
        ssh -i "$ssh_key" "$ssh_user@$a" "sudo bash -c '
    rm -rf /home/y/logs/openstack-coverage/*
    chmod 777 /home/y/logs/openstack-coverage
    yinst set openstack_nova_common_conf.coverage=1
    /sbin/initctl emit all_os_stop; /sbin/initctl emit all_os_start
    '"
    done

    sleep 30
    runTest

    for a in $(echo $hosts); do
        echo $a
        ssh -i "$ssh_key" "$ssh_user@$a" "sudo bash -c '
    yinst set openstack_nova_common_conf.coverage=0
    /sbin/initctl emit all_os_stop; /sbin/initctl emit all_os_start
    cd /home/y/logs/openstack-coverage
    cp */.coverage* ./
    coverage -c
    coverage xml -o coverage.$a.xml -i
    chown $ssh_user coverage.*.xml'"
        scp -r -i "$ssh_key" -o ConnectTimeout=5 -o StrictHostKeychecking=no  "$ssh_user@$a":/home/y/logs/openstack-coverage/"coverage.$a.xml" "$LOG_DIR"/
    done
else
    runTest
fi


# Trying to re-run the failed test to see if they pass in this attempt
#reRunFailedTest
#reRunFailedTest
#reRunFailedTest

# Masking the return code from nose test as we want the test failure to be yellow in hudson instead of RED

exit 0;
