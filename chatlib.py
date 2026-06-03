CMD_FIELD_LENGTH = 16	
LENGTH_FIELD_LENGTH = 4  
MAX_DATA_LENGTH = 10**LENGTH_FIELD_LENGTH-1  
MSG_HEADER_LENGTH = CMD_FIELD_LENGTH + 1 + LENGTH_FIELD_LENGTH + 1  
MAX_MSG_LENGTH = MSG_HEADER_LENGTH + MAX_DATA_LENGTH  
DELIMITER = "|"  
DATA_DELIMITER = "#"  

# Protocol Messages 
# In this dictionary we will have all the client and server command names

PROTOCOL_CLIENT = {
"login_msg" : "LOGIN",
"logout_msg" : "LOGOUT",
"get_score_msg" : "MY_SCORE",
"get_high_score_msg" : 'HIGH_SCORE',
"get_question_msg" : "GET_QUESTION",
"send_answer_msg" : "SEND_ANSWER",
"get_logged_users_msg" : "LOGGED_USERS"
} # .. Add more commands if needed


PROTOCOL_SERVER = {
"login_ok_msg" : "LOGIN_OK",
"login_failed_msg" : "ERROR",
"your_score_msg" : "YOUR_SCORE",
"high_score_msg" : "HIGH_SCORE_OK",
"your_question_msg" : "YOUR_QUESTION",
"no_questions_msg" : "NO_QUESTIONS",
"correct_answer_msg" : "CORRECT_ANSWER",
"wrong_answer_msg" : "WRONG_ANSWER",
'logged_users_msg' : "LOGGES_USERS_OK"
} # ..  Add more commands if needed


# Other constants

ERROR_RETURN = None  # What is returned in case of an error


def build_message(cmd, data):
    """
    Gets command name (str) and data field (str) and creates a valid protocol message
    Returns: str, or None if error occured
	"""
    if len(cmd) > 16:
        return None
    elif len(data) > 9999:
        return None
    cmd = cmd.ljust(16)
    LLLL = str(len(data)).zfill(4)
    full_msg = cmd + DELIMITER + LLLL + DELIMITER + data 
    return full_msg


def parse_message(data):
    """
    Parses protocol message and returns command name and data field
    Returns: cmd (str), data (str). If some error occured, returns None, None
    """
    data_list = data.split(DELIMITER)
    if len(data_list) != 3: 
        return None, None

    cmd = data_list[0].strip()
    msg = data_list[2]
    length_str = data_list[1].strip()

    if not length_str.isdigit() or int(length_str) != len(msg):
        return None, None

    return cmd, msg

	
def split_data(msg, expected_fields):
    """
    Helper method. gets a string and number of expected fields in it. Splits the string 
    using protocol's data field delimiter (|#) and validates that there are correct number of fields.
    Returns: list of fields if all ok. If some error occured, returns None
    """
    if not msg:
        return None
    msg_split = msg.split(DATA_DELIMITER)
    cleaned_fields = []
    for field in msg_split:
        cleaned_fields.append(field.strip())
    if len(cleaned_fields) == expected_fields:
        return cleaned_fields
    else:
        return None






def join_data(msg_fields):
    """
    Helper method. Gets a list, joins all of it's fields to one string divided by the data delimiter. 
    Returns: string that looks like cell1#cell2#cell3
    """
    cleaned_fields = []
    for field in msg_fields:
        str_msg = str(field)
        cleaned_fields.append(str_msg)
    return DATA_DELIMITER.join(cleaned_fields)
	