import os
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

    def __init__(self, password, norder):
        self.password_segments = []
        self.password = password
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

    def _create_segments(self):
        if len(self.password) < self.norder:
            begin = 0 - len(self.password)
        else:
            begin = 0 - self.norder  # Start at the 0th character of the password
        end = 0  # End such that the segment is of length n-order
        password_segments = []

        # Add segments of n-order length from beginning to end of password
        while end < len(self.password):
            if __debug__:
                print(f"Length of password is {len(self.password)}")
            if __debug__:
                print(f"Looping again with {begin} and {end}")
            if begin < 0:
                prefix = "😀" * abs(begin)
                next_char = (
                    self.password[-1] if begin == -1 else self.password[: begin + 1][-1]
                )
                word = prefix + self.password[:begin]
                encoded_next_char = Password_Segment.get_type_and_rank(next_char) + Password_Segment.get_keyboard_coordinate(next_char)
                if begin == (0 - len(self.password)):
                    next_segment = Password_Segment(word, 0, 0).processed_segment
                else:
                    next_segment = Password_Segment(
                        word,
                        len(self.password[:begin]) - 1,
                        self._find_streaks(end - 1),
                    ).processed_segment
                self.feature_label.append((encoded_next_char, next_segment))
            elif len(self.password) > self.norder:
                next_char = self.password[end]
                encoded_next_char = Password_Segment.get_type_and_rank(next_char) + Password_Segment.get_keyboard_coordinate(next_char)
                next_segment = Password_Segment(
                    self.password[begin:end], end, self._find_streaks(end - 1)
                ).processed_segment
                self.feature_label.append((encoded_next_char, next_segment))
            begin += 1
            end += 1
            if __debug__:
                print(f"Now begin is {begin} and end is {end}")

        self.feature_label.append(
            (
                [-1, -1, -1, -1],
                Password_Segment(
                    self.password[begin:end], end, self._find_streaks(end - 1)
                ).processed_segment,
            )
        )

    def get_array(self):
        return self.feature_label


def get_ascii(iterable):
    for line in iterable:
        try:
            yield line.decode("ASCII")
        except UnicodeDecodeError:
            pass


if __name__ == '__main__':
    # password = input("password: ")
    parser = argparse.ArgumentParser(
        prog="preprocess",
        description="This encodes ascii password lists for training in RFGuess",
    )
    parser.add_argument("input")
    parser.add_argument("norder", type=int),
    parser.add_argument("-o", "--output_dir", default="/home/tiennv/Github/EE6363_AdvancedML/Project/preprocess/processed_datasets")
    args = parser.parse_args()
    # filename = input("filename: ")
    # norder = int(input("n-order: "))

    # test = Password(password, norder)
    # for seg in test.password_segments:
    #    print(seg.processed_segment)
    #    print(json.dumps(seg.processed_segment))
    features = {}
    labels = {}
    print(f"Encoding file {args.input}...")
    with open(args.input, "rb") as password_dump:
        count = sum(1 for _ in password_dump)
    with open(args.input, "rb") as password_dump:
        for line in tqdm(get_ascii(password_dump), desc="Encoding", total=count):
            if __debug__:
                print(f"Adding password: {line.strip()}")
            try:
                if not line.strip():
                    continue
                current = Password(line.strip(), args.norder)
                lab_builder = []
                feat_builder = []
                for lab, feat in current.get_array():
                    lab_builder.append(lab)
                    feat_builder.append(feat)
                features[line.strip()] = feat_builder
                labels[line.strip()] = lab_builder
            except TypeError:
                continue

    output_file_feature = os.path.join(args.output_dir, os.path.basename(args.input).split(".")[0]+'.json')
    with open(output_file_feature, 'w') as f:
        print(f"Writing features to {output_file_feature}")
        json.dump(features, f, indent=4, ensure_ascii=False)
        # output_file.write(json.dumps(features))

    output_file_label = os.path.join(args.output_dir, os.path.basename(args.input).split(".")[0]+'.label.json')
    with open(output_file_label, 'w') as f:
        print(f"Writing labels to {output_file_label}")
        json.dump(labels, f, indent=4, ensure_ascii=False)
    # There are no tuples in JSON so this saves as lists of lists
    # print(json.dumps(passwords) # Use this to print ugly, machine-friendly JSON
    # print(json.dumps(passwords, indent=4, sort_keys=True)) # Uncomment this if you want the JSON output to look pretty
    # with open(f"{filename}.pkl", 'wb') as pickle_file:
    #    pickle.dump(passwords, pickle_file) # Use this to create a pickle file that saves the Python objects as bytes and can be easily imported
    # print(passwords)
