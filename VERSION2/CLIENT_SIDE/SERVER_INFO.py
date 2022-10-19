SERVER_IP = "127.0.0.1"
PORT = 7275
ADDR = (SERVER_IP, PORT)
from copy import deepcopy
def get_server_info():
    return deepcopy(ADDR) 