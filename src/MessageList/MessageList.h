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

#ifndef MESSAGELIST_MESSAGELIST_H_
#define MESSAGELIST_MESSAGELIST_H_

#include "../Message/contentMessage_m.h"
#include "../Message/comMessage_m.h"

struct scheduledMessage {
    ContentMessage *content;
    scheduledMessage *next;

    scheduledMessage(ContentMessage *msg_content) {
        content = msg_content;
        next = nullptr;
    }

    ~scheduledMessage() {
        delete content;
    }
};

class MessageList {
private:
    //this attribute identifies the list of content messages that have to be sent once terminal has received a grant
    scheduledMessage *msg_list;

    //added pointer to last element of the list
    scheduledMessage *last;

    //integer value used to count number of queued messages
    int qLength;

    //bytes contained in queue
    double bytesQueue;

public:
    //constructor
    MessageList();
    //destructor
    virtual ~MessageList();
    //function to insert a message at tail of list
    void addMessage(ContentMessage*);
    //function to extract msg from head of list
    ContentMessage* extractMessage();
    scheduledMessage* getLast();
    //function to retrieve length of queue
    int getQLength();
    //function to retrieve bytes contained in queue
    double getBytesQueue();
};

#endif /* MESSAGELIST_MESSAGELIST_H_ */
