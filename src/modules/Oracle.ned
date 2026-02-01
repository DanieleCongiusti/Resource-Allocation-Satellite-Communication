// This module is provided for supporting Oracle in order to emit signal values and
// compute statistics

// statistics: Throughput and AvgQueueLength that measures throughput of overall system and the avarage value for queue
// length of terminals during a time frame
package resource_allocator.modules;

simple Oracle{

    parameters:
        //timeframe duration
        double timeframe_duration @unit(s) = 0.08s;


		//signal for collecting values in order to retrieve the warmup-period
		@signal[throughputWarmUp](type = double);
		//signal for collecting values in order to retrieve throughput
		@signal[throughput](type = double);
		//signal for collecting values in order to retrieve AvgQueueLength
		@signal[avgQueueLength](type = int);
		//signal for collecting values in order to retrieve the number of time frame between 2 grants
		@signal[waitingTimeFrame](type = int);
		//signal for collecting values in order to retrieve the queue length accumulated between 2 grants
		@signal[accumulatedBytesGrant](type = int);
		//signal for collecting values in order to retrieve the B value at grant
		@signal[bGrant](type = int);
		
		//statistic for computing warmup period
		@statistic[throughputWarmUpStat](source = "throughputWarmUp"; record = vector;);
        //statistic for computing throughput
		@statistic[throughputStat](source = "throughput"; record = last;);
        //statistic for computing AvgQueueLength
		@statistic[AvgQLStat](source = "avgQueueLength"; record = mean, vector;);
		//statistic for computing waitingTimeFrame
		@statistic[avgWaitingTimeFrame](source = "waitingTimeFrame"; record = mean;);
		//statistic for computing accumulatedBytesGrant
		@statistic[avgAccumulatedBytesGrant](source = "accumulatedBytesGrant"; record = mean;);
		//statistic for computing bGrant
		@statistic[avgBGrant](source = "bGrant"; record = histogram, vector;);

    gates:
        //gate that receives data from other nodes
        input wirelessGate @directIn;

};
