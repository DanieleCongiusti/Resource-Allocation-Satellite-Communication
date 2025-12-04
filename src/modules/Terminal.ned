// This NED file defines module for 'Terminal', entity of model
// that sends packets to ground station and defines random variables
// S and T uniform and exponential iid rvs

// defines and send B values for total of bytes to send to Ground Station module

package resource_allocator.modules;

simple Terminal
{
    parameters:
        // TimeFrame durations
        double timeFrame_duration @unit(s) = 0.08s;

        // To generate Grant Request msg
        volatile int B = intuniform(1, 4, 0);
        volatile int K;  // defined in "System.ned"

        // To generate packet with random S every random T seconds
		int a @unit(bytes);       // lower bound of uniform 				-> *to be defined in .ini file*
        int b @unit(bytes);       // upper bound of uniform 				-> *to be defined in .ini file*
        double lambda @unit(s);      		 // rate of exponential distribution 	-> *to be defined in .ini file*

        volatile int S @unit(bytes) = intuniform(a, b, 1);       	// bytes per packet
        volatile double T @unit(s) = exponential(lambda, 2); 		// inter-arrival time
		
	gates:
			inout t_io;
}
