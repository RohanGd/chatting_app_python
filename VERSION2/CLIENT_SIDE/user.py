from ClientClass import User
import threading
I = User()
I.login()
t = threading.Thread(target=(I.get_my_messages))
t.start()

while True:
    command = input("Press 0 to quit, any other to send a message")
    if command == '0':
        t.join(3)
        I.show_messages()
        I.logout()
        break
    I.prompt_user_for_message()

# I.logout()