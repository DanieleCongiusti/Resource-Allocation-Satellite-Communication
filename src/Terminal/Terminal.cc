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

Define_Module(Terminal);

void Terminal::initialize()
{
    // TODO - Generated method body
}

void Terminal::handleMessage(cMessage *msg)
{
    // TODO - Generated method body
}
