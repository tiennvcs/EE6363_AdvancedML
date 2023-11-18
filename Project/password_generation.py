import argparse
import json
from joblib import load
from tqdm import tqdm
from preprocess.preprocess import Password
import numpy as np
import pandas as pd
from typing import List


class PasswordGenerator:
    def __init__(self, label_mapping_file: str, label_mapping_invert_file: str, RRmodel_path: str):
        self._label_mapping_file = label_mapping_file
        self._label_mapping_invert_file = label_mapping_invert_file
        self._RRmodel_path = RRmodel_path
        
        self._preprocessor = None
        self._label_map = None
        self._label_map_invert = None
        self._model = None

        self._load_mapping_label()
        self._load_trained_RFmodel()
        self._load_preprocessor()

    def _load_mapping_label(self):
        with open(self._label_mapping_file, 'r', encoding='utf-8') as f:
            self._label_map = json.load(f)
        with open(self._label_mapping_invert_file, 'r', encoding='utf-8') as f:
            self._label_map_invert = json.load(f)

    def _load_preprocessor(self):
        self._preprocessor = Password

    def _load_trained_RFmodel(self):
        print("Loading and using model at {}".format(self._RRmodel_path))
        self._model = load(self._RRmodel_path)
        print(self._model)

    def one_step_inference(self, current_str):
        password = self._preprocessor(current_str, 6)
        input_encoding = password.get_array()[-1][-1]
        if len(input_encoding) < 7:
            input_encoding = [(0, 0, 0, 0)]*(7-len(input_encoding)) + input_encoding
        flatten_encoding = np.array([x for sub_encoding in input_encoding for x in sub_encoding]).reshape(1, -1)
        next_char_int = self._model.predict(flatten_encoding)[-1]
        next_char = self._label_map_invert[str(next_char_int)]
        return next_char

    def single_inference(self, inputs: str):
        current_str = inputs
        max_num = 30
        while True or max_num >= 1:
            next_char = self.one_step_inference(current_str=current_str)
            if next_char == "Es":
                break
            current_str = current_str + next_char
            max_num -= 1
        return [current_str]


    def inference(self, inputs: List[str]):
        y_pred = []
        for input_str in tqdm(inputs, desc="Inference each password ...", total=len(inputs)):
            current_str = input_str
            max_num = 30
            while True or max_num >= 1:
                next_char = self.one_step_inference(current_str=current_str)
                if next_char == "Es" or len(current_str) > max_num:
                    break
                current_str = current_str + next_char
            y_pred.append(current_str)
        return y_pred


def load_entire_dataset(data_file: str):
    with open(data_file, 'r', encoding='utf-8') as f:
        df = pd.read_csv(f)
    filter_X, filter_y = [], []
    for _, col in df.iterrows():
        if type(col['input_prefix']) == str:
            if len(col['input_prefix']) <= 3:
                continue
            filter_X.append(col['input_prefix'])
            filter_y.append(col['entire_pass'])
    return filter_X, filter_y

def get_argument():
    args = argparse.ArgumentParser(description="Data processing to get feature")
    args.add_argument("--label_map_file", 
                      default="/home/tiennv/Github/EE6363_AdvancedML/Project/data/label_mapping.json")
    args.add_argument("--label_map_invert_file", 
                      default="/home/tiennv/Github/EE6363_AdvancedML/Project/data/label_mapping_invert.json")
    args.add_argument("--model_path", required=True, type=str)
    args.add_argument("--test", required=True, type=str, help="The path of testing dataset.")
    return vars(args.parse_args())


def metric(y_pred, y_true):
    count = 0
    for y1, y2 in zip(y_pred, y_true):
        if y1 == y2:
            count += 1
    return count/len(y_pred)

def evaluation(args):
    # Initialize password generator model
    generator = PasswordGenerator(
        label_mapping_file=args['label_map_file'],
        label_mapping_invert_file=args['label_map_invert_file'],
        RRmodel_path=args['model_path']
    )

    # Load dataset
    X, y_true = load_entire_dataset(data_file=args['test'])

    # Make inference
    y_pred = generator.inference(inputs=X)

    # Perform evaluation
    acc = metric(y_pred=y_pred, y_true=y_true)
    print("The accuracy is: {}%".format(np.round(acc*100, 2)))

    # Plot curve


if __name__ == '__main__':
    args = get_argument()
    evaluation(args)
