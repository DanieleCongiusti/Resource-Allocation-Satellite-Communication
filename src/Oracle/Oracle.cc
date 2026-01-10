// The Oracle receives type "ContentMessages" and its "Size" field contains either:
// - the BytesSent by the Terminal  -> The message is labeled as "byte_sent"
// - the Queue Length               -> The message is labeled as "q_len"

// P.S.: Remember to Delete each message at the end of processing

#include "Oracle.h"
#include "../Message/contentMessage_m.h"

Define_Module(Oracle);

Oracle::~Oracle() {
    cancelAndDelete(throughputTimer);
}

void Oracle::initialize() {
    throughputSignal = registerSignal("throughput");
    throughputWarmUpSignal = registerSignal("throughputWarmUp");
    avgQLSignal = registerSignal("avgQueueLength");

    throughputTimer = new cMessage("throughputTimer");
    scheduleAt(simTime() + interval, throughputTimer);
}

void Oracle::handleMessage(cMessage *msg) {

    if (msg->isSelfMessage() && msg->isName("throughputTimer")) {
        double throuhgput = currentBytes/interval;
        //EV_INFO << "Throughput: " << throuhgput << endl;
        //EV_INFO << "Bytes: " << currentBytes << endl;
        emit(throughputWarmUpSignal, currentBytes/interval);
        currentBytes = 0;
        scheduleAt(simTime() + interval, throughputTimer);
    }
    // here I can receive a contentMessage for throughput
    // or for AvgQueueLength
    else if (!msg->isName("byte_sent") && !msg->isName("q_len")) {
        delete msg;
        throw cRuntimeError("Message type not accepted by oracle");
    } else {
        ContentMessage *c_msg = check_and_cast<ContentMessage*>(msg);
        if (msg->isName("byte_sent")){
            totBytes += c_msg->getSize();
            currentBytes += c_msg->getSize();
        }
        else
            emit(avgQLSignal, c_msg->getSize());
        delete c_msg;
    }
}

void Oracle::finish() {
    double totTime = simTime().dbl();
    emit(throughputSignal, totBytes / totTime);
}
