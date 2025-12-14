//this header provided to implement Oracle class

#ifndef __RESOURCE_ALLOCATOR_ORACLE_H_
#define __RESOURCE_ALLOCATOR_ORACLE_H_

#include <omnetpp.h>
using namespace omnetpp;

class Oracle : public cSimpleModule {

    private:
        //singal for throughput
        simsignal_t throughputSignal;
        //signal for AvgQueueLength
        simsignal_t avgQLSignal;

    public:
        virtual ~Oracle();

    protected:
        virtual void initialize() override;
        virtual void handleMessage(cMessage *msg) override;
};

#endif
