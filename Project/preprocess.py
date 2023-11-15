import string, json, pickle

# ( type , rank , row , column )


class Password_Segment:
    keyboard_coordinates = {
        "`": (-1, 0),
        "~": (-1, 0),
        "1": (0, 0),
        "!": (0, 0),
        "2": (0, 1),
        "@": (0, 1),
        "3": (0, 2),
        "#": (0, 2),
        "4": (0, 3),
        "$": (0, 3),
        "5": (0, 4),
        "%": (0, 4),
        "6": (0, 5),
        "^": (0, 5),
        "7": (0, 6),
        "&": (0, 6),
        "8": (0, 7),
        "*": (0, 7),
        "9": (0, 8),
        "(": (0, 8),
        "0": (0, 9),
        ")": (0, 9),
        "-": (0, 10),
        "_": (0, 10),
        "=": (0, 11),
        "+": (0, 11),
        "q": (1, 0),
        "w": (1, 1),
        "e": (1, 2),
        "r": (1, 3),
        "t": (1, 4),
        "y": (1, 5),
        "u": (1, 6),
        "i": (1, 7),
        "o": (1, 8),
        "p": (1, 9),
        "[": (1, 10),
        "{": (1, 10),
        "]": (1, 11),
        "}": (1, 11),
        "\\": (1, 12),
        "|": (1, 12),
        "a": (2, 1),
        "s": (2, 2),
        "d": (2, 3),
        "f": (2, 4),
        "g": (2, 5),
        "h": (2, 6),
        "j": (2, 7),
        "k": (2, 8),
        "l": (2, 9),
        ";": (2, 10),
        ":": (2, 10),
        "'": (2, 11),
        '"': (2, 11),
        "z": (3, 1),
        "x": (3, 2),
        "c": (3, 3),
        "v": (3, 4),
        "b": (3, 5),
        "n": (3, 6),
        "m": (3, 7),
        ",": (3, 8),
        "<": (3, 8),
        ".": (3, 9),
        ">": (3, 9),
        "/": (3, 10),
        "?": (3, 10),
    }

    def __init__(self, segment, position, streak):
        if __debug__: print(f"Creating segment {segment}")
        self.segment = segment
        if __debug__: print(f"Creating position {position}")
        self.position = position
        if __debug__: print(f"Creating streak {streak}")
        self.streak = streak
        self.processed_segment = []
        for c in self.segment:
            if __debug__: print(f"Adding character {c}")
            entry = self.get_type_and_rank(c) + self.get_keyboard_coordinate(c)
            if __debug__: print(f"{c} processed to {entry}")
            self.processed_segment.append(entry)
        if __debug__: print(f"Length information is ({self.position}, {self.streak})")
        self.processed_segment.append((self.position, self.streak))
        if __debug__: print(f"processed_segment is now {self.processed_segment}")

    @staticmethod
    def get_type_and_rank(character):
        char_class = None
        rank = None
        if __debug__: print(f"Looking for character {character} of type {type(character)}")
        if (rank := string.ascii_lowercase.find(character)) > -1:
            char_class = 0
        elif (rank := string.ascii_uppercase.find(character)) > -1:
            char_class = 1
        elif (rank := string.digits.find(character)) > -1:
            char_class = 2
        elif (rank := string.punctuation.find(character)) > -1:
            char_class = 3
        else:
            raise TypeError()
        return (char_class, rank)

    def get_keyboard_coordinate(self, character):
        lookup = character
        if lookup in string.ascii_uppercase:
            lookup = lookup.lower()
        return self.keyboard_coordinates[lookup]


class Password:
    """
    This class holds all processed password segments for a single password.
    """

    def __init__(self, password, norder):
        self.password_segments = []
        self.password = password
        self.norder = norder
        # If the password's length is equal or less than the order, we can just process the entire password as a single segment
        if len(password) <= norder:
            self.long_password = True
        else:
            self.long_password = False
        self._create_streaks()
        self._create_segments()

    def _create_streaks(self):
        """
        A "streak" is a pattern of repeating chracter types.

        E.g. for the password "ABCD1234abcd"

        self.streaks would be:
        [(A,B,C,D), (1,2,3,4), (a,b,c,d)]
        """
        class_list = (
            []
        )  # Converts the password into a list of ordered classes for each character, e.g. "pass1234" would be [0, 0, 0, 0, 2, 2, 2, 2]
        for c in self.password:
            class_list.append(Password_Segment.get_type_and_rank(c)[0])
        self.streaks = []
        # Process the first character as the first character in the first streak tuple
        last_class = class_list[
            0
        ]  # To start, the "last class" is the first class. Put another way, initialize with the class of the first character.
        streak = tuple(
            self.password[0]
        )  # The first char in the first streak is the 0th letter of the password
        for i in range(1,len(class_list)):
            if class_list[i] == last_class:
                streak = streak + tuple(
                    self.password[i]
                )  # If this character is the same class as the previous, append it to this streak tuple
            else:
                self.streaks.append(
                    streak
                )  # If it's different append the streak as is to the streak list...
                streak = tuple(self.password[i])  # ... and create a new streak.
                last_class = class_list[i] # Reset last_class so we can restart the streak

    def _find_streaks(self, index):
        """
        Given a particular index, find where the character is in it's "streak". Return that position in the streak tuple.
        """
        position = 0
        for stk in self.streaks:
            if __debug__: print(stk)
            if (len(stk) + position) <= index:
                if __debug__: print(f"Position {position} is less than index {index}")
                position += len(stk)
                if __debug__: print(f"Moving to position {position}")
        return (index - position + 1)

    def _create_segments(self):
        begin = 0  # Start at the 0th character of the password
        end = self.norder  # End such that the segment is of length n-order

        if self.long_password:
            # If it's not a long password, then just do it once since it's less than or equal to the configured n-order
            self.password_segments.append(
                    Password_Segment(self.password[begin:], len(self.password), self._find_streaks(len(self.password) -1))
                )
        else:
            # Add segments of n-order length from beginning to end of password
            while end <= len(self.password):
                if __debug__: print(f"End is {end}, creating new segment {self.password[begin:end]}")
                self.password_segments.append(
                        Password_Segment(self.password[begin:end], end, self._find_streaks(end - 1))
                    )
                if __debug__:
                    print(f"self.password_segments now has length {len(self.password)}")
                begin += 1
                end += 1
                if __debug__:
                    print(f"Now begin is {begin} and end is {end}")


#password = input("password: ")
filename = input("filename: ")
norder = int(input("n-order: "))

#test = Password(password, norder)
#for seg in test.password_segments:
#    print(seg.processed_segment)
#    print(json.dumps(seg.processed_segment))

passwords = {}
with open(filename, 'r') as password_dump:
    for line in password_dump:
        if __debug__: print(f"Adding password: {line.strip()}")
        current = Password(line.strip(), norder)
        list_builder = []
        for seg in current.password_segments:
           list_builder.append(seg.processed_segment)
        passwords[line.strip()] = list_builder

# There are no tuples in JSON so this saves as lists of lists
#print(json.dumps(passwords) # Use this to print ugly, machine-friendly JSON
print(json.dumps(passwords, indent=4, sort_keys=True)) # Uncomment this if you want the JSON output to look pretty
#with open(f"{filename}.pkl", 'wb') as pickle_file:
#    pickle.dump(passwords, pickle_file) # Use this to create a pickle file that saves the Python objects as bytes and can be easily imported

# Or do something else
