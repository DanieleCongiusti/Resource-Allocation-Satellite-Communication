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

#include "MessageList.h"

MessageList::MessageList() {
    //create empty list
    msg_list = nullptr;
    last = nullptr;
    qLength = 0;
    bytesQueue = 0;
}

MessageList::~MessageList() {

    last=nullptr;
    //some element in
    while(msg_list){
        scheduledMessage *app=msg_list;
        msg_list=msg_list->next;
        delete app;
    }
}

void MessageList::addMessage(ContentMessage* msg){
    if(last){
        //insert message at tail of list
        last->next=new scheduledMessage(msg);
        //update the last pointer for future insert operations
        last=last->next;
    }
    else{
        msg_list=new scheduledMessage(msg);
        last=msg_list;
    }
    qLength++;
    bytesQueue+=msg->getSize();
}

ContentMessage* MessageList::extractMessage(){
    //take the reference for the target message to extract
    if(msg_list){
        ContentMessage* targetMessage=msg_list->content;
        //make advance the pointer of the list for eventually next messages
        msg_list = msg_list->next;

        if (!msg_list)
            last = nullptr; 

        qLength--;
        bytesQueue-=targetMessage->getSize();
        return targetMessage;
    }
    return nullptr; 
}

scheduledMessage* MessageList::getLast(){
    return last;
}


int MessageList::getQLength(){
    return qLength;
}


double MessageList::getBytesQueue(){
    return bytesQueue;
}

