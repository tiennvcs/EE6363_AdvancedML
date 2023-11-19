import argparse
import json
import os
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import time
from sklearn.model_selection import train_test_split
from joblib import dump

random_state = 2000


def load_dataset(data_file: str):
    with open(data_file, 'r', encoding='utf-8') as f:
        df = pd.read_csv(f)
    X = df.iloc[:, :26].to_numpy()
    y = df.iloc[:, -1:].to_numpy().ravel()
    return X, y


def create_classifer(max_depth=5, random_state=None):
    model = RandomForestClassifier(
        max_features=0.8, 
        min_samples_leaf=10, 
        n_estimators=30,
        # max_depth=max_depth,
        random_state=random_state,
    )
    return model


def run(args):
    # Load dataset
    print("Loading dataset ...")
    X, y = load_dataset(data_file=args['data_input'])
    print("\t--> Number of samples: {}".format(len(X)))

    # Initilize clasifier
    print("Creating classifier ...")
    model = create_classifer(max_depth=args['max_depth'], random_state=random_state)
    print("\t--> Model configuratio: {}".format(model))

    # Split dataset into training and testset
    print("Spiting dataset ...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=args['test_size'], shuffle=True, random_state=random_state
    )
    print("\t--> Training sample num: {}, testing sample num: {}".format(len(X_train), len(X_test)))

    # Perform training classifer on loaded data
    print("Performing training classifer")
    start_time = time.time()
    model.fit(X_train, y_train)
    print("\t--> Training time: {} second/sample".format((time.time()-start_time)/len(X_train)))

    # Perform evaluation trained model
    print("Scoring trained model")
    train_score = model.score(X_train, y_train)
    test_score = model.score(X_test, y_test)
    print("\t--> Train acc: {}, test acc: {}".format(train_score, test_score))

    # Save model to disk
    output_model_folder = os.path.join(args['output_dir'], os.path.basename(args['data_input']).split(".")[0])
    os.makedirs(output_model_folder, exist_ok=True)
    output_model_file = os.path.join(output_model_folder, 'model.joblib')
    dump(model, output_model_file)
    output_score_file = os.path.join(output_model_folder, 'score.json')
    with open(output_score_file, 'w') as f:
        json.dump({'train': train_score, 'test': test_score}, f, indent=4, ensure_ascii=False)
    output_config_file = os.path.join(output_model_folder, 'config.json')
    with open(output_config_file, 'w') as f:
        json.dump(args, f, indent=4, ensure_ascii=False)
    

def get_argument():
    args = argparse.ArgumentParser(description="Data processing to get feature")
    args.add_argument("--data_input", required=True, type=str, help="The json data path to target processed data")
    args.add_argument("--output_dir", default="/home/tiennv/Github/EE6363_AdvancedML/Project/data/output", type=str)
    args.add_argument("--max_depth", default=5, type=int)
    args.add_argument("--test_size", default=0.2, type=float)
    return vars(args.parse_args())


if __name__ == '__main__':
    args = get_argument()
    run(args)