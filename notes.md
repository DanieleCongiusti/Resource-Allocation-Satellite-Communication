**OBJECTIVES**

1\.  Determine the performance of communication system, with actors Ground station and Terminals, given a specific protocol, where various varying terminals and transmittable bytes at a time

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

**KPI**

1. Determine **average throughput** based on N, K values
2. Determine **average queue length** based on "" "" ""

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

**MODELING**
**NtS**: *Describing the Model consists in:* 
- Describe how it will work (tied to Implementation step) -> *Show a Screenshot of the Design from the NED file of the System and from the QTEnv at run time. Describe the elements in the images referencing the specs from the Project's Documentation and their behaviour that is going to be implemented in the next step.*

- What we expect from it in the results, OUR CLAIM (tied to Data Analysis) -> *Describe what we expect from varying N and K respectively as our claim to demonstrate in the final results*

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

**IMPLEMENTATION**  
**NtS**: *Make an overview of the project by describing the organization of the Directory showcasing the content of each of the following folders:*
- NED File (Modules) -> *Contain the NED Declaration of each of the following modules implemented...*
- Terminal -> *Describe the contents of the .h file (not necessary to go into details because the code is already commented for that) and the .cc file and the purpose of this module in function of the project's specs* 
- Ground Station -> *Same as before* 
- Oracle -> *Same as before* 
- MessageList -> *Same as before*
- New Message Type (CommMsg, ContentMsg) -> *Same as before*
  
*Describing the .h files for each module implemented is redudant since their implementation is already commented in the code.*

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

**VERIFICATION && VALIDATION TESTS**
**NtS**: *For **Verification** show an image of the running simulation of a "simple scenario" from QTEnv and associated to it the event traces that occur between the beginning of two timeframes. From the event traces describe the phases of the protocol:*
- Sending Grant Requests to Satellite and then to GS  
- Sending Grant Responses to Satellite and then to Terminal 
- Terminals with Grant start Transmitting to GS through Satellite

*For **Validation** show the results from the Consistency, Degeneracy, Continuity tests and describe how each test was conducted:*
- Consistency & Continuity -> Show the graphs obtained from the tested configuration for N and K 
- Degeneracy -> Show the Terminal's message to prove that the configuration does not crash and ends run correctly

**Consistency**:

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

**Degeneracy**:

 	The process should not crash if setting factors and parameters at extreme values

 	Values tested:
 	- N = 0
 	- K = 0
 	- T = 0
 	- S = \[10^6, 10^7]

 	These are "absurd values" for each case to see if the the program still works

\_\_\_\_\_\_\_\_\_\_\_\_

**Continuinty**:

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
* K: { 2, 5, 20, 50, 1000 }

For ***N***, we initially started by looking at the max and min possible terminals that can transmit considering B and C (Scheduling Capacity). From this we obtained that the range of possible transmittable Terminals is between \[4, 32]
 	But the likeliness of how many terminals will transmit isn't uniformally distributed since, just an example, the likeliness of having 4 terminals generating B = 16 (4x16 = 64 => Max Capacity reached, no more space for other terminals to transmit) is much more likely than 32 B = 2. Also, the series of B requests get ordered in decresing order when received, therefore it's sufficient that out of N terminals 4 random ones generate B = 16 and all the rest would be irrelevant.
 	So, we studied the probability of having the same value of B multiple times (an RV with Binomial Distribution) and quickly demonstrated that as N grows the most dominant case would eventually become 4 B = b, where b can be any of { 2, 4, 8, 16 }, therefore the ones transmitting would be those with b = 16.
 	From this, we determined the upper limit for our values, 24, since the probability of having 4 B = b is approximately 1, so anything above it didn't make sense testing. And from there we picked the rest of the values decreasing
 	by a factor of 4 each time since the likeliness of the dominant case decreased enough to hope for meaningful results to prove our conclusions on N.


For ***K***, we picked values for it based on the expected bytes generated per timeframe (Btf) given S and T. From that, we picked the values for K by which M would be large enough that ALL Btf from a terminal would pass for a given value of B, which is one of the factors that determines M. We start from a value of K which would compute M by which it would never suffice for the Btf and from there picked those which would give an M that would suffice for B = 16, B >= 8 and so forth. Then we also picked some larger values to demonstrate how increasing K does not provide any meaningful improvements after K is large enough so that even for the case B = 4 M would suffice for Btf. (We do not consider B = 2 since in this case for any value of K, M = 100).

---

Parameters:

* B, this has been provided to us by the project's specs.
* S, this has been choses based on the project's specific for M, where M = 100\*K^(log\_2(B)-1), in particular: when B=2 the M is ALWAYS M=100 because the exponent will be 0, therefore it doesn't matter what K is, M will be this constant value and since we want the packets to always be transmittable at any B.

* T, this has been chosen after testing different values for it in order to have enough bytes generated per timeframe (Btf) to have enough of a change for K; BUT not too small to have Btf so large that would create persistent backlog, so terminals that are not scheduled for several frames accumulate packets and then transmit in large bursts up to M(B) when granted, producing high variance in per-frame per-terminal throughput. We select T in an intermediae range so that the impact of K on throughput can be observed while keeping backlog-induced burstiness within reasonable bounds.

