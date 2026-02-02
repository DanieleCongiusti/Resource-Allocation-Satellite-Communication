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
    waitingTimeFrameSignal = registerSignal("waitingTimeFrame");
    bGrantSignal = registerSignal("bGrant");

    throughputTimer = new cMessage("throughputTimer");
    scheduleAt(simTime() + interval, throughputTimer);
}

void Oracle::handleMessage(cMessage *msg) {

    if (msg->isSelfMessage() && msg->isName("throughputTimer")) {
        double throuhgput = currentBytes / interval;
        //EV_INFO << "Throughput: " << throuhgput << endl;
        //EV_INFO << "Bytes: " << currentBytes << endl;
        emit(throughputWarmUpSignal, currentBytes / interval);
        currentBytes = 0;
        scheduleAt(simTime() + interval, throughputTimer);
    }
    // here I can receive a contentMessage for throughput
    // or for AvgQueueLength
    else if (!msg->isName("byte_sent") && !msg->isName("q_len")
            && !msg->isName("time_frame_counter")
            && !msg->isName("accumulated_bytes_grant") && !msg->isName("B")) {
        delete msg;
        throw cRuntimeError("Message type not accepted by oracle");
    } else {
        ContentMessage *c_msg = check_and_cast<ContentMessage*>(msg);
        if (msg->isName("byte_sent")) {
            totBytes += c_msg->getSize();
            currentBytes += c_msg->getSize();
        } else if (msg->isName("time_frame_counter")) {
            emit(waitingTimeFrameSignal, c_msg->getSize());
        } else if (msg->isName("B")) {
            int B = c_msg->getSize();
            if (B == -1){
                b_values[4]++;
            }
            else
            {
                b_values[(int)(log2(B)-1)]++;
            }
        }
        else
            emit(avgQLSignal, c_msg->getSize());
        delete c_msg;
    }
}

void Oracle::finish() {
    double totTime = simTime().dbl();
    emit(throughputSignal, totBytes / totTime);

    double totTimeFrame = totTime/(double)par("timeframe_duration");

    for (int count : b_values)
    {
        emit(bGrantSignal, count/totTimeFrame);
    }

    //emit(....., M>100.000/totTimeFrame)
}
