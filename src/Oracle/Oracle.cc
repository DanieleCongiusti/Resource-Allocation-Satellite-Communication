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
    exceedMSignal = registerSignal("exceedM");

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
            && !msg->isName("accumulated_bytes_grant") && !msg->isName("B") && !msg->isName("queued_bytes")) {
        delete msg;
        throw cRuntimeError("Message type not accepted by oracle");
    } else {
        ContentMessage *c_msg = check_and_cast<ContentMessage*>(msg);
        if (msg->isName("byte_sent")) {
            totBytes += c_msg->getContent();
            currentBytes += c_msg->getContent();
        } else if (msg->isName("time_frame_counter")) {
            emit(waitingTimeFrameSignal, c_msg->getContent());
        } else if (msg->isName("B")) {
            int B = c_msg->getContent();
            if (B == -1) {
                b_values[4]++;
            } else {
                b_values[(int) (log2(B) - 1)]++;
            }
        } else if (msg->isName("queued_bytes")) {
            exceed_m++;
        } else
            emit(avgQLSignal, c_msg->getContent());
        delete c_msg;
    }
}

void Oracle::finish() {
    double totTime = simTime().dbl();
    emit(throughputSignal, totBytes / totTime);

    double totTimeFrame = totTime / (double) par("timeframe_duration");

    const char *bLabels[] = { "B_2", "B_4", "B_8", "B_16", "B_Minus1" };

    for (int i = 0; i < 5; i++) {
        recordScalar(bLabels[i], b_values[i] / totTimeFrame);
    }

    emit(exceedMSignal, exceed_m / totTimeFrame);
}
