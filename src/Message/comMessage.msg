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

// This class models the packet that terminal sends to ground station to ask for a grant and start the
// communication

//this kind of message doesn't need to be queued, because is the only one that terminal sends to
//ask to be active during the time frame

// declaration of cpacket with: B, gate_index, boolean grant


message ComMessage {
    //parameter to allocate slots at ground station and tells me how much byte I have to send
    int B;
    //parameter set by the terminal that represent the gate at satellite
    int gateIndex;
    //parameter set by GS to grant communication permission to the terminal that has requested for 
    bool grant;
}
