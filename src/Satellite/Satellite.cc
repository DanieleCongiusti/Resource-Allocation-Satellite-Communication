//
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU Lesser General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
// 
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without //EVen the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU Lesser General Public License for more details.
// 
// You should have received a copy of the GNU Lesser General Public License
// along with this program.  If not, see http://www.gnu.org/licenses/.
// 


// if packet from terminal, send to GS
// if packet from GS, analyze gate_index and send to the gate

#include "../Satellite/Satellite.h"
#include "../Message/comMessage_m.h"

Define_Module(Satellite);

void Satellite::initialize()
{
        //NOTHING TO DO 
}

void Satellite::handleMessage(cMessage *msg)
{
    //check if message comes from GS
    if(strcmp(msg->getArrivalGate()->getName(),"s_iogs$i")==0){
        //check for destination terminal
        //check the gateIndex if it is comMessage
        ComMessage *comMsg = check_and_cast<ComMessage*>(msg);
        //EV << "Sending to terminal index " << comMsg->getGateIndex()
           //<< " (max: " << gateSize("s_iot$o") << ")" << endl;
        send(comMsg,"s_iot$o",comMsg->getGateIndex());
    }
    else{
        //message from a terminal
        //need to insert arrival gate
        if(msg->isName("grant_request")){
            ComMessage *comMsg=check_and_cast<ComMessage*>(msg);
            comMsg->setGateIndex(msg->getArrivalGate()->getIndex());
            send(comMsg,"s_iogs$o");
        }
        else if ("bytes")
            send(msg,"s_iogs$o"); //we're dealing with a ContMessage that terminal is sending
        else
            delete msg;
    }

}
