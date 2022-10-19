from ClientClass import User

I = User()
I.login()
while True:
    command = input("Press 0 to quit, any other to continue")
    if command == '0':
        I.logout()
        break
    I.prompt_user_for_message()

# I.logout()