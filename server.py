import socket
import chatlib
import random
import select

# GLOBALS
users = {}
questions = {}
logged_users = {} # a dictionary of client hostnames to usernames - will be used later
messages_to_send = []


ERROR_MSG = "Error! "
SERVER_PORT = 5678
SERVER_IP = "127.0.0.1"


# HELPER SOCKET METHODS

def build_and_send_message(conn, code, data):
	"""
	Builds a new message using chatlib, wanted code and message. 
	Prints debug info, then sends it to the given socket.
	Paramaters: conn (socket object), code (str), data (str)
	Returns: Nothing
	"""
	global messages_to_send

	full_msg = chatlib.build_message(code, data)
	messages_to_send.append((conn, full_msg))
	print("[SERVER] ",full_msg)	


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
	
	print("[CLIENT] ",full_msg)	  

def print_client_sockets(client_sockets):
	global logged_users
	for conn in client_sockets:
		addr = conn.getpeername()
		user_IP = addr[0]
		user_PORT = addr[1]
		if conn in logged_users:
			user_name = logged_users[conn]
			print(f"{user_name} IP: {user_IP}, and port {user_PORT}")
		else:
			print(f"{user_IP} is not logged in yet")



# Data Loaders #

def load_questions():
	"""
	Loads questions bank from file	## FILE SUPPORT TO BE ADDED LATER
	Recieves: -
	Returns: questions dictionary
	"""
	questions = {2313 : {"question":"How much is 2+2","answers":["3","4","2","1"],"correct":2},
				4122 : {"question":"What is the capital of France?","answers":["Lion","Marseille","Paris","Montpellier"],"correct":3} 
				}
	
	return questions

def load_user_database():
	"""
	Loads users list from file	## FILE SUPPORT TO BE ADDED LATER
	Recieves: -
	Returns: user dictionary
	"""
	users = {
			"test"		:	{"password":"test","score":0,"questions_asked":[]},
			"yossi"		:	{"password":"123","score":50,"questions_asked":[]},
			"master"	:	{"password":"master","score":200,"questions_asked":[]}
			}
	return users


def create_random_question():
	global questions
	Q_keys = list(questions.keys())
	random_id = random.choice(Q_keys)
	Q_data = questions[random_id]
	Q_text = Q_data["question"]
	answers_list = Q_data["answers"]
	correct_A = Q_data["correct"]
	data = (f"{random_id}#{Q_text}#{answers_list[0]}#{answers_list[1]}#{answers_list[2]}#{answers_list[3]}#{correct_A}")
	return data

	
# SOCKET CREATOR

def setup_socket():
	"""
	Creates new listening socket and returns it
	Recieves: -
	Returns: the socket object
	"""
	print("The server is up and running...")
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_socket.bind((SERVER_IP, SERVER_PORT))
	server_socket.listen()
	
	return server_socket
	


		
def send_error(conn, error_msg):
	"""
	Send error message with given message
	Recieves: socket, message error string from called function
	Returns: None
	"""
	build_and_send_message(conn, ERROR_MSG, error_msg)
	


	
##### MESSAGE HANDLING

def handle_question_message(conn):
	data = create_random_question()
	build_and_send_message(conn, chatlib.PROTOCOL_SERVER["your_question_msg"], data)

def handle_answer_message(conn, username, data):
	global questions
	global users

	data = chatlib.split_data(data, 2)
	user_Q = data[0]
	user_A = int(data[1])
	correct_A = (questions[int(user_Q)]["correct"])


	if user_A == correct_A:
		users[username]["score"] += 5
		build_and_send_message(conn, chatlib.PROTOCOL_SERVER["correct_answer_msg"], "")
	else:
		build_and_send_message(conn, chatlib.PROTOCOL_SERVER["wrong_answer_msg"], str(correct_A))


