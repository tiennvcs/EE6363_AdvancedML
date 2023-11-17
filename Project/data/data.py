import json


class Dataset:
    def __init__(self, data_file):
        self._data_path = data_file
        self._raw_data = None
        self._data = None
        self._X = None
        self._y = None
        
    def load_data_from_json(self):
        with open(self._data_path, 'r') as f:
            self._raw_data = json.load(f)
        
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
            # print("Entire password: ", passwd_str)
            # for i in range(len(passwd_str)-6):
            #     print("\tInput 6-order prefix: ", passwd_str[i:i+6])
            #     print("\tEncoding: ", encodings[i])
            #     print("\tLabel: ", passwd_str[i+6])
            #     print("\tEncoding label: ", ord(passwd_str[i+6]))
            #     input()
            for i in range(len(passwd_str)-6):
                self._data.append(
                    {
                        'entire_pass': passwd_str,
                        'input_prefix': passwd_str[i: i+6],
                    }
                )

            
        


if __name__ == '__main__':
    data_path = '/home/tiennv/Github/EE6363_AdvancedML/Project/output/encoded_password.json'
    dataloader = Dataset(data_file=data_path)
    dataloader.load_data_from_json()
    dataloader.process_data()