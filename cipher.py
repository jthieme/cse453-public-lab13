##############################################################################
# COMPONENT:
#    CIPHER01
# Author:
#    Br. Helfrich, Kyle Mueller, <your name here if you made a change>
# Summary:
#    Implement your cipher here. You can view 'example.py' to see the
#    completed Caesar Cipher example.
##############################################################################


##############################################################################
# CIPHER
##############################################################################
class Cipher:
    def __init__(self):
        pass

    def get_author(self):
        # TODO: Return your name
        return "Josh Thieme"

    def get_cipher_name(self):
        # TODO: Return the cipher name
        return "Playfair Cipher"

    ##########################################################################
    # GET CIPHER CITATION
    # Returns the citation from which we learned about the cipher
    ##########################################################################
    def get_cipher_citation(self):
        # TODO: This function should return your citation(s)
        return "\nPractical Cryptography, \n" \
               "'PlayFair Cipher', \n" \
               "retreived: \n\thttp://practicalcryptography.com/ciphers/classical-era/playfair/"

    ##########################################################################
    # GET PSEUDOCODE
    # Returns the pseudocode as a string to be used by the caller
    ##########################################################################
    def get_pseudocode(self):

        # main helper method
        pc = "playfair(key, message, inc):\n" \
             "  matrix <- create_matrix(key)\n" \
             "  message <- message.upper()\n" \
             "  message.replace(' ', '')\n" \
             "  message.separate_same_letters(message)\n"\
             "  FOR (l1, l2) in zip(message[0::2], message[1::2]):\n" \
             "    row1, col1 <- index_of(l1, matrix)\n" \
             "    row2, col2 <- index_of(l2, matrix)\n" \
             "    IF row1 == row2:\n"\
             "      cipher_text <- matrix[row1][(col1 + inc) % 5] + matrix[row2][(col2 + inc) % 5]\n" \
             "    ELIF col1 == col2:\n" \
             "      cipher_text <- matrix[(row1 + inc) % 5][col1] + matrix[(row2 + inc) % 5][col2]\n" \
             "    ELSE:\n" \
             "      cipher_text <- matrix[row1][col2] + matrix[row2][col1]\n"\
             "  RETURN cipher_text\n\n"

        # The encrypt pseudocode
        pc += "encrypt(key, message):\n" \
              "  inc <- 1\n" \
              "  RETURN playfair(key, message, inc)\n\n"

        # The decrypt pseudocode
        pc += "decrypt(key, message):\n" \
              "  inc <- -1\n" \
              "  RETURN playfair(key, message, inc)\n\n"

        return pc

    ##########################################################################
    # ENCRYPT
    # Increment by 1 if we are encrypting and pass all the parameters along
    # Ensure that the password is 6 letters long, otherwise, use default 
    # password
    ##########################################################################
    def encrypt(self, plaintext, password):
        inc = 1
        if len(password) < 6:
            password = 'secret'
            return self.playfair(password, plaintext, inc)
        return self.playfair(password, plaintext, inc)

    ##########################################################################
    # DECRYPT
    # Increment by -1 if we are decrypting and pass all the parameters along
    # Ensure that the password is 6 letters long, otherwise, use default 
    # password
    ##########################################################################
    def decrypt(self, ciphertext, password):
        inc = -1
        if len(password) < 6:
            password = 'secret'
            return self.playfair(password, ciphertext, inc)
        return self.playfair(password, ciphertext, inc)

    ##########################################################################
    # CREATE MATRIX
    # Create a 5 x 5 matrix while using the key that Playfair depends on, 
    # and ensure that no duplicate letters are within the matrix
    ##########################################################################
    def create_matrix(self, key):
        key = key.upper()
        matrix = [[0 for i in range(5)] for j in range(5)]
        letters_added = []
        row = 0
        col = 0
        
        # Add the key to the matrix
        for letter in key:
            if letter not in letters_added:
                matrix[row][col] = letter
                letters_added.append(letter)
            else:
                continue
            if col == 4:
                col = 0
                row += 1
            else:
                col += 1
        
        # Add the rest of the alphabet to the matrix
        # A: 65, Z: 90
        for letter in range(65,91):
            
            # I / J are in the same position
            if letter == 74:
                continue

            # Cannot add repeated letters
            if chr(letter) not in letters_added:
                letters_added.append(chr(letter))
            
        index = 0
        for i in range(5):
            for j in range(5):
                matrix[i][j] = letters_added[index]
                index += 1
        
        return matrix

    ##########################################################################
    # SEPARATE SAME LETTERS
    # This is to add filler letters if the same letter in already in a pair
    ##########################################################################
    def separate_same_letters(self, message):
        # initialize variable
        index = 0

        # loop as long as index in less than the length of the message
        while index < len(message):
            # look at current letter
            l1 = message[index]

            # if we reach the size of the message - 1
            if index == len(message) - 1:

                # note that we reached the end of the message
                message = message + 'X'
                index += 2
                continue
            
            # look at next letter
            l2 = message[index + 1]
            
            # if the current and next letters are the same
            if l1 == l2:
                # note that they are the same with an X in between the letters
                message = message[:index + 1] + "X" + message[index + 1:]
            index += 2
       
        return message

    ##########################################################################
    # INDEX OF
    # Return the index of each letter in the matrix so we know which rule
    # to use in the playfair() method
    ##########################################################################
    def index_of(self, letter, matrix):
        # for every letter
        for i in range(5):
            try:
                # find the index and return it
                index = matrix[i].index(letter)
                return (i, index)
            except:
                continue

    ##########################################################################
    # PLAY FAIR
    # This will either encrypt a message (if inc is 1), or decrypt a message
    # (if inc is -1)
    ##########################################################################
    def playfair(self, key, message, inc):
        
        # initialize variables we will need
        matrix = self.create_matrix(key)
        message = message.upper()
        message = message.replace(' ', '')
        message = self.separate_same_letters(message)
        cipher_text = ''

        # loop through two indices at once
        for (l1, l2) in zip(message[0::2], message[1::2]):
            
            # find the indices for both rows and cols
            # to know for sure which rule we need to use
            row1, col1 = self.index_of(l1, matrix)
            row2, col2 = self.index_of(l2, matrix)

            # Rule 2: Letters are in same row
            if row1 == row2:
                cipher_text += matrix[row1][(col1 + inc) % 5] + matrix[row2][(col2 + inc) % 5]
            
            # Rule 3: The letters are in the same column
            elif col1 == col2:
                 cipher_text += matrix[(row1 + inc) % 5][col1] + matrix[(row2 + inc) % 5][col2]
            
            # Rule 4: The letters are in a different row and column
            else:
                cipher_text += matrix[row1][col2] + matrix[row2][col1]

        return cipher_text

