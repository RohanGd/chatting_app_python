[1] I think I should first start with making a console application.
    [1.1] Two user peer to peer application.
    [1.2] Users are on the same Network i.e. LAN 

- I think a central server/s should be running infinitely and each time a user sends a message to a fellow contact they should be queued until the other user comes up active.
- Thus, we should maintain a queue of messages to be shown as soon as the other user logs into his/her account.
- Also, this queue must be maintained for each known contact of the user.
- Maintain a ALL_USERS dictionary containing userId, and socket at which they are connected.
- Every time userA wants to message a userB, they can specify their contact userB and send the message to the server. THe server will store this message as an object of (senderID, recieverID, msg) and this message will be disposed off the queue as soon as userB logsin / becomes active.

CURRENT PROGRESS AS OF (19/10/2022):
- User can connect to server and send messages to the server.
- Server is able to store these messages as a list of messages called pending_messages

NEXT GOAL:
- Implement Message dispatch.
- For this first, detect if userId exists in pending messages list, if yes send message to userB using socket
(ofcourse).