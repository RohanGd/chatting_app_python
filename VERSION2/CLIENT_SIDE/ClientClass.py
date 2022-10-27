import socket
# from CLIENT_SIDE.Message import Message_obj
from SERVER_INFO import get_server_info
from Message import Message_obj
from pickle import dumps, loads

class User:
    def __init__(self):
        self.Id = None
        while self.Id == None:
            print("Enter a valid ", end='')
            self.Id = self.set_id()
        self.sock = None 
        self.server_ADDR = get_server_info()
        self.my_messages = []
    
    def login(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(self.server_ADDR)
        self.sock.send(str(self.Id).encode())
        # self.get_my_messages()

    def logout(self):
        # s = "0_EOF_0"
        # self.sock.send(str(s).encode())
        self.sock.send("0".encode())
        self.sock.close()
    
    def prompt_user_for_message(self):
        # s = "1!EOF!1"
        # self.sock.send(s.encode())
        reciever = int(input("Enter contact to send to: ")) 
        if not (reciever > 1000000000 and reciever < 10000000000):
            print("Invalid contact")
            return

        msg = input(f"{self.Id} -> {reciever} :")
        msg = Message_obj(self.Id, reciever, msg)
        msg = dumps(msg)
        
        self.send_message(msg)

    def send_message(self, msg):
        # buff = 64
        dat_size = len(msg)
        print(dat_size)
        self.sock.send(str(dat_size).encode())
        # while dat_size:
        #     self.sock.send(msg, buff)
        #     dat_size -= buff
        self.sock.send(msg)

    def set_id(self):
        x = input("Phone number: (IN +91) ")
        x = int(x) 
        if x > 1000000000 and x < 10000000000:
            return x
        return None 

    def get_my_messages(self):
        while True:
            try:
                buff = 64
                dat_size = int(self.sock.recv(64).decode())
                if dat_size == 0:
                    return
                msg = b""
                print(dat_size)
                while dat_size>0:
                    dat = self.sock.recv(min(buff,dat_size))
                    dat_size -= buff
                    msg += dat
                
                msg = loads(msg)
                print(msg.message)
                self.my_messages.append(msg)
            except:
                return
    def show_messages(self):
        print(self.my_messages)
    

