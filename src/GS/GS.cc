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

GS::~GS() {
    while (!rcv_B.empty()) {
        delete rcv_B.top();
        rcv_B.pop();
    }
}

void GS::initialize() {
    scheduler = par("scheduler_slots");
    terminal_counter = par("terminal_counter");
    byte_received = 0;
}

void GS::handleMessage(cMessage *msg) {

    // when a message with B arrives
    if (msg->isName("grant_request"))
    {
        handleComMessage(msg);
    }
    else if (msg->isName("bytes"))
    {
        handleContMessage(msg);
    }
    else
    {
        delete msg; 
        throw cRuntimeError("Unrecognized message type. Abort");
    }
}

void GS::handleComMessage(cMessage *msg) {
    ComMessage *rcv_msg;
    ComMessage *send_msg;
    // another terminal has sent bearer index value
    terminal_counter--;
    rcv_msg = check_and_cast<ComMessage*>(msg);

    // send bytes accumulated in previous time frame (if exist)
    if (byte_received > 0)
    {
        ContentMessage* byte = new ContentMessage("byte_sent");
        byte->setContent(byte_received);
        sendDirect(byte, 0, 0, oracle, "wirelessGate");
        byte_received = 0;
    }

    if (rcv_msg->getB() != -1) // Terminal is active
    {
        rcv_B.push(rcv_msg);
    }
    else
    {
        delete rcv_msg;
    }

    if (terminal_counter == 0) { // GS received all the B values
        // extract all messages and determine grant permission for each terminal
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
        // update counters for next operations
        terminal_counter = par("terminal_counter");
        scheduler = par("scheduler_slots");
    }
}

void GS::handleContMessage(cMessage *msg) {
    ContentMessage *rcv_bytes;
    rcv_bytes = check_and_cast<ContentMessage*>(msg);
    byte_received += rcv_bytes->getContent();
    delete rcv_bytes;
}
