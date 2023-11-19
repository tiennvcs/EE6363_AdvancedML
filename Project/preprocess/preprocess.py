import string, json, pickle, argparse, sys
from tqdm import tqdm

# ( type , rank , row , column )


class Password_Segment:
    keyboard_coordinates = {
        "`": (1, 0),
        "~": (1, 0),
        "1": (1, 1),
        "!": (1, 1),
        "2": (1, 2),
        "@": (1, 2),
        "3": (1, 3),
        "#": (1, 3),
        "4": (1, 4),
        "$": (1, 4),
        "5": (1, 5),
        "%": (1, 5),
        "6": (1, 6),
        "^": (1, 6),
        "7": (1, 7),
        "&": (1, 7),
        "8": (1, 8),
        "*": (1, 8),
        "9": (1, 9),
        "(": (1, 9),
        "0": (1, 10),
        ")": (1, 10),
        "-": (1, 11),
        "_": (1, 11),
        "=": (1, 12),
        "+": (1, 12),
        "q": (2, 1),
        "w": (2, 2),
        "e": (2, 3),
        "r": (2, 4),
        "t": (2, 5),
        "y": (2, 6),
        "u": (2, 7),
        "i": (2, 8),
        "o": (2, 9),
        "p": (2, 10),
        "[": (2, 11),
        "{": (2, 11),
        "]": (2, 12),
        "}": (2, 12),
        "\\": (2, 13),
        "|": (2, 13),
        "a": (3, 1),
        "s": (3, 2),
        "d": (3, 3),
        "f": (3, 4),
        "g": (3, 5),
        "h": (3, 6),
        "j": (3, 7),
        "k": (3, 8),
        "l": (3, 9),
        ";": (3, 10),
        ":": (3, 10),
        "'": (3, 11),
        '"': (3, 11),
        "z": (4, 1),
        "x": (4, 2),
        "c": (4, 3),
        "v": (4, 4),
        "b": (4, 5),
        "n": (4, 6),
        "m": (4, 7),
        ",": (4, 8),
        "<": (4, 8),
        ".": (4, 9),
        ">": (4, 9),
        "/": (4, 10),
        "?": (4, 10),
    }

    def __init__(self, segment, position, streak, suffix=[]):
        if __debug__:
            print(f"Creating segment {segment}")
        self.segment = segment
        if __debug__:
            print(f"Creating position {position}")
        self.position = position
        if __debug__:
            print(f"Creating streak {streak}")
        self.streak = streak
        self.processed_segment = []
        for c in self.segment:
            if c == "😀":
                self.processed_segment.append((0, 0, 0, 0))
            else:
                if __debug__:
                    print(f"Adding character {c}")
                entry = self.get_type_and_rank(c) + self.get_keyboard_coordinate(c)
                self.processed_segment.append(entry)
                if __debug__:
                    print(f"{c} processed to {entry}")
                #for num in entry:
                #    self.processed_segment.append(num)
        if __debug__:
            print(f"Length information is ({self.position}, {self.streak})")
        self.processed_segment.append((self.position, self.streak))
        if __debug__:
            print(f"processed_segment is now {self.processed_segment}")

    @staticmethod
    def get_type_and_rank(character):
        char_class = None
        rank = None
        if __debug__:
            print(f"Looking for character {character} of type {type(character)}")
        if (rank := string.ascii_lowercase.find(character)) > -1:
            char_class = 1
        elif (rank := string.ascii_uppercase.find(character)) > -1:
            char_class = 2
        elif (rank := string.digits.find(character)) > -1:
            char_class = 3
        elif (rank := string.punctuation.find(character)) > -1:
            char_class = 4
        else:
            if __debug__:
                print(f"{character} is not valid ascii")
            raise TypeError()
        rank += 1
        return (char_class, rank)

    @staticmethod
    def get_keyboard_coordinate(character):
        lookup = character
        if lookup in string.ascii_uppercase:
            lookup = lookup.lower()
        return Password_Segment.keyboard_coordinates[lookup]


class Password:
    """
    This class holds all processed password segments for a single password.
    """

    def __init__(self, password, norder, prefix=None):
        self.password = password
        self.prefix = prefix
        self.norder = norder
        self.feature_label = []
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
        )  # Converts the password into a list of ordered classes for each character, e.g. "pass1234" would be [1, 1, 1, 1, 3, 3, 3, 3]
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
        for i in range(1, len(class_list)):
            if class_list[i] == last_class:
                streak = streak + tuple(
                    self.password[i]
                )  # If this character is the same class as the previous, append it to this streak tuple
            else:
                self.streaks.append(
                    streak
                )  # If it's different append the streak as is to the streak list...
                streak = tuple(self.password[i])  # ... and create a new streak.
                last_class = class_list[
                    i
                ]  # Reset last_class so we can restart the streak

    def _find_streaks(self, index):
        """
        Given a particular index, find where the character is in it's "streak". Return that position in the streak tuple.
        """
        position = 0
        for stk in self.streaks:
            if __debug__:
                print(stk)
            if (len(stk) + position) <= index:
                if __debug__:
                    print(f"Position {position} is less than index {index}")
                position += len(stk)
                if __debug__:
                    print(f"Moving to position {position}")
        return index - position + 1
    
    @staticmethod
    def _scroll(string, n):
        lst = []
        for i in range(len(string)):
            addition  = string[:i+1]
            lst.append(addition[-n:])
        if __debug__: print(lst)
        return lst

    def _create_segments(self):
        pass_chunks = self._scroll(self.password, self.norder)
        encoded_next_char = Password_Segment.get_type_and_rank(pass_chunks[0]) + Password_Segment.get_keyboard_coordinate(pass_chunks[0])
        prefix = "😀" * self.norder
        next_segment = Password_Segment(prefix, 0, 0).processed_segment
        if self.prefix:
            next_segment.insert(0, self.prefix)
        self.feature_label.append(
                (encoded_next_char, next_segment)
        )
        count = 1
        if __debug__: print("Entering loop")
        its = len(pass_chunks) - 1
        for i in range(its):
            if __debug__: print(f"In loop on {pass_chunks[i]}")
            if len(pass_chunks[i]) < self.norder:
                prefix = "😀" * (self.norder - len(pass_chunks[i]))
            else:
                prefix = ""

            encoded_next_char = Password_Segment.get_type_and_rank(pass_chunks[i + 1][-1]) + Password_Segment.get_keyboard_coordinate(pass_chunks[i + 1][-1])
            next_segment = Password_Segment(prefix + pass_chunks[i], count, self._find_streaks(count - 1)).processed_segment
            if self.prefix:
                next_segment.insert(0, self.prefix)
            #assert(len(next_segment), 7)
            self.feature_label.append(
                (encoded_next_char, next_segment)
            )
            count += 1
        
        next_segment = Password_Segment(pass_chunks[-1], count, self._find_streaks(count - 1)).processed_segment
        if self.prefix:
            next_segment.insert(0, self.prefix)
        self.feature_label.append(
            ([-1,-1,-1,-1],
             next_segment) 
        )

    def get_array(self):
        return self.feature_label

class User:
    def __init__(self, username, password, norder):
        self.username_string = username
        self.password_string = password

        unflattened_username = Password_Segment(username[:6], 0, 0).processed_segment
        flattened_username = [element for tupl in unflattened_username for element in tupl]
        self.username_encoded = flattened_username
        self.password_encoded = Password(password, norder, prefix=self.username_encoded)

    def get_array(self):
        return self.password_encoded.feature_label

