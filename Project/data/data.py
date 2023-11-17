import json, os
import pandas as pd


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
            if len(passwd_str) < 7:
                continue
            k = 0
            while k < len(passwd_str)-6:
                self._data.append(
                    {
                        'entire_pass': passwd_str,
                        'start_index_prefix': k,
                        'input_prefix': passwd_str[k: k+6],
                        'input_encoding': encodings[k],
                        'flatten_input_encoding': [x for sub_encode in encodings[k] for x in sub_encode],
                        'next_char': passwd_str[k+6],
                        'label': self._label_map[passwd_str[k+6]]
                    }
                )
                k += 1
            # At the end, add the end character.
            self._data.append(
                {
                    'entire_pass': passwd_str,
                    'start_index_prefix': k,
                    'input_prefix': passwd_str[k: k+6],
                    'input_encoding': encodings[k],
                    'flatten_input_encoding': [x for sub_encode in encodings[k] for x in sub_encode],
                    'next_char': 'Es',
                    'label': self._label_map['Es']
                }
            )
        self._X = [x['flatten_input_encoding'] for x in self._data]
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


if __name__ == '__main__':
    data_path = '/home/tiennv/Github/EE6363_AdvancedML/Project/output/encoded_password.json'
    label_mapping_path = '/home/tiennv/Github/EE6363_AdvancedML/Project/data/label_mapping.json'
    label_mapping_invert_path = '/home/tiennv/Github/EE6363_AdvancedML/Project/data/label_mapping_invert.json'
    output_data_folder = './data/output/'
    entire_data_file = os.path.join(output_data_folder, 'entire.csv')
    feature_data_file = os.path.join(output_data_folder, 'feature.csv')
    dataloader = Dataset(data_file=data_path, label_map_path=label_mapping_path, label_map_invert_path=label_mapping_invert_path)
    dataloader.load_data_from_json()
    dataloader.process_data()
    dataloader.save_to_csv(data_file=entire_data_file, entire_data=True)