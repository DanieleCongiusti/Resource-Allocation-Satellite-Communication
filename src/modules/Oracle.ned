// This module is provided for supporting Oracle in order to emit signal values and
// compute statistics

// statistics: Throughput and AvgQueueLength that measures throughput of overall system and the avarage value for queue
// length of terminals during a time frame
package resource_allocator.modules;

simple Oracle{

    parameters:
        //timeframe duration
        double timeframe_duration @unit(s) = 0.08s;

        //signal for collecting values in order to retrieve throughput
		@signal[throughput](type = double);
        //statistic for computing throughput
		@statistic[throughputStat](source = "throughput"; record = last;);

		//signal for collecting values in order to retrieve AvgQueueLength
		@signal[avgQueueLength](type = int);
        //statistic for computing AvgQueueLength
		@statistic[AvgQLStat](source = "avgQueueLength"; record = mean;);

    gates:
        //gate that receives data from other nodes
        input wirelessGate @directIn;

};
