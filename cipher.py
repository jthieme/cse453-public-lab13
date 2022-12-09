##############################################################################
# COMPONENT:
#    CIPHER01
# Author:
#    Br. Helfrich, Kyle Mueller, Josh Thieme
# Summary:
#    The Playfair cipher starts by creating a perfect square matrix.
#    It then loops through the message, using 2 iterators at a time, then
#    looks up the index of each of those in the matrix, and depending on
#    how the two iterators compare with each others index, then it performs
#    a mathmatical calculation. If there is no relationship, then it simply
#    adds each others indices together. Either of these ways is what actually
#    encrypts the message. To decrypt, it performs the exact same method, with
#    the only difference being it increments by -1, rather than 1 which happens
#    when it encrypts a message.
##############################################################################


##############################################################################
# CIPHER
##############################################################################
class PlayfairCipher:
    def __init__(self):
        self.size = 10
        self.row = self.size
        self.col = self.size

    def get_author(self):
        return "Josh Thieme"

    def get_cipher_name(self):
        return "Playfair Cipher"

    ##########################################################################
    # GET CIPHER CITATION
    # Returns the citation from which we learned about the cipher
    ##########################################################################
    def get_cipher_citation(self):
        return "\nPractical Cryptography, \n" \
               "'PlayFair Cipher', \n" \
               "retreived: \n\thttp://practicalcryptography.com/ciphers/classical-era/playfair/\n\n"\
               "\ndCode, \n" \
               "'PlayFair Cipher', \n" \
               "retreived: \n\thttps://www.dcode.fr/playfair-cipher"

    ##########################################################################
    # GET PSEUDOCODE
    # Returns the pseudocode as a string to be used by the caller
    ##########################################################################
    def get_pseudocode(self):

        # main helper method
        pc = "create_matrix(self, key):\n" \
             "  key <- key.upper()\n" \
             "  fillers <- ['ç', 'è', 'é', 'ê', 'ë']\n" \
             "  matrix <- [['' for i in range(10)] for j in range(10)]\n" \
             "  letters_added <- []\n" \
             "  row <- 0\n" \
             "  col <- 0\n" \
             "  FOR letter IN key:\n" \
             "    IF letter NOT IN letters_added:\n" \
             "      matrix[row][col] <- letter\n" \
             "        letters_added.append(letter)\n" \
             "    ELSE:\n" \
             "      CONTINUE\n" \
             "    IF col == 4:\n" \
             "      col <- 0\n" \
             "      row <- 1\n" \
             "    ELSE:\n" \
             "      col <- 1\n" \
             "  i <- 0\n" \
             "  FOR letter IN range(32,132):\n" \
             "    IF letter < 127:\n" \
             "      IF chr(letter) NOT IN letters_added:\n" \
             "        letters_added.append(chr(letter))\n" \
             "      ELSE:\n" \
             "        letters_added.append(fillers[i])\n" \
             "        i <- 1\n" \
             "  index <- 0\n" \
             "  FOR i IN range(10):\n" \
             "    FOR j IN range(10):\n" \
             "      matrix[i][j] = letters_added[index]\n" \
             "      index <- 1\n" \
             "  RETURN matrix\n\n" \
        
        # helper method
        pc += "playfair(key, message, inc):\n" \
              "  matrix <- create_matrix(key)\n" \
              "  message.separate_same_letters(message)\n"\
              "  FOR (l1, l2) in zip(message[0::2], message[1::2]):\n" \
              "    row1, col1 <- index_of(l1, matrix)\n" \
              "    row2, col2 <- index_of(l2, matrix)\n" \
              "    IF row1 == row2:\n"\
              "      cipher_text <- matrix[row1][(col1 + inc) % self.size] + matrix[row2][(col2 + inc) % self.size]\n" \
              "    ELIF col1 == col2:\n" \
              "      cipher_text <- matrix[(row1 + inc) % self.size][col1] + matrix[(row2 + inc) % self.size][col2]\n" \
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
        
        # initialize needed variables
        key = key.upper()

        # give bogus values to keep things working
        fillers = ['ç', 'è', 'é', 'ê', 'ë']
        matrix = [['' for i in range(self.row)] for j in range(self.col)]
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
            if col == self.size - 1:
                col = 0
                row += 1
            else:
                col += 1
        
        # Add the rest of the alphabet to the matrix
        # ' ': 32, ~: 126 
        # A: 65, Z: 90
        # fillers['\n', '\t', '\r', '\!', '\#']
        #          127   128   129   130   131

        # index for the filler list
        i = 0
        for letter in range(32,132):
            # when we reach the end of the 95 normal characters
            # then use our 5 filler characters   
            if letter < 127:       
                # Cannot add repeated letters
                if chr(letter) not in letters_added:
                    letters_added.append(chr(letter))
            # add our our bogus "characters" to make a perfect 10x10 matrix
            else:
                letters_added.append(fillers[i])
                i += 1
        
        # replace the initial values ('') with everything
        # inside the letters_added list
        index = 0

        for i in range(self.row):
            for j in range(self.col):
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
                # message = message + 'X'
                index += 2
                continue
            
            # look at next letter
            l2 = message[index + 1]
            
            # if the current and next letters are the same
            if l1 == l2:
                # note that they are the same with an X in between the letters
                # message = message[:index + 1] + "X" + message[index + 1:]
                message = message[:index + 1] + message[index + 1:]
            index += 2
       
        return message

    ##########################################################################
    # INDEX OF
    # Return the index of each letter in the matrix so we know which rule
    # to use in the playfair() method
    ##########################################################################
    def index_of(self, letter, matrix):
        # for every letter
        for i in range(100):
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
        # message = message.upper()
        # message = message.replace(' ', '')
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
                cipher_text += matrix[row1][(col1 + inc) % self.size] + matrix[row2][(col2 + inc) % self.size]
            
            # Rule 3: The letters are in the same column
            elif col1 == col2:
                cipher_text += matrix[(row1 + inc) % self.size][col1] + matrix[(row2 + inc) % self.size][col2]
            
            # Rule 4: The letters are in a different row and column
            else:
                cipher_text += matrix[row1][col2] + matrix[row2][col1]
        
        return cipher_text