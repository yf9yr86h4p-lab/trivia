import socket
import chatlib 

SERVER_IP = "127.0.0.1" 
SERVER_PORT = 8888

def build_and_send_message(conn, code, data):
    """
    Builds a new message using chatlib, wanted code and message. 
    Prints debug info, then sends it to the given socket.
    Paramaters: conn (socket object), code (str), data (str)
    Returns: Nothing
    """
    full_msg = chatlib.build_message(code, data)
    conn.send(full_msg.encode())

	

def recv_message_and_parse(conn):
    """
    Recieves a new message from given socket,
    then parses the message using chatlib.
    Paramaters: conn (socket object)
    Returns: cmd (str) and data (str) of the received message. 
    If error occured, will return None, None
    """
    full_msg = conn.recv(1024).decode()
    if full_msg == '':
        return None, None
    cmd, data = chatlib.parse_message(full_msg)
    return cmd, data
	
	

def connect():
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.connect((SERVER_IP, SERVER_PORT))
    return my_socket


def error_and_exit(error_msg):
    print(error_msg)
    exit()

def login(conn):
    while True:
        username = input("Please enter username:\n")
        password = input("Please enter password:\n")
        data = username + "#"  + password	
        build_and_send_message(conn, chatlib.PROTOCOL_CLIENT["login_msg"], data)
        cmd, msg = recv_message_and_parse(conn)
        if cmd == chatlib.PROTOCOL_SERVER["login_ok_msg"]:
            print("Logged in!")
            return
        else:
            print(chatlib.PROTOCOL_SERVER["login_failed_msg"])            
        


def logout(conn):
    build_and_send_message(conn, chatlib.PROTOCOL_CLIENT["logout_msg"], "")
    print("Goodbye!")

def build_send_recv_parse(conn, code, data):
    build_and_send_message(conn, code, data)
    msg_code, data = recv_message_and_parse(conn)
    return msg_code, data

def get_score(conn):
    msg_code, data = build_send_recv_parse(conn, chatlib.PROTOCOL_CLIENT["get_score_msg"], "")
    if msg_code == chatlib.PROTOCOL_SERVER["your_score_msg"]:
        print("Your score is:", data)
    else:
        print("ERROR")

def get_highscore(conn):
    score_msg, data = build_send_recv_parse(conn, chatlib.PROTOCOL_CLIENT["get_high_score_msg"], "")
    if score_msg == chatlib.PROTOCOL_SERVER["high_score_msg"]:
        print(data)
    else:
        print("ERROR")

def play_question(conn):
    msg_code, data =  build_send_recv_parse(conn, chatlib.PROTOCOL_CLIENT["get_question_msg"], "")
    if msg_code == chatlib.PROTOCOL_SERVER["no_questions_msg"]:
        print("No more question left!")
    elif msg_code == chatlib.PROTOCOL_SERVER["your_question_msg"]:
        print("Question is:", data)
        user_answer = input("Please choose an answer [1-4]: ")
        msg_code, data = build_send_recv_parse(conn, chatlib.PROTOCOL_CLIENT["send_answer_msg"], user_answer)
        if msg_code == chatlib.PROTOCOL_SERVER["correct_answer_msg"]:
            print("Your answer is correct!")
        elif msg_code == chatlib.PROTOCOL_SERVER["wrong_answer_msg"]:
            print("Nope, correct answer is", data)

def  get_logged_users(conn):
    msg_code, data = build_send_recv_parse(conn, chatlib.PROTOCOL_CLIENT["get_logged_users_msg"], "")
    if msg_code == chatlib.PROTOCOL_SERVER["logged_users_msg"]:
        print(data)
    else:
        print("ERROR")

    

def main():
    my_socket = connect()
    login(my_socket)
    while True:
        print("p       Play a trivia question\ns       Get my score\nh       Get highscore\nl       Get logged users\nq       Quit")
        user_input = input("Please enter your choice: ")
        if user_input == "p":
            play_question(my_socket)
        elif user_input == "s":
            get_score(my_socket)
        elif user_input == "h":
            get_highscore(my_socket)
        elif user_input == "l":
            get_logged_users(my_socket)
        elif user_input == "q":
            logout(my_socket)
            break
    my_socket.close()
    

if __name__ == '__main__':
    main()