from preprocess import Password, Password_Segment
import argparse, json
from tqdm import tqdm

def get_ascii(iterable):
    for line in iterable:
        try:
            yield line.decode("ASCII")
        except UnicodeDecodeError:
            pass

# password = input("password: ")
parser = argparse.ArgumentParser(
    prog="preprocess",
    description="This encodes ascii password lists for training in RFGuess",
)
parser.add_argument("input")
parser.add_argument("norder", type=int),
parser.add_argument("-o", "--output", default="output.csv")
args = parser.parse_args()
# filename = input("filename: ")
# norder = int(input("n-order: "))

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

with open(f"{args.output}.feature", 'w') as output_file:
    print(f"Writing features to {args.output}.features")
    json.dump(features, output_file, indent=4, ensure_ascii=True)
    # output_file.write(json.dumps(features))

with open(f"{args.output}.label", 'w') as output_file:
    print(f"Writing labels to {args.output}.labels")
    json.dump(labels, output_file, indent=4, ensure_ascii=True)
# There are no tuples in JSON so this saves as lists of lists
# print(json.dumps(passwords) # Use this to print ugly, machine-friendly JSON
# print(json.dumps(passwords, indent=4, sort_keys=True)) # Uncomment this if you want the JSON output to look pretty
# with open(f"{filename}.pkl", 'wb') as pickle_file:
#    pickle.dump(passwords, pickle_file) # Use this to create a pickle file that saves the Python objects as bytes and can be easily imported
# print(passwords)

with open(f"{args.output}.csv" ,'w') as csv_file:
    csv_file.write("features|labels\n")
    for k in features:
        for i in range(len(features[k])):
            unpack_tuple = [element for tupl in features[k][i] for element in tupl]
            feat_str = ', '.join(str(x) for x in unpack_tuple)
            lab_str = ', '.join(str(x) for x in labels[k][i])
            csv_file.write("[" + feat_str + "]" + " | " + "[" + lab_str + "]\n")
