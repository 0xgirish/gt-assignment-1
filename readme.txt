## Author: Girish Kumar (2016csb1040@iitrpr.ac.in)

Requirements:
---------------
- python 3.7
- numpy
- pytest

input format:
-------------
> for questions 1, 2, 3
  Program excepts a direactory which contains two files, meta.txt and utility.csv

    meta.txt format:
	---------------
	> Any line which starts with a # is a comment and will be ignored
	> First uncommented line represents number of players
	> Next n lines represents strategy profiles of players {1,2, ..., n}

	utility.csv format:
	------------------
	> First line contains indexes. e.g. s1, s2, u1, u2
	> rest of the lines represents mapping of strategy vector to utilities of players
	> e.g. utility.csv

	| s1, s2, u1, u2
	| a, x, 2, -2
	| a, y, 0, 0
	| b, x, -1, 1
	| b, y, 3, -3
	
    > in above example utility.csv file, when player 1 & 2 plays strategies a & x respectively
	> then player 1 & 2 gets utility of 2 & -2 respectively

> for question 4
  Program excepts a direactory which contains two files, meta.txt and utility.csv

	meta.txt format:
	---------------
	> Any line which starts with a # is a comment and will be ignored
	> First uncommented line represents number of players
	> Next n uncommented lines represents type set of all the players {1, 2, ..., n}
	> Last uncommented lines represents outcome set of the mechanism design setting


	utility.csv format:
	-----------------
	> First line contains indexes. e.g. Outcome, Ѳ1, Ѳ2, U1, U2
    > rest of the lines represents mapping of outcome and Ѳ to utilities of players
    > e.g. utility.csv

    | Outcome, Ѳ1, Ѳ2, U1, U2
    | x, a1, a2, 100, 0
    | x, a1, b2, 100, 0
    | y, a1, a2, 50, 50
    | y, a1, b2, 50, 50
    | z, a1, a2, 0, 100
    | z, a1, b2, 0, 25

    > in the above example utility.csv file, when the outcome is 'x' and player 1 & 2 has types a1, a2 respectively
    > then player 1 & 2 gets utility of 100, 0 respectively

Note: for more examples see testdir/test.game and testdir/test.msne direactories


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
