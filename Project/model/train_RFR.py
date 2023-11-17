from sklearn.ensemble import RandomForestClassifier
# Import datasets, classifiers and performance metrics
from sklearn import datasets, metrics, svm
from sklearn.model_selection import train_test_split



# Load and prepare data 
digits = datasets.load_digits()
n_samples = len(digits.images)
data = digits.images.reshape((n_samples, -1))

# Create classification model
model = RandomForestClassifier(
    max_depth=2,
    random_state=2505,
)

# Split data into 80% train, 20% test
X_train, X_test, y_train, y_test = train_test_split(
    data, digits.target, test_size=0.2, shuffle=True
)

# Train classification model
model.fit(X_train, y_train)

# Model evaluation
train_score = model.score(X_train, y_train)
test_score = model.score(X_test, y_test)

print("Train accuracy: ", train_score)
print("Test accuracy: ", test_score)
