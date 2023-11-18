import argparse

def ascii_lines(iterable):
    for line in iterable:
        if all(ord(ch) < 128 for ch in line):
            yield line

parser = argparse.ArgumentParser(
        prog='fix',
        description='Remove non-ascii lines'
        )
parser.add_argument('input')
parser.add_argument('output')

args = parser.parse_args()

with open(args.input, 'rb') as input_file:
    with open(args.output, 'w') as output_file:
        for line in input_file:
            try:
                output_file.write(line.decode('ASCII'))
            except UnicodeDecodeError:
                pass
