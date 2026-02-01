//this header provided to implement Oracle class

#ifndef __RESOURCE_ALLOCATOR_ORACLE_H_
#define __RESOURCE_ALLOCATOR_ORACLE_H_

#include <omnetpp.h>
using namespace omnetpp;

class Oracle : public cSimpleModule {

    private:
        //signals for throughput
        simsignal_t throughputSignal;
        simsignal_t throughputWarmUpSignal;
        //signal for AvgQueueLength
        simsignal_t avgQLSignal;
        //signal for number of time frame between 2 grants
        simsignal_t waitingTimeFrameSignal;
        //signal for the bytes accumulated between 2 grants
        simsignal_t accumulatedBytesGrantSignal;
        //signal for the B values at grant
        simsignal_t bGrantSignal;

        //total number of bytes recevied
        int totBytes = 0;
        //interval of emit for warmup
        double interval = 0.25;
        //total number of bytes received in an interval
        double currentBytes = 0;
        //timer for warmup-period
        cMessage *throughputTimer;

    public:
        virtual ~Oracle();

    protected:
        virtual void initialize() override;
        virtual void handleMessage(cMessage *msg) override;
        virtual void finish() override;
};

#endif
