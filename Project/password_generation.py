import argparse
import json
import os
import time
from joblib import load
from matplotlib import pyplot as plt
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
        """
            current_str <- "abc1234"
        """
        if current_str != "":
            password = self._preprocessor(current_str, 6)
            input_encoding = password.get_array()[-1][-1]
            if len(input_encoding) < 7:
                input_encoding = [(0, 0, 0, 0)]*(7-len(input_encoding)) + input_encoding
            flatten_encoding = np.array([x for sub_encoding in input_encoding for x in sub_encoding]).reshape(1, -1)
        else:
            flatten_encoding = np.zeros(shape=(1, 26))
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
        start_time = time.time()
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
        speed_inference = (time.time() - start_time)/len(inputs)
        return {'y_pred': y_pred, 'speed_inference': speed_inference} 


def load_entire_dataset(data_file: str):
    with open(data_file, 'r', encoding='utf-8') as f:
        df = pd.read_csv(f)
    X, y = [], []
    for _, col in df.iterrows():
        # if type(col['input_prefix']) == str:
        if type(col['input_prefix']) is float:
            X.append("")
        else:    
            X.append(col['input_prefix'])
        y.append(col['entire_pass'])
    return X, y

def get_argument():
    args = argparse.ArgumentParser(description="Data processing to get feature")
    args.add_argument("--label_map_file", 
                      default="/home/tiennv/Github/EE6363_AdvancedML/Project/data/label_mapping.json")
    args.add_argument("--label_map_invert_file", 
                      default="/home/tiennv/Github/EE6363_AdvancedML/Project/data/label_mapping_invert.json")
    args.add_argument("--model_path", required=True, type=str)
    args.add_argument("--test", required=True, type=str, help="The path of testing dataset.")
    args.add_argument("--output_dir", default="output/", type=str, help="The output directory containing evaluation results and predictions.")
    return vars(args.parse_args())


def metric_acc(y_pred, y_true):
    count = 0
    for y1, y2 in zip(y_pred, y_true):
        if y1 == y2:
            count += 1
    return count/len(y_pred)

def metric_acc2(y_pred, y_true):
    """
        y_pred = ["123213", "2312"]
        y_true = ["123213", "2323122"]
    """
    count = 0
    for y in y_pred:
        if y in y_true:
            count += 1
    return count/len(y_true)


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
    L = 100
    success_rate = []
    total_guess = []
    speed = []
    # y_pred_total = []
    for l in tqdm(range(1, L+1)):
        portion_X = X[:int(l/L*len(X))]
        output = generator.inference(inputs=portion_X)
        y_pred, speed_time = output['y_pred'], output['speed_inference']
        # y_pred_total.extend(y_pred)
        # y_pred_total = list(set(y_pred_total))
        acc = metric_acc2(y_pred=y_pred, y_true=y_true)
        total_guess.append(len(y_pred)) # ->x
        success_rate.append(acc)        # ->y
        speed.append(speed_time)
        # Perform evaluation
        print("The successful rate is: {}%".format(np.round(acc*100, 4)))
        print("The inference time is: {} sample/second".format(np.round(speed_time, 4)))

    # Plot 
    fig, ax = plt.subplots()
    ax.plot(total_guess, success_rate, label="Successful rate")
    ax.legend(loc='best')
    ax.set_ylabel("Fraction of successfully cracked", fontsize=14)
    ax.set_xlabel("Guess number", fontsize=14)
    fig.savefig(os.path.join(args['output_dir'], os.path.basename(args['test']).split(".")[0]+"_crack.pdf"))

    fig, ax = plt.subplots()
    ax.plot(total_guess, speed, label="Time inference")
    ax.legend(loc='best')
    ax.set_ylabel("Running time average per guess", fontsize=14)
    ax.set_xlabel("Guess number", fontsize=14)
    fig.savefig(os.path.join(args['output_dir'], os.path.basename(args['test']).split(".")[0]+"_speed.pdf"))

    # Save prediction and true label
    df = pd.DataFrame({
        'x': X,
        'y_true': y_true,
        'y_pred': y_pred
    })
    saving_file = os.path.join(args['output_dir'], "pred_"+os.path.basename(args['test']))
    df.to_csv(saving_file, index=False)

    # Save metric evaluation
    saving_score_file = os.path.join(args['output_dir'], 'score.json')
    with open(saving_score_file, 'w', encoding='utf-8') as f:
        json.dump({'success_rate': success_rate, 'speed': speed_time, 'total_samples': len(X)}, f, indent=4, ensure_ascii=False)
    # Plot curve


if __name__ == '__main__':
    args = get_argument()
    evaluation(args)