---

Warm-Up Duration:
**NtS**: *Describe how the Warm-up duration has been determined (copy description below) and add the graphs of the Moving Average for Throughput and Queue Length of the worst cases (QLen: any N,K=5 | Throup.: N24, any K).*

&nbsp;	- Add the Statistics to collect the "Moving Average" for Throughput and Queue Length values 
&nbsp;	- Gather Test results
&nbsp;	- Infer from the results how much Warm-Up time we need to consider before collecting the proper results 
&nbsp;		NB: IF the "Moving Average" is constant from the start, NO warm up period needed	
        - About 7s of warmup for the throughput and 3s for queue length -> Decided on 10s to add a little margin 


Simulation Time Duration:
&nbsp;	The simulation time was selected to ensure a sufficiently large sample size, allowing the application of the Central Limit Theorem for the statistical analysis of aggregated metrics.
&nbsp;	Since the recorded samples per run are done at every timeframe and a timeframe lasts 80ms, we picked a simulation time of 30s to have a large amount of data to compute the average Throughput and Queue Length after the Warm-Up period ((30-10)/0.08=250 timeframes total from which we gather samples for the final computation of the Avg Throughput and Avg Queue Length at the end of one run). 

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

**DATA COLLECTION \& ANALYSIS**

For each configuration of N, K (which are |N|\*|K|=5\*5=25 distinct configurations) we ran the experiment for >30 times in order to have a sufficient amount of results from Indipendent Identically Distributed RVs and also verified at the same time that the Sample Variance is finite for each KPI to assume the Mean of each KPI to be Normally distributed. This way we can use the Standardized Sample Mean, an RV normally distributed defined as Z=(X-mu/S\*sqrt(n)), to compute the Confidence Intervals of the true mean of our experiments. 

We also computed the Sample Width for different confidence levels (90, 95, 99) by computing the Sample Mean (X^bar) and the Sample Variance (S) from a total of (around 35 to 400) samples to verify that this amount of samples were enough for our estimate. We found that we had enough samples for 90 and 95% but not for the last 99, we needed many more samples. So we went for a Confidence Level of 95%.

We then had to gather many more samples to properly assert that the Sample Variance was limited, for the Queue Length in particular, since it starts with an upward trend (not good) but then stabilizes around a fixed value for a large sample width of at least 200 to 400. 

Given X^bar and S and verified that the sample width is sufficiently large enough and the variance is indeed limited, we then proceeded with computing the CI for 90, 95% certainty. Under it's shown the histograms of our results at different configurations of N and K:	

"Showing the graph results"
1) Grafico sul throughput al variare di N (throughput_N.png)
    - si nota un aumento lineare del throughput al variare di N, mentre K ha un impatto maggiore per N più grande
    - vogliamo evidenziare come K sia irrilevante per un certo range di N e cominci ad impattare maggiormente all'aumentare del numero dei terminali dato che la queue length aumenta sempre di più

2) Grafico sulla queue length al variare di N (queueLength_N.png)
    - allo stesso tempo, se si aumentasse N, avremmo un aumento della coda poiché il numero di terminali che non trasmettono aumenta
    - si può notare come, anche aumentando K (teoricamente dovrebbe diminuire la coda), ciò non succeda poiché la capacità massima della GS è di 64 slot e quindi il numero massimo di terminali che possono trasmettere sarà pari a 4 (con probabilità vicina a 1), causando comunque un aumento delle dimensioni delle code 

Come mai allora non avete provato ad aumentare il numero di N ulteriormente per verificare questo andamento? -> max 64 slots

3) Grafico sul ratio (ratio.png)
    - Volevamo trovare la migliore configurazione di N e K per avere il massimo throughput e la minima queue length e, dal grafico, vediamo come il rapporto ottimo si ha per N = 16 ed aumentando N la queue length crescerebbe molto di più rispetto al throughput

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

**CONCLUSIONS**

"Conclusions provided by recapping most relevant comments on graphs"
=======
\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_
\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_
\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

**EXTRA NOTES**

Dubbio "Wait Timeframes N40, K=*": *Perché aumentando K aumenta W?*
    - Per K<10 i terminali non si svuotano (quasi) mai per cui i terminali che hanno appena trasmesso possono ricevere un nuovo grant anche al prossimo timeframe (pur sempre con probabilità bassa MA non nulla)
    - Per K>10 invece i terminali (quasi) sempre si svuotano per cui i terminali "" "" "" NON potranno MAI ricevere un nuovo grant al prossimo timeframe  

Hints:
    - impatto N e K su diversa scala, basta un aumento lineare di N per avere dei miglioramenti in termini di throughput, mentre K basta aumentarlo di poco e si ottengono prestazioni nettamente migliori;

    - con gli slot fissati a 64 non è sufficiente aumentare N e K (le performance non migliorano considerando che anche la queue length aumenta);

    - considerare trade off tra throughput e queue length, perché aumentare mole di byte ha benefici su throughput, ma anche di costo in termini di memoria nella queue length.
 