def handle_getscore_message(conn, username):
	global users
	user_score = users[username]["score"]
	data = str(user_score)
	build_and_send_message(conn, chatlib.PROTOCOL_SERVER["your_score_msg"], data)

def handle_highscore_message(conn):
	global users
	sorted_users = sorted(users.items(), key = lambda item: item[1]["score"], reverse = True)
	highscore_table = ""
	for username, user_data in sorted_users:
		highscore_table += f"{username}:{user_data['score']}\n"	
	build_and_send_message(conn, chatlib.PROTOCOL_SERVER["high_score_msg"], highscore_table)


def handle_logged_message(conn):
	global logged_users

	current_logged_users = logged_users.values()
	str_users = ", ".join(current_logged_users)
	build_and_send_message(conn, "LOGGED_USERS_OK", str_users)



def handle_logout_message(conn):
	"""
	Closes the given socket (in laster chapters, also remove user from logged_users dictioary)
	Recieves: socket
	Returns: None
	"""
	global logged_users
	if conn in logged_users:
		del logged_users[conn]
	conn.close()

def handle_login_message(conn, data):
	"""
	Gets socket and message data of login message. Checks  user and pass exists and match.
	If not - sends error and finished. If all ok, sends OK message and adds user and address to logged_users
	Recieves: socket, message code and data
	Returns: None (sends answer to client)
	"""
	global users  # This is needed to access the same users dictionary from all functions
	global logged_users	 # To be used later

	
	user_passw_data = chatlib.split_data(data, 2)
	username = user_passw_data[0]
	password = user_passw_data[1]
	if username in users:
		if users[username]["password"] == password:
			build_and_send_message(conn, "LOGIN_OK", "")
			logged_users[conn] = username
		else:
			send_error(conn, "Wrong password")
	else:
		send_error(conn, "Username does not exist")
	


def handle_client_message(conn, cmd, data):
	"""
	Gets message code and data and calls the right function to handle command
	Recieves: socket, message code and data
	Returns: None
	"""
	global logged_users	 # To be used later
	cmd = cmd.strip()	
	if conn  not in logged_users:
		if cmd == "LOGIN":
			handle_login_message(conn, data)
		else:
			send_error(conn, "you are not connected")
	else:
		if cmd == "LOGOUT":
			handle_logout_message(conn)
		elif cmd == "MY_SCORE":
			handle_getscore_message(conn, logged_users[conn])
		elif cmd == "HIGH_SCORE":
			handle_highscore_message(conn)
		elif cmd == "LOGGED_USERS":
			handle_logged_message(conn)
		elif cmd == "GET_QUESTION":
			handle_question_message(conn)
		elif cmd == "SEND_ANSWER":
			handle_answer_message(conn, logged_users[conn], data)
		else:
			send_error(conn, "Command is not familier with the server")	


def main():
	# Initializes global users and questions dicionaries using load functions, will be used later
	global users
	global questions
	global messages_to_send
	users = load_user_database()
	questions = load_questions()
	client_sockets = []
	
	print("Welcome to Trivia Server!")
	server_socket = setup_socket()
	print("Waiting for new connections")
	while True:
		rlist, wlist, xlist = select.select([server_socket] + client_sockets, [], [])
		for conn in rlist:
			if conn == server_socket:
				new_conn,  addr = server_socket.accept()
				client_sockets.append(new_conn)
				print(f"new connection from{addr}")
			else:
				cmd, data = recv_message_and_parse(conn)
				if cmd == None:
					print("Client is disconnected")
					client_sockets.remove(conn)
					conn.close()
				elif cmd == "LOGOUT":
					print("Client is disconnected")
					handle_logout_message(conn)
					client_sockets.remove(conn)
				else:
					handle_client_message(conn, cmd, data)

		for message_tuple in messages_to_send:
			sock, msg = message_tuple
			sock.send(msg.encode())
		messages_to_send = []


	# Implement code ...



if __name__ == '__main__':
	main()



