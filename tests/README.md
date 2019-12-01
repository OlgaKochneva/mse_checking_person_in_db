## Running tests

In `testing` use `py.test -v` to run testing and `python clean.py` to clear directory from test generators products.

Tested:
1) correct behavior of the program if it accepts an invalid format file
(expected correct shutdown without video processing);
2) correct behavior of the program if it accepts file which doesn't exist
(expected correct shutdown without video processing);
3) the quality of scanning faces in the frame (one parameter of test case is the quality threshold);
4) the quality of comparing faces (one parameter of test case is the quality threshold).