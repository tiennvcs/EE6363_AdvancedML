import json, os
import pandas as pd
import argparse


label_mapping_path = '/home/tiennv/Github/EE6363_AdvancedML/Project/data/label_mapping.json'
label_mapping_invert_path = '/home/tiennv/Github/EE6363_AdvancedML/Project/data/label_mapping_invert.json'


class Dataset:
    def __init__(self, data_file: str, label_map_path: str, label_map_invert_path: str):
        self._data_path = data_file
        self._label_map_path = label_map_path
        self._label_map_invert_path = label_map_invert_path
        self._raw_data = None
        self._label_map = None
        self._label_map_invert = None
        self._data = None
        self._X = None
        self._y = None
        
    def load_data_from_json(self):
        with open(self._data_path, 'r') as f:
            self._raw_data = json.load(f)
        with open(self._label_map_path, 'r', encoding='utf-8') as f:
            self._label_map = json.load(f)
        with open(self._label_map_invert_path, 'r', encoding='utf-8') as f:
            self._label_map_invert = json.load(f)

    def _char_label_to_int(self, char):
        return ord(char)
    
    def process_data(self):
        self._data = []
        self._X = []
        self._y = []
        # Temporaly ignore these passwords less than 7 characters.
        for passwd_str, encodings in self._raw_data.items():
            k = 0
            while k <= len(passwd_str)-1:
                sample = {
                    'entire_pass': passwd_str,
                    'label_index': k,
                    'input_prefix': passwd_str[:k] if k <= 5 else passwd_str[k-6:k],
                    'input_encoding': encodings[k][-7:] if len(encodings[k]) >= 8 else [encodings[k][0]]*(7-len(encodings))+encodings[k],
                    'flatten_input_encoding': None,
                    'next_char': passwd_str[k],
                    'label': self._label_map[passwd_str[k]]
                }
                sample['flatten_input_encoding'] = [x for sub_encode in sample['input_encoding'] for x in sub_encode]
                if len(sample['input_encoding']) != 7 or len(sample['flatten_input_encoding']) != 26:
                    print(sample)
                    input("wait..")
                self._data.append(sample)
                k += 1
            # At the end, add the ending character.
            final_sample = {
                    'entire_pass': passwd_str,
                    'label_index': k,
                    'input_prefix': passwd_str[:k] if k <= 5 else passwd_str[k-6:k],
                    'input_encoding': encodings[k][-7:] if len(encodings[k]) >= 8 else [encodings[k][0]]*(7-len(encodings))+encodings[k],
                    'flatten_input_encoding': None,
                    'next_char': 'Es',
                    'label': self._label_map['Es']
            }
            final_sample['flatten_input_encoding'] = [x for sub_encode in final_sample['input_encoding'] for x in sub_encode]
            self._data.append(final_sample)
        self._X = [x['flatten_input_encoding'] for x in self._data]
        for x in self._X:
            if len(x) != 26:
                print(x)
        self._y = [x['label'] for x in self._data]

    def save_to_csv(self, data_file, entire_data=False):
        if entire_data:
            df = pd.DataFrame(self._data)
        else:
            df = {i:[] for i in range(26)}
            df['label'] = []
            for x, label in zip(self._X, self._y):
                for i in range(len(x)):
                    df[i].append(x[i])
                df['label'].append(label)
            df = pd.DataFrame(df)
        df.to_csv(data_file, index=False)


def get_argument():
    args = argparse.ArgumentParser(description="Data processing to get feature")
    args.add_argument("--data_path", required=True, type=str, help="The json data path to target processed data")
    args.add_argument("--output_dir", default="/home/tiennv/Github/EE6363_AdvancedML/Project/data/output", type=str)
    return vars(args.parse_args())


if __name__ == '__main__':
    # data_path = '/home/tiennv/Github/EE6363_AdvancedML/Project/output/encoded_password.json'
    args = get_argument()    
    os.makedirs(args['output_dir'], exist_ok=True)
    entire_data_file = os.path.join(args['output_dir'], os.path.basename(args['data_path']).split(".")[0]+'_entire.csv')
    feature_data_file = os.path.join(args['output_dir'], os.path.basename(args['data_path']).split(".")[0]+'_feature.csv')
    dataloader = Dataset(data_file=args['data_path'], label_map_path=label_mapping_path, label_map_invert_path=label_mapping_invert_path)
    dataloader.load_data_from_json()
    dataloader.process_data()
    dataloader.save_to_csv(data_file=feature_data_file, entire_data=False)
    dataloader.save_to_csv(data_file=entire_data_file, entire_data=True)