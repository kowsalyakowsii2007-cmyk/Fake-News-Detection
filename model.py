import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pickle

# Load existing dataset
fake = pd.read_csv('Fake.csv')
true = pd.read_csv('True.csv')
fake['label'] = 0
true['label'] = 1
df1 = pd.concat([fake[['text', 'label']], true[['text', 'label']]])

# Load IFND Indian dataset
ifnd = pd.read_csv('IFND.csv', encoding='latin-1')
ifnd = ifnd[['Statement', 'Label']].copy()
ifnd.columns = ['text', 'label']
ifnd['label'] = ifnd['label'].map({'Fake': 0, 'Real': 1, 'fake': 0, 'real': 1})
ifnd = ifnd.dropna()

# Merge both datasets
df = pd.concat([df1, ifnd], ignore_index=True)
df = df.dropna()

print("Total data:", len(df))

X_train, X_test, y_train, y_test = train_test_split(df['text'], df['label'], test_size=0.2, random_state=42)
vectorizer = TfidfVectorizer(max_features=5000)
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

model = LogisticRegression(max_iter=1000)
model.fit(X_train_vec, y_train)

accuracy = accuracy_score(y_test, model.predict(X_test_vec))
print(f"Accuracy: {accuracy * 100:.2f}%")

pickle.dump(model, open('model.pkl', 'wb'))
pickle.dump(vectorizer, open('vectorizer.pkl', 'wb'))
print("Model saved!")