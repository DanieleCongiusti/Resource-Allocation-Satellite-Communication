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



For ***N***, we initially started by looking at the max and min possible terminals that can transmit considering B and C (Scheduling Capacity). From this we obtained that the range of possible transmittable Terminals is between \[4, 32]

 	But the likeliness of how many terminals will transmit isn't uniformally distributed since, just an example, the likeliness of having 4 terminals generating B = 16 (4x16 = 64 => Max Capacity reached, no more space for other

 	terminals to transmit) is much more likely than 32 B = 2. Also, the B get ordered in decresing order when received, therefore it's sufficient that out of N terminals 4 random ones generate B = 16 and all the rest would be

 	irrelevant.

 	So, we studied the probability of having the same value of B multiple times (an RV with Binomial Distribution) and quickly demonstrated that as N grows the most dominant case would eventually become 4 B = b, where b can be

 	any of { 2, 4, 8, 16 }, therefore the ones transmitting would be those with b = 16.

 	From this, we determined the upper limit for our values, 24, since the probability of having 4 B = b is approximately 1, so anything above it didn't make sense testing. And from there we picked the rest of the values decreasing

 	by a factor of 4 each time since the likeliness of the dominant case decreased enough to hope for meaningful results to prove our conclusions on N.



 	CGPT: "Since the GS allocates bearers starting from the largest B and the schedule has capacity 64 slots, the schedule is filled by four B=16 bearers whenever at least four active terminals report B=16.

 		Under uniform B, the probability of this event increases rapidly with N; therefore, for sufficiently large N, the typical number of transmitting terminals per timeframe approaches 4."



For ***K***, we picked values for it based on the expected bytes generated per timeframe (Btf) given S and T. From that, we picked the values for K by which M would be large enough that ALL Btf from a terminal would pass for a given

 	value of B, which is one of the factors that determines M. We start from a value of K which would compute M by which it would never suffice for the Btf and from there picked those which would give an M that would suffice

 	for B = 16, B >= 8 and so forth. Then we also picked some larger values to demonstrate how increasing K does not provide any meaningful improvements after K is large enough so that even for the case B = 4 M would suffice

 	for Btf. (We do not consider B = 2 since in this case for any value of K, M = 100).



---

Parameters:

* B, this has been provided to us by the project's specs
* S, this has been choses based on the project's specific for M, where M = 100\*K^(log\_2(B)-1), in particular:

 	when B=2 the M is ALWAYS M=100 because the exponent will be 0, therefore it doesn't matter what K is, M will be this constant value

 	and since we want the packets to always be transmittable at any B

* T, this has been computed in function of S and the possible Throughput that our system could have in the context of M2M/IoT systems.

 	range so that the impact of K on throughput can be observed while keeping backlog-induced burstiness within reasonable bounds.



 	We then used this possible Throughput value as a reference to then determine the value for T by checking the value of the Throughput through simple testing 

	and came to the value of T by which is closest to the reference value chosen (200KBps): T = 0.0025s

---

.Warm-Up Duration:

&nbsp;	- Add the Statistics to collect the "Moving Average" for Throughput and Queue Length values 

&nbsp;	- Gather Test results 

&nbsp;	- Infer from the results how much Warm-Up time we need to consider before collecting the proper results 

&nbsp;		NB: IF the "Moving Average" is constant from the start, NO warm up period needed	

        - About 7s of warmup for the throughput (as N >= 12 is about 3s) and 3s for queue length



.Simulation Time Duration:

&nbsp;	The simulation time was selected to ensure a sufficiently large sample size, allowing the application of the Central Limit Theorem for the statistical analysis of aggregated metrics.

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

**DATA COLLECTION \& ANALYSIS** 





