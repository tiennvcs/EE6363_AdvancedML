from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification


X, y = make_classification(
    n_samples=10000,
    n_features=4,
    n_informative=3,
    n_redundant=0,
    random_state=None,
    shuffle=True
)

model = RandomForestClassifier(
    max_depth=10,
    random_state=0,
)

model.fit(X, y)

print(model.predict([[0, 0, 1, 10]]))
print("Input: ", X)
print("Label: ", y)