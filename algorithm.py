import sqlite3
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score

# Connect to the SQLite database
conn = sqlite3.connect('diagnosis.db')

# Query the database to get the data
query = "SELECT symptoms, diagnoses FROM diagnosis"
df = pd.read_sql_query(query, conn)
print(df)

# Close the connection
conn.close()

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(df['symptoms'], df['diagnoses'], test_size=0.2, random_state=42)

# Convert the symptoms to a matrix of token counts
vectorizer = CountVectorizer()
X_train_counts = vectorizer.fit_transform(X_train)

# Train a Naive Bayes classifier
clf = MultinomialNB()
clf.fit(X_train_counts, y_train)

# Test the model
X_test_counts = vectorizer.transform(X_test)
y_pred = clf.predict(X_test_counts)

# Print the accuracy of the model
# print("Accuracy: ", accuracy_score(y_test, y_pred))

# Function to predict diagnosis based on symptoms
def predict_diagnosis(symptoms):
    # Convert the symptoms to a matrix of token counts
    symptoms_counts = vectorizer.transform([symptoms])
    # Use the trained classifier to predict the diagnosis
    diagnosis = clf.predict(symptoms_counts)
    return diagnosis[0]