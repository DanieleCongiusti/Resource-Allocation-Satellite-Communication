//this header provided to implement Oracle class

#ifndef __RESOURCE_ALLOCATOR_ORACLE_H_
#define __RESOURCE_ALLOCATOR_ORACLE_H_

#include <omnetpp.h>
using namespace omnetpp;

class Oracle : public cSimpleModule {

    private:
        //signals for average throughput of the system
        simsignal_t throughputSignal;
        //signal for average queue length
        simsignal_t avgQLSignal;
        //signal for number of time frame between 2 grants
        simsignal_t waitingTimeFrameSignal;

        int exceed_m = 0;

        int b_values[5] = {0};

    public:
        virtual ~Oracle();

    protected:
        virtual void initialize() override;
        virtual void handleMessage(cMessage *msg) override;
        virtual void finish() override;
};

#endif
