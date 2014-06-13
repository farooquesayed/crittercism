Selenium Web Testing Framework built using nosetest
===========
1) Install pip 
2) Install list of packages mentioned in ./pkg folder
pip install -r pkg/requirements.txt

3) Run the test against any browser
 ./scripts/test_runner.sh  
4) Run any set of test 
 ./scripts/test_runner.sh -t regression/smoke
5) Re-run failed test automatically
 ./scripts/test_runner.sh  -f ./config/webtesting.conf  -g failed
