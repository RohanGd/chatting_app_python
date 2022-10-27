import socket
from pickle import dumps, loads
# import json
import threading
import queue
# import multiprocessing.connection

# from numpy import array, unique
from Message import Message_obj

from SERVER_INFO import get_server_info

# ________________________________________________________________________ #
ADDR = get_server_info()
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(ADDR)
# sock.setblocking(0)
pending_messages = queue.Queue()
ALL_USERS = dict()
ACTIVE_USERS = set()
HEADER_LENGTH = 32

def is_communicating(client_sock):
    try:
        client_sock.send(b"ping")
    except:
        return False
    return True

def communicate_with_client(client_sock, client_addr, pending_messages, ACTIVE_USERS, client_id):
    print("[CONNECTION ESTABLISHED]")
    buff = 64
    # while is_communicating(client_sock):
    while True:
        try:
            dat_size = int(client_sock.recv(64).decode())
            msg = b""
            print(dat_size)
            while dat_size>0:
                dat = client_sock.recv(min(buff,dat_size))
                dat_size -= buff
                msg += dat
            
            msg = loads(msg)
            pending_messages.put(msg)
        except:
            # client_sock.close()
            ACTIVE_USERS.remove(client_id)
            break

    for msg_obj in list(pending_messages.queue):
        print(msg_obj.message)


def setup_connections(ADDR, sock, pending_messages, ALL_USERS, ACTIVE_USERS):
    run = True
    while run:
        client_sock, client_addr = sock.accept()
        client_id = int(client_sock.recv(10).decode())
        ALL_USERS[client_id] = client_sock
        ACTIVE_USERS.add(client_id)
        threading.Thread(target=communicate_with_client, args=(client_sock, client_addr, pending_messages, ACTIVE_USERS, client_id)).start()
        print(ALL_USERS.keys)
        print(ACTIVE_USERS)


def send_message(client_sock, msg):
    try:
        msg = dumps(msg)
        dat_size = len(msg)
        # print(dat_size)
        client_sock.send(str(dat_size).encode())

        client_sock.send(msg)
    except:
        return
def distribute_messages(ADDR, sock, pending_messages, ALL_USERS, ACTIVE_USERS):
    while True:
        try: 
            msg = pending_messages.get()
        except:
            continue
        reciever = msg.reciever
        reciever_sock = None
        try: 
            reciever_sock = ALL_USERS.get(reciever)
        except:
            print(f"[INVALID MESSAGE] User not found - {reciever}. Message from {msg.sender} cannot be sent.")
        
        if reciever in ACTIVE_USERS:
            send_message(reciever_sock,msg)
        else:
            pending_messages.put_nowait(msg)   


sock.listen(10)
print('[Searching for Connections...]')
set_connections_thread = threading.Thread(target=setup_connections, args=(ADDR, sock, pending_messages, ALL_USERS, ACTIVE_USERS))
message_distribution_thread = threading.Thread(target=distribute_messages, args=(ADDR, sock, pending_messages, ALL_USERS, ACTIVE_USERS))

set_connections_thread.start()
message_distribution_thread.start()

set_connections_thread.join()
message_distribution_thread.join()

for msg_obj in list(pending_messages.queue):
    print(msg_obj.message)


