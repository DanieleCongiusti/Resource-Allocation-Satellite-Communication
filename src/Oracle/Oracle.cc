// The Oracle receives type "ContentMessages" and its "Size" field contains either:
// - the BytesSent by the Terminal  -> The message is labeled as "byte_sent"
// - the Queue Length               -> The message is labeled as "q_len"

// P.S.: Remember to Delete each message at the end of processing

#include "Oracle.h"
#include "../Message/contentMessage_m.h"

Define_Module(Oracle);

Oracle::~Oracle(){

}

void Oracle::initialize(){
    throughputSignal = registerSignal("throughput");
    avgQLSignal = registerSignal("avgQueueLength");
}

void Oracle::handleMessage(cMessage *msg){

    // here I can receive a contentMessage for throughput
    // or for AvgQueueLength
        if(!msg->isName("byte_sent") && !msg->isName("q_len")){
            delete msg;
            throw cRuntimeError("Message type not accepted by oracle");
            }
        else{
                ContentMessage *c_msg=check_and_cast<ContentMessage*>(msg);
                if(msg->isName("byte_sent"))
                    totBytes += c_msg->getSize();
                else
                    emit(avgQLSignal,c_msg->getSize());
                delete c_msg;
             }
}

void Oracle::finish(){
    double totTime = simTime().dbl();
    emit(throughputSignal,totBytes/totTime);
}
