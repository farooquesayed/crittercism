#!/bin/bash
######################################################
# Copyright (C) Crittercism Inc. All Rights Reserved
#
######################################################
#Exports to python test framework
CONFIG_FILE=
export TEST_TYPE=
export LOG_DIR=
export BROWSER="firefox"

#Constants
DIR=/usr/lib/python2.6/site-packages/crittercism-test
LOG_DIR=
PARALLEL_PROCESS=
CI="NO"
VERBOSITY=
OUTPUT_STRING="Running "
PORT=$(($RANDOM + 2000)) # First 2000 ports are reserved somehow and increasing the number by 2k


###########################Function Defination #########################
function removeOldLogFiles() {
    echo "Cleaning up the log file from previous run : rm -f ${LOG_DIR}/*${TEST_TYPE}.log"
    # Logger should have an option to do that for us. Doing it temporarily
    $(rm -f ${LOG_DIR}/*${TEST_TYPE}.log ${LOG_DIR}/failed-test.txt ${LOG_DIR}/*xml ${LOG_DIR}/screenshots/*png )
}

function startSeleniumHub() {

     #PORT=$(grep selenium_hub_port ${CONFIG_FILE} | sed 's/selenium_hub_port=//')
     if [ "X${CI}" == "XNO" ] ; then
         #Read the port number from config file to start the hub
	     echo "Starting the Selenium standalone server in background on port : ${PORT}"
         hubresponse=$(java -jar ${DIR}/bin/selenium-server-standalone-2.41.0.jar -port ${PORT} -Dwebdriver.chrome.driver=${DIR}/bin/chromedriver 2>&1 > ${LOG_DIR}/seleniumhub_${PORT}_${TEST_TYPE}.log) &
         echo ${hubresponse} >>  ${LOG_DIR}/seleniumhub_${PORT}_${TEST_TYPE}.log
         sleep 5
     fi
}

function isSeleniumServerRunning(){

    # Make sure selenium Server is running before starting the test
    if [ $(echo quit | telnet 0 ${PORT} 2>&1 | grep -c 'Connection refused') == "1" ] ; then
        echo "[FATAL]: Selenium Server not running at localhost:${PORT}. Hence quitting the test";
        exit 1
    fi
    echo "Selenium Server is running on localhost:${PORT}"

}
function runTest() {
    # Create the log folder incase it is not present
    mkdir -p ${LOG_DIR}/screenshots
    if [ "X${CI}" == "XNO" ] ; then
        isSeleniumServerRunning
    fi
    #EXEC_CMD="${BIN} ${DIR} --with-xunit --xunit-file=$LOG_DIR/nosetests.xml $TEST_TYPE_ARG  ${PARALLEL_PROCESS_ARG} -v --debug-log=$LOG_DIR/debug.log"
    EXEC_CMD="${BIN} ${DIR}/tests*/*/*py --with-xunit --xunit-file=$LOG_DIR/nosetests.xml $TEST_TYPE_ARG  ${PARALLEL_PROCESS_ARG} -v "
    echo "Executing test on ${BROWSER} : ${EXEC_CMD}"
    echo "${OUTPUT_STRING} [${TEST_TYPE} test] ..."
    
    # Actually Executing the test and redirecting stdout to stderr as shell buffer stdout making it non-interactive
    output=$(${EXEC_CMD} 1>&2)
    exitCode=$?
}

function stopSeleniumHub() {

     if [ "X${CI}" == "XNO" ] ; then
         ps aux |grep java.*${PORT}|grep -v grep|awk '{print $2}' | xargs kill -15
     fi
}


function reRunFailedTest() {
    local RETRY_NUMBER=$1
    BIN="${BIN} --failed "
    testPassed=$(egrep -c 'errors="0".*failures="0"'  ${LOG_DIR}/nosetests.xml)
    if [[ ${testPassed} == 1 ]] ; then
        echo "All test passed. Nothing to re-run"
        exit 0
    fi
    echo "Rerunning the test after 5 Second ... "
    sleep 5
    #Copy the nosetest.xml from first run to preserve the numbers
    cp ${LOG_DIR}/nosetests.xml ${LOG_DIR}/nosetests.${RETRY_NUMBER}.xml
    runTest
}

function generateResultFile() {
  # Generate one XML file from all the run for hudson for proper accounting
  echo "Combile all the nosstest.xml files"   
}

if [ -e ./tests/ ]; then
  #DIR=./tests/*/*py
  DIR=./
fi

set -- `getopt "f:t:d:p:g:b:h:c:v" "$@"`

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
  echo "         -b To run a specific browser. default is firefox. other options are firefox/chrome/safari/etc"
  echo "         -c To run on a CI cluster"
  echo "         -v To enable 2 level verbosity on console"
  echo ""
  echo "  -h"
  echo "     Print this help"
  echo ""
  echo " Additional details can be found under this link"
  echo "   http://documentme.org"
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
    -b) BROWSER="$2";;
    -c) CI="$2";;
    -v) VERBOSITY="$2";;
    -h) usage ; exit 0;;
  esac
  shift
  shift
