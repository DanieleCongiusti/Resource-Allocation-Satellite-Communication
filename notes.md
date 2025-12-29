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

 

 	Values tested (x5 Tests each) for Throughput:

 	- N = 2, 6, 18

 	- K = "Large Number" (10^6)	-> To have NO MAX CEILING for any B value, except for B = 2

 	- T = 80/5 (16) ms

 	- S between \[4, 1036]B

 

 	We are focusing on N because it's an important factor in determining the overall throughput of the system, more so than the others

 	We expect to have a Throughput increasing at roughly the same rate as N

 	Results:

 	-----------------------

 	Values tested ("") for Queue Length:

 	- T = (16, 8, 4)ms

 	- N = 18

 	- K = "Small Number" (1)	-> To have a VERY LOW CEILING for any B value to focus on the queuing aspect

 	- S ...



Degeneracy:

 



Continuinty:



\*\*\*TO BE DEFINED (help with Prof's Slides) AND DONE\*\*\*

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
* S, took inspiration by M2M/IoT networks used in "remote monitoring" that connect devices in remote areas that rely over satellite communications

 	SOURCE: https://iris.cnr.it/bitstream/20.500.14243/339013/1/prod\_380288-doc\_133133.pdf		\[PG. 3/9, CoAP Protocol]

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

