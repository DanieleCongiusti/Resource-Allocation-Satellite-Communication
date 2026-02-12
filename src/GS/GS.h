//
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU Lesser General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
// 
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU Lesser General Public License for more details.
// 
// You should have received a copy of the GNU Lesser General Public License
// along with this program.  If not, see http://www.gnu.org/licenses/.
// 

#ifndef __RESOURCE_ALLOCATOR_GS_H_
#define __RESOURCE_ALLOCATOR_GS_H_

#include <omnetpp.h>
#include <queue>
#include <vector>
#include "../Message/comMessage_m.h"

using namespace omnetpp;
using namespace std;

/**
 * TODO - Generated class
 */

struct Comp {
    bool operator()(ComMessage *a, ComMessage *b) {
        if (a->getB() < b->getB())
        {
            return true;
        }
        else
        {
            return false;
        }
    }
};

class GS: public cSimpleModule {
private:
    // upper limit of scheduled slots within a time frame
    int scheduler;
    // counter to determine when to start scheduling (wait for all terminals to send B)
    int terminal_counter;
    // counter to determine the total number of bytes received in a time frame for throughput statistics
    int byte_received;
    // scheduler
    priority_queue<ComMessage*, vector<ComMessage*>, Comp> rcv_B;

    cModule *oracle = getParentModule()->getSubmodule("oracle");

public: 
    virtual ~GS(); 

protected:    
    virtual void initialize() override;
    virtual void handleMessage(cMessage *msg) override;
    void handleComMessage(cMessage *msg);
    void handleContMessage(cMessage *msg);
};

#endif