done

if [ "X${CONFIG_FILE}" == "X" ] ; then
	   CONFIG_FILE=./config/webtesting.conf
fi

if [[ "X${TEST_TYPE}" == "X" &&  "X${GENRE}" == "X" ]] ; then
       TEST_TYPE="smoke"
       TEST_TYPE_ARG=" -a ${TEST_TYPE}=TRUE "
elif [[ "X${TEST_TYPE}" == "XREGRESSION" || "X${TEST_TYPE}" == "Xregression" || "X${TEST_TYPE}" == "Xnightly" ]] ; then
	   TEST_TYPE_ARG=
else
	   TEST_TYPE_ARG=" -a ${TEST_TYPE}=TRUE"	   
fi

if [ "X${GENRE}" != "X" ] ; then
      TEST_TYPE=${GENRE}  
      TEST_TYPE_ARG=" -a genre=${GENRE} "
      OUTPUT_STRING="Running group "
fi

if [ "X${LOG_DIR}" == "X" ] ; then
	   LOG_DIR="./logs/"
fi

if [ "X${PARALLEL_PROCESS}" != "X" ] ; then
       PARALLEL_PROCESS_ARG=" --processes=${PARALLEL_PROCESS} --process-timeout=5000 "
fi

if [ "X${TEST_DURATION_HOURS}" == "X" ] ; then
       TEST_DURATION_HOURS=0.002
fi

if [ "X${BROWSER}" == "X" ] ; then
       BROWSER="firefox"
fi

if [ "X${VERBOSITY}" != "X" ] ; then
       VERBOSITY="-v -v"
fi

#Constructing executing command line
BIN="nosetests-2.7 ${VERBOSITY} --nocapture --with-id --id-file ${LOG_DIR}/failed-test.txt "
#BIN="/usr/bin/nosetests  --nocapture  --with-coverage --cover-html-dir=${LOG_DIR} --with-id --id-file ${LOG_DIR}/failed-test.txt "

# Export all the variable which needs to be accessed from python
export CONFIG_FILE
export TEST_TYPE
export LOG_DIR
export BROWSER
export PORT

#Start the Selenium Hub
startSeleniumHub

# Trying to re-run the failed test to see if they pass in this attempt
if [ "X${GENRE}" == "Xfailed" ] ; then
      OUTPUT_STRING="Re-Running failed test "
      reRunFailedTest
      reRunFailedTest
      reRunFailedTest
      exit 0
fi

# Remove the log files from previous runs
removeOldLogFiles

#Execute the test
runTest

# Terminate the hub. Not able to find a graceful way of killing it
stopSeleniumHub

# Masking the return code from nose test as we want the test failure to be yellow in hudson instead of RED
exit 0;
