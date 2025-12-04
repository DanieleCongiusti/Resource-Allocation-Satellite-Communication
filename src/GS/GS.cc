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

// schedule, as a counter of 64 slots
// receiving packets from Satellite, must order by B desc -> while (schedule > 0) schedule -= B (desc. order) + grant=true + send back
// ... (waiting for packets)
// data anlalysis (signal and statistics)

#include "../GS/GS.h"
#include "../Message/comMessage_m.h"
#include "../MessageList/MessageList.h"

Define_Module(GS);

void GS::initialize() {
    scheduler = par("scheduler_slots");
    terminal_counter = par("terminal_counter");
}

void GS::handleMessage(cMessage *msg) {

    // When a message with B arrives
    if (msg->isName("grant_request"))
    {
        handleComMessage(msg);
    }
    else if (msg->isName("bytes")) // Message with S
    {
        handleContMessage(msg);
    }
    else
    {
        EV_INFO << "Message: " << msg->getName() << endl;
        throw cRuntimeError("Unrecognized message type. Abort");
    }
}

void GS::handleComMessage(cMessage *msg) {
    ComMessage *rcv_msg;
    ComMessage *send_msg;

    terminal_counter--;
    rcv_msg = check_and_cast<ComMessage*>(msg);

    if (rcv_msg->getB() != -1) // Terminal is active
    {
        rcv_B.push(rcv_msg);
    }

    if (terminal_counter == 0) { // GS received all the B values
        //Extract all messages and send grant or not
        while (!rcv_B.empty()) {
            send_msg = rcv_B.top();
            int B = send_msg->getB();
            if (scheduler < B) {
                send_msg->setGrant(false);
            } else {
                scheduler -= B;
                send_msg->setGrant(true);
            }
            send(send_msg, "gs_io$o");
            rcv_B.pop();
        }
        terminal_counter = par("terminal_counter");
        scheduler = par("scheduler_slots");
    }
}

void GS::handleContMessage(cMessage *msg) {
    ContentMessage *rcv_bytes;
    rcv_bytes = check_and_cast<ContentMessage*>(msg);
    EV_INFO << "Received message of size " << rcv_bytes->getSize() << endl;
}
