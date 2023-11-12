import string

# ( type , rank , row , column )

keyboard_coordinates = {
        "`" : (-1, 0),
        "~" : (-1, 0),
        "1" : (0, 0),
        "!" : (0, 0),
        "2" : (0, 1),
        "@" : (0, 1),
        "3" : (0, 2),
        "#" : (0, 2),
        "4" : (0, 3),
        "$" : (0, 3),
        "5" : (0, 4),
        "%" : (0, 4),
        "6" : (0, 5),
        "^" : (0, 5),
        "7" : (0, 6),
        "&" : (0, 6),
        "8" : (0, 7),
        "*" : (0, 7),
        "9" : (0, 8),
        "(" : (0, 8),
        "0" : (0, 9),
        ")" : (0, 9),
        "-" : (0, 10),
        "_" : (0, 10),
        "=" : (0, 11),
        "+" : (0, 11),
        "q" : (1, 0),
        "w" : (1, 1),
        "e" : (1, 2),
        "r" : (1, 3),
        "t" : (1, 4),
        "y" : (1, 5),
        "u" : (1, 6),
        "i" : (1, 7),
        "o" : (1, 8),
        "p" : (1, 9),
        "[" : (1, 10),
        "{" : (1, 10),
        "]" : (1, 11),
        "}" : (1, 11),
        "\\" : (1, 12),
        "|" : (1, 12),
        "a" : (2, 1),
        "s" : (2, 2),
        "d" : (2, 3),
        "f" : (2, 4),
        "g" : (2, 5),
        "h" : (2, 6),
        "j" : (2, 7),
        "k" : (2, 8),
        "l" : (2, 9),
        ";" : (2, 10),
        ":" : (2, 10),
        "'" : (2, 11),
        "\"" : (2, 11),
        "z" : (3, 1),
        "x" : (3, 2),
        "c" : (3, 3),
        "v" : (3, 4),
        "b" : (3, 5),
        "n" : (3, 6),
        "m" : (3, 7),
        "," : (3, 8),
        "<" : (3, 8),
        "." : (3, 9),
        ">" : (3, 9),
        "/" : (3, 10),
        "?" : (3, 10)
    }

def get_type_and_rank(character):
    char_class = None
    rank = None
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

def get_keyboard_coordinate(character):
    lookup = character
    if lookup in string.ascii_uppercase:
        lookup = lookup.lower()
    return keyboard_coordinates[lookup]

#password = input('--> ')

#ml_rep = []

#for c in password:
#    entry = (get_type_and_rank(c) + get_keyboard_coordinate(c))
#    ml_rep.append(entry)

#print(ml_rep)
