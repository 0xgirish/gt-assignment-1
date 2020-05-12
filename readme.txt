## Author: Girish Kumar (2016csb1040@iitrpr.ac.in)

Requirements:
---------------
- python 3.7
- numpy
- pytest

How to compile/run:
--------------------

> install dependencies
	$ pip install -r requirements.txt

> run testcases
	$ python -W ignore main.py --q question-number --testcase path/to/testcase/dir

> You can run multiple questions at the same time
e.g $ python -W ignore main.py --q 1 1 2 3 --testcase testdir/test.game/test.1 testdir/test.game/test.2 testdir/test.msne/test.1 testdir/test.msne/test.0

above command will run questions with following testcases

	question	|	testcase
----------------------------------------------
	   1		|	testdir/test.game/test.1
----------------------------------------------
	   1		|	testdir/test.game/test.2
----------------------------------------------
	   2		|	testdir/test.msne/test.1
----------------------------------------------
	   3		|	testdir/test.msne/test.0
----------------------------------------------
