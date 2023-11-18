from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import time
from sklearn.model_selection import train_test_split
from joblib import dump


def load_dataset(data_file: str):
    with open(data_file, 'r', encoding='utf-8') as f:
        df = pd.read_csv(f)
    X = df.iloc[:, :26].to_numpy()
    y = df.iloc[:, -1:].to_numpy().ravel()
    return X, y


def create_classifer(max_depth=5, random_state=None):
    model = RandomForestClassifier(
        max_depth=max_depth,
        random_state=random_state,
    )
    return model


def run(data_file, max_depth, random_state, test_size):
    # Load dataset
    print("Loading dataset ...")
    X, y = load_dataset(data_file=data_file)
    print("\t--> Number of samples: {}".format(len(X)))

    # Initilize clasifier
    print("Creating classifier ...")
    model = create_classifer(max_depth=max_depth, random_state=random_state)
    print("\t--> Model configuratio: {}".format(model))

    # Split dataset into training and testset
    print("Spiting dataset ...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, shuffle=True, random_state=random_state
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
    dump(model, 'model.joblib')
    




if __name__ == '__main__':
    data_file = './data/output/feature.csv'
    max_depth = 20
    random_state = 1000
    test_size =  0.2
    run(data_file, max_depth, random_state, test_size)