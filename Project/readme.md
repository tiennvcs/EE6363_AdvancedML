# Repository for Semester project
***EE 6363: Advanced Machine Learning***


## Introduction
This repository tried to reimplement the password generation in [1]. In that, the problem can be formulate as classification task, given input as the hint characters, the model is required to predict the password. There are steps:
- Input encoding: given a sequence of characters as a hint word, the encoder module need to convert it under feature vector.
- Password generation: predict the next sequence of characters.
In particular, we train the Random Forest model as the submodule in password generator. In every step, the RF predict the next character from the current lasted n-order string. The process is described as Markov-n process.


## Installation
- Python 3.11.5
- Ubuntu 22.04.2 LTS 

```bash
  pip install -r ./requirements.txt
```

## Usage
**To test the encoding module**
```bash
  python -O preprocess/preprocess.py ./preprocess/datasets/500-worst-passwords.txt 6
```
in that, *./preprocess/datasets/500-worst-passwords.txt* is a path to a file storing raw data (each line is a complete password), 6 is the n-order string.
The output of this command would be a file with name *./preprocess/processed_datasets/500-worst-passwords.json*.

**The next step is running ./data/data.py script to convert the processed data below into feature file csv format.**
```bash
  python data/data.py -data_path ./preprocess/processed_datasets/500-worst-passwords.json
```
The output is saved in file ./data/output/500-worst-passwords_feature.csv which contains the first columns as the feature vector and the last column is the integer encoded label, and ./data/output/500-worst-passwords_entire.csv which contains features, labels and metadata.

**To train the random forest module**
```
  python train.py --data_input ./data/output/500-worst-passwords_feature.csv --output_dir ./trained_models/ --max_depth 10 --test_size 0.2
```
The trained model could be found at directory ./trained_models/500-worst-passwords_feature/ which contains: config.json, score.json and model.joblib.

**The final step is performing password generation process base on the trained Random Forest model.**
```
  python -O password_generation.py --model_path ./trained_models/500-worst-passwords_feature/model.joblib --test ./data/output/500-worst-passwords_entire.csv
```
The output is the evaluation result of password generation including sucessfully cracked ratio: ./output/500-worst-passwords_entire_crack.pdf, and running time ./output/500-worst-passwords_entire_speed.pdf

Contact email: tiennvcs@gmail.com






