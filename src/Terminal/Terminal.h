#ifndef __RESOURCE_ALLOCATOR_TERMINAL_H_
#define __RESOURCE_ALLOCATOR_TERMINAL_H_

#include <omnetpp.h>
#include "../MessageList/MessageList.h"
#include "../Message/comMessage_m.h"
//#include "../Message/contentMessage_m.h"  // <-- already included in "MessageList.h"

using namespace omnetpp;

/**
 * TODO - Generated class
 */

class Terminal : public cSimpleModule
{
  private: 
    // Timers for each Routine:
    //  - Message Timer to Create one and Queue it + Message Queue itself
    //  - Time Frame notification timer to start Communication Protocol
    //  - Value to Store B and Message to Send { Grant Request, B }  at the Start of the Time Frame
    //  - Value to Store M, the max amount of Bytes to send 
    //  - Transmission Timer                            (NB): This is necessary because I can't send packets in a "while-loop" 
    //                                                        in the section of "handleMessage()" dedicated to the transmission of packets
    //                                                        upon receiving the Grant because otherwise it wouldn't be interruptable 
    //                                                        by other messages, it would necessarily need to get out of the while loop 
    //                                                        before it can actually react to the reception of outside messages 
    cMessage* t_msg_to_q = nullptr;
    MessageList* msg_queue = nullptr;  
    
    cMessage* t_time_frame = nullptr;

    int B = 0; 
    bool G = false;
    long double M = 0; 
    cMessage* t_tx = nullptr;

    // Fields for Data Collection
    int time_frame_counter = 0;

    cModule *oracle = getParentModule()->getSubmodule("oracle");

  public:
    Terminal() = default;
    virtual ~Terminal();
    
  protected:
    virtual void initialize() override;
    virtual void handleMessage(cMessage *msg) override;
    
    void generateRequest(ComMessage* msg);

};

#endif
