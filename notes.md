**OBJECTIVES**

1\.  Determine the performance of communication system, with actors Ground station and Terminals, given a specific protocol, where various varying terminals and transmittable bytes at a time

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

**KPI**

1. Determine **throughput** based on N, K, T values
2. Determine **average queue length** based on "" "" ""

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

**IMPLEMENTATION -> VERIFICATION TESTS**

Consistency:

 	Results should scale in accordance to the increase of the values of each Factor/Parameter

 

 	Values tested (x30 Tests each) for Throughput:

 	- N = 2, 4, 8, 16, 32

 	- K = "Large Number" (100)	-> To have NO MAX CEILING for any B value, except for B = 2

 	- T = 80/5 (16) ms

 	- S between \[4, 100]B

 

 	We are focusing on N because it's an important factor in determining the overall throughput of the system, more so than the others

 	We expect to have a Throughput increasing at roughly the same rate as N

 	Results:

 	-----------------------

 	Values tested ("") for Queue Length:

 	- T = (16, 8, 4, 2, 1)ms

 	- N = 18

 	- K = "Small Number" (1)	-> To have a VERY LOW CEILING for any B value to focus on the queuing aspect

 	- S ...



\_\_\_\_\_\_\_\_\_\_\_

Degeneracy:

&nbsp;	The process should not crash if setting factors and parameters at extreme values 

&nbsp;	

&nbsp;	Values tested: 

&nbsp;	- N = 0

&nbsp;	- K = 0

&nbsp;	- T = 0

&nbsp;	- S = \[10^6, 10^7]

 

&nbsp;	These are "absurd values" for each case to see if the the program still works 

\_\_\_\_\_\_\_\_\_\_\_\_

Continuinty:

&nbsp;	Results should not vary much if the values for each factor and parameter vary little

&nbsp;	

&nbsp;	Values tested: 

&nbsp;	- N = 2, 3, 4, 5, 6

&nbsp;	- K = 10, 11, 12, 13, 14

&nbsp;	- T = (10, 11, 12, 13, 14)ms

&nbsp;	- S between \[4, 100]B



&nbsp;	These are increment gradually to verify that the output results do not change drastically from each configuration

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

**CALIBRATION \& EXPERIMENT DESIGN**

Factors:

* N,
* K,
* T,



\*\*\*TO BE DEFINED THROUGH TESTING\*\*\*



---

Parameters:

* B, this has been provided to us by the project's specs
* S, this has been choses based on the project's specific for M, where M = 100\*K^(log\_2(B)-1), in particular: 

&nbsp;	when B=2 the M is ALWAYS M=100 because the exponent will be 0, therefore it doesn't matter what K is, M will be this constant value

&nbsp;	and since we want the packets to always be transmittable at any B

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

