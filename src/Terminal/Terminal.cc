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
#include <omnetpp.h>
using namespace std;

Define_Module(Terminal);

void Terminal::generateRequest(ComMessage *msg) {
    // Check if Queue is Empty
    if (!msg_queue->getLast()) {
        msg->setB(-1);
        return;
    }

    // IF NOT EMPTY: Pick a number among 2, 4, 8, 16 to set B with 
    B = pow(2, (int) par("B"));
    msg->setB(B);
}

Terminal::~Terminal() {
    // Cancel and delete self-messages
    if (t_msg_to_q)
        cancelAndDelete(t_msg_to_q);
    if (t_time_frame)
        cancelAndDelete(t_time_frame);
    if (t_tx)
        cancelAndDelete(t_tx);

    // Delete all messages inside the queue
    if (msg_queue) {
        ContentMessage *m;
        while ((m = msg_queue->extractMessage()) != nullptr)
            delete m;
        delete msg_queue;
        msg_queue = nullptr;
    }
}

void Terminal::initialize() {
    //// FIELDS 
    // Timers 
    t_msg_to_q = new cMessage("contentMessage_timer");
    t_time_frame = new cMessage("timeframe_timer");
    t_tx = new cMessage("transmission");

    // Message Queue
    msg_queue = new MessageList();


    //// LOOP BEGINNING
    // "Create Message to Queue"
    scheduleAt(simTime() + par("T"), t_msg_to_q);

    // "Protocol Loop (at every Time Frame)"
    scheduleAt(simTime() + par("timeFrame_duration"), t_time_frame);
}

void Terminal::handleMessage(cMessage *msg) {

    // [Create Packets]
    if(msg == t_msg_to_q) {
        ContentMessage* new_msg = new ContentMessage("bytes");
        new_msg->setContent(par("S"));
        msg_queue->addMessage(new_msg);

        // If the Terminal has received a Grant and the Time Frame hasn't ended yet, it resumes transmission
        if (G)
            scheduleAt(simTime(), t_tx);

        // Timer for next packet to be generated
        scheduleAt(simTime() + par("T"), t_msg_to_q);
    }

    // [Start of a New Time Frame (Tf)]
    else if (msg == t_time_frame) {
        // Restart Timer for Time Frame
        scheduleAt(simTime() + par("timeFrame_duration"), t_time_frame);

        // Couting waiting time frames
        time_frame_counter++;

        // Resetting "grant"
        G = false;

        // Delete any previous Transmission Timer coming from the previous Time Frame
        if (t_tx->isScheduled())
            cancelEvent(t_tx);

        // Data Collection: Send #qLength from previous Time Frame to the Oracle
        ContentMessage* q_len = new ContentMessage("q_len");
        q_len->setContent(msg_queue->getQLength());
        sendDirect(q_len, 0, 0, oracle, "wirelessGate");

        // 1. Create ComMessage -> Save and Send B to GS (NB: call message "grant_request") 
        ComMessage *msg_grant = new ComMessage("grant_request");
        generateRequest(msg_grant);        // B value saved
        if (msg_grant->getB() == -1) {
            ContentMessage *b = new ContentMessage("B");
            b->setContent(-1);
            sendDirect(b, 0, 0, oracle, "wirelessGate");
        }
        send(msg_grant, "t_io$o");         // B value sent
    }

    // [Receive 'Grant' (GS)]  
    else if (msg->isName("grant_request")) {
        // 2.a IF Grant is NOT given => DO NOTHING (return)
        ComMessage *comMsg = check_and_cast<ComMessage*>(msg);
        if (!comMsg->getGrant()) {
            delete comMsg;
            return;
        }
        // Setting Grant to true so that during the  
        G = true;

        //computed number of time frames terminal has waited before transmission
        ContentMessage *tf_count = new ContentMessage("time_frame_counter");
        tf_count->setContent(time_frame_counter);
        sendDirect(tf_count, 0, 0, oracle, "wirelessGate");
        time_frame_counter = 0;

        ContentMessage *b_grant = new ContentMessage("B");
        b_grant->setContent(comMsg->getB());
        sendDirect(b_grant, 0, 0, oracle, "wirelessGate");

        // 2.b OTHERWISE => Compute M and Start Transmission Timer (t_tx), 
        M = floor(100 * pow((int) par("K"), log2(B) - 1)); // M = 100*K^(log_2(B)-1)

        long double queued_bytes = msg_queue->getBytesQueue();

        if (queued_bytes > M) {
            ContentMessage *q_bytes = new ContentMessage("queued_bytes");
            q_bytes->setContent(1);
            sendDirect(q_bytes, 0, 0, oracle, "wirelessGate");
        }

        scheduleAt(simTime(), t_tx);    // Begin Transmission Timer
        delete comMsg;
    }

    // [Receive "Transmission Notification" (T)]
    else if (msg == t_tx) {
        // 3. Transmit as much as 100*K^(log_2(B)-1) AND until the Queue is NOT empty 
        //      (NB: call message "bytes")

        ContentMessage *byte_msg = nullptr;

        // If there are still messages to send AND the amount of bytes hasn't been reached yet, extract them
        // OTHERWISE stop the routine (return)
        if (msg_queue->getLast() && M > 0)
            byte_msg = msg_queue->extractMessage();
        else
            return;

        // If max amount M hasn't reached, send them 
        // OTHERWISE stop the routine (return)
        int size = byte_msg->getContent();
        if (M >= size) {
            M -= size;
            //content message is sent to GS
            send(byte_msg, "t_io$o");
        } else {
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
