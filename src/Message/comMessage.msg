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

// This class models the packet that terminals use to request B scheduling slots to the GS

message ComMessage {
    //parameter to allocate slots at GS
    int B;
    //parameter set by the satellite to know on which gate to forward back to the terminal the answered request from GS (
    int gateIndex;
    //parameter set by GS to grant communication to the terminal that has requested 
    bool grant;
}
