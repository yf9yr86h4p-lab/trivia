HANGMAN_PHOTOS = {
    1  : """x-------x""" , 
    2 : """\n    x-------x\n    |\n    |\n    |\n    |\n    |\n\t""",  
    3 : """\n    x-------x\n    |       |\n    |       0\n    |\n    |\n    |\n\t""", 
    4 : """\n    x-------x\n    |       |\n    |       0\n    |       |\n    |\n    |\n\t""", 
    5 : """\n    x-------x\n    |       |\n    |       0\n    |      /|\\\n    |\n    |\n\t""", 
    6 : """\n    x-------x\n    |       |\n    |       0\n    |      /|\\\n    |      /\n    |\n\t""", 
    7 : """\n    x-------x\n    |       |\n    |       0\n    |      /|\\\n    |      / \\\n    |\n\t"""}
def check_win(secret_word, old_letters_guessed):
    """ The function returns True if all the letters that make up the secret word are included in the list of letters that the user guessed. Otherwise, the function returns False.
    param secret word = the secret word the user must guess
    param old letters guessed = A list contains user's old letter guessed
    type secret word = str
    type old letters guessed = list"""
    for char in secret_word.lower():
        if char not in old_letters_guessed:
            return False
    return True
def show_hidden_word(secret_word, old_letters_guessed):
    """ This function shows and helps the user how many letters are left to guess using ' _ '.
    param secret word = the secret word the user must guess.
    param old letters guessed = A list contains user's old letter guessed.
    type secret word = str
    type old letters guessed = list """
    display_str = ""
    for char in secret_word:
        if char in old_letters_guessed:
           display_str += char + " "
        else: display_str += "_ "
    return display_str.strip()
def is_valid_input(letter_guessed, old_letters_guessed):
    """ The function returns a Boolean value representing the validity of the string and
    whether the user has already guessed the character before.
    param letter guessed = represents the character received from the player.
    param old letters guessed = A list contains user's old letter guessed.
    type letter guessed = str
    type old letters guessed = list """
    letter_guessed = letter_guessed.lower()
    if len(letter_guessed) > 1:
        return False
    elif not letter_guessed.isalpha():
        return False
    else:
        return True
def try_update_letter_guessed(letter_guessed, old_letters_guessed):
    """ The function returns True and updates the list if the guess is a new valid letter. Otherwise, it prints 'X' with the sorted list of guesses and returns False.
    param letter guessed = represents the character received from the player.
    param old letters guessed = A list contains user's old letter guessed.
    type letter guessed = str
    type old letters guessed = list """
    letter_guessed = letter_guessed.lower()
    if is_valid_input(letter_guessed, old_letters_guessed) == True:
        letter_guessed = letter_guessed.lower()
        old_letters_guessed.append(letter_guessed)
        return True
    else:
       print("X")
       print(" -> ".join(sorted(old_letters_guessed)))
       return False
def choose_word(file_path, index):
    """ This function chooses a word for the player that will be the secret word to guess, from a text file containing a list of words. 
    param file path = A path to the text file
    param index = A location of a specific word in the file.
    type file path = file
    type index = int 
    The function returns a tuple of the number of distinct words in the file, and
    a word at the position received as an argument to the function. """
    file = open(file_path, "r")
    content = file.read()
    file.close()
    
    words_list = content.split() 
    
    unique_words = set(words_list)
    num_unique = len(unique_words)
    
    word_index = (index - 1) % len(words_list)
    chosen_word = words_list[word_index]
    
    return (num_unique, chosen_word)
def main():
    OPENING_STATEMENT = "Welcome to the game Hangman"
    OPENING_STRING = r"""   | |  | |                                        
        | |__| | __ _ _ __   __ _ _ __ ___   __ _ _ __  
        |  __  |/ _` | '_ \ / _` | '_ ` _ \ / _` | '_ \ 
        | |  | | (_| | | | | (_| | | | | | | (_| | | | |
        |_|  |_|\__,_|_| |_|\__, |_| |_| |_|\__,_|_| |_|
                            __/  |                      
                           |___ /"""
    HANGMAN_ASCII_ART = OPENING_STATEMENT + "\n\n" + OPENING_STRING + "\n\n\n" 
    MAX_TRIES = 6
    print(HANGMAN_ASCII_ART , MAX_TRIES ,"\n")
    file_path = input("Enter file path: ")
    index = int(input("Enter a index: "))
    result = choose_word(file_path, index)
    secret_word = result[1]  
    old_letters_guessed = []
    num_of_tries = 0
    MAX_TRIES = 6
    while num_of_tries < MAX_TRIES:
        print(show_hidden_word(secret_word, old_letters_guessed))
        letter = input("Guess a letter: ")
        if letter.lower() in old_letters_guessed:
            print(" -> ".join(sorted(old_letters_guessed)))
            continue
        if try_update_letter_guessed(letter, old_letters_guessed):
            if check_win(secret_word, old_letters_guessed):
                print("WIN")
                return
            if letter.lower() not in secret_word.lower():
                num_of_tries += 1
                print("X")
                print(HANGMAN_PHOTOS[num_of_tries + 1])
        
    print("LOSE")
if __name__ == "__main__":
    main()