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

 	The process should not crash if setting factors and parameters at extreme values

 

 	Values tested:

 	- N = 0

 	- K = 0

 	- T = 0

 	- S = \[10^6, 10^7]

 

 	These are "absurd values" for each case to see if the the program still works

\_\_\_\_\_\_\_\_\_\_\_\_

Continuinty:

 	Results should not vary much if the values for each factor and parameter vary little

 

 	Values tested (x30 Tests each) for Throughput:

 	- N = 2, 3, 4, 5, 6

 	- K = "Large Number" (100)	-> To have NO MAX CEILING for any B value, except for B = 2

 	- T = 80/5 (16) ms

 	- S between \[4, 100]B

 

  	-----------------------

 	Values tested ("") for Queue Length:

 	- T = (16, 15, 14, 13, 12)ms

 	- N = 18

 	- K = "Small Number" (1)	-> To have a VERY LOW CEILING for any B value to focus on the queuing aspect

 	- S ...



 	These are increment gradually to verify that the output results do not change drastically from each configuration



**NB**: *The test results are saved in a specific folder separate from "simulation results"*

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

**CALIBRATION \& EXPERIMENT DESIGN**

Factors:

* N: { 8, 12, 16, 20, 24 }
* K: { 10, 20, 50, 100, 1000 }



\*\*\*WRITE THE LOGIC BEHIND THE VALUES OF EACH FACTOR\*\*\*



---

Parameters:

* B, this has been provided to us by the project's specs
* S, this has been choses based on the project's specific for M, where M = 100\*K^(log\_2(B)-1), in particular:

 	when B=2 the M is ALWAYS M=100 because the exponent will be 0, therefore it doesn't matter what K is, M will be this constant value

 	and since we want the packets to always be transmittable at any B

* T, this has been computed in function of S and the possible Throughput that our system could have in the context of M2M/IoT systems.

 	We used the following sources to take an example for the Throughput:

 		- https://www.iotitaly.net/wp-content/uploads/2017/07/TEC\_Communication\_Technologies\_M2M\_IoT\_Ver\_12\_0\_-3rd-July-2017.pdf 	\[pg 32, Table2 -> LTE Cat-M1]

 		- https://www.1nce.com/it-it/risorse/iot-knowledge-base/cos-e-lte-cat-1 							\[LTE Cat-M2, used for IoT operations -> Data Rate: 2Mbps=0.25MBps=250KBps]

 	Since these values represent peak physical-layer capabilities, and not the effective throughput experienced by M2M/IoT applications,

 	a margin was assumed between the maximum data rate supported by the technology and the achievable system throughput.

 	Considering the small packet sizes of typical of M2M/IoT systems, the modeled system throughput

 	was therefore set to 200 KBps.

 

 	We then used this possible Throughput value and S's range to then compute the average of T, the rate of packet generation

---

.Warm-Up Duration:

&nbsp;	- Add the Statistics to collect the "Moving Average" for Throughput and Queue Length values 

&nbsp;	- Gather Test results 

&nbsp;	- Infer from the results how much Warm-Up time we need to consider before collecting the proper results 

&nbsp;		NB: IF the "Moving Average" is constant from the start, NO warm up period needed	



.Simulation Time Duration:

&nbsp;	The simulation time was selected to ensure a sufficiently large sample size, allowing the application of the Central Limit Theorem for the statistical analysis of aggregated metrics.

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_







