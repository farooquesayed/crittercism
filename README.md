Selenium Web Testing Framework built using nosetest
===========
1) Install pip <br>
2) Install list of packages mentioned in ./pkg folder<br>
<verbatim> pip install -r pkg/requirements.txt </verbatim> <br>
3) Run the test against any browser <br>
        <verbatim> ./scripts/test_runner.sh  </verbatim> <br>
4) Run any set of test <br>
       <verbatim>  ./scripts/test_runner.sh -t regression/smoke </verbatim> <br>
5) Re-run failed test automatically <br>
       <verbatim> ./scripts/test_runner.sh  -f ./config/webtesting.conf  -g failed </verbatim> 
