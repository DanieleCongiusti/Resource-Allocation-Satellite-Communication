// This module is provided for supporting Oracle in order to emit signal values and
// compute statistics

// statistics: Throughput and AvgQueueLength that measures throughput of overall system and the avarage value for queue
// length of terminals during a time frame
package resource_allocator.modules;

simple Oracle{

    parameters:
        //time frame duration
        double timeframe_duration @unit(s) = 0.08s;

		// signal to collect data for computing throughput
		@signal[throughput](type = double);
		// signal to monitor the queue length
		@signal[avgQueueLength](type = int);
		// signal to measure the time interval between two consecutive grants
		@signal[waitingTimeFrame](type = int);
		// signal to count how many times the msg queue exceeds M within a time frame
		@signal[exceedM](type = double);
		// signal to count the number of occurrencies of B index
		@signal[bValue](type = int);
		
        // statistic for computing throughput
		@statistic[throughputStat](source = "throughput"; record = mean, vector;);
        // statistic for computing the average queue length
		@statistic[AvgQLStat](source = "avgQueueLength"; record = mean, vector;);
		// statistic for computing waiting time frame
		@statistic[avgWaitingTimeFrame](source = "waitingTimeFrame"; record = mean;);

    gates:
        //gate that receives data from other nodes
        input wirelessGate @directIn;

};
