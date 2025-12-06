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
    int scheduler;
    int terminal_counter;
    priority_queue<ComMessage*, vector<ComMessage*>, Comp> rcv_B;

public: 
    virtual ~GS(); 

protected:    
    virtual void initialize() override;
    virtual void handleMessage(cMessage *msg) override;
    void handleComMessage(cMessage *msg);
    void handleContMessage(cMessage *msg);
};

#endif
