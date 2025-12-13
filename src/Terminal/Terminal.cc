// declaration of cpacket with: B, gate_index, boolean grant
// declaration of cpacket with S bytes

// T e S parameters NED file
// Every T (expon. distributed), using scheduleAt(), message to itself (timer) to generate a packet of size S (uniform. distributed)
// Queue, that is a list, to accumulate the packets with a FIFO policy -> header file
// while (simTime = k*80ms && list is not empty) -> generate B (uniform distributed i = [1,4] and B = 2^i)
// send to Satellite with index of the terminal based on the index gate and boolean grant
// ... (waiting for grant)
// if (grant) transmits M bytes, based on B value: B=2->M=100*K^0, B=4->M=100*K^1, B=8->M=100*K^2, B=16->M=100*K^3
// read S of the packet (FIFO policy), while(M >= S && list is not empty), extract, M -= S and send to Satellite, otherwise finish

#include "../Terminal/Terminal.h"
#include <cmath>
using namespace std;

Define_Module(Terminal);

void Terminal::generateGrant(ComMessage* msg) {
    // Check if Queue is Empty
    if (!msg_queue->getLast()) {
        msg->setB(-1);
        return;  
    } 

    // IF NOT EMPTY: Pick a number among 2, 4, 8, 16 to set B with 
    B = pow(2,(int)par("B")); 
    msg->setB(B); 
}

Terminal::~Terminal()
{
    // Cancel and delete self-messages
    if (t_msg_to_q)        cancelAndDelete(t_msg_to_q);
    if (t_time_frame)      cancelAndDelete(t_time_frame);
    if (t_tx)              cancelAndDelete(t_tx);
    
    // Delete all messages inside the queue
    if (msg_queue) {
        ContentMessage* m;
        while ((m = msg_queue->extractMessage()) != nullptr)
        delete m;
        delete msg_queue;
        msg_queue = nullptr; 
    }
}

void Terminal::initialize()
{
    //// FIELDS 
    // Timers 
    t_msg_to_q = new cMessage("contentMessage_timer");
    t_time_frame = new cMessage("timeframe_timer");
    t_tx = new cMessage("transmission");
    
    // Message Queue
    msg_queue = new MessageList(); 
    
    // Signals 
    // ... 
    
    //// LOOP BEGINNING
    // "Create Message to Queue"
    scheduleAt(simTime()+par("T"), t_msg_to_q);
    
    // "Protocol Loop (at every Time Frame)"
    scheduleAt(simTime() + par("timeFrame_duration"), t_time_frame);
}

void Terminal::handleMessage(cMessage *msg) {

    // [Create Packets]
    if(msg == t_msg_to_q) {
        ContentMessage* new_msg = new ContentMessage("bytes");
        new_msg->setSize(par("S"));
        msg_queue->addMessage(new_msg);
        EV_INFO << "Added New Message of Size: " << new_msg->getSize() << "\n";

        scheduleAt(simTime()+par("T"), t_msg_to_q);
    }

    // [Start of a New Time Frame (T)] 
    else if (msg == t_time_frame) {
        // Delete any previous Transmission Timer coming from the previous Time Frame
        if (t_tx->isScheduled())  cancelEvent(t_tx);
        
        // Restart Timer for Time Frame as soon as possible
        scheduleAt(simTime() + par("timeFrame_duration"), t_time_frame);    

        // Data Collection: Send #byteSent + #qLength from previous Time Frame to the Oracle
        cModule *oracle = getParentModule()->getSubmodule("oracle");
        cGate *oracle_gate = oracle->gate("wirelessGate", getIndex());

        ContentMessage* byte_sent = new ContentMessage("byte_sent");
        byte_sent->setSize(byteSent);
        sendDirect(byte_sent, 0, 0, oracle, oracle_gate);
        // delete byte_sent; // DO IT ON THE ORACLE SIDE

        ContentMessage* q_len = new ContentMessage("q_len");
        q_len->setSize(msg_queue->getQLength());
        sendDirect(q_len, 0, 0, oracle, oracle_gate);
        // delete q_len;    // DO IT ON THE ORACLE SIDE

        // 1. Create ComMessage -> Save and Send B to GS (NB: call message "grant_request") 
        ComMessage* msg_grant = new ComMessage("grant_request");
        generateGrant(msg_grant);       // B value saved
        send(msg_grant, "t_io$o");      // B value sent
        EV_INFO << "Terminal " << this->getName() << " has sent Grant Request to GS w/ value B = " << msg_grant->getB() << "\n"; 
    }

    // [Receive 'Grant' (GS)]  
    else if (msg->isName("grant_request")) {
        // 2.a IF Grant is NOT given => DO NOTHING (return)
        ComMessage *comMsg=check_and_cast<ComMessage*>(msg);
        if (!comMsg->getGrant()) {
            delete comMsg; 
            return;
        }

        // 2.b OTHERWISE => Compute M and Start Transmission Timer (t_tx), 
        M = floor(100 * pow((int)par("K"), log2(B) - 1));      // M = 100*K^(log_2(B)-1)

        scheduleAt(simTime(), t_tx);    // Begin Transmission Timer
        delete comMsg; 
    }

    // [Receive "Transmission Notification" (T)]
    else if (msg == t_tx) {
        // 3. Transmit as much as 100*K^(log_2(B)-1) AND until the Queue is NOT empty 
        //      (NB: call message "bytes")
    
        // NB: DON'T USE WHILE LOOP, instead create a new section (this one) in handleMessage to handle 
        //      the transmission of packets so that it can be interruptable; the timer is "fake" as in 
        //      the "scheduleAt()" takes as the delay time directly simTime() meaning that the module 
        //      receives the message immediately 

        ContentMessage* byte_msg = nullptr; 
        
        // If there are still messages to send AND the amount of bytes hasn't been reached yet, extract them
        // OTHERWISE stop the routine (return)
        if (msg_queue->getLast() && M > 0)
            byte_msg = msg_queue->extractMessage(); 
        else 
            return;

        // If max amount M hasn't reached, send them 
        // OTHERWISE stop the routine (return)
        int size = byte_msg->getSize();
        if (M >= size) {
            M -= size;

            // Data Collection
            byteSent += size;

            send(byte_msg, "t_io$o");
            EV_INFO << "Sent message." << endl;
        }
        else {
            // Re-insert the message back in the queue if it goes beyond the max amount
            msg_queue->addMessage(byte_msg); 
            return; 
        }

        // Resend Transmission Notification to send next packet (OR to stop routine) 
        // Continue only if both conditions hold
        if (M > 0 && msg_queue->getLast() != nullptr)
            scheduleAt(simTime(), t_tx);
    }
}
